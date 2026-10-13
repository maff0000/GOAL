# Backlog Schema

Field reference for `backlog/backlog.yaml`.

## Authority

`backlog/backlog.yaml` is the **machine-readable authority** for delivery
automation. Validation, readiness and dispatch all read it and nothing else.

`backlog/MASTER-BACKLOG.md` is the **human view generated from it**. The two
are not independent truths: the markdown's generated regions are rendered
from the YAML, and drift between them is a defect that `./tools/goal-docs`
detects and repairs. Never hand-edit a generated region, and never treat the
markdown as the source when the two disagree.

The vocabularies below come from `governance/DELIVERY-STATE-MACHINE.md`.
`tools/goal_dcp/model.py` holds the single machine copy of them.

## Document shape

The top level is a mapping with exactly one key, `items`, whose value is a
list of item mappings. Every item carries **all 13 keys explicitly**, in the
order listed below. A key is never omitted; absence of a value is expressed
as `null` (currently only for `pid_path`), not by dropping the key.

## Fields

| field | type | required | allowed values | meaning |
|---|---|---|---|---|
| `id` | string | yes | matches `^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$`, unique across items | Canonical complete work-item identifier. |
| `title` | string | yes | non-empty | Human-readable delivery outcome. |
| `lane` | string | yes | `shared`, `research`, `trading`, `ops` | Delivery lane; lowercase to match the `lane:*` label vocabulary. |
| `component` | string | yes | non-empty | System or estate area the work belongs to. |
| `target_repository` | string | yes | matches `^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$` | `owner/name` of the repository the work lands in. |
| `priority` | string | yes | `P0`, `P1`, `P2` | Programme priority. |
| `risk` | string | yes | `low`, `medium`, `high`, `capital` | Delivery risk class — see **Risk vocabulary** below. |
| `state` | string | yes | one of the 19 canonical states below | Current delivery state. |
| `depends_on` | list of strings | yes (may be empty) | each entry a canonical complete `id` declared by another item | Work that must reach an accepted terminal state first. |
| `po_gate` | boolean | yes | `true`, `false` | Whether PO acceptance is required. |
| `matt_gate` | boolean | yes | `true`, `false` | Whether a declared owner/capital decision is required. |
| `pid_path` | string or null | yes (value may be `null`) | repo-relative POSIX path to an existing file, or `null` | The item's canonical PID. Non-`null`, pointing at a readable file, and a valid PID from `DELIVERY_READY` onwards — see **Minimum PID validity**; `null` only while the item is in a pre-delivery state. |
| `architecture_refs` | list of strings | yes (may be empty) | repo-relative POSIX paths to existing files | Architecture and decision records governing the item. |

`pid_path` and `architecture_refs` entries are repo-relative POSIX paths,
resolved against the repository root. They are never absolute.

### Risk vocabulary

`risk` records **delivery** risk — how much can go wrong in building and
landing the work — not expected trading loss. The ratified baseline reading:

| value | meaning |
|---|---|
| `low` | Bounded. Contained blast radius, well-understood change. |
| `medium` | Meaningful architecture or integration impact. |
| `high` | Operational, security or execution-system impact. |
| `capital` | Carries an explicit PAPER/LIVE capital gate. |

This is the initial baseline interpretation, ratified by the Product Owner /
Central Architecture. `capital` is the only value that implies a gate rather
than merely a magnitude, and it is why `matt_gate` and `risk: capital` tend to
travel together — but they are independent fields and neither is derived from
the other.

### Canonical states

In state-machine order:

```text
DISCOVERED, ARCHITECTURE_REQUIRED, PID_DRAFT, PO_REVIEW, BLOCKED,
DELIVERY_READY, ROGUE_DISPATCHED, FORGE_BUILD, FORGE_AUDIT, REPAIR,
PO_ACCEPTANCE, MATT_DECISION, CANDIDATE, MERGED, DEPLOYMENT_READY,
PAPER, LIVE, CLOSED, CANCELLED
```

## `ACCEPTED_TERMINAL_STATES`

```text
MERGED, DEPLOYMENT_READY, PAPER, LIVE, CLOSED
```

A dependency counts as satisfied **only** in one of these states. This set is
what readiness computes dependencies against: an item is dispatchable when its
own state is `DELIVERY_READY`, every dependency resolves to a declared item in
an accepted terminal state, and it declares a canonical PID. The PID clause is
the subject of the next section.

Reasoning for the exclusions:

- `CANCELLED` is **terminal but not accepted**. Work can stop permanently
  without its outcome ever being delivered, so a cancelled dependency must not
  unblock the work that needed it.
- `BLOCKED` is not terminal at all — it is a live state awaiting resolution.
- `PO_ACCEPTANCE`, `MATT_DECISION` and `CANDIDATE` are **in-flight gates, not
  acceptance**. Work sitting in a gate has not yet been accepted, and treating
  a pending gate as satisfied would let dependent work start on an outcome
  that may still be rejected.

## `PID_REQUIRED_STATES`

```text
DELIVERY_READY, ROGUE_DISPATCHED, FORGE_BUILD, FORGE_AUDIT, REPAIR,
PO_ACCEPTANCE, MATT_DECISION, CANDIDATE, MERGED, DEPLOYMENT_READY,
PAPER, LIVE, CLOSED
```

These are the states that mean delivery has been committed to: FORGE is about
to be engaged, is engaged, or has finished. From `DELIVERY_READY` onwards a
canonical PID must exist — otherwise there is no authoritative statement of
what is to be built, what was built, or what acceptance meant. An item in one
of these states with `pid_path: null` is a `MISSING_PID` finding; a declared
PID that does not exist or cannot be read is `PID_FILE_NOT_FOUND`; a declared
PID that exists but is not a PID is `PID_INVALID` (see **Minimum PID validity**
below); and PID metadata that disagrees with the backlog is
`BACKLOG_PID_MISMATCH`.

`DELIVERY_READY` is included, and that inclusion is the substance of the rule:
**no PID = not `DELIVERY_READY`** — and neither is an existing-but-content-free
PID. What permits the transition into `DELIVERY_READY` is an approved canonical
PID — one that exists, is a valid PID, agrees with
this backlog, and has passed the item's declared PO gate. FORGE delivers
against a PID, so an item without one has nothing for a PL to build to;
calling it "ready" would promise a dispatch that cannot happen.

The requirement is nonetheless deliberately **state-conditional**:

- Most backlog items have no PID yet. Requiring one unconditionally would make
  the canonical data permanently invalid, which is a defect rather than a
  check — and it would be the wrong complaint, because the absence of a PID is
  normal for work that has not been specified.
- That is now exactly why such items sit in a **pre-delivery** state.
  `DISCOVERED`, `ARCHITECTURE_REQUIRED`, `PID_DRAFT`, `PO_REVIEW` and
  `BLOCKED` do not require a PID; an item with no PID belongs in one of them,
  not in `DELIVERY_READY`. The validator is not excusing the missing PID, it
  is checking the state is honest about it.
- `CANCELLED` requires no PID either. Work can be abandoned before it was ever
  specified.
- The canonical sequence is what makes this coherent:
  `ARCHITECTURE_REQUIRED → PID_DRAFT → PO_REVIEW → DELIVERY_READY →
  ROGUE_DISPATCHED → FORGE_BUILD`. *Architecture before PID, PID before
  build.* Each PID-required state is reached only by passing through the
  states in which the PID is authored and reviewed, so by the time the
  requirement bites it has already been satisfied in the normal course of
  events. See `governance/DELIVERY-STATE-MACHINE.md`, which is the authority
  for the sequence and the sets.
- The rule is exercised by canonical data today via `GOAL-DCP-001`, which
  declares `pids/GOAL-DCP-001.md` and is in a PID-required state, so the
  existence, readability, validity and metadata-agreement checks all run on
  real data rather than on fixtures alone.

### Minimum PID validity

Existence is not enough. A single `touch` of the pointed-to file used to pass
the whole gate: a zero-byte PID satisfies `PID_FILE_NOT_FOUND` (the file
exists) and satisfies `BACKLOG_PID_MISMATCH` (it declares no labels, and a
label the PID omits is not a mismatch). An empty PID therefore established
delivery readiness while carrying none of the authority a PID exists to carry.

So from `DELIVERY_READY` onwards the declared file must also **be** a PID. Five
requirements, all of which must hold, or the item is a `PID_INVALID` finding:

| # | requirement | what the validator reads |
|---|---|---|
| R1 | identity | the file's **first** ATX heading names the item's `id` as a whole token |
| R2 | purpose | a section whose heading matches, with a non-trivial body |
| R3 | scope | a section whose heading matches, with a non-trivial body |
| R4 | acceptance criteria | a section whose heading matches, with a non-trivial body |
| R5 | approval evidence | a section whose heading matches, with a non-trivial body |

**Accepted heading spellings.** A heading is normalised by stripping its
leading `#` characters and surrounding whitespace, stripping a trailing `:`,
collapsing internal whitespace runs to one space and case-folding. It satisfies
a requirement when the normalised result is **exactly equal** to one of:

| requirement | accepted spellings |
|---|---|
| purpose | `purpose`, `objective` |
| scope | `scope` |
| acceptance criteria | `acceptance`, `acceptance criteria` |
| approval evidence | `approval`, `approval evidence`, `po approval` |

Exact equality, never a substring test. `## Out of scope` and
`## Non-goals (scope)` both contain "scope" and neither states the item's
scope; a PID may legitimately carry both *alongside* its `## Scope` section.
The spelling sets are deliberately short, and this table is the list — a PID
author should not have to guess what the validator reads.

**Section body.** The lines after a matched heading, up to but not including
the next ATX heading of any level, or end of file. Each heading occurrence is
its own section: the bodies of two `## Scope` headings are never pooled, so two
thin sections cannot add up to one substantive one.

**Non-trivial body.** At least **6 distinct words**, where a word is a maximal
run of `[A-Za-z0-9]` characters of length 2 or more and distinctness is
compared case-folded. That single number is what the following rest on:

- a zero-byte or whitespace-only file has no heading at all, so it fails R1–R5
  outright and never reaches the floor;
- a heading followed by an empty body yields 0 words;
- padding such as `xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx` yields 1 distinct word,
  which is why the floor counts *distinct* words rather than characters, bytes,
  lines or total words;
- prose that merely contains the words "purpose", "scope", "acceptance
  criteria" and "approval" has no section headings and fails before any body is
  counted.

**R1 is a whole-token test**, not a substring search: a PID headed
`# GOAL-DCP-0011 — …` does not establish identity for `GOAL-DCP-001`, because
the occurrence is immediately followed by a character in `[A-Za-z0-9_-]`. A
file with no ATX heading fails R1. One consequence worth stating: a PID cannot
be shared by two items with different ids.

**What this establishes, and what it does not.** This is a **structural**
check. It proves the five things are present and not content-free. It cannot
and does not judge whether what they say is *good*, correct, complete or
sufficient — a PID can satisfy every requirement above and still be a bad PID.
Semantic quality is what the item's PO gate is for, and the rule deliberately
stops here rather than accumulating heuristics that would let it pretend
otherwise.

**R5 is not a delivery-acceptance check.** It requires an approval-evidence
section with content and nothing more: the section's meaning is never parsed,
and no field whose value depends on the item's current delivery state is read.
A PID's approval section records approval **of the PID** — the authority that
permitted the item to leave `PID_DRAFT` and reach `DELIVERY_READY` — not
acceptance of the delivered work, which is the separate, later `PO_ACCEPTANCE`
gate. Requiring anything stronger would make an item's PID validity depend on
its own delivery outcome, which is circular: every state from `DELIVERY_READY`
onwards requires a valid PID, including the states an item passes through long
before its delivery is accepted.

**It is state-conditional, exactly like `MISSING_PID`.** `PID_INVALID` is
evaluated only for the states listed above, and only once `pid_path` has
resolved to a file that was read successfully. An item in `PID_DRAFT` whose
`pid_path` points at a half-written draft is correct and yields nothing — that
state exists to produce the finished document, so failing a draft there would
make it unusable.

`PID_INVALID` and `BACKLOG_PID_MISMATCH` are **independent** and may
legitimately co-occur: a structurally incomplete document and a document whose
metadata contradicts the backlog are different defects, and a reader repairing
a PID needs to be told both.

## Identifier rules

Canonical ids are **complete**. Valid: `GOAL-DCP-001`, `GOAL-CONTRACT-001`,
`OPS-SAFE-001`, `DARWIN-R1`, `MT5-GW-001`, `PAPER-E2E-001`. Not valid:
`DCP-001`, `CONTRACT-001`, `CORE-001`, `OPS-SAFE-*`, `GOAL-*`, `tron-t1`,
`TRON-T2,T3,T4`.

Rejection of shorthand is **two-layered**, because no regular expression can
tell `DCP-001` (shorthand, invalid) from `DARWIN-R1` (canonical, valid):

1. **Syntax** — the `id` pattern rejects wildcards, lowercase, commas,
   whitespace and empty strings.
2. **Membership** — a dependency must resolve to an `id` some item declares.
   This is the layer that rejects shorthand, aliases and unknown ids:
   `DCP-001` fails because no item declares it.

Both layers are required; neither alone is sufficient.

## `target_repository` is a declared target

`target_repository` records where work is *intended* to land. It is never
checked against GitHub: validation is offline and deterministic. Several
declared targets do not exist yet, which is correct and expected for work that
has not started. Repository name casing is significant and recorded as the
remote actually spells it.

## Loading behaviour

`tools/goal_dcp/model.py` provides a **structural** loader, not a validator.
It fails only when the document cannot be read as a structure — the YAML does
not parse, the top level is not a mapping, `items` is missing, `items` is not
a list, or an `items` entry is not a mapping.

Everything else is handed through intact so the validator can report it: a
missing field becomes `None`, a wrong-typed field is carried through
unconverted, and the original mapping is always retained so "absent" can be
told apart from "present but null". Semantically broken data therefore loads
successfully and then produces findings, which is what makes the validator
able to describe the problem instead of merely refusing to start.

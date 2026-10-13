# Delivery State Machine

Canonical states:

```text
DISCOVERED
ARCHITECTURE_REQUIRED
PID_DRAFT
PO_REVIEW
BLOCKED
DELIVERY_READY
ROGUE_DISPATCHED
FORGE_BUILD
FORGE_AUDIT
REPAIR
PO_ACCEPTANCE
MATT_DECISION
CANDIDATE
MERGED
DEPLOYMENT_READY
PAPER
LIVE
CLOSED
CANCELLED
```

This document is the authority for the vocabulary above and for the rules
below. `tools/goal_dcp/model.py` holds the single machine copy of them;
`backlog/backlog.yaml` records which state each item is actually in.

## Canonical sequence

The states are a vocabulary, not an unordered set. The sequence an item
follows into delivery is:

```text
ARCHITECTURE_REQUIRED → PID_DRAFT → PO_REVIEW → DELIVERY_READY
                      → ROGUE_DISPATCHED → FORGE_BUILD
```

Doctrine: **architecture before PID, PID before build.**

`DISCOVERED` precedes the sequence — work is known about but not yet
architecturally owned. `BLOCKED` suspends an item awaiting resolution.
`FORGE_BUILD` continues into the build and acceptance tail: `FORGE_AUDIT`,
`REPAIR`, `PO_ACCEPTANCE`, `MATT_DECISION`, `CANDIDATE`, `MERGED`,
`DEPLOYMENT_READY`, `PAPER`, `LIVE`, `CLOSED`. `CANCELLED` ends an item
permanently without its outcome ever being delivered, and can be reached from
anywhere in the sequence.

## Pre-delivery states and PID-required states

**Pre-delivery.** A canonical PID is not required, because these are the
states in which the PID does not exist yet, or is still being drafted and
reviewed:

```text
DISCOVERED  ARCHITECTURE_REQUIRED  PID_DRAFT  PO_REVIEW  BLOCKED
```

`BLOCKED` is in this set because an item can be blocked before its PID was
ever written — most obviously when the thing blocking it is the architecture
decision the PID would depend on. An item blocked later in the sequence will
normally still have its PID; the requirement simply is not enforced while it
is suspended.

**PID-required.** A canonical PID must exist, be readable, be a valid PID, and
agree with the backlog:

```text
DELIVERY_READY  ROGUE_DISPATCHED  FORGE_BUILD  FORGE_AUDIT  REPAIR
PO_ACCEPTANCE   MATT_DECISION     CANDIDATE    MERGED
DEPLOYMENT_READY  PAPER  LIVE  CLOSED
```

`CANCELLED` is in neither set. Work can be abandoned at any point, including
before a PID was ever authored, so demanding one of cancelled work would make
cancellation impossible to record honestly.

### No PID = not `DELIVERY_READY`

`DELIVERY_READY` and every state after it require a canonical PID. An item
that has no PID stays in a **pre-delivery** state. It does not become
`DELIVERY_READY`, and it never appears in a readiness answer.

**An existing-but-content-free PID does not satisfy the requirement either.**
A file that merely exists is not a PID. Before this was enforced, a single
`touch` of the pointed-to file passed the whole gate — the file existed, and a
PID that declares no metadata labels contradicts nothing — so a zero-byte
document could establish delivery readiness while carrying none of the
authority a PID exists to carry. From `DELIVERY_READY` onwards the declared
file must therefore also *be* a PID: it must name the item in its first
heading and state its purpose, scope, acceptance criteria and approval
evidence, each with substantive content. `backlog/SCHEMA.md` holds the exact
rule — the accepted heading spellings, the distinct-word floor, and the honest
statement of what the check does and does not establish. It is a structural
check; whether a PID is *good* is the PO gate's judgement, not the
validator's.

What permits the transition into `DELIVERY_READY` is an **approved canonical
PID**: one that exists, is a valid PID, whose metadata agrees with the backlog,
and which has passed the PO gate the item declares. Only once an item is
`DELIVERY_READY` may `./tools/goal-ready` surface it.

The reasoning is that `DELIVERY_READY` must mean what its name claims. FORGE
delivers against a canonical PID; without one there is nothing for a PL to
build to, no statement of scope, no non-goals and no definition of acceptance.
Calling such work "ready" would promise a dispatch that cannot actually
happen, and would put the burden of discovering that on whoever tried to act
on the answer. The missing PID is not a detail to resolve during dispatch —
it is the reason the item is not ready.

Deterministic consequences, enforced by `./tools/goal-validate`:

- a PID-required state with `pid_path: null` is a `MISSING_PID` finding;
- a declared PID that does not exist or cannot be read is a
  `PID_FILE_NOT_FOUND` finding;
- a declared PID that exists and is readable but does not meet minimum PID
  validity — no identity, or no purpose, scope, acceptance-criteria or
  approval-evidence section with substantive content — is a `PID_INVALID`
  finding, one per item, naming every unmet requirement;
- PID metadata that disagrees with the backlog is a `BACKLOG_PID_MISMATCH`
  finding.

`PID_INVALID` is state-conditional in exactly the way `MISSING_PID` is: it is
evaluated only in the PID-required states above. An item in `PID_DRAFT` whose
`pid_path` points at a half-written draft is correct, and yields nothing —
that state exists to produce the finished document.

An item lacking a PID is therefore not a validation failure to be worked
around; it is an item whose correct state is `PID_DRAFT` or earlier, and whose
next action belongs to the PO.

## Accepted terminal states

A dependency counts as satisfied **only** in one of these states:

```text
MERGED  DEPLOYMENT_READY  PAPER  LIVE  CLOSED
```

- `CANCELLED` is **terminal but not accepted**. Work can stop permanently
  without its outcome ever being delivered, so a cancelled dependency must not
  unblock the work that needed that outcome.
- `BLOCKED` is not terminal at all — it is a live state awaiting resolution.
- `PO_ACCEPTANCE`, `MATT_DECISION` and `CANDIDATE` are **in-flight gates, not
  acceptance**. Work sitting in a gate may still be rejected, and treating a
  pending gate as satisfied would let dependent work start on an outcome that
  never arrives.

Authority:
- PO controls architecture/PID/readiness/acceptance.
- ROGUE controls dispatch state.
- FORGE PL controls build/audit loop state.
- Matt controls only declared `MATT_DECISION` gates.
- PAPER→LIVE always requires Matt/capital authority.

Suggested labels:

```text
state:*
lane:shared
lane:research
lane:trading
lane:ops
gate:po
gate:matt
risk:low
risk:medium
risk:high
risk:capital
```

Exactly one `state:*` label may be present.

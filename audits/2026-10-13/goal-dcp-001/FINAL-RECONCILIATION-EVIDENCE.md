# GOAL-DCP-001 — Final PO Reconciliation Round, Delivery Evidence (2026-10-13)

Canonical PID: `pids/GOAL-DCP-001.md`
Tracking issue: `maff0000/GOAL#1`. PR: `maff0000/GOAL#2` (`wo/GOAL-DCP-001`).
First-round evidence: `audits/2026-10-12/goal-dcp-001/`.
Repair-round evidence: `audits/2026-10-13/goal-dcp-001/REPAIR-EVIDENCE.md` and
`AUDIT-VERDICT.md` alongside this file.

This round's independent verdict is
`audits/2026-10-13/goal-dcp-001/FINAL-AUDIT-VERDICT.md`.

Matt gate: **NO**. PO gate: **YES**. Merge is **not** authorised by this work
order — delivery stops at an open governed PR.

This is the third round on GOAL-DCP-001 and the narrowest. The Product Owner /
Central Architecture reviewed PR #2 at `438bf186` and returned **CHANGES
REQUIRED**: the semantic repair of the previous round is accepted subject to
final verification, and two mandatory items remained. This is a PO / Central
Architecture decision, recorded on PR #2 by ROGUE. Nothing here is attributed
to any individual.

Corrections to earlier evidence are **forward-only**. This is a new file; no
prior evidence document, and no commit any prior evidence cites by SHA, is
rewritten.

## 1. Repository truth at dispatch

Verified directly before any work began, not taken from prior documents:

| check | result |
|---|---|
| git repository | project root is a work tree |
| remote `origin` | `maff0000/GOAL` |
| working tree | clean |
| `main` | `acc3f48ea3379843719741b56e30267845af78bd` (untouched this round) |
| `origin/wo/GOAL-DCP-001` at dispatch | `438bf186f123cbb859755ee423f832109bce1b00` |
| previous round's audited SHA | `653ce7cc2271549e82fbd10e5fbc0f6e17231c5f` |
| repaired head this round | `452c3e81646d89c597a06e923dfba061c2c03e98` |

`438bf186` is an ancestor of `452c3e81` (`git merge-base --is-ancestor`), so
history was appended by one normal commit. Nothing was amended, rebased or
force-pushed, and no commit any earlier citation points at was altered.

### FORGE startup gate

`ops/pl-startup-gate` returns RED on exactly one check — it requires a
`PID.md` at the project root, while this project's canonical PIDs live under
`pids/`. The standing waiver from the first round applies. No `PID.md`, copy,
symlink, shim or pointer was created, and the gate itself was not modified.
Repository, remote and clean tree — the gate's three substantive concerns —
were each verified independently above.

Host governance note: the `tradingGovernance` database was unreachable from the
delivery session (`ERROR 1045 (28000): Access denied`), so the session-start
governance confirmation could not state a CRITICAL rule count. Known
environment issue, recorded rather than worked around. The dispatched Engineers
and the Auditor had no access either, and each declined to fabricate a count.
It does not bear on a read-only audit or on deterministic offline tooling.

## 2. Decomposition

Two work items, dispatched **concurrently** into two worktrees the PL created
itself against the project root. Under the hub model a PL booted from the Forge
hub must not use bare `isolation: "worktree"` — that cuts a clean worktree of
the *wrong* repository. Each worktree was proved to resolve this repository's
own history with `git cat-file -t 438bf186…` and `git cat-file -t acc3f48…`
before an Engineer was dispatched, each dispatch prompt stated its absolute
worktree path and forbade the shared project path, and isolation was
re-verified after both returned.

The two items are coupled through one thing: the canonical PID's own approval
section. The PL fixed that seam as a written contract **before** dispatch — the
finding code, the five requirements, the accepted heading spellings, the
distinct-word floor, the replacement example literal, and the verbatim text of
the PID's `## Approval` section — so both Engineers implemented against a
stated interface rather than guessing at each other. The two declared overlaps
(`pids/GOAL-DCP-001.md` and `operations/ROGUE-READINESS.md`) were given
disjoint regions. Both patches applied to the integration worktree with
`git apply` and **no conflict**; the PID that landed is byte-identical to the
owning Engineer's version.

Neither Engineer committed anything. The PL reviewed both diffs and committed
them.

## 3. Item 1 — canonical PID reconciliation (PO-authorised)

The PO explicitly authorised updating `pids/GOAL-DCP-001.md` so it reflects the
implemented three-clause readiness rule. The previous round changed the
implementation and left the PID describing the rule it had replaced.

Every change to the PID, and why:

| # | change | justification |
|---|---|---|
| 1 | Target outcome 5 now reads "…`DELIVERY_READY` work for which a valid, canonical, PO-approved PID exists" | The implemented rule has a third clause. The stated outcome understated what the command guarantees. |
| 2 | Scope's validator failure list gains one bullet: "a PID that exists but is empty or effectively content-free" | The PO mandated this capability in the same decision. The list previously implied "missing PID" was the whole of the PID check. |
| 3 | The Scope readiness block gains `AND a valid, canonical, PO-approved PID exists for the item` | This block *was* the two-clause rule the implementation makes false. The two existing lines are untouched. |
| 4 | The published example changes from `{"ready":[{"id":"MT5-GW-001","target_repository":"maff0000/mt5-gateway"}]}` to `{"ready":[{"id":"EXAMPLE-ID-001","target_repository":"owner/name"}]}` | `MT5-GW-001` is `PID_DRAFT` with `pid_path: null`. It can never legitimately appear under `ready`; publishing it as ready was the defect this round corrects. |
| 5 | One new paragraph after the example | States that the example illustrates **shape** only, names no declared backlog item, and is never a dispatch authorisation. An uncaveated example is how the previous one came to be read as one. |
| 6 | Acceptance gains one item: minimum PID validity proven | The acceptance list was silent about a capability the PO mandated. The list is not restructured and no existing item is reworded. |
| 7 | New `## Approval` section | The approval record the new validity rule reads. Discussed in full below. |

**Substantive scope, non-goals and stop conditions are unchanged** — the
Non-goals and Stop conditions sections have zero diff hunks. The seven bold
header label lines are byte-unchanged, so the backlog/PID metadata comparison
sees the same label set and `BACKLOG_PID_MISMATCH` cannot fire. **No acceptance
evidence, SHA, date, verdict or approval is invented anywhere.**

The same example correction landed in `operations/ROGUE-READINESS.md`, which
republished the same line.

`tests/test_cli.py` is where the old example was mechanically load-bearing: a
test read the `{"ready"…}` line out of the PID and asserted the `MT5-GW-001`
entry appeared in it. After the correction that test would have been asserting
the defect, so it was rewritten to prove something stronger and still true. It
still reads the example out of the PID rather than restating it, still proves
the published byte contract (`json.dumps(json.loads(example), sort_keys=True,
separators=(",", ":")) == example`), now checks the entry shape against real
command output, and — the new guarantee — loads `backlog/backlog.yaml` and
asserts the example names **no declared id**. The PID's example cannot silently
claim a real pre-PID item is dispatchable again.

### The `## Approval` section, and why it is not invented evidence

The new minimum-validity rule requires approval evidence. The PO's instruction
was explicit: do not fabricate it, reference the genuine record truthfully, and
if the rule cannot be satisfied without inventing evidence or changing the
PID's substantive scope, stop and report a PID/PO conflict instead of
inventing around it. No conflict arose — the record exists.

The section cites exactly four things and claims nothing beyond them:

- `maff0000/GOAL` issue #1, the delivery tracking issue, which names
  `pids/GOAL-DCP-001.md` as the canonical PID, records the PO gate as YES and
  the Matt gate as NO, pins the base SHA `acc3f48ea…`, and states that merge is
  not authorised;
- `operations/ROGUE-DISPATCH-GOAL-DCP-001.md`, ROGUE's record of being
  instructed to deliver this PID through the existing FORGE process;
- `backlog/backlog.yaml`, which declares `po_gate: true` for `GOAL-DCP-001`;
- `maff0000/GOAL` pull request #2 on `wo/GOAL-DCP-001`, with the evidence trail
  under `audits/`.

It records approval **of the PID** — the authority that permitted the item to
leave `PID_DRAFT` and reach `DELIVERY_READY` — and says so twice, explicitly
naming `PO_ACCEPTANCE` as the separate later gate and deferring the item's
current state to `backlog/backlog.yaml`. That distinction is what keeps the
rule non-circular: `GOAL-DCP-001` is itself in `FORGE_AUDIT`, a PID-required
state, so it is subject to the rule it implements. A rule that required a
statement of *delivery acceptance* would make an item's PID validity depend on
its own delivery outcome.

The PID as it stood at `438bf186` fails this round's own rule
(`PID_INVALID … no 'approval evidence' section with substantive content`). The
section was necessary, not decorative. The Auditor proved this independently.

## 4. Item 2 — minimum PID validity

### The defect

`PID_FILE_NOT_FOUND` proved the pointer resolved and `BACKLOG_PID_MISMATCH`
proved the metadata agreed — and a single `touch` of the pointed-to file
satisfied both, because the file existed and a label the PID omits is not a
mismatch. A zero-byte document therefore established delivery readiness while
carrying none of the authority a PID exists to carry.

### The rule, exactly

New finding code **`PID_INVALID`**, in `tools/goal_dcp/validate.py`. Evaluated
only when the item's `state` is structurally sound, is a member of the state
vocabulary, **and is one of `PID_REQUIRED_STATES`** — `DELIVERY_READY` onward
and nowhere else — and only once `pid_path` has resolved to a file read
successfully as UTF-8, i.e. after `PID_FILE_NOT_FOUND` has been ruled out.

Five requirements, all of which must hold:

| # | requirement | what is read |
|---|---|---|
| R1 | identity | the file's **first** ATX heading must name the item's `id` as a whole token — an occurrence not adjacent to `[A-Za-z0-9_-]`, so `# GOAL-DCP-0011` does not establish identity for `GOAL-DCP-001`. No ATX heading at all fails R1. |
| R2 | purpose | a section whose normalised heading is exactly `purpose` or `objective`, with a non-trivial body |
| R3 | scope | likewise `scope` |
| R4 | acceptance criteria | likewise `acceptance` or `acceptance criteria` |
| R5 | approval evidence | likewise `approval`, `approval evidence` or `po approval` |

A heading is normalised by stripping leading `#`s and surrounding whitespace,
stripping a trailing `:`, collapsing internal whitespace runs to one space and
case-folding. Matching is **exact equality**, never a substring test: `## Out of
scope` and `## Non-goals (scope)` both contain "scope" and neither states the
item's scope. A section's body is the lines after its heading up to the next
ATX heading of any level or end of file; each heading occurrence is its own
section, so two thin `## Scope` sections never pool into one substantive one.

**Non-trivial body: at least 6 distinct words**, where a word is a maximal run
of `[A-Za-z0-9]` of length 2 or more and distinctness is case-folded. Distinct
words, not characters, bytes, lines or total words — padding such as
`xxxxx xxxxx xxxxx xxxxx xxxxx xxxxx` yields one.

One file yields **at most one** `PID_INVALID` finding, naming every unmet
requirement with the reasons sorted. The defect is the document, not each
heading it lacks; five findings on one zero-byte file would break the module's
documented one-defect-one-finding precedence. `PID_INVALID` and
`BACKLOG_PID_MISMATCH` are independent and may co-occur: a structurally
incomplete document and a document whose metadata contradicts the backlog are
different defects, and a reader repairing a PID needs to be told both.

### What the rule does not establish, stated plainly

It is a **structural** check. It proves the five things are present and not
content-free. It cannot and does not judge whether what they say is good,
correct, complete or sufficient — a PID can satisfy every requirement and still
be a bad PID. Semantic quality is the item's PO gate, and the rule deliberately
stops rather than accumulating heuristics that would let it pretend otherwise.

The concrete consequence, measured rather than estimated: the cheapest document
that passes is 133 bytes — the id as a heading and six distinct two-character
words under each of the four required headings. `tests/fixtures/pid-valid-minimal.md`
pins that boundary in the test suite and says of itself that it is nowhere near
an acceptable real PID. `operations/ROGUE-READINESS.md` states the same limit
to ROGUE in prose. There is no gap between the documented floor and the
enforced floor, and no claim anywhere that the check does more than it does.

### Purity and the gate that makes it bite

`tools/goal_dcp/readiness.py` gained **no clause** and still reads no file;
both it and `tools/goal-ready` changed by docstring only, which the Auditor
confirmed by reading both diffs in full. The whole behavioural change is in
`validate.py`. The two-layer PID rule stands: readiness checks that an item
*declares* a PID, the validator proves the declared PID exists, is readable, is
structurally valid and agrees with the backlog, and `./tools/goal-ready`
validates first and refuses to answer from an invalid backlog. That existing
refusal is what makes `PID_INVALID` bite on the `ready` answer — no second
invariant check was added, because one would have had to read the PID file from
a module that must stay pure.

### Fixtures

Minimum PID validity means a PID must name the item that declares it, so a
single fixture PID can no longer be shared across differently-identified items.
Fourteen validator and readiness fixtures now declare their own PID. Eight new
invalid fixtures cover zero-byte, whitespace-only, empty-section,
wrong-identity (including a `GOAL-DCP-0011`-style near-miss), approval-less,
acceptance-less, keywords-as-prose and padded PIDs — each isolating
`PID_INVALID` and nothing else, preserving the one-fixture-one-code discipline
in `tests/fixtures/README.md`. Two negative controls cover a minimal valid PID
sitting exactly on the six-word floor and a `PID_DRAFT` draft that must yield
nothing. `tests/fixtures_readiness/state_not_delivery_ready.yaml` was
deliberately left as it was: its item is `ARCHITECTURE_REQUIRED`, so it is a
live proof the rule is state-scoped.

No test assertion was weakened. `tests/test_readiness.py`'s PID-finding-code
guard was expanded to include `PID_INVALID`, which is what forced the fixture
repointing rather than letting fixtures quietly become documents the validator
rejects. Test functions went from 209 to 232; none was deleted.

### Documentation

`backlog/SCHEMA.md` holds the rule — the five requirements, the accepted
heading spellings, the distinct-word floor with each thing it rejects, the
honest structural-only limit, the non-circularity argument and the
state-conditionality. `governance/DELIVERY-STATE-MACHINE.md` and
`operations/ROGUE-READINESS.md` cite it rather than restating it; five
documents independently restating one rule is how this class of defect
recurred in the first place. `README.md`'s validator row gains the check.
`operations/ROGUE-READINESS.md` previously *admitted* that a stub PID would
satisfy the validator while delivering none of the authority a PID exists to
carry; that admission is now mechanically false, and the limit that remains is
stated rather than glossed. `MANIFEST.md` was regenerated with
`./tools/goal-docs --write` after the new files were staged, never hand-edited.

## 5. Items 3 and 4 — deferred, and confirmed not smuggled in

**State-machine documentation drift guard: DEFERRED by the PO.** Not
implemented. It remains an acknowledged **unguarded** item: no test reads
`governance/DELIVERY-STATE-MACHINE.md`, so its prose can still drift from
`tools/goal_dcp/model.py` without anything failing. ROGUE recorded it as
`maff0000/GOAL#3`. GOAL-DCP-001 was not expanded with it. The Auditor confirmed
independently that `tools/goal_dcp/docsync.py` and `tools/goal-docs` have zero
diff hunks, that the generated-region set is unchanged, and that no marker pair
was added to the state-machine document.

**FORGE framework issues: DEFERRED.** Recorded by ROGUE as `maff0000/forge#5..#8`.
None of those repairs is mixed into this PR and `/srv/forge` was not modified.
The Auditor confirmed no path in the diff matches `forge`, `.claude` or
`skills/`.

## 6. Mechanical results — fresh checkout of the repaired head

Run by the PL in a `git clone --no-local` of `452c3e81` under `/tmp`, not in
any working tree. **No `chmod` was issued.** `git ls-files -s tools/` records
`100755` for `goal-docs`, `goal-ready`, `goal-validate` and `secret-scan`; all
four were executable straight out of the clone.

Environment: Python 3.11.2, pytest 9.0.2, gitleaks 8.30.1.

| command | result |
|---|---|
| `python3 -m pytest tests/ -q` | **357 passed** (276 at `438bf186`) |
| `./tools/goal-validate` | `backlog OK: 40 items`, rc 0 |
| `./tools/goal-docs --check` | `goal-docs: generated regions in sync`, rc 0 |
| `./tools/secret-scan` | working tree CLEAN, git history CLEAN, `RESULT: CLEAN`, rc 0 |

Readiness answers at `452c3e81`:

```text
./tools/goal-ready                                      -> {"ready":[]}
./tools/goal-ready --assume-closed GOAL-DCP-001         -> {"ready":[]}
./tools/goal-ready --pid-wave                           -> {"pid_authoring_wave":[]}
./tools/goal-ready --pid-wave --assume-closed GOAL-DCP-001
  -> the eleven items below, all PID_DRAFT, sorted by id
```

```text
ARES-CUR-001  DARWIN-R1  GOAL-CONTRACT-001  HERMES-CUR-001  MT5-GW-001
OPS-CRED-001  OPS-LEGACY-001  OPS-SAFE-001  OPS-SAFE-002  OPS-SAFE-003
TRON-T1
```

`{"ready":[]}` is the correct answer, not an empty one: no item is
`DELIVERY_READY`. The eleven are awaiting **PO PID authoring** and are not
FORGE-dispatchable.

### CI on the pushed head

`https://github.com/maff0000/GOAL/actions/runs/38394498308`, head
`452c3e81646d89c597a06e923dfba061c2c03e98`, event `pull_request`, conclusion
**success**. Every step green: Validate backlog, Check generated documents for
drift, Secret scan, Run test suite.

### No unrelated changes

`git diff --stat 438bf186 452c3e81` covers 47 paths, reviewed path by path, all
under `tests/`, `tools/`, `pids/`, `backlog/`, `governance/`, `operations/`,
`MANIFEST.md` and `README.md`. `backlog/backlog.yaml`, `.github/`,
`architecture/`, `decisions/`, `templates/`, `conftest.py`,
`tools/goal_dcp/model.py` and `tools/goal_dcp/docsync.py` are untouched.
`MANIFEST.md` gained exactly 15 bullets and the diff added exactly 15 files,
matched one for one. No new dependency file, no daemon, no scheduler, no
committed browser or test framework. No `/srv` path was added by this diff.
`main` remains `acc3f48ea…`.

## 7. PL spot-check of the Auditor

Routine, not triggered by a contradiction: an Auditor that has never been
independently checked is not proven independent, it is trusted by default. The
PL re-ran the Auditor's three findings and its bypass claim directly against
the artifact in a sandbox, and every one reproduced exactly, including the
133-byte figure and the six-versus-five-distinct-word boundary:

| Auditor claim | PL re-run |
|---|---|
| UTF-8 BOM on the real PID → `PID_INVALID … the first heading does not name 'GOAL-DCP-001'` | reproduced verbatim |
| `##` indented by two spaces → all four sections reported missing | reproduced verbatim |
| `## Purpose ##` (closed ATX) → purpose reported missing | reproduced verbatim |
| 133-byte, six-distinct-word document passes; the five-word variant fails | reproduced, byte count confirmed |
| required headings inside a fenced code block pass (lenient-only) | reproduced |
| `/srv/GOAL` strings predate this round | confirmed: added by `acc3f48`; this diff adds zero `/srv` paths |

The Auditor's worktree was byte-clean at `452c3e81` afterwards and the shared
project root and integration worktree were untouched, so it audited without
editing, as required.

## 8. Adjudication of the Auditor's three findings

The verdict is **GREEN** with three findings, all low/nit, **zero RED**. None
falsifies a delivered claim. All three fail **closed** — they can block a
genuinely ready item with a confusing message; none can cause a wrong dispatch.
They are recorded rather than repaired, because repairing a low hardening nit
after GREEN would invalidate the audited head and cost a full round for no RED,
and the Auditor stated it would not hold the round for any of them.

1. **`_ATX_HEADING_PATTERN` accepts a strict subset of CommonMark ATX, and the
   gap is undocumented.** A UTF-8 BOM, a heading indented one to three spaces,
   or a closed ATX heading (`## Purpose ##`) each make a legitimate PID
   `PID_INVALID` — and the BOM case reports "the first heading does not name
   …", which points the reader at the wrong defect. Setext exclusion *is*
   documented in the module; these three are not. **This is the one worth
   fixing** and the fix is cheap: read the PID with `encoding="utf-8-sig"` and
   either widen the pattern or state the subset in `backlog/SCHEMA.md`. Left
   for the PO to schedule rather than recorded as a GitHub issue unilaterally —
   recording follow-ups is ROGUE's, and the PO's, call.
2. **Fenced code blocks are not tracked**, so a required heading inside a code
   fence counts as a section the renderer never shows. Already disclosed in the
   implementation's own docstring and correctly characterised there as
   lenient-only: it can let a section be found that a renderer would not show,
   never refuse one that is really there. A known limit, not a defect. Worth
   knowing as a latent trap for a future PID author pasting a shell example
   with a `# comment` line.
3. **`/srv/GOAL` absolute host paths in two pre-existing `operations/`
   documents.** Traced to `acc3f48`, the root commit of `main`. This round
   introduced none. Out of scope for this diff; raised only because the
   dispatch asked about host-specific topology in the public tree.

## 9. What remains for the PO

- **Acceptance of this PR.** Merge is not authorised by this work order.
- **Finding 1**, the ATX/BOM tolerance fix, if the PO wants it scheduled rather
  than left as a known subset.
- **`maff0000/GOAL#3`**, the state-machine documentation drift guard, still
  deferred and still unguarded.
- Nothing else. No PID/architecture conflict was uncovered, and no stop
  condition in `pids/GOAL-DCP-001.md` was reached.

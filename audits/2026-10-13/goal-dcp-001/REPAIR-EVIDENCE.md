# GOAL-DCP-001 — Repair-Round Delivery Evidence (2026-10-13)

Canonical PID: `pids/GOAL-DCP-001.md`
Tracking issue: `maff0000/GOAL#1`. PR: `maff0000/GOAL#2` (`wo/GOAL-DCP-001`).
First-round evidence: `audits/2026-10-12/goal-dcp-001/`.

Matt gate: **NO**. PO gate: **YES**. Merge is **not** authorised by this work
order — delivery stops at an open governed PR.

This round is a repair, not a new increment. The Product Owner / Central
Architecture reviewed PR #2 and returned **CHANGES REQUIRED**: the architecture
is accepted, and what follows is semantic hardening. This is a PO / Central
Architecture decision, recorded on PR #2 by ROGUE.

## 1. Repository truth at dispatch

Verified directly before any work began, not taken from prior documents:

| check | result |
|---|---|
| git repository | project root is a work tree |
| remote `origin` | `maff0000/GOAL` |
| working tree | clean |
| `main` | `acc3f48ea3379843719741b56e30267845af78bd` (untouched this round) |
| `origin/wo/GOAL-DCP-001` | `b40c4f131b2a026b0e5f25c5b953bc9e32951c36` |
| first-round audited SHA | `16e28909c43e8ea07ba27544f66fd830bec794f3` |

### FORGE startup gate

`ops/pl-startup-gate` returned RED on exactly one check — it requires a
`PID.md` at the project root, while this project's canonical PIDs live under
`pids/`. The standing waiver from the first round applies. No `PID.md`, copy,
symlink, shim or pointer was created, and the gate itself was not modified:
papering over a gate to make it pass would defeat the only thing it is for.
Repository, remote and clean tree — the gate's three substantive concerns —
were each verified independently above.

Host governance note: the `tradingGovernance` database was unreachable from the
delivery session, so the session-start governance confirmation could not be
issued. Known environment issue, not a delivery blocker; recorded rather than
worked around.

## 2. The two blockers, and what was delivered

### Blocker 1 — `DELIVERY_READY` must mean actually delivery-ready

`state: DELIVERY_READY` with `pid_path: null` was permitted, and
`operations/ROGUE-READINESS.md` told ROGUE such an item was "ready but cannot
be dispatched until the PO authors a PID". An item with no PID has nothing for
a FORGE PL to build to — no scope, no non-goals, no definition of acceptance —
so calling it ready promises a dispatch that cannot happen and moves the job of
discovering that onto whoever acts on the answer.

**The rule now: no PID = not `DELIVERY_READY`.** Canonical sequence:
`ARCHITECTURE_REQUIRED → PID_DRAFT → PO_REVIEW → DELIVERY_READY →
ROGUE_DISPATCHED → FORGE_BUILD`. *Architecture before PID, PID before build.*

- **Validator.** `DELIVERY_READY` joined `PID_REQUIRED_STATES`. A
  `DELIVERY_READY` item is RED when `pid_path` is null (`MISSING_PID`), absent
  (`MISSING_FIELD`), wrong-typed (`INVALID_FIELD_TYPE`), unusable as a
  repo-relative path or naming a file that does not exist or cannot be read
  (`PID_FILE_NOT_FOUND`), or when PID metadata disagrees with the backlog
  (`BACKLOG_PID_MISMATCH`). Existing finding precedence is preserved — one
  defect, one finding. Every later delivery state still requires a PID,
  asserted against the state vocabulary mechanically rather than by eye.
  Pre-delivery states still do not; `CANCELLED` does not either, because work
  can be abandoned before it was ever specified.
- **Readiness.** The dispatch rule gained a third clause: the item must declare
  a PID. `tools/goal_dcp/readiness.py` stays pure — no file I/O — so this is
  the *data* half of a two-layer rule. The validator owns the other half (file
  exists, readable, metadata agrees), and `tools/goal-ready` validates first
  and refuses to answer from an invalid backlog. A *successful* `ready` answer
  therefore cannot contain an item whose PID does not exist. `goal-ready` also
  re-checks that post-condition at the emit boundary before printing.
- **Documentation.** The ready-without-PID doctrine is removed. The rule is now
  stated once, in full, in `governance/DELIVERY-STATE-MACHINE.md` — the
  state-vocabulary authority — and `operations/ROGUE-READINESS.md`,
  `backlog/SCHEMA.md`, `architecture/DELIVERY-CONTROL-PLANE.md` and `README.md`
  cite it rather than re-deriving it. Five documents independently restating
  one rule is how this class of defect recurs.

### The eleven: a PID-authoring wave, not a dispatchable wave

The eleven post-DCP items have no canonical PIDs. **No placeholder, shim or
content-free PID was created** to preserve the old test expectation; `pids/`
contains exactly one file, the real canonical PID. The eleven moved from
`DELIVERY_READY` to `PID_DRAFT` — Central Architecture's preferred pre-delivery
state, their architecture intent already being sufficient for PO PID authoring.
None of the eleven was placed in `ARCHITECTURE_REQUIRED`, because nothing in
the repository's own architecture or backlog text shows any of them still
needing an architectural decision before its PID can be written.

They remain mechanically identifiable, via a new mode on the existing command
rather than new infrastructure:

```bash
./tools/goal-ready --pid-wave                               # {"pid_authoring_wave":[]}
./tools/goal-ready --pid-wave --assume-closed GOAL-DCP-001  # exactly the eleven
```

The answer carries its own key, `pid_authoring_wave`, never `ready`. `ready` is
the published FORGE-dispatchable contract; emitting a PID-less item under it
would tell ROGUE to dispatch work FORGE cannot build. The rule is: own state
`PID_DRAFT` and every dependency accepted-terminal. It is computed, never a
written-down list.

### Blocker 2 — `GOAL-DCP-002` duplicated `GOAL-DCP-001`

At `b40c4f13`, `GOAL-DCP-002` was titled *"Machine-readable backlog +
dependency/readiness validator"* — precisely what `GOAL-DCP-001` delivers. The
sequence is reconciled:

| item | definition | state | depends on | risk |
|---|---|---|---|---|
| `GOAL-DCP-001` | GitHub control-plane authority: machine backlog, validation, dependency graph, strict delivery readiness, generated views, CI enforcement | `FORGE_AUDIT` | — | medium |
| `GOAL-DCP-002` | ROGUE dispatcher — deterministic consumption and multi-project dispatch control. ROGUE consumes canonical GOAL state and safely dispatches independent FORGE PLs without Matt mediating work selection. **Not** automated GitHub-triggered execution | `ARCHITECTURE_REQUIRED` | `GOAL-DCP-001` | medium |
| `GOAL-DCP-003` | Automated GitHub-triggered sandboxed delivery launch, only after DCP-002's dispatcher behaviour is proven | `ARCHITECTURE_REQUIRED` | `GOAL-DCP-002` | high |
| `GOAL-DCP-004` | Automated PO/ROGUE status and stale/blocked brief (retained) | `ARCHITECTURE_REQUIRED` | `GOAL-DCP-002` | low |

`GOAL-DCP-003`'s risk rose from medium to high: autonomous launch carries
operational/execution-system impact. All three remain pre-delivery with
`pid_path: null`, which is exactly what the rule above requires of an item
with no PID. **No auto-merge anywhere** —
`architecture/DELIVERY-CONTROL-PLANE.md`'s rung 4 previously read "selective
auto-merge", contradicting both the backlog's DCP-004 and the standing rule;
every surviving mention of auto-merge is now an explicit negation.

## 3. Process

Decomposed into two work items with genuinely disjoint file sets — the
mechanically-coupled core (code, tests, fixtures, `backlog.yaml`, the generated
human view) and the doctrine documents — dispatched to two bounded Engineers in
parallel. No test in the suite reads any of the five doctrine documents, which
is what made the split genuinely independent rather than merely convenient. The
identical written contract went to both.

Worktrees were created explicitly against the project root, and
`git cat-file -t` on the project's own commits was run inside each before
dispatch: under the hub model a bare `isolation: "worktree"` flag cuts a
worktree from the *PL's* repository, which would have handed each Engineer a
clean worktree of the wrong project's history. Isolation was re-verified after
each dispatch; the two diffs had **zero** overlapping paths, and the integrated
tree was confirmed byte-for-byte identical to the union of both.

The seam — consistency between the two halves, which neither Engineer could see
— was checked by the PL: every state set in the doctrine documents was compared
against `tools/goal_dcp/model.py` programmatically, and the whole tree was
swept for surviving statements of the old doctrine.

One repair cycle was needed. The integrated suite came back **1 failed, 275
passed**: the first Engineer had written a negative fixture encoding a
deliberately PID-less `DELIVERY_READY` item *and* a blanket fixture-integrity
guard asserting no fixture does that. Each was individually correct; the
contradiction existed only in the relationship between them. A fresh repair
Engineer replaced the blanket guard with an explicit, self-policing exemption
scoped to the one `(fixture, item)` pair, which fails if the exemption stops
being earned, and removed a second incidental defect from that fixture.

## 4. Acceptance evidence — fresh checkout of the repaired head

Run in a **fresh `git clone`** of `653ce7c`, not in the integration working
tree, and with **no `chmod`**: an earlier round of this project produced a
false green through permission adjustment, so the recorded modes are part of
what is being verified. `git ls-files -s tools/` records `100755` for all four
entry points, and all four were executable straight out of the clone.

```
$ python3 -m pytest tests/ -q
276 passed

$ ./tools/goal-validate                 backlog OK: 40 items                exit 0
$ ./tools/goal-docs --check             generated regions in sync           exit 0
$ ./tools/secret-scan                   working tree CLEAN, history CLEAN   exit 0
$ ./tools/goal-ready                    {"ready":[]}                        exit 0
$ ./tools/goal-ready --with-pid         {"ready":[]}                        exit 0
$ ./tools/goal-ready --assume-closed GOAL-DCP-001
                                        {"ready":[]}                        exit 0
$ ./tools/goal-ready --pid-wave         {"pid_authoring_wave":[]}           exit 0
```

`python3 -m pytest tests/ -q` is the single acceptance test command.

`{"ready":[]}` is the honest answer and the point of the repair: nothing in the
programme is FORGE-dispatchable right now, because nothing has both an approved
canonical PID and satisfied dependencies. `GOAL-DCP-001` itself is in
`FORGE_AUDIT`, deliberately not an accepted terminal state.

### The next PID-authoring wave, proven mechanically

```
$ ./tools/goal-ready --pid-wave --assume-closed GOAL-DCP-001
{"pid_authoring_wave":[{"id":"ARES-CUR-001","target_repository":"maff0000/ARES"},{"id":"DARWIN-R1","target_repository":"maff0000/DARWIN"},{"id":"GOAL-CONTRACT-001","target_repository":"maff0000/GOAL"},{"id":"HERMES-CUR-001","target_repository":"maff0000/hermes"},{"id":"MT5-GW-001","target_repository":"maff0000/mt5-gateway"},{"id":"OPS-CRED-001","target_repository":"maff0000/GOAL"},{"id":"OPS-LEGACY-001","target_repository":"maff0000/GOAL"},{"id":"OPS-SAFE-001","target_repository":"maff0000/GOAL"},{"id":"OPS-SAFE-002","target_repository":"maff0000/GOAL"},{"id":"OPS-SAFE-003","target_repository":"maff0000/GOAL"},{"id":"TRON-T1","target_repository":"maff0000/tron"}]}
```

Exactly the eleven. The proof is non-vacuous by construction: the wave is
asserted **empty** before closure, so the post-projection assertion is not
measuring a list that was always there; the post-projection set is asserted
**equal** to the eleven, so an over-permissive rule fails as loudly as an
over-restrictive one; `GOAL-DCP-002` has fully satisfied dependencies under the
projection and stays out **on state alone**, which is what proves the state
clause independently; and a `PID_DRAFT` item with an unmet dependency stays out
— proven against a temporary copy, since every `PID_DRAFT` item in canonical
data depends only on `GOAL-DCP-001` and canonical data therefore cannot prove
it. No wave id is hard-coded anywhere, asserted against
comment-and-docstring-stripped source so that prose may cite an id while
executable code may not.

## 5. Correction to commit `653ce7c`'s message — overclaim

**Recorded here rather than by amending the commit.** The repair-round Auditor
cited `653ce7c` by SHA, so rewriting it would break that citation while leaving
the overclaim uncorrected where a reader following the citation arrives.

Commit `653ce7c`'s message states: *"Each set is byte-checked against
`tools/goal_dcp/model.py`."* **That is an overclaim.** The byte-check was real
but was performed **by the PL by hand at integration time** — it is not a
mechanical guard in the test suite, and nothing in `tests/` reads
`governance/DELIVERY-STATE-MACHINE.md`. The Auditor caught this (finding F1)
and the PL confirmed it independently: removing `DELIVERY_READY` from that
document's PID-required block, and separately adding `CANCELLED` to its
accepted-terminal block, each leave the suite at **276 passed** and
`./tools/goal-docs --check` green.

The documents are correct at this commit — all six were read end to end, and
every state set in them was compared against `model.py` and matched exactly.
Nothing shipped is wrong. What the message should have said is that the sets
were verified by hand, and that the document designated as the single authority
for the rule is the one restatement of machine truth in this repository with no
mechanical guard behind it. That gap is recorded as a follow-up in §6.

## 6. Open items for the Product Owner — not repaired here

Each is either outside this work order's authority or outside the PO's stated
scope for it. None was invented around.

1. **The canonical PID still states the pre-repair rule.**
   `pids/GOAL-DCP-001.md` defines readiness as two clauses and publishes
   `{"ready":[{"id":"MT5-GW-001","target_repository":"maff0000/mt5-gateway"}]}`
   as its example. `MT5-GW-001` is now `PID_DRAFT`, so the tool classifies that
   item the opposite way. The PL adjudicated this as a documentation divergence
   rather than an unresolvable contradiction — the third clause is a
   *restriction*, so the shipped rule can never emit anything the PID's rule
   would forbid; the PID already lists "missing PID" among the validator's
   required failure modes; and the PO's CHANGES REQUIRED supersedes earlier PID
   prose on exactly this point. The Auditor agreed on the substance and argued
   the PO-authored PID update should be **closure-blocking** rather than an
   intention. `pids/` is PO authority; the PL did not edit it.
2. **A content-free PID satisfies the gate.** A zero-byte `pids/X.md` with
   `pid_path: pids/X.md` passes `goal-validate` and `goal-ready` emits the item
   as `ready` — PL-confirmed directly. `BACKLOG_PID_MISMATCH` compares only
   labels the PID actually declares, so a PID declaring none agrees vacuously.
   This is within the PID's failure modes as written, and
   `operations/ROGUE-READINESS.md` already forbids stub PIDs in prose — but the
   hardening is bypassable by one `touch`. Defining what makes a PID
   substantive (which labels a canonical PID must declare) is a PO decision,
   so no rule was invented.
3. **`governance/DELIVERY-STATE-MACHINE.md` has no mechanical drift guard.**
   See §5. The natural fix is a test that reads the document's state blocks and
   compares them to `model.py`, in the spirit of the existing generated-region
   checks. Deliberately not added in this round: it would change the test suite
   after the audited head, making the audited code no longer the delivered
   code for the sake of a gap that falsifies nothing shipped.
4. **Test coverage gap, low severity.** Removing the `goal-ready` emit-time
   post-condition's *wiring* in `main()` leaves the suite green, because the
   CLI path is unreachable while validation stands. The function itself is
   directly tested.
5. **Inaccurate justification, corrected here.** Ten fixtures under
   `tests/fixtures_readiness/` carry an incidental `MISSING_PID` on a `DEP-*`
   dependency item. These were deliberately left, and the substance is sound —
   the Auditor confirmed empirically that a dependency's own `pid_path` is
   never read when deciding whether it satisfies a dependant. But the reason
   recorded during the round, that readiness fixtures are never validated, is
   **false**: the fixture-integrity guard does call `validate()` on them and
   merely scopes its assertion to `DELIVERY_READY` items. Right answer, wrong
   reason; the correct reason is the one above.
6. **Accepted public-repo residue, unchanged by PO ratification.** No history
   rewrite; root commit `acc3f48` untouched; generic project paths in
   historical files remain; the MT5 ADR bind-all-address reference remains.

## 7. Boundaries honoured

- No merge. The PR stays open and unmerged pending PO acceptance.
- `main` untouched at `acc3f48ea3379843719741b56e30267845af78bd`.
- No history rewritten, no commit amended, no force-push. Both corrections to
  first-round evidence were appended in a new commit, leaving the original text
  intact and readable.
- No secrets; no host-specific topology introduced into tracked files.
- No PID authored, and no placeholder PID created.
- No new autonomous dispatch machinery, no daemon, no scheduler, no new tool —
  `--pid-wave` is a mode on the existing command.

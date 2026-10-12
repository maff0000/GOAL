# GOAL-DCP-001 — Delivery Evidence

Canonical PID: `pids/GOAL-DCP-001.md`
Delivery tracking issue: `maff0000/GOAL#1`
Delivery train: ROGUE → FORGE. Implementation by a FORGE PL with bounded
Engineer dispatches and an independent fresh-context Auditor.

Matt gate: **NO**. PO gate: **YES**. Merge is **not** authorised by this
work order — delivery stops at an open governed PR.

## 1. Repository truth at dispatch

Verified directly before any work began, not taken from prior documents:

| check | result |
|---|---|
| git repository | `/` project root is a work tree |
| remote `origin` | `maff0000/GOAL` |
| working tree | clean |
| `main` | `acc3f48ea3379843719741b56e30267845af78bd` |
| `origin/main` | same SHA — nothing unpushed |
| repository visibility | public |
| history | `acc3f48` is the root commit |

Base SHA for this increment: **`acc3f48ea3379843719741b56e30267845af78bd`**
Branch: **`wo/GOAL-DCP-001`**

### FORGE startup gate

`ops/pl-startup-gate` returned RED on exactly one check — it requires
`$PROJECT_ROOT/PID.md`, while this is a multi-PID repository whose canonical
PID is `pids/GOAL-DCP-001.md`. Central Architecture authorised a narrow
waiver of that single check. No `PID.md` was created, no copy, symlink, shim
or pointer, and the gate itself was not modified.

Every other precondition was independently verified and passed: repository,
remote, clean tree, base SHA, branch isolation, PID compliance, mechanical
tests, secret scanning, independent audit and PR governance.

## 2. What was delivered

| path | purpose |
|---|---|
| `backlog/backlog.yaml` | canonical machine-readable automation authority, 40 items |
| `backlog/SCHEMA.md` | field reference for the above |
| `tools/goal_dcp/model.py` | vocabularies, identifier rules, structural loader |
| `tools/goal_dcp/validate.py` | deterministic validator, 21 finding codes |
| `tools/goal_dcp/readiness.py` | deterministic readiness rule |
| `tools/goal_dcp/docsync.py` | generated-region sync for the human views |
| `tools/goal-validate` | validator command |
| `tools/goal-ready` | readiness command |
| `tools/goal-docs` | generated-document drift check / rewrite |
| `tools/secret-scan` | repeatable public-repository secret scan |
| `tests/` | 216 tests, including deliberately invalid fixtures |
| `operations/ROGUE-READINESS.md` | how ROGUE consumes readiness without Matt |
| `.github/workflows/control-plane.yml` | CI: validate, drift, scan, tests |

`MASTER-BACKLOG.md` remains the human view. Its table and first-wave list
are now generated regions rendered from `backlog/backlog.yaml`, so the two
cannot become independent truths. `MANIFEST.md`'s file list is likewise
generated from `git ls-files`.

## 3. Acceptance commands and results

All run from the repository root in a **fresh checkout** of the delivered
head, not in a working tree that had been manually adjusted.

```text
$ python3 -m pytest tests/ -q
216 passed

$ ./tools/goal-validate
backlog OK: 40 items                                        exit 0

$ ./tools/goal-docs --check
goal-docs: generated regions in sync                        exit 0

$ ./tools/secret-scan
working-tree (gitleaks dir): CLEAN
git-history (gitleaks git): CLEAN
RESULT: CLEAN                                               exit 0

$ ./tools/goal-ready
{"ready":[]}                                                exit 0
```

`python3 -m pytest tests/ -q` is this PID's single acceptance test command.

Environment: Python 3.11.2, PyYAML 6.0, pytest 9.0.2, gitleaks 8.30.1.

### Secret scan

`tools/secret-scan` covers the working tree **and** full git history,
because a clean working tree says nothing about history. It is repeatable,
deterministic, and also runs in CI against a pinned gitleaks 8.30.1.

Two gitleaks behaviours made a naive wrapper unsafe, both confirmed by
direct observation rather than assumption:

- `gitleaks git` exits `0` with `0 commits scanned` when handed a path that
  is not a git repository. A wrapper trusting that exit status would report
  a never-scanned history as clean. The wrapper therefore pre-checks that
  the target is a repository with commits.
- gitleaks uses exit `1` for both "leaks found" and "the scan crashed". The
  wrapper moves the findings signal to a dedicated exit code so any other
  non-zero exit is treated as a failure to scan. A scan that could not run
  is never reported as a scan that passed.

The test suite carries a **positive control**: a fake credential is planted
in a temporary repository and detection is asserted. A scanner that never
fires is indistinguishable from one that does nothing.

## 4. Readiness is mechanical

The rule, implemented once and generically in `tools/goal_dcp/readiness.py`:

```text
state == DELIVERY_READY
AND every dependency resolves to a declared item whose state is an
    accepted terminal state
```

`ACCEPTED_TERMINAL_STATES = {MERGED, DEPLOYMENT_READY, PAPER, LIVE, CLOSED}`.

`CANCELLED` is terminal but **not** accepted — cancelled work stopped
without ever delivering the outcome something depended on. `BLOCKED` is not
terminal. `PO_ACCEPTANCE`, `MATT_DECISION` and `CANDIDATE` are in-flight
gates, not acceptance.

There is **no hard-coded readiness list and no per-id special case.** A test
asserts this mechanically against comment- and docstring-stripped source:
no first-wave id appears in `readiness.py` or `docsync.py`, and the only id
in executable code is `GOAL-DCP-001` as the documented first-wave
projection *input*.

Readiness **fails closed**: a dependency that does not resolve to a declared
item makes the dependent item not ready, so shorthand, wildcards and typos
never unblock work by default.

## 5. First-wave proof

`GOAL-DCP-001` is recorded in state `FORGE_AUDIT` — deliberately **not** an
accepted terminal state, because this increment is the one under audit. So
the proof runs against canonical data, not only fixtures.

**Before closure** — the honest current answer:

```text
$ ./tools/goal-ready
{"ready":[]}
```

**Under the projection that `GOAL-DCP-001` reaches an accepted terminal
state:**

```text
$ ./tools/goal-ready --assume-closed GOAL-DCP-001
{"ready":[{"id":"ARES-CUR-001","target_repository":"maff0000/ARES"},{"id":"DARWIN-R1","target_repository":"maff0000/DARWIN"},{"id":"GOAL-CONTRACT-001","target_repository":"maff0000/GOAL"},{"id":"HERMES-CUR-001","target_repository":"maff0000/hermes"},{"id":"MT5-GW-001","target_repository":"maff0000/mt5-gateway"},{"id":"OPS-CRED-001","target_repository":"maff0000/GOAL"},{"id":"OPS-LEGACY-001","target_repository":"maff0000/GOAL"},{"id":"OPS-SAFE-001","target_repository":"maff0000/GOAL"},{"id":"OPS-SAFE-002","target_repository":"maff0000/GOAL"},{"id":"OPS-SAFE-003","target_repository":"maff0000/GOAL"},{"id":"TRON-T1","target_repository":"maff0000/tron"}]}
```

Exactly the eleven items, matching the backlog's own documented first wave.

### Why the proof is not vacuous

Asserted in `tests/test_first_wave.py`:

1. **Before** closure, each of the eleven ids is specifically asserted
   **absent** — the ready set is empty, so a rule that always returned
   everything would fail here.
2. **After** the projection, the ready set is asserted **equal** to exactly
   those eleven — set equality, not containment, so extras fail too.
3. **The state clause is independently load-bearing.** `GOAL-DCP-002`
   depends only on `GOAL-DCP-001`, so under the projection its dependencies
   *are* satisfied — yet it must stay out, because its own state is
   `ARCHITECTURE_REQUIRED`. A rule that checked only dependencies would
   wrongly admit it.
4. **Items with unmet dependencies stay out** under the projection:
   `HERMES-FACT-001`, `GOAL-CORE-001`, `PAPER-E2E-001`, `LIVE-GATE-001`.
5. **`LIVE-GATE-001` needs all six declared dependencies.** Progressively
   larger projected subsets are asserted to leave it out until the sixth
   closes, plus a loop holding exactly one of the six open each time. This
   is the Central Architecture no-wildcard requirement proven mechanically
   rather than asserted in prose.
6. Fixtures prove each accepted terminal state satisfies a dependency, that
   `CANCELLED` does not, that `BLOCKED`/`PO_ACCEPTANCE`/`MATT_DECISION`/
   `CANDIDATE` do not, and that one met plus one unmet dependency is not
   ready — proving **all**, not **any**.

## 6. Validator

21 stable finding codes. A fixture under `tests/fixtures/` provokes each
one, and the suite asserts the union of provoked codes **equals** the
declared set — so a silently skipped check fails the tests rather than
passing unnoticed.

```text
MISSING_FIELD              INVALID_FIELD_TYPE          MALFORMED_ID
DUPLICATE_ID               EMPTY_FIELD                 INVALID_LANE
INVALID_STATE              INVALID_PRIORITY            INVALID_RISK
MISSING_TARGET_REPOSITORY  MALFORMED_TARGET_REPOSITORY WILDCARD_DEPENDENCY
MALFORMED_DEPENDENCY_ID    UNKNOWN_DEPENDENCY          DUPLICATE_DEPENDENCY
SELF_DEPENDENCY            DEPENDENCY_CYCLE            MISSING_PID
PID_FILE_NOT_FOUND         MISSING_ARCHITECTURE_REF_FILE
BACKLOG_PID_MISMATCH
```

### Rejecting shorthand requires two layers

No regex can distinguish `DCP-001` (shorthand, invalid) from `DARWIN-R1`
(canonical, valid) — both are letters, a hyphen, then alphanumerics. So:

1. **Syntax** (`ID_PATTERN`) rejects wildcards (`OPS-SAFE-*`), lowercase
   (`tron-t1`), comma lists (`TRON-T2,T3,T4`), whitespace and empty strings.
2. **Membership** rejects shorthand, aliases and unknown ids, because a
   dependency must resolve to a declared item `id`.

Both are implemented and both are tested. Neither alone is sufficient.
`backlog/MASTER-BACKLOG.md` previously carried exactly these invalid
spellings in its `Depends on` column; the canonicalised complete ids now
live in `backlog/backlog.yaml` and the human table is generated from them.

### Cycle detection

Covers self-loops, two-node, three-node, several disjoint cycles in one
document, and a cycle reachable only through a chain from an acyclic node.
Output is canonically rotated (smallest id first) and sorted, so findings
are byte-stable across runs.

### Two deliberate design decisions, recorded for scrutiny

**`MISSING_PID` is state-conditional.** It fires when an item's state is one
where FORGE is already engaged (`ROGUE_DISPATCHED` through `CLOSED`) but
`pid_path` is null. Only `GOAL-DCP-001` currently has a PID, so an
unconditional "every item needs a PID" rule would make canonical data
permanently invalid and make the required first-wave proof impossible.
`DELIVERY_READY` therefore does not require a PID — readiness is exactly the
rule in §4 and nothing more. `PID_FILE_NOT_FOUND` is the separate
dangling-pointer case. The rule is exercised by canonical data, not dormant:
`GOAL-DCP-001` sits in `FORGE_AUDIT`, a PID-required state, and declares its
PID.

The operational consequence is documented for ROGUE in
`operations/ROGUE-READINESS.md`: a ready item whose `pid_path` is null is
not yet FORGE-dispatchable and routes to the PO to commission a canonical
PID. `./tools/goal-ready --with-pid` surfaces this.

**`target_repository` is a declared target and is never checked against
GitHub.** The validator is offline and deterministic; a network call would
make it neither. `maff0000/ARES`, `maff0000/NEO` and `maff0000/mt5-gateway`
do not exist yet — the last is the PID's own documented example. Repository
name casing was verified against GitHub and is deliberate:
`maff0000/hermes`, `maff0000/falcon` and `maff0000/tron` are lowercase;
`maff0000/HELIOS`, `maff0000/DARWIN`, `maff0000/CER` and `maff0000/GOAL` are
uppercase.

## 7. Assumptions requiring PO ratification

These are recorded explicitly rather than presented as established truth.

- **`risk` values.** `backlog/MASTER-BACKLOG.md` has no risk column.
  `GOAL-DCP-001`'s `medium` comes from its own PID. Every other item's risk
  is a PL-assigned provisional value, pending PO ratification. The validator
  enforces the enum, never the choice of value.
- **`po_gate` is `true` for all items**, following
  `architecture/DELIVERY-CONTROL-PLANE.md`, which gives the PO acceptance
  authority across the programme. `matt_gate` is `true` only for
  `PAPER-E2E-001` and `LIVE-GATE-001`, per the master backlog.
- **States.** `GOAL-DCP-001` is `FORGE_AUDIT`. The eleven items the master
  backlog's own "First wave after DCP-001" section clears are
  `DELIVERY_READY`. Every other item is `ARCHITECTURE_REQUIRED`, since no
  PID has been drafted for it. Note `GOAL-DCP-002/003/004` are deliberately
  **not** `DELIVERY_READY` despite satisfied dependencies, because the
  backlog's documented first wave omits them.
- **`target_repository` for ops items.** `OPS-SAFE-001..003`,
  `OPS-CRED-001` and `OPS-LEGACY-001` are estate work with no component
  repository, so their evidence target is `maff0000/GOAL`.

## 8. Bootstrap reconciliation

- `README.md` no longer claims `BOOTSTRAP CANDIDATE`. It records that
  `acc3f48` is the root commit of `main` and pushed, and replaces a pack
  date that had already gone stale with a commit-anchored statement.
- `operations/HELM-BOOTSTRAP-INSTRUCTIONS.md` and
  `operations/HELM-NEXT-ACTIONS.md` are marked historical and superseded,
  with their content left intact as the record of what was instructed.
- Both instruction files specified a `GOAL-000` commit message that differs
  from the one actually on `main`
  (`GOAL-000: establish public delivery control plane authority`). History
  was **not** rewritten; the divergence is recorded in the historical
  markers instead.
- An internal host identifier was removed from the bootstrap target line,
  since this repository is public.
- `MANIFEST.md` now reflects actual tracked files, generated from
  `git ls-files`, so it cannot silently go stale.

### Known residue, deliberately not rewritten

The internal host identifier removed above **remains in the root commit**
`acc3f48`. Rewriting the root commit was explicitly out of scope for this
increment, and `maff0000/GOAL#1` already cites `acc3f48` by SHA — rewriting
it would break that citation. It is a low-sensitivity internal hostname
already public since the bootstrap push. Recorded here for the PO to decide
on, rather than silently rewritten or silently ignored.

## 9. Non-goals honoured

No Redis, database, daemon, message broker, scheduler, workflow DSL, custom
web UI, autonomous delivery agent, auto-merge, or component trading code.
No component repository was modified. No packaging file, build step, or
dependency beyond PyYAML and pytest was introduced — `conftest.py` puts
`tools/` on `sys.path`, which is why no packaging is needed.

The CI workflow only validates. It has `permissions: contents: read`, no
`workflow_dispatch`, no schedule, no issue or PR mutation, no secrets, and
no third-party marketplace action beyond `actions/checkout` and
`actions/setup-python`. A test parses the workflow and asserts this.

## 10. Delivery method

Five bounded Engineer dispatches across two parallel waves, plus one
end-to-end dispatch and one repair dispatch. Each Engineer worked in its own
isolated worktree cut from this repository, verified before dispatch by
resolving `acc3f48` inside it. **No Engineer committed**; the PL reviewed
every diff and made every commit. Isolation was re-verified after each
dispatch, including that the shared project working tree stayed clean.

| dispatch | scope |
|---|---|
| E1 | `backlog.yaml`, `model.py`, `SCHEMA.md`, `conftest.py`, model tests |
| E2 | `tools/secret-scan` and its positive control |
| E3 | validator, cycle detection, 21-code fixture set |
| E4 | readiness, docsync, `goal-ready`/`goal-docs`, generated regions |
| E5 | bootstrap reconciliation, `ROGUE-READINESS.md`, `.gitignore`, CI |
| E6 | end-to-end CLI tests; PID-documented output bytes |
| E7 | repair: assert the committed executable bit, not the checkout umask |

### Defects caught before audit

- **A vacuous positive control was avoided.** The PL's dispatch suggested
  the AWS example key for the secret-scan positive control. That key is
  allowlisted in gitleaks' default configuration and does not fire —
  confirmed directly. The Engineer overrode the instruction and used a
  pattern that fires reliably, so the control is real.
- **Python bytecode leaked a planted credential into the scan.** CPython
  constant-folds adjacent string literals, so a fake token built with `+`
  was stored contiguously in `__pycache__/*.pyc` and detected by the
  repository's own working-tree scan. Fixed with runtime `"".join(...)`, not
  with an allowlist or ignore file, which would have blinded the scan to
  real secrets.
- **A fixture could have passed vacuously via path escape.** A fixture's
  repository root is its own parent directory, so an unguarded
  `../pids/GOAL-DCP-001.md` resolved to the *real* PID and would have passed
  regardless of the fixture. `pid_path` and `architecture_refs` are now
  refused if absolute or containing `..`, and a test covers it.
- **A test asserted the checkout umask rather than repository content.** An
  on-disk `0o755` assertion passed only in a working tree where modes had
  been set by hand and failed in any ordinary checkout under umask `0002`,
  where git materialises a committed `100755` as `0775`. It now asserts the
  index mode plus `os.access`. Caught by running the suite in a fresh
  checkout rather than trusting the integration tree's green result.

## 11. Independent audit

A fresh-context FORGE Auditor was dispatched against the delivered head
with no inherited Engineer context. Its structured verdict block is recorded
alongside this file in `AUDIT-VERDICT.md`.

Presentation target: this increment has **no user-facing browser surface**.
It delivers repository data, command-line tools, tests and documentation, so
the Auditor's real-browser verification gate does not apply. The acceptance
evidence is mechanical command output instead.

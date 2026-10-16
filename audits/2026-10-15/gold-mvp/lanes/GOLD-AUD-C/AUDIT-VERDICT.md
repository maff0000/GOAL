# GOLD-AUD-C independent audit verdict

**Status: pending independent audit by ROGUE.** This lane does not self-certify. Items 9 and 10 of CA's evidence list, and acceptance A-9, are left open for the independent auditor and for PO acceptance.

Verification output for the head commit is appended below by the lane PL (commands and results only; not a verdict).

## Verification run by the lane PL (results only)

Environment: Python 3.11, `pytest`, `pyyaml`, `jsonschema` and `cryptography` installed.

| Command | Result |
|---|---|
| `python3 -m pytest tests -q` | 582 passed, 6 failed at the committed head: all six are the MANIFEST.md generated-region drift (five in tests/test_cli.py, one in tests/test_docsync.py), which ROGUE clears by regenerating MANIFEST.md at integration; before the commit, with the new files untracked, all 588 passed (357 pre-existing, 231 added) |
| `python3 -m pytest tests/test_cp1_conformance.py tests/test_cp2_conformance.py tests/test_cp_packages_common.py -q` | 231 passed |
| same, with `jsonschema` and `cryptography` made unimportable (CI-like) | 140 passed, 91 skipped (the checker A tests, reported not hidden) |
| `./tools/goal-validate` | `backlog OK: 49 items` |
| `./tools/goal-docs --check` | in sync when run before the commit with the new files untracked; at the committed head `goal-docs --check` reports drift on `MANIFEST.md` until ROGUE regenerates it at integration (not run with `--write` here) |
| `./tools/secret-scan` | working tree CLEAN, git history CLEAN |
| `CLONE_ROOT=<clones> GOAL_LOCAL_CHECKOUT=<checkout holding 64c843b> ./verify-sources.sh` | `verified=87 mismatched=0 skipped=0` (without `GOAL_LOCAL_CHECKOUT`: 84 verified, 3 skipped as UNPUBLISHED) |
| `CLONE_ROOT=<clones> ./negative-searches.sh` | N1 to N10 each empty |

Acceptance map (mechanical): A-1 and A-3 to A-8 are covered by the tests above; A-2 holds for fixtures (verdicts, codes and emitted frames identical in the two checkers) with the independence limit stated in `RECONCILIATION.md` section 10; A-9 is the independent audit, pending.

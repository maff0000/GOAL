# GOLD-AUD-C independent audit verdict

**Status: pending independent audit by ROGUE.** This lane does not self-certify. Items 9 and 10 of CA's evidence list, and acceptance A-9, are left open for the independent auditor and for PO acceptance.

This is the clean replacement of the earlier lane C change: CP-2 is reference-only and CP-1 plus the non-conflicting evidence are preserved. Results below are for this change only and were run on the delivery host after all edits and after MANIFEST regeneration.

## Verification run by the lane PL (results only)

Environment: Python 3.11, `pytest`, `pyyaml`, `jsonschema` installed.

| Command | Result |
|---|---|
| `./tools/goal-docs --write` then `./tools/goal-docs --check` | generated regions in sync; MANIFEST.md modified and committed |
| `./tools/goal-validate` | `backlog OK: 50 items` |
| `./tools/secret-scan` | CLEAN |
| `python3 -m pytest tests -q` | 493 passed |
| `python3 -m pytest tests/test_cp1_conformance.py tests/test_cp_packages_common.py -q` | 136 passed |
| same, with `jsonschema` and `cryptography` made unimportable (CI-like) | 80 passed, 56 skipped (the checker A tests, reported not hidden) |
| `CLONE_ROOT=<clones> ./verify-sources.sh` | `verified=84 mismatched=0 skipped=3` on the delivery host (the three skipped rows are the unpublished candidate texts). An earlier independent run on another host reported one mismatch, the mt5-gateway README object at `6263d61f`, which is not present on that host; it is not claimed verified there |
| `CLONE_ROOT=<clones> ./negative-searches.sh` | N1 to N10 each empty |

Acceptance map (mechanical): A-1 and A-3 to A-8 are covered by the tests above for CP-1; CP-2 acceptance items are not claimed (reference-only). A-9 is the independent audit, pending.

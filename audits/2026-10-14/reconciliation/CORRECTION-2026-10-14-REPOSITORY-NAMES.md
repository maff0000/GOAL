# Correction record 2026-10-14 — repository names in the GOAL-DCP-001 delivery evidence

**Status:** forward-only correction. The historical file is not edited.
**Date:** 2026-10-14. **Baseline:** `main` at `1739e74`.
**Corrects:** `audits/2026-10-12/goal-dcp-001/DELIVERY-EVIDENCE.md`, section 6 ("Validator"), the paragraph on `target_repository` (line 249 at the baseline).
**Evidence:** reconciliation analyst reports RECON-G (branch `wo/GOAL-RECON-G-neo`, `9bd67f3`), RECON-H1 (`wo/GOAL-RECON-H1-datachain`, `142cc55`) and RECON-H2 (`wo/GOAL-RECON-H2-tradechain`, `2780076`). Each was produced by reading GitHub and the component checkouts on 2026-10-14.

## What the historical record says

Section 6 of the delivery evidence states that `maff0000/ARES`, `maff0000/NEO` and `maff0000/mt5-gateway` "do not exist yet", and that repository name casing "was verified against GitHub and is deliberate".

## Corrections

| statement in the historical record | finding on 2026-10-14 | correct fact |
|---|---|---|
| `maff0000/NEO` does not exist | **False.** | The repository exists as `maff0000/neo` (private, lowercase). GitHub resolves the name case-insensitively, so `maff0000/NEO` returns `maff0000/neo`. It holds a mature, cron-driven NEO runtime, not a greenfield target. |
| `maff0000/mt5-gateway` does not exist | **False.** | The repository exists (private) and holds the gateway platform and a stack of open work-order pull requests. |
| `maff0000/ARES` does not exist | **True as spelled, misleading.** | `maff0000/ARES` does not resolve. The ARES repository is `maff0000/trading-ares` (private). |
| Casing "was verified ... and is deliberate" | **Incorrect for NEO.** | The real name is lowercase `neo`. The listed lowercase names `hermes`, `falcon`, `tron` and the uppercase `HELIOS`, `DARWIN`, `CER`, `GOAL` were not contradicted by the analysts. |

## Effect on the backlog

`backlog/backlog.yaml` now declares `maff0000/trading-ares` for `ARES-CUR-001`, `ARES-RISK-001` and `ARES-PIT-001`, and `maff0000/neo` for `NEO-R1`. `maff0000/mt5-gateway` was already the declared target and needed no change.

## What this does not change

`target_repository` remains a declared target that the validator never checks against GitHub; validation stays offline and deterministic. The historical delivery evidence and its audit verdicts remain as written. This record supersedes only the factual statements tabulated above.

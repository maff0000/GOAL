# GOAL MT5 Connector Audit — Sanitised Public Summary

## Audit

- Date: 2026-10-11
- Auditor: HELM
- Mode: read-only
- Private evidence ID: `GOAL-EVIDENCE-MT5-2026-10-11`

## Verdict

`REUSE_CONTAINER_REPLACE_BRIDGE`

## Proven findings

1. A current Docker/Wine/MetaTrader 5 Vantage DEMO platform exists and is operational.
2. The reusable MT5 gateway/container foundation is real.
3. The current new-generation gateway has proven terminal startup, DEMO connectivity and basic runtime operation, but does not yet constitute a complete broker execution adapter.
4. Earlier GOAL execution generations contain real evidence that the underlying MetaTrader Python surface can place and modify orders.
5. The current unrestricted generic bridge is not suitable as TRON's broker-control boundary.
6. The container platform itself should be retained.
7. TRON requires a new broker-neutral adapter and a narrow typed MT5 service.
8. Pending-order, cancel, partial-close, reconciliation, idempotency and complete restart-recovery behaviour still require DEMO proof.
9. The mt5-gateway development history requires canonical Git reconciliation and CI/provenance hardening.
10. A legacy executor was discovered in a configuration that must be treated as potentially live until separately audited.
11. Plaintext credential findings were identified in legacy operational locations and require separate security remediation.
12. Vantage remains the intended first execution venue, DEMO-first.

## Architecture decision

```text
TRON
  ↓
broker-neutral Vantage MT5 adapter
  ↓
narrow typed MT5 service
  ↓
existing Docker / Wine / MetaTrader 5 platform
  ↓
Vantage DEMO
```

## Raw evidence

Raw forensic evidence is intentionally retained outside the public repository in the private GOAL evidence store, under the opaque evidence ID `GOAL-EVIDENCE-MT5-2026-10-11`.

Integrity references are in `EVIDENCE-HASHES.txt` (SHA-256 of the consolidated raw audit and of each worker report).

## Security note

The public copy is intentionally sanitised to avoid exposing private infrastructure topology and account-adjacent operational detail.

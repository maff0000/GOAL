# THE GOAL — Initial Master Backlog

This document is the **human view** of the programme backlog.
`backlog/backlog.yaml` is the machine authority, and the two are not
independent truths: everything between the generated-region markers below is
rendered from the YAML by `./tools/goal-docs`. Never hand-edit a generated
region — change `backlog/backlog.yaml` and run `./tools/goal-docs --write`.
`./tools/goal-docs --check` fails when the two disagree. See
`backlog/SCHEMA.md` for the field reference.

<!-- BEGIN GENERATED: backlog-table -->

| ID | Lane | Component | Outcome | Target repository | Depends on | Priority | Risk | State | PO gate | Matt gate |
|---|---|---|---|---|---|---|---|---|---|---|
| GOAL-DCP-001 | shared | GOAL | GitHub delivery-control foundation | maff0000/GOAL | — | P0 | medium | FORGE_AUDIT | Yes | No |
| GOAL-DCP-002 | shared | GOAL/ROGUE | Machine-readable backlog + dependency/readiness validator | maff0000/GOAL | GOAL-DCP-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-DCP-003 | shared | ROGUE/FORGE | Multi-project dispatch proof | maff0000/GOAL | GOAL-DCP-002 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-DCP-004 | shared | GOAL | Automated PO/Rogue status and stale/blocked brief | maff0000/GOAL | GOAL-DCP-002 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| OPS-SAFE-001 | ops | Estate | Backup/off-host/restore programme | maff0000/GOAL | GOAL-DCP-001 | P0 | high | DELIVERY_READY | Yes | No |
| OPS-SAFE-002 | ops | Estate | Network/data-store containment | maff0000/GOAL | GOAL-DCP-001 | P0 | high | DELIVERY_READY | Yes | No |
| OPS-SAFE-003 | ops | Estate | Secrets/runtime identity hygiene | maff0000/GOAL | GOAL-DCP-001 | P0 | high | DELIVERY_READY | Yes | No |
| OPS-LEGACY-001 | ops | Legacy MT5 | Prove/quarantine `agent-smith-original` and dell `MT5_Vantage` safely | maff0000/GOAL | GOAL-DCP-001 | P0 | high | DELIVERY_READY | Yes | No |
| OPS-CRED-001 | ops | Estate | Remove plaintext broker/DB credentials and rotate where appropriate | maff0000/GOAL | GOAL-DCP-001 | P0 | high | DELIVERY_READY | Yes | No |
| HERMES-CUR-001 | shared | HERMES | Authoritative PROD/current-state reconciliation | maff0000/hermes | GOAL-DCP-001 | P0 | medium | DELIVERY_READY | Yes | No |
| HERMES-FACT-001 | shared | HERMES | `goal.market-fact/v1` | maff0000/hermes | HERMES-CUR-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| HERMES-GR-001 | research | HERMES | Golden replay proof | maff0000/hermes | HERMES-FACT-001 | P0 | low | ARCHITECTURE_REQUIRED | Yes | No |
| ARES-CUR-001 | shared | ARES | Canonical generation + legacy reconciliation | maff0000/ARES | GOAL-DCP-001 | P0 | medium | DELIVERY_READY | Yes | No |
| ARES-RISK-001 | shared | ARES | `goal.risk-event/v1` | maff0000/ARES | ARES-CUR-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| ARES-PIT-001 | research | ARES | Trading Economics PIT prototype | maff0000/ARES | ARES-RISK-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-CONTRACT-001 | shared | GOAL | `goal.strategy/v1` | maff0000/GOAL | GOAL-DCP-001 | P0 | medium | DELIVERY_READY | Yes | No |
| GOAL-CORE-001 | shared | GOAL | `goal-strategy-core` | maff0000/GOAL | GOAL-CONTRACT-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-REF-001 | shared | GOAL | independent semantic reference | maff0000/GOAL | GOAL-CORE-001 | P0 | low | ARCHITECTURE_REQUIRED | Yes | No |
| DARWIN-R1 | research | DARWIN | Source/runtime reconciliation | maff0000/DARWIN | GOAL-DCP-001 | P0 | medium | DELIVERY_READY | Yes | No |
| DARWIN-R2 | research | DARWIN | ResearchEngineAdapter | maff0000/DARWIN | GOAL-CONTRACT-001, DARWIN-R1 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| DARWIN-R3 | research | DARWIN | APOLLO narrowed causal proof | maff0000/DARWIN | GOAL-CORE-001, DARWIN-R1 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| LEAN-P1 | research | DARWIN | LEAN bounded prototype | maff0000/DARWIN | DARWIN-R2, GOAL-CORE-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| CER-R1 | research | CER | Research evidence + EdgeProfileVersion | maff0000/CER | DARWIN-R2 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| NEO-R1 | research | NEO | Read-only evidence/MCP architecture | maff0000/NEO | CER-R1 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| HELIOS-T1 | trading | HELIOS | Refactor to GOAL strategy contract/core | maff0000/HELIOS | GOAL-CORE-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| HELIOS-T2 | trading | HELIOS | Live HERMES/ARES adapters | maff0000/HELIOS | HELIOS-T1, HERMES-FACT-001, ARES-RISK-001 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| HELIOS-T3 | trading | HELIOS | Signed durable StrategyTrigger | maff0000/HELIOS | HELIOS-T2 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| FALCON-T1 | trading | FALCON | Reconcile event registry | maff0000/falcon | HELIOS-T3 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| MT5-GW-001 | trading | mt5-gateway | Reconcile eight stacked WO branches into canonical Git history | maff0000/mt5-gateway | GOAL-DCP-001 | P0 | medium | DELIVERY_READY | Yes | No |
| MT5-GW-002 | trading | mt5-gateway | Reproducible image/build provenance, version pinning, environment guard, health and CI | maff0000/mt5-gateway | MT5-GW-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| MT5-GW-003 | trading | mt5-gateway | Replace raw SlaveService with typed in-container allow-list service; UDS preferred | maff0000/mt5-gateway | MT5-GW-001, MT5-GW-002 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| MT5-GW-004 | trading | mt5-gateway | Vantage DEMO execution/reconciliation capability proof | maff0000/mt5-gateway | MT5-GW-003 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T1 | trading | TRON | Core ledger/reconciliation + Trading Postgres | maff0000/tron | GOAL-DCP-001 | P0 | high | DELIVERY_READY | Yes | No |
| TRON-T2 | trading | TRON | Vantage DEMO broker-neutral adapter | maff0000/tron | TRON-T1, MT5-GW-003, MT5-GW-004 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T3 | trading | TRON | DIKE/hard risk/kill | maff0000/tron | TRON-T1 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T4 | trading | TRON | TriggerInbox intake/idempotency | maff0000/tron | TRON-T1, HELIOS-T3 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T5 | trading | TRON | SizingPolicy + frozen EdgeProfile binding | maff0000/tron | TRON-T3, CER-R1 | P1 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| SKEPTIC-T1 | trading | TRON | asynchronous SHADOW reviewer | maff0000/tron | TRON-T1 | P2 | low | ARCHITECTURE_REQUIRED | Yes | No |
| PAPER-E2E-001 | trading | GOAL | Full paper lane end-to-end proof | maff0000/GOAL | HELIOS-T3, TRON-T2, TRON-T3, TRON-T4 | P0 | capital | ARCHITECTURE_REQUIRED | Yes | **Yes** |
| LIVE-GATE-001 | ops | GOAL | Capital readiness + LIVE decision | maff0000/GOAL | PAPER-E2E-001, OPS-SAFE-001, OPS-SAFE-002, OPS-SAFE-003, OPS-LEGACY-001, OPS-CRED-001 | P0 | capital | ARCHITECTURE_REQUIRED | Yes | **Yes** |

<!-- END GENERATED: backlog-table -->

## First wave after GOAL-DCP-001

These can proceed independently once the control plane is GREEN.

The list is **computed, not maintained by hand**: it is the readiness answer
for the projection "`GOAL-DCP-001` has reached an accepted terminal state" —
every item whose own state is `DELIVERY_READY` and whose every dependency is
then satisfied. Ids are canonical and complete, which is what makes the list
mechanically checkable; range notation such as `OPS-SAFE-001..003` is not a
canonical id and cannot be verified against the backlog.

Reproduce it with:

```bash
./tools/goal-ready --assume-closed GOAL-DCP-001
```

<!-- BEGIN GENERATED: first-wave -->

- `ARES-CUR-001` — Canonical generation + legacy reconciliation (`maff0000/ARES`)
- `DARWIN-R1` — Source/runtime reconciliation (`maff0000/DARWIN`)
- `GOAL-CONTRACT-001` — `goal.strategy/v1` (`maff0000/GOAL`)
- `HERMES-CUR-001` — Authoritative PROD/current-state reconciliation (`maff0000/hermes`)
- `MT5-GW-001` — Reconcile eight stacked WO branches into canonical Git history (`maff0000/mt5-gateway`)
- `OPS-CRED-001` — Remove plaintext broker/DB credentials and rotate where appropriate (`maff0000/GOAL`)
- `OPS-LEGACY-001` — Prove/quarantine `agent-smith-original` and dell `MT5_Vantage` safely (`maff0000/GOAL`)
- `OPS-SAFE-001` — Backup/off-host/restore programme (`maff0000/GOAL`)
- `OPS-SAFE-002` — Network/data-store containment (`maff0000/GOAL`)
- `OPS-SAFE-003` — Secrets/runtime identity hygiene (`maff0000/GOAL`)
- `TRON-T1` — Core ledger/reconciliation + Trading Postgres (`maff0000/tron`)

<!-- END GENERATED: first-wave -->

# THE GOAL — Initial Master Backlog

| ID | Lane | Component | Outcome | Depends on | Priority | Matt gate |
|---|---|---|---|---|---|---|
| GOAL-DCP-001 | Shared | GOAL | GitHub delivery-control foundation | — | P0 | No |
| GOAL-DCP-002 | Shared | GOAL/ROGUE | Machine-readable backlog + dependency/readiness validator | DCP-001 | P0 | No |
| GOAL-DCP-003 | Shared | ROGUE/FORGE | Multi-project dispatch proof | DCP-002 | P0 | No |
| GOAL-DCP-004 | Shared | GOAL | Automated PO/Rogue status and stale/blocked brief | DCP-002 | P1 | No |
| OPS-SAFE-001 | Ops | Estate | Backup/off-host/restore programme | DCP-001 | P0 | No |
| OPS-SAFE-002 | Ops | Estate | Network/data-store containment | DCP-001 | P0 | No |
| OPS-SAFE-003 | Ops | Estate | Secrets/runtime identity hygiene | DCP-001 | P0 | No |
| OPS-LEGACY-001 | Ops | Legacy MT5 | Prove/quarantine `agent-smith-original` and dell `MT5_Vantage` safely | DCP-001 | P0 | No |
| OPS-CRED-001 | Ops | Estate | Remove plaintext broker/DB credentials and rotate where appropriate | DCP-001 | P0 | No |
| HERMES-CUR-001 | Shared | HERMES | Authoritative PROD/current-state reconciliation | DCP-001 | P0 | No |
| HERMES-FACT-001 | Shared | HERMES | `goal.market-fact/v1` | HERMES-CUR-001 | P0 | No |
| HERMES-GR-001 | Research | HERMES | Golden replay proof | HERMES-FACT-001 | P0 | No |
| ARES-CUR-001 | Shared | ARES | Canonical generation + legacy reconciliation | DCP-001 | P0 | No |
| ARES-RISK-001 | Shared | ARES | `goal.risk-event/v1` | ARES-CUR-001 | P0 | No |
| ARES-PIT-001 | Research | ARES | Trading Economics PIT prototype | ARES-RISK-001 | P1 | No |
| GOAL-CONTRACT-001 | Shared | GOAL | `goal.strategy/v1` | DCP-001 | P0 | No |
| GOAL-CORE-001 | Shared | GOAL | `goal-strategy-core` | CONTRACT-001 | P0 | No |
| GOAL-REF-001 | Shared | GOAL | independent semantic reference | CORE-001 | P0 | No |
| DARWIN-R1 | Research | DARWIN | Source/runtime reconciliation | DCP-001 | P0 | No |
| DARWIN-R2 | Research | DARWIN | ResearchEngineAdapter | CONTRACT-001, DARWIN-R1 | P0 | No |
| DARWIN-R3 | Research | DARWIN | APOLLO narrowed causal proof | CORE-001, DARWIN-R1 | P1 | No |
| LEAN-P1 | Research | DARWIN | LEAN bounded prototype | DARWIN-R2, CORE-001 | P1 | No |
| CER-R1 | Research | CER | Research evidence + EdgeProfileVersion | DARWIN-R2 | P1 | No |
| NEO-R1 | Research | NEO | Read-only evidence/MCP architecture | CER-R1 | P1 | No |
| HELIOS-T1 | Trading | HELIOS | Refactor to GOAL strategy contract/core | CORE-001 | P0 | No |
| HELIOS-T2 | Trading | HELIOS | Live HERMES/ARES adapters | HELIOS-T1, HERMES-FACT-001, ARES-RISK-001 | P0 | No |
| HELIOS-T3 | Trading | HELIOS | Signed durable StrategyTrigger | HELIOS-T2 | P0 | No |
| FALCON-T1 | Trading | FALCON | Reconcile event registry | HELIOS-T3 | P1 | No |
| MT5-GW-001 | Trading | mt5-gateway | Reconcile eight stacked WO branches into canonical Git history | DCP-001 | P0 | No |
| MT5-GW-002 | Trading | mt5-gateway | Reproducible image/build provenance, version pinning, environment guard, health and CI | MT5-GW-001 | P0 | No |
| MT5-GW-003 | Trading | mt5-gateway | Replace raw SlaveService with typed in-container allow-list service; UDS preferred | MT5-GW-001, MT5-GW-002 | P0 | No |
| MT5-GW-004 | Trading | mt5-gateway | Vantage DEMO execution/reconciliation capability proof | MT5-GW-003 | P0 | No |
| TRON-T1 | Trading | TRON | Core ledger/reconciliation + Trading Postgres | DCP-001 | P0 | No |
| TRON-T2 | Trading | TRON | Vantage DEMO broker-neutral adapter | TRON-T1, MT5-GW-003, MT5-GW-004 | P0 | No |
| TRON-T3 | Trading | TRON | DIKE/hard risk/kill | TRON-T1 | P0 | No |
| TRON-T4 | Trading | TRON | TriggerInbox intake/idempotency | TRON-T1, HELIOS-T3 | P0 | No |
| TRON-T5 | Trading | TRON | SizingPolicy + frozen EdgeProfile binding | TRON-T3, CER-R1 | P1 | No |
| SKEPTIC-T1 | Trading | TRON | asynchronous SHADOW reviewer | TRON-T1 | P2 | No |
| PAPER-E2E-001 | Trading | GOAL | Full paper lane end-to-end proof | HELIOS-T3, TRON-T2,T3,T4 | P0 | **Yes** |
| LIVE-GATE-001 | Ops | GOAL | Capital readiness + LIVE decision | PAPER-E2E-001, OPS-SAFE-* | P0 | **Yes** |

## First wave after DCP-001

These can proceed independently after the control plane is GREEN:

- OPS-SAFE-001..003
- OPS-LEGACY-001
- OPS-CRED-001
- HERMES-CUR-001
- ARES-CUR-001
- GOAL-CONTRACT-001
- DARWIN-R1
- MT5-GW-001
- TRON-T1

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
| GOAL-DCP-001 | shared | GOAL | GitHub control-plane authority: machine backlog, validation, dependency graph, strict delivery readiness, generated views, CI enforcement | maff0000/GOAL | — | P0 | medium | CLOSED | Yes | No |
| GOAL-DCP-002 | shared | GOAL/ROGUE | ROGUE dispatcher — deterministic consumption and multi-project dispatch control | maff0000/GOAL | GOAL-DCP-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-DCP-003 | shared | ROGUE/FORGE | Automated GitHub-triggered sandboxed delivery launch | maff0000/GOAL | GOAL-DCP-002 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-DCP-004 | shared | GOAL | Automated PO/ROGUE status and stale/blocked brief | maff0000/GOAL | GOAL-DCP-002 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| OPS-SAFE-001 | ops | Estate | Backup/off-host/restore programme | maff0000/GOAL | GOAL-DCP-001 | P0 | high | PID_DRAFT | Yes | No |
| OPS-SAFE-002 | ops | Estate | Network/data-store containment | maff0000/GOAL | GOAL-DCP-001 | P0 | high | PID_DRAFT | Yes | No |
| OPS-SAFE-003 | ops | Estate | Secrets/runtime identity hygiene | maff0000/GOAL | GOAL-DCP-001 | P0 | high | PID_DRAFT | Yes | No |
| OPS-LEGACY-001 | ops | Legacy MT5 | Prove/quarantine `agent-smith-original` and dell `MT5_Vantage` safely | maff0000/GOAL | GOAL-DCP-001 | P0 | high | PID_DRAFT | Yes | No |
| OPS-CRED-001 | ops | Estate | Remove plaintext broker/DB credentials and rotate where appropriate | maff0000/GOAL | GOAL-DCP-001 | P0 | high | PID_DRAFT | Yes | No |
| HERMES-CUR-001 | shared | HERMES | Authoritative PROD/current-state reconciliation | maff0000/hermes | GOAL-DCP-001 | P0 | medium | PID_DRAFT | Yes | No |
| HERMES-FACT-001 | shared | HERMES | `goal.market-fact/v1` | maff0000/hermes | HERMES-CUR-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| HERMES-GR-001 | research | HERMES | Golden replay proof | maff0000/hermes | HERMES-FACT-001 | P0 | low | ARCHITECTURE_REQUIRED | Yes | No |
| ARES-CUR-001 | shared | ARES | Canonical generation + legacy reconciliation | maff0000/trading-ares | GOAL-DCP-001 | P0 | medium | PID_DRAFT | Yes | No |
| ARES-RISK-001 | shared | ARES | `goal.risk-event/v1` | maff0000/trading-ares | ARES-CUR-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| ARES-PIT-001 | research | ARES | Trading Economics PIT prototype | maff0000/trading-ares | ARES-RISK-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-CONTRACT-001 | shared | GOAL | `goal.strategy/v1` | maff0000/GOAL | GOAL-DCP-001 | P0 | medium | PID_DRAFT | Yes | No |
| GOAL-CORE-001 | shared | GOAL | `goal-strategy-core` | maff0000/GOAL | GOAL-CONTRACT-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-REF-001 | shared | GOAL | independent semantic reference | maff0000/GOAL | GOAL-CONTRACT-001 | P0 | low | ARCHITECTURE_REQUIRED | Yes | No |
| DARWIN-R1 | research | DARWIN | Source/runtime reconciliation | maff0000/DARWIN | GOAL-DCP-001 | P0 | medium | PID_DRAFT | Yes | No |
| DARWIN-R2 | research | DARWIN | ResearchEngineAdapter | maff0000/DARWIN | GOAL-CONTRACT-001, DARWIN-R1 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| DARWIN-R3 | research | DARWIN | APOLLO narrowed causal proof | maff0000/DARWIN | GOAL-CORE-001, DARWIN-R1 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| LEAN-P1 | research | DARWIN | LEAN bounded prototype | maff0000/DARWIN | DARWIN-R2, GOAL-CORE-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| HSA-C1 | research | HSA | HSA adopts goal.strategy/v1 and the goal.market-fact/v1 fact catalogue | maff0000/HSA | GOAL-CONTRACT-001, HERMES-FACT-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| CER-R1 | research | CER | EdgeProfileVersion and contract v1.1 on delivered CER v1.0.0 | maff0000/CER | GOAL-DCP-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| NEO-R1 | research | NEO | Read-only evidence/MCP architecture | maff0000/neo | GOAL-DCP-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| GOAL-TRIGGER-001 | shared | GOAL | Cross-system trigger contract: trigger envelope, signed canonical form, validity, dedupe key, terminal outcomes and TriggerInbox delivery semantics | maff0000/GOAL | GOAL-DCP-001, GOAL-CONTRACT-001 | P0 | high | ARCHITECTURE_REQUIRED | Yes | **Yes** |
| HELIOS-T1 | trading | HELIOS | Refactor to GOAL strategy contract/core | maff0000/HELIOS | GOAL-CORE-001 | P0 | medium | PID_DRAFT | Yes | No |
| HELIOS-T2 | trading | HELIOS | Live HERMES adapter | maff0000/HELIOS | HELIOS-T1, HERMES-FACT-001 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| HELIOS-T3 | trading | HELIOS | Signed durable StrategyTrigger | maff0000/HELIOS | HELIOS-T2, GOAL-TRIGGER-001 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| FALCON-T1 | trading | FALCON | Reconcile FALCON event registry with delivered HERMES/ARES/HELIOS reality (excludes strategy_trigger and tron.* families) | maff0000/falcon | GOAL-DCP-001 | P1 | low | ARCHITECTURE_REQUIRED | Yes | No |
| MT5-GW-001 | trading | mt5-gateway | Reconcile eight stacked WO branches into canonical Git history | maff0000/mt5-gateway | GOAL-DCP-001 | P0 | medium | PID_DRAFT | Yes | No |
| MT5-GW-002 | trading | mt5-gateway | Reproducible image/build provenance, version pinning, environment guard, health and CI | maff0000/mt5-gateway | MT5-GW-001 | P0 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| MT5-GW-003 | trading | mt5-gateway | Replace raw SlaveService with typed in-container allow-list service; UDS preferred | maff0000/mt5-gateway | MT5-GW-001, MT5-GW-002 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| MT5-GW-004 | trading | mt5-gateway | Vantage DEMO execution/reconciliation capability proof | maff0000/mt5-gateway | MT5-GW-003 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-D1-RATIFY | trading | TRON | Ratify TRON D1 design baseline: independent audit, merge to the default branch, and disposition of open decisions | maff0000/tron | GOAL-DCP-001 | P0 | medium | PID_DRAFT | Yes | **Yes** |
| TRON-T1 | trading | TRON | Core execution journal/reconciliation + Trading Postgres | maff0000/tron | GOAL-DCP-001, TRON-D1-RATIFY | P0 | high | PID_DRAFT | Yes | No |
| TRON-T2 | trading | TRON | Vantage DEMO broker-neutral adapter | maff0000/tron | TRON-T1, MT5-GW-004 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T3A | trading | TRON | Minimum fixed DEMO sizing, limits, one kill state | maff0000/tron | TRON-T1 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T3 | trading | TRON | DIKE/hard risk/kill | maff0000/tron | TRON-T1, TRON-T3A | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T4 | trading | TRON | TriggerInbox intake/idempotency | maff0000/tron | TRON-T1, GOAL-TRIGGER-001 | P0 | high | ARCHITECTURE_REQUIRED | Yes | No |
| TRON-T5 | trading | TRON | SizingPolicy + frozen EdgeProfile binding | maff0000/tron | TRON-T3, CER-R1 | P1 | medium | ARCHITECTURE_REQUIRED | Yes | No |
| SKEPTIC-T1 | trading | TRON | asynchronous SHADOW reviewer | maff0000/tron | TRON-T1 | P2 | low | ARCHITECTURE_REQUIRED | Yes | No |
| PAPER-E2E-001 | trading | GOAL | Full paper lane end-to-end proof on Vantage DEMO (not satisfiable by simulation) | maff0000/GOAL | HELIOS-T3, TRON-T2, TRON-T3, TRON-T4, GOLD-MVP-001 | P0 | capital | ARCHITECTURE_REQUIRED | Yes | **Yes** |
| LIVE-GATE-001 | ops | GOAL | Capital readiness + LIVE decision | maff0000/GOAL | PAPER-E2E-001, OPS-SAFE-001, OPS-SAFE-002, OPS-SAFE-003, OPS-LEGACY-001, OPS-CRED-001 | P0 | capital | ARCHITECTURE_REQUIRED | Yes | **Yes** |
| GOLD-AUD-A | research | HERMES | GOLD MVP audit A: HERMES PROD XAUUSD Redis publication (read-only; strict subset of HERMES-CUR-001 scope item 1) | maff0000/hermes | GOAL-DCP-001 | P0 | medium | ROGUE_DISPATCHED | Yes | **Yes** |
| GOLD-AUD-B | research | HELIOS | GOLD MVP audit B: locate and reconcile the HERMES Redis to HELIOS GOLD integration and review HSA packages (read-only) | maff0000/HELIOS | GOAL-DCP-001 | P0 | low | PO_ACCEPTANCE | Yes | No |
| GOLD-AUD-C | research | GOAL | GOLD MVP audit C: shared contract reconciliation, compatibility matrix and evidence index (read-only; complements GOAL-CONTRACT-001 and GOAL-TRIGGER-001) | maff0000/GOAL | GOAL-DCP-001 | P0 | medium | PO_ACCEPTANCE | Yes | No |
| GOLD-AUD-D | research | TRON/MT5 | GOLD MVP audit D: TRON design, risk rules, journal, trigger intake and the smallest MT5 DEMO execution path (read-only) | maff0000/GOAL | GOAL-DCP-001 | P0 | medium | PO_ACCEPTANCE | Yes | No |
| GOLD-AUD-E | research | FALCON | GOLD MVP audit E: FALCON registry and ingestion, minimum HELIOS and TRON event publication (read-only; complements FALCON-T1) | maff0000/falcon | GOAL-DCP-001 | P0 | low | PO_ACCEPTANCE | Yes | No |
| GOLD-AUD-F | research | CER/HSA/DARWIN/NEO | GOLD MVP audit F: strategy qualification, registration, execution and NEO review across CER, HSA, DARWIN and NEO (read-only) | maff0000/GOAL | GOAL-DCP-001 | P1 | low | PO_ACCEPTANCE | Yes | No |
| GOLD-MVP-001 | trading | GOAL | GOLD MVP integration and acceptance: one governed XAUUSD strategy end to end on Vantage DEMO with FALCON evidence (state PAPER only after DEMO proof) | maff0000/GOAL | GOLD-AUD-A, GOLD-AUD-B, GOLD-AUD-C, GOLD-AUD-D, GOLD-AUD-E, GOLD-AUD-F, GOAL-CONTRACT-001, GOAL-TRIGGER-001, HELIOS-T3, TRON-T2, TRON-T3A, TRON-T4, FALCON-T1 | P0 | capital | BLOCKED | Yes | **Yes** |
| HELIOS-STRATEGY-STANDARD-001 | shared | HELIOS | HELIOS Strategy Development Standard and Common Strategy Language (documentation and interoperability planning) | maff0000/HELIOS | GOAL-DCP-001, GOLD-AUD-B, GOLD-AUD-C, GOLD-AUD-F | P1 | low | BLOCKED | Yes | No |
| GOLD-AUDIT-CLOSEOUT-001 | shared | GOAL | Governed GOLD Audit Completion Train | maff0000/GOAL | GOAL-DCP-001 | P0 | medium | PO_REVIEW | Yes | No |

<!-- END GENERATED: backlog-table -->

## Next PID-authoring wave after GOAL-DCP-001

These are the next **independent PO/PID-authoring** wave. Once the control
plane is GREEN, each of them is waiting on exactly one thing: a canonical PID,
authored and approved by the Product Owner.

They are **not FORGE-dispatchable**, and nothing here should be read as a
dispatch list. FORGE dispatch requires an approved canonical PID *and then*
the item moving to `DELIVERY_READY` — no PID means not `DELIVERY_READY`. Until
that happens these items sit in `PID_DRAFT`, `./tools/goal-ready` returns
`{"ready":[]}`, and that empty answer is the correct one.

The list is **computed, not maintained by hand**: it is the answer for the
projection "`GOAL-DCP-001` has reached an accepted terminal state" — every
item whose own state is `PID_DRAFT` and whose every dependency is then
satisfied. Ids are canonical and complete, which is what makes the list
mechanically checkable; range notation such as `OPS-SAFE-001..003` is not a
canonical id and cannot be verified against the backlog.

Reproduce it with:

```bash
./tools/goal-ready --pid-wave --assume-closed GOAL-DCP-001
```

<!-- BEGIN GENERATED: pid-authoring-wave -->

- `ARES-CUR-001` — Canonical generation + legacy reconciliation (`maff0000/trading-ares`)
- `DARWIN-R1` — Source/runtime reconciliation (`maff0000/DARWIN`)
- `GOAL-CONTRACT-001` — `goal.strategy/v1` (`maff0000/GOAL`)
- `HERMES-CUR-001` — Authoritative PROD/current-state reconciliation (`maff0000/hermes`)
- `MT5-GW-001` — Reconcile eight stacked WO branches into canonical Git history (`maff0000/mt5-gateway`)
- `OPS-CRED-001` — Remove plaintext broker/DB credentials and rotate where appropriate (`maff0000/GOAL`)
- `OPS-LEGACY-001` — Prove/quarantine `agent-smith-original` and dell `MT5_Vantage` safely (`maff0000/GOAL`)
- `OPS-SAFE-001` — Backup/off-host/restore programme (`maff0000/GOAL`)
- `OPS-SAFE-002` — Network/data-store containment (`maff0000/GOAL`)
- `OPS-SAFE-003` — Secrets/runtime identity hygiene (`maff0000/GOAL`)
- `TRON-D1-RATIFY` — Ratify TRON D1 design baseline: independent audit, merge to the default branch, and disposition of open decisions (`maff0000/tron`)

<!-- END GENERATED: pid-authoring-wave -->

# GOLD-AUD-F external evaluation register (INFORMATION ONLY)

Status: DRAFT, pending independent audit by ROGUE. Source revisions as in `AUDIT-F.md` section 2.

**This register is information only.** It records what earlier (2026-09) reviews said at the time. It contains no recommendation to use any external engine, library, platform or service for the MVP, and no licence ruling. Under CA guidance 2026-10-15 (item 4) the MVP takes no new third-party engine or SaaS dependency, so none of these is an MVP option. Nothing was installed, executed or called, and no outbound request to any evaluated service was made.

## 1. Memory-fabric review records (12; carried from the approved PID table, NOT re-read by this audit: UNVERIFIED)

Re-verification status: the records live only in the memory fabric. A search of GOAL, CER, HSA, DARWIN, HELIOS, GOLD-STRATEGY-RUNTIME, tron and neo (case-insensitive terms: each project name below, `kernc`, `quantconnect`, `lean`, `vectorbt`, `zipline`, `freqtrade`, `nautilus`, `qlib`, `mlflow`, `cloudquant`) found **no GitHub-resident copy of any review**; the only hits are `LEAN-P1` and its backlog row in GOAL. Dates, verdicts and notes below are therefore the PID's, unverified.

| # | Evaluated | Kind | Date | Verdict recorded then | Note recorded then | New third-party service if used? |
|---|---|---|---|---|---|---|
| 1 | cloudQuant fork of backtrader (GPL-3.0) | library | 2026-09-19 | recorded then: use as backtest / live engine | verify its test claims first | no (library); live-capable, so execution use is out of scope |
| 2 | kernc/backtesting.py (AGPL-3.0) | library | 2026-09-19 | recorded then: use as fast-iteration front end | sketch only, never validation | no |
| 3 | OpenBB (AGPL-3.0) | data platform | 2026-09-19 | recorded then: use for macro / fundamentals | context only; default price feed unofficial | yes (data provider) |
| 4 | FinceptTerminal (AGPL-3.0) | desktop app | 2026-09-19 | recorded then: use as research console | not wired to pipeline | no |
| 5 | TradingAgents (Apache-2.0) | multi-agent LLM | 2026-09-19 | recorded then: use on demand for due diligence | one opinion, never a signal | implies external model calls |
| 6 | ai-hedge-fund (MIT) | multi-agent LLM | 2026-09-19 | long-horizon only | not applicable to GOLD | implies external model calls |
| 7 | Alpaca MCP server | vendor SaaS | 2026-09-19 | skip | duplicates governed paper stack; conversational orders bypass governance | yes |
| 8 | daily_stock_analysis | repo | 2026-09-19 | reject / park | methodology only | no |
| 9 | macro-monitoring | repo | 2026-09-19 | reject / park | methodology only | no |
| 10 | recession-radar | repo | 2026-09-19 | reject / park | methodology only | no |
| 11 | macro-regime-nowcaster | repo | 2026-09-19 | reject / park | methodology only | no |
| 12 | Risk and position-sizing open source (gap search) | search | 2026-09-19 | no credible candidate; build in-house | build as governed work order | n/a |

The PID states that detail was read for seven of these twelve and the other five rest on index and synthesis only. Staleness note: the backtrader and backtesting.py reviews predate the APOLLO core merge (2026-10-02), so their premise of an external engine under APOLLO no longer holds. Not found in any searched repository: any evaluation of QuantConnect / LEAN, vectorbt, zipline, freqtrade, nautilus, qlib, MLflow or an experiment-tracking service. `LEAN-P1` is defined nowhere (UNVERIFIED whether it means an external engine).

## 2. Internal legacy reuse assessments (5 documents, GitHub-resident, read)

`DARWIN@bf1142b5be9f6988ec36b60ba3db9022c76a47af` `docs/archaeology/`. Classifications are the documents' own words and counts of their tables.

| # | Document | Subject | Classifications used (as written) | New third-party service? |
|---|---|---|---|---|
| 13 | `HSA-PID004A-REUSE-ASSESSMENT.md` (188 lines) | HSA | 14 concepts: REUSE, REUSE_WITH_ADAPTATION, REIMPLEMENT_FROM_DOCTRINE, DO_NOT_REUSE (atomic conditions and condition typing do not carry over) | no |
| 14 | `HELIOS-PID004A-SEMANTIC-COMPATIBILITY.md` (171) | HELIOS legacy-to-DARWIN compatibility | 12 concepts: DIRECTLY_COMPATIBLE, COMPILABLE_WITH_VERSIONED_ADAPTER, DARWIN_MODEL_MUST_EXPLICITLY_REPRESENT, HELIOS_CURRENTLY_UNSUPPORTED, DEFER | no |
| 15 | `ATHENA-PID005-CURRENT-STATE-LEGACY-REUSE-ASSESSMENT.md` (135) | legacy ATHENA | 16 concepts: REUSE, REUSE_WITH_ADAPTATION, ADAPT, REJECT, UNKNOWN | no |
| 16 | `DIKE-PID005-LEGACY-REUSE-ASSESSMENT.md` (91) | legacy DIKE | six independent implementations, no canonical source; REUSE / ADAPT per item | no |
| 17 | `ATHENA-DIKE-BOUNDARY-PID005-RECOMMENDATIONS.md` (132) | boundary recommendations | 15 incorporated rulings; deterministic grid search only as first milestone | no |

Count check: 12 memory-fabric review records plus 5 archaeology documents = 17 register rows.

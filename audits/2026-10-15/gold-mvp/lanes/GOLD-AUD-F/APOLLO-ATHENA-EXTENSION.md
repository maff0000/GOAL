# GOLD-AUD-F: Minimum APOLLO / ATHENA extension (added scope, CA directive 16 Oct 2026)

Status: DRAFT evidence, pending independent audit by ROGUE. Strategy-neutral. This section lists a **minimal requirement set** only. It does not design, size-commit or authorise an expanded APOLLO or ATHENA implementation. `GOLD-TREND-PO3-001` is a design candidate only and is not selected; no document named it in GOAL `main` at `ceaf0291a43d029b1a47b1c192a62ff147f05ac0` (searched), so nothing here depends on it.

Goal stated by the directive: DARWIN / APOLLO / ATHENA can reproduce HELIOS atomic and chain semantics, LONG and SHORT, using the same governed market facts and the same strategy identity, so that HSA, CER and NEO can reference one strategy consistently.

Sources (full SHAs): `DARWIN@bf1142b5be9f6988ec36b60ba3db9022c76a47af`, `HELIOS@7f7193d55475e40583892b94dd461b1b64d6f1ef`, `HSA@279ec181b5cd78df953671e087e01b7c1190ff96`, `CER@60eae45305a25f8b1ad03769e5bf4264b4d294e2`.

## A. Current capability (from source)

| # | Capability | Mark | Evidence |
|---|---|---|---|
| A1 | DARWIN's specification model already represents the HELIOS composition vocabulary: ATOMIC, ALL, ANY, SEQUENCE (with tie semantics), CONTEXT_TRIGGER; directions LONG / SHORT / BOTH; component direction relationships SAME / OPPOSITE / ANY; expiry NEVER / FRAMES / DURATION; a 7-value normalised state enum equal in names to HELIOS's (DORMANT, FORMING, MATCHED, ACTIVE, WEAKENING, INVALID, EXPIRED); a rearm-only-via-DORMANT policy | **PROVEN** (representation) | `DARWIN` `darwin/specification/composition.py:61-95,153-358,493-540`; `HELIOS` `helios/spec/model.py:53-92`, `helios/contracts/state.py:110-187` |
| A2 | DARWIN model of facts: governed canonical facts (HERMES OHLCV fields only: open, high, low, close, volume) and a distinct type for specification-derived facts (EMA, ATR and similar, each with algorithm id, version, parameters) | **PROVEN** (types) | `darwin/specification/facts.py:34-110,192-232` |
| A3 | The compiler turns a finalised `StrategyVersion` into an `ExecutableStrategyPlan` carrying composition, and APOLLO derives its entry only from that plan | **PROVEN** | `darwin/apollo/plan_adapter.py:1-40`; `darwin/research_contracts/compiler.py` |
| A4 | APOLLO executes only: ATOMIC, LONG, one `Comparison` of an OHLCV field against a literal or parameter, one timeframe, one instrument; every other shape is a typed capability block at preflight | **PROVEN** | `darwin/apollo/plan_adapter.py:160-312`, `darwin/apollo/errors.py:46-70`, tests `tests/unit/test_apollo_plan_adapter.py:48,57` |
| A5 | APOLLO has no evaluation of derived facts (no moving-average, ATR, range or candle-shape computation), no CROSSES operators, no multi-timeframe alignment, no state machine, no expiry or invalidation handling, no SHORT | **PROVEN** (searched `darwin/apollo/*.py`) | `plan_adapter.py:226-231` (operators), absence in `darwin/apollo` |
| A6 | APOLLO's result is a trade replay with fixed stop / target from declared risk parameters; HELIOS is execution-blind and emits **states**, never trades. The two outputs are different kinds of thing | **PROVEN** | `darwin/apollo/engine.py`, `HELIOS` `docs/CONTRACTS.md` section 3 |
| A7 | HELIOS consumes its indicators as given HERMES facts and never recomputes them; DARWIN models indicators as its own derived facts with its own algorithm identity. These are two different "same fact" sources unless one is made authoritative | **PROVEN** | `HELIOS` `docs/CONTRACTS.md:22-60`; `darwin/specification/facts.py:192-232` |
| A8 | ATHENA does not exist (4-line placeholder). Its PID defines deterministic grid search only as a first milestone | **PROVEN** | `darwin/athena/__init__.py`; `docs/pids/PID-005-ATHENA.md` (705 lines, a PID, not code) |
| A9 | Identity: DARWIN keeps `strategy_version_id` (opaque) + a semantic fingerprint; HELIOS / HSA / CER use `strategy_id@strategy_version` | **PROVEN** | see AUDIT-F sections 3.2, 4.1 |
| A10 | Whether the deployed DARWIN includes any of this | **UNVERIFIED** | not inspected |

## B. Minimum requirement set (what must be true, not how)

Each requirement is the least needed for reproduction of HELIOS semantics; none is a design.

| Req | Requirement | Why it is minimal | Capability check needed (fail closed otherwise) |
|---|---|---|---|
| R-1 | **One identity.** A research `StrategyVersion` for a given HSA package is traceable to `strategy_id@strategy_version` and to one package hash; the same pair appears in APOLLO/ATHENA evidence, CER records, HELIOS state and NEO reports | Without it, no component can cite another's result for the same strategy (AUDIT-F F-02) | preflight refuses a run whose research identity lacks the pair or whose package hash differs from the registered one |
| R-2 | **One fact source of truth.** Indicator and context values used by APOLLO/ATHENA for a HELIOS strategy are the same governed facts HELIOS reads, identified by one fact catalogue (this is the `goal.market-fact` work, owned elsewhere), not independently recomputed variants | HELIOS never recomputes; a second computation can differ in warm-up, rounding or periods and then "reproduction" is untestable | preflight refuses a derived fact whose algorithm id / version is not the catalogue's; dataset binding names the fact versions |
| R-3 | **Atomic semantics reproduced.** Evaluate any HELIOS atomic's per-timeframe condition on closed frames for both directions, including cross-type conditions that need previous-frame state | A4/A5: today only OHLCV-vs-literal LONG | capability block per unsupported operator / fact (existing mechanism, vocabulary extended) |
| R-4 | **Chain semantics reproduced.** The four primitives (ALL, ANY, SEQUENCE with ordering window and tie rule, CONTEXT_TRIGGER) with direction relationship SAME / OPPOSITE / ANY and the required-state sets per component | The specification model already expresses them (A1); the engine does not execute them | block any composition field the engine does not implement, per field (existing exhaustive-gate discipline) |
| R-5 | **Multi-timeframe alignment on closed frames.** Higher-timeframe context is visible to a lower-timeframe evaluation only after that context frame has closed (no look-ahead), with the same role-to-timeframe binding as the package | Both candidates under review use two timeframes; causality is the engine's core promise | preflight proves each role's timeframe is bound and a no-look-ahead test exists for the binding |
| R-6 | **State-stream output equivalent to HELIOS.** For a package, APOLLO/ATHENA can emit the per-frame normalised state sequence (7 states, legal transitions, expiry, invalidation, persistence, rearm-only-via-DORMANT) for comparison with HELIOS on the same facts. Trade replay (stops, targets, fills) stays a separate layer on top | HELIOS emits states, not trades (A6); reproduction means state-sequence equality, then trades | a parity check: for the same package and same facts, state sequences are equal frame for frame, else the run is not marked reproduced |
| R-7 | **SHORT symmetry.** Direction handling for SHORT (entry, exits, MAE / MFE, sign of P&L) governed the same way as LONG | A4: LONG only | explicit capability gate per direction; no silent mirroring |
| R-8 | **Evidence class and honesty.** Results remain `APOLLO_RESULT` (non-proof) until a qualification gate exists; no result for an extended shape may be labelled proof | A8: no qualification module | persistence refuses a proof level without the gate |
| R-9 | **Reference-only ATHENA for the MVP.** ATHENA must not be required for the MVP path; if introduced later it consumes the same deterministic evaluator as APOLLO (one definition of strategy meaning) and starts with deterministic grid search only | avoids two engines diverging; matches DARWIN's own archaeology rulings | ATHENA refuses any strategy APOLLO would capability-block |

## C. CER evidence and promotion touchpoints

| Touchpoint | Requirement | Current | Mark |
|---|---|---|---|
| C-1 | An APOLLO/ATHENA run is registered in CER as evidence of class `BACKTEST` (or the relevant historical class), with `strategy_id`, `strategy_version`, artifact hash of the result, dataset id / version, `config_hash` carrying the package hash (until a dedicated field exists), producer, and a provenance-completeness marking | CER fields exist; no DARWIN-to-CER writer exists | CER side PROVEN present; writer MISSING |
| C-2 | Parity evidence (R-6 outcome) is itself recorded, so a promotion can cite "reproduced, N frames equal" separately from "performance" | no class named for it; the closest existing class is `BACKTEST` with a verdict / status field | gap: naming decision for CA |
| C-3 | A promotion transition that relies on this evidence cites its evidence ids and states the authority (CER does not validate either; ADR-001: an unresolved citation is not verified support) | free text, unvalidated | PROVEN gap (F-07) |
| C-4 | NEO references the strategy by the same pair and the CER evidence ids; it reads evidence, never writes research results | no NEO read path | MISSING (F-09, F-10) |
| C-5 | Evidence for an extended-shape run never reuses the evidence of a different shape or package hash | not enforced by CER | rule for the PO / CA, enforceable by R-1 |

## D. Verdicts (recommendations only) and comparative cost

Unit: engineer-days (ed), a planning estimate by this audit, not measured. Method: component size and test volume, the number of bounded changes in the requirement list at roughly 0.5-2 ed each including tests, plus contingency for unknown coupling. Basis: source size and test volume of the existing parts and the requirement list above.

| Component | Generation | Verdict | Cost: reuse / refactor-extend / clean rebuild | Basis and retained value |
|---|---|---|---|---|
| APOLLO core (replay, causal order, MAE / MFE, persistence, preflight gates) | newer canonical | **REUSE** the engine core and its gating discipline | 0 / see next row / 40-60 | 2.7k source lines, 3.1k lines of APOLLO tests, three adversarial correction rounds recorded; a rebuild discards all of that |
| APOLLO entry evaluation (plan adapter + signal) | newer canonical | **REFACTOR** (extend the evaluator behind the existing capability gate for R-3..R-5, R-7) | n/a / 25-45 ed for R-3 to R-5 and R-7 | the gate pattern is reused; the evaluator is the missing piece. Range reflects the unknown depth of cross-type conditions and the chain primitives |
| State-stream parity layer (R-6) | not existing | **new, small relative to the evaluator** | n/a / 10-18 ed | pure function over the same evaluator; reference is HELIOS's published states and its 1,005 tests |
| DARWIN specification model and compiler | newer canonical | **REUSE** | 0 / 0 / 30-50 | already expresses the vocabulary (A1) |
| Fact model (R-2) | newer canonical | **REFACTOR** (align derived-fact identities to the shared catalogue) | n/a / 5-10 ed in DARWIN, plus the catalogue work owned elsewhere | |
| ATHENA | placeholder | **REUSE the PID, build nothing now** | n/a / 20-35 ed for deterministic grid search, deferred | R-9 |
| Alternative: bypass APOLLO and use HELIOS itself as the evaluator for reproduction | n/a | not recommended by this audit; HELIOS is execution-blind and has no history / backtest layer; noted as an option only | UNVERIFIED | HELIOS dispositions belong to lane B |

Total minimum to reach "reproduce HELIOS semantics, LONG and SHORT": roughly **40-75 ed** inside DARWIN, against a clean replacement estimated at **70-110 ed**; neither includes ATHENA, qualification or production hardening. These figures are comparative planning estimates only and are not a commitment or an authorisation.

## E. What this section does not do

It selects no strategy; it does not say which candidate would be ported first; it does not authorise a work order; it proposes no APOLLO / ATHENA design; and it does not assert that the deployed DARWIN matches `main` (UNVERIFIED).

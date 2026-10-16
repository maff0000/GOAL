# GOLD-AUD-C: shared contract reconciliation, CP-1 and CP-2

**Work item:** `GOLD-AUD-C` (`pids/GOLD-AUD-C.md`, APPROVED by Central Architecture 16 October 2026). **Lane:** research, read-only audit.  
**Audited scope (quoted from the PID):** "Exactly CP-1 and CP-2": (CP-1) HERMES Redis to HELIOS input and (CP-2) HELIOS signed trigger to durable outbox to TRON inbox, each with explicit versioning, golden fixtures, rejection behaviour and failure-recovery semantics; plus, added by Central Architecture directive 16 October 2026, the **strategy-definition contract reconciliation** (section 8).  
**Interaction statement (no competing freeze):** this item freezes nothing. The package `cp-1/0.1.0` is PROPOSED. CP-2 is a **reference-only** package (`contracts/packages/cp-2-trigger-outbox-inbox/PACKAGE.md`): it replaces an earlier draft, names the dependency on the unpublished trigger authority and lists only which questions are open. The normative text of the trigger path belongs to its owning PID and is not restated, mirrored, encoded as a schema or exercised by fixtures here. CP-1's freeze mechanics are open decision D-C1. No package, schema or table in this directory is a competing contract. Section 8 lists options only.
**GOAL base:** the audit read sources from `ceaf0291a43d029b1a47b1c192a62ff147f05ac0`; this clean replacement is branched from GOAL `main` `e80fcda25a50140dc24793f2dd2770b1da2db517`. **Branch:** `wo/GOAL-GOLD-AUD-C-CLEAN` (local; not pushed).
**Independent audit verdict:** pending independent audit by ROGUE (see `AUDIT-VERDICT.md`). This lane does not self-certify.

Labels used throughout: PROVEN (read in source at a recorded revision, or reproduced by an offline test in this change), PARTIAL, UNVERIFIED (not verifiable from source and GitHub in this audit), MISSING (searched for, absent; scope and command recorded).

## 1. Where each of CA's ten evidence items is

| CA # | Item | Location |
|---|---|---|
| 1 | PID/WO identifier and exact scope | this header |
| 2 | Source repositories, revisions, documentation | section 2 and `SOURCES.tsv`; re-read script `verify-sources.sh` |
| 3 | Existing implementation, classified | section 3 |
| 4 | Actual versus expected comparison | mapping tables in the CP-1 `PACKAGE.md`; section 5; section 6; section 8 |
| 5 | Tests, fixtures, evidence | `contracts/packages/*/fixtures`, `tests/test_cp*.py`, section 10 |
| 6 | Defects and compatibility gaps | section 4 (AC-1 to AC-38), matrix rows in the CP-1 package; no matrix rows are prepared for CP-2 (reference-only) |
| 7 | Reusable code and documentation | `DISPOSITION.md` |
| 8 | Minimum recommended changes | `DISPOSITION.md`, section 9 |
| 9 | Safety and deployment constraints | section 10 |
| 10 | Independent audit verdict | `AUDIT-VERDICT.md` (pending) |

## 2. Source revisions (frozen at start)

| Repository | Revision | Notes |
|---|---|---|
| GOAL `main` | `ceaf0291a43d029b1a47b1c192a62ff147f05ac0` | evidence branch base |
| HERMES `main` | `ca1901789f8c7a7e085d02ebde8f7264d90d669e` | |
| HELIOS `main` | `7f7193d55475e40583892b94dd461b1b64d6f1ef` | |
| FALCON `main` | `8f218ec1b85b932285b042a7b1ae64dbd11eebee` | |
| TRON `main` | `5577039b5db05e70effef72c7e59df14db408419` | contains `PID.md` and tooling only |
| TRON `wo/WO-TRON-D1` | `37d5f009a080d25930eea37cf8c627bb0f3a1ff4` | schemas and lifecycle documents exist only here |
| MT5 gateway `main` | `6263d61f4cb0d4d5b16337e67c30f409bc9c5051` | read; downstream of TRON; out of scope for CP-1 and CP-2 |
| HSA `main` | `279ec181b5cd78df953671e087e01b7c1190ff96` | added scope |
| DARWIN `main` | `bf1142b5be9f6988ec36b60ba3db9022c76a47af` | added scope |
| CER `main` | `60eae45305a25f8b1ad03769e5bf4264b4d294e2` | added scope |
| `GOAL-CONTRACT-001`, `GOAL-TRIGGER-001`, ADR-CONTRACT-001 candidates | `64c843b` on a local branch of the delivery host | UNPUBLISHED; SHA-256 of each text in `SOURCES.tsv` (AC-26) |

DARWIN files cited live under `darwin/specification/` (`fingerprint.py`, `domain.py`, `serialization.py`, `validation.py`, `expressions.py`, `facts.py`, `composition.py`, `timeframe.py`), `darwin/research_contracts/compiler.py`, `darwin/apollo/` and `docs/archaeology/`.

APOLLO and ATHENA are packages inside the DARWIN repository (`darwin/apollo`, `darwin/athena`); there is no separate repository (`gh repo list` shows none). Working trees of all clones were unmodified; nothing was run against any component and no running system was contacted. Live HERMES production state, TRON runtime and private repositories were not read.

## 3. Existing implementation inventory (CA item 3)

| Area | Finding | Class | Evidence |
|---|---|---|---|
| HERMES candle publication | Governed v1 envelope with validator; closed key set; millisecond instants; prices quantised to 6 decimals; history record family with ZSET index | PROVEN (source) | `utils/candle_contract_v1.py` lines 21, 32, 63, 131, 280 at `ca19017`; `utils/candle_history_v1.py` 33, 129, 142 |
| HERMES indicator publication | Latest and history envelope, 14 names, declared method tokens, forbidden-token scan | PROVEN (source) | `utils/hermes_indicators_v1.py` 38, 52, 152; `utils/indicator_history_v1.py` 44, 67, 105 |
| HERMES manifest entry for candles and indicators | Manifest registers ticks only | PROVEN missing | `docs/contracts/hermes_redis_contract_manifest.md` 33-37 |
| HERMES production activation of indicator history, H4 repair, retention normalisation | Code in main; production steps "NOT YET EXECUTED" | PARTIAL; PROD state UNVERIFIED (Lane A) | `docs/governance/PID-HERMES-MVP-001.md` 202-205 |
| HELIOS fact input contract | Closed-world models, exact decimals, ordered windows, freshness policy | PROVEN (source) | `helios/contracts/market_fact.py` 27-47, 50, 100, 163, 197; `_fields.py` 63-131; `window.py`; `freshness.py` 45, 167, 197 |
| HELIOS reader of HERMES Redis | None; import ban; facts from fixtures | PROVEN absent (N1, N2) | `tests/test_execution_blind.py` 257; `docs/INTEGRATION.md` section 2 |
| External adapter | None found in HELIOS, HSA, DARWIN, FALCON, TRON at the revisions | MISSING in the searched locations; absence elsewhere UNVERIFIED (Lane B re-runs the wider search) | N1 to N3 |
| HELIOS trigger, signing, outbox | None | MISSING (N1, N3) | `helios/publish/sink.py`: file, stream, memory only |
| FALCON trigger payload | Evidence-shaped payload, free-string identifiers, stop-loss and take-profit fields, score fields | PROVEN | `schemas/payloads/helios/strategy_trigger.v1.schema.json` at `8f218ec` |
| FALCON signing doctrine | "Ed25519, subject to implementation proof"; canonical form unspecified | PROVEN | `docs/security/FALCON-HELIOS-TRIGGER-SIGNING.md` 13 |
| FALCON outbox | None in code; documents only mention it | MISSING (N7) | `docs/contracts/ARES-FALCON-CONTRACT.md` (ARES-owned outbox, not a trigger outbox) |
| TRON intake | `falcon.trade_action.v1`, ingestion RECEIVED/VALIDATE/EXPIRE/DEDUPLICATE, terminals REJECTED/EXPIRED/DUPLICATE/NEGOTIATED, epoch milliseconds | PROVEN on the D1 branch only | `docs/04-TRADE-LIFECYCLE.md` 80-110; `docs/05-CONTRACTS.md` 56 at `37d5f00`; none of it on TRON `main` |
| TRON inbox or outbox design | None | MISSING (N5, N6) | |
| TradingTriggerInbox specification | None except the CA statement; an unpublished candidate exists and is not restated here | MISSING as an existing design; a candidate is PROPOSED but unpublished | N4 to N6; section 6 |

### Negative-search commands

`negative-searches.sh` in this directory re-runs every absence claim (`CLONE_ROOT=<fresh clones> ./negative-searches.sh`). Scope: `git grep` over the named revision only. Result at audit time: N1 to N10 each returned no line (empty under each heading), including N10 (no JSON Schema file anywhere in the DARWIN tree at `bf1142b`). They prove absence at those revisions and in those repositories only.

## 4. Findings (CA item 6)

Each finding has a label and citations. Fixtures prove the rule; the numbering AC-n is this lane's own (it never edits the owning PIDs).

### CP-1

| Id | Finding | Label | Evidence |
|---|---|---|---|
| AC-1 | HERMES candle and indicator keys have no registered manifest entry or schema file; the manifest says they are "separately designed" | PROVEN | manifest 33-37 at `ca19017` |
| AC-2 | Version-string inconsistency: HERMES publishes `v1`; HELIOS advertises `helios.market_fact/1.0.0` through `describe_input_contract()` while its tests, configuration and fixtures accept and use `hermes.market_fact/1.0.0` | PROVEN | `market_fact.py` 47; `hermes_boundary.py` 73; `tests/test_config.py` 44, 122; `integration/exemplars.py` 52 at `7f7193d`. HELIOS-side fix is D-C3 |
| AC-3 | HELIOS has no machine-readable rejection codes, only exception text; its own tests assert message substrings | PROVEN | `hermes_boundary.py` 47 (tuple of prose rules); `tests/test_hermes_fixtures.py` `MALFORMED_CASES`. CP-1 assigns codes |
| AC-4 | Number form: HERMES publishes JSON numbers rounded to 6 decimals from binary floats; HELIOS contract text requires exact decimal text, yet its fixture loader reads JSON numbers with `parse_float=Decimal` and so accepts them | PROVEN | `candle_contract_v1.py` 131; `_compute_indicators` 431-477 (`round(..., 6)` and `round(..., 4)`); `fixture_source.py` 9, 110. D-C5 |
| AC-5 | Instant form: HERMES millisecond `Z`; HELIOS canonical fixed-width microsecond `Z`, but its parser accepts instants without fractions and with offsets | PROVEN | `candle_contract_v1.py` 63, 101; `helios/clock.py` 17, 49; fixtures use `...00Z` |
| AC-6 | `regime` and `session` have no supplier. HERMES forbids `regime` in its payload and publishes no `session`; HELIOS fixtures supply both | PROVEN | `hermes_indicators_v1.py` 38; `market_fact.py` 31-44; `fixtures/hermes/xau_usd/*.json`. Impact on any strategy requiring either: Lane B |
| AC-7 | HERMES publishes indicators HELIOS does not know (`ema_12`, `ema_26`, Bollinger, ADX) against HELIOS's closed-world refusal of unknown fields | PROVEN | `hermes_runtime_publisher_steps_v1.py` 431-477; `_fields.py` 131 |
| AC-8 | HERMES declares RSI as Cutler SMA and ATR as SMA; HELIOS names no method. A smoothing change would silently change meaning | PROVEN (HERMES side); strategy assumptions UNVERIFIED | `hermes_indicators_v1.py` 52-60 |
| AC-9 | Two Redis keys per bar joined on instrument, timeframe and open instant; indicator history is code-in-main but its production activation, the 65-object H4 repair and retention normalisation are recorded as not executed | PARTIAL | PID 202-205; PROD UNVERIFIED (Lane A) |
| AC-10 | H4 buckets open at 22/02/06/10/14/18 UTC; HELIOS checks only minute zero for H4, so it accepts them, but its own fixtures use the 00/04/08 grid; a strategy that assumes the UTC midnight grid is not checked by any fixture | PROVEN (HERMES); impact UNVERIFIED | `candle_h4_derivation_v1.py` 10, 31; `timeframe.py` 148 |
| AC-11 | D1: HERMES carries a legacy token `D` and a governed `D1`; indicator history excludes D1; D1 candle history retains 35 sealed bars, fewer than any 200-bar indicator needs | PROVEN | `candle_contract_v1.py` 32; `indicator_history_v1.py` 44; `candle_d1_history_v1.py` 41 |
| AC-12 | HELIOS implements a future-dated refusal (`FutureFactError`) that its published `INPUT_REJECTION_RULES` list omits; freshness and incomplete-bar rules apply to the newest frame only | PROVEN | `freshness.py` 167-230; `errors.py` 45; `hermes_boundary.py` 47-62 |
| AC-13 | `ingested_at_utc` has no HERMES source and HELIOS requires it not to precede `observed_at_utc`; a reader clock behind HERMES would be refused. The adapter must not clamp | PROVEN (rule); operational frequency UNVERIFIED | `market_fact.py` 163-195 |
| AC-14 | FALCON's `hermes.market_fact` payload (`fact_id`, `series_id`, `value_decimal`) is an evidence-side third shape, not an input | PROVEN | `registry/event_family_registry.v1.json` at `8f218ec` |
| AC-15 | No external adapter and no Redis reader exists | MISSING (N1 to N3); wider search is Lane B | |

### CP-2 (published-component findings only)

Findings about the text of the unpublished trigger candidate (AC-19 to AC-25, AC-27, AC-28) are **withheld from this change**: they would restate that text in substance. Their identifiers are reserved so numbering stays stable; the content is held in the private record and is for the owner of the trigger authority once it is published.

| Id | Finding | Label | Evidence |
|---|---|---|---|
| AC-16 | HELIOS has no trigger, signing or outbox code; its sinks are file, stream and memory | PROVEN absent (N1, N3) | `helios/publish/sink.py` |
| AC-17 | FALCON's registered trigger payload is an evidence-shaped record, not a signal-only boundary: a free-string trigger identifier, a flat direction, entry/exit/adjust action types, 30-minute and weekly timeframes, stop-loss and take-profit fields, duplicate decimal and numeric fields, a score field and variable-precision instants | PROVEN | FALCON payload schema file at `8f218ec` |
| AC-18 | TRON D1 intake requires stop-loss, take-profit and confidence for OPEN, uses epoch milliseconds and an action identifier, and its terminal set is REJECTED, EXPIRED, DUPLICATE, NEGOTIATED; the documents are on a design branch, not on `main`, and describe nothing deployed | PROVEN | `docs/05-CONTRACTS.md` 56, `docs/04-TRADE-LIFECYCLE.md` 80-110 at `37d5f00` |
| AC-26 | The normative sources for the trigger path are unpublished: the candidates are a local commit and the trigger item has no PID file path. Any conformance package for the path is premature until the authority is published | PROVEN | `SOURCES.tsv` (`GOAL-LOCAL` rows) |

Strategy-definition findings AC-29 to AC-38 are in section 8.

## 5. Re-test of C-1 to C-14 (`GOAL-CONTRACT-001`) against current commits

Status: CONFIRMED (the candidate's statement is still true at the audited revisions), CHANGED (true with a correction), NEW (a detail the candidate lacks). Rows proposed to the owning PID, never edited.

| Row | Status | Note and evidence |
|---|---|---|
| C-1 | CONFIRMED, plus NEW detail | DARWIN `canonicalize` (`fingerprint.py` 28-61) tags dataclasses with `__type__`, writes `Decimal` with `str()`, datetimes with `isoformat()`, and `json.dumps` without `ensure_ascii=False`; HELIOS `canonical_dumps` (`serialisation.py` 38, 120) normalises decimals and uses `ensure_ascii=False`. HELIOS emits bare hex, DARWIN bare hex. HSA has no fingerprint at all (N9) |
| C-2 | CONFIRMED | HELIOS fingerprint input excludes `metadata` and `identity.strategy_version` but includes `strategy_id` (`cer_boundary.py` 66, 120-145); DARWIN excludes ids, title, thesis, provenance (`domain.py` 132-153) |
| C-3 | CONFIRMED | DARWIN's fingerprint covers `exit_rules` and `intrabar_ambiguity_policy` (`domain.py` 132-144); HSA's package has `invalidation_conditions` and `validity_conditions` but no exit-rule field (`strategy_package.schema.json` required list) |
| C-4 | CONFIRMED, plus NEW | HELIOS/HSA identity patterns identical (`identity.py` 53-73; `common.defs.json` 13, `semver` pattern); DARWIN accepts any non-empty `strategy_version_id` (`validation.py` 596-597); CER accepts the looser `^[A-Za-z0-9][A-Za-z0-9._-]*$` (`identity.py` 45), so its own documentation example version `v1.2.0` is not a HELIOS/HSA version |
| C-5 | CONFIRMED | seven states `helios/contracts/state.py`; DARWIN representation by archaeology study only |
| C-6 | CONFIRMED, plus NEW | FALCON adds `FLAT` and `M30/W1` (AC-17) |
| C-7 | CONFIRMED | `domain.py` 132-144 |
| C-8 | CONFIRMED, plus NEW | FALCON `score_value` with `helios.entry_confidence.v1` ids |
| C-9 | CHANGED | HELIOS accepts the HERMES lower-case codes and so also accepts HSA-style `4H`, `15M`, `1H`, `1D` through `Timeframe.parse` (`timeframe.py` 100-122) but refuses `30M`, `1W`; HSA's grammar `^[1-9][0-9]*(M|H|D|W)$` is wider (AC-34) |
| C-10 | CONFIRMED | HSA `chain.schema.json` closed primitive enum and flat inputs; HELIOS `ChainSpec` (`spec/model.py` 381); DARWIN study rows 2-5 |
| C-11 | CONFIRMED, plus NEW | HSA carries `lifecycle` inside the package; the HELIOS package has no lifecycle field and is a closed schema, so an HSA package cannot be loaded by HELIOS unchanged (AC-35) |
| C-12 | CONFIRMED | HSA `required_hermes_fields` strings, HELIOS `InputRequirement` (`spec/model.py` 125), DARWIN `CanonicalFactReference`; `HERMES-FACT-001` has no PID |
| C-13 | CONFIRMED | no published canonicalisation vectors found at the audited revisions; the earlier CP-2 draft's fixtures are withdrawn from this change |
| C-14 | CONFIRMED | `helios/contracts/identity.py` 45-52 keeps CER identifiers out |

## 6. Trigger path: published-source facts and open questions (reference only)

The earlier draft re-tested every row of the unpublished trigger candidate. That text is not restated in this change. What follows is limited to facts read from published repositories at the recorded revisions, and to the names of open questions.

**Published-source facts**

* Three inbound shapes for strategy signals exist: HELIOS state publication, FALCON's registered trigger payload and TRON's D1 intake (AC-17, AC-18). TRON `main` holds only `PID.md` and tooling.
* Time precision differs: TRON uses epoch milliseconds, FALCON variable-precision instants, HELIOS fixed-width microsecond instants.
* FALCON's payload carries duplicate decimal and numeric fields and the `FLAT` and `ENTRY/EXIT/ADJUST` vocabularies.
* HELIOS keeps execution vocabulary out by a test (`tests/data/forbidden_execution_vocabulary.txt`, `tests/test_execution_blind.py`).
* FALCON's signing doctrine leaves the canonical form unspecified (`FALCON-HELIOS-TRIGGER-SIGNING.md` 13). No signer owner or key custody was found (N1).
* TRON D1 `PID.md` 1541 states that Redis is messaging, not durable state.

**TradingTriggerInbox specification status:** MISSING as an existing design (N4, N5, N6: zero hits for `TradingTriggerInbox` and `TriggerInbox`; the only prior statement is CA's). An unpublished candidate exists; whether it is the specification of record is an open decision of that candidate.

**Open questions:** tracked in the unpublished candidate, not here.

## 7. Cross-lane dependency register

Lanes A, B, D, E, F run in parallel. This lane did not wait for any. Soft inputs are read only after that lane commits; none had committed when this audit read the sources, so each dependency below is an explicit assumption and the dependent rows are marked.

| Lane | Needed for | State in this lane | Marked as |
|---|---|---|---|
| A (HERMES surface) | PROD key inventory and readiness for CP-1; H4/D1 depth | not read; HERMES PID text used | AC-9, AC-10, AC-11 UNVERIFIED; matrix rows 2 and 3 of cp-1 |
| B (HELIOS adapter and strategies) | whether an adapter exists; which facts strategies require (regime, session, method assumptions) | wider search not done | AC-15, AC-6, AC-8 |
| D (TRON intake facts) | trigger-path context; TRON-T4 state names | TRON read directly from the repository | AC-18 |
| E (FALCON registry facts) | evidence-event context | FALCON read directly | AC-17 |
| F (private consumer) | a private consumer's use of strategy identity | not published; not audited here | AC-37 |
| `GOLD-MVP-001` | consumes the matrix rows | CP-1 rows prepared in the package; none for CP-2 (reference-only); not contributed to `COMPATIBILITY-MATRIX.md` (separate PR after acceptance) | |

## 8. Strategy-definition contract reconciliation

Scope note: this section comes from the Central Architecture directive of 16 October 2026; the approved PID text still says "Exactly CP-1 and CP-2".

Added scope (Central Architecture directive 16 October 2026: HELIOS Strategy Development Standard and Common Strategy Language). Reconcile the HSA strategy blueprint and package schema, the HELIOS versioned strategy-package JSON Schema, and DARWIN Amendment A-007. They are **not** treated as interchangeable without proof. **No contract is proposed or frozen here; options are listed in 8.6.** `GOLD-TREND-PO3-001` (a generic Trend-Pullback-PO3 family) is a design candidate only, is not selected, and is not used as an example by this section.

### 8.1 The three definitions and their provenance

| Aspect | HSA strategy package | HELIOS strategy package | DARWIN A-007 and Specification |
|---|---|---|---|
| Artefact | `contracts/strategy_package.schema.json` (+ `chain`, `atomic_strategy`, `cer_reference`, `common.defs`), JSON Schema 2020-12; blueprint doctrine `docs/HELIOS-STRATEGY-BLUEPRINT.md` | `docs/schema/strategy_package.schema.json`, generated from the models in `helios/spec/model.py` (`StrategyPackage` line 466) | doctrine `AMENDMENT-A007-...md` (LOCKED); typed model `StrategyVersion` (`domain.py` 162); lossless serialiser `serialization.py` 769-865; compiled `ExecutableStrategyPlan` (`compiler.py` 77) |
| Schema version marker | `$hsa_kind` const `strategy_package`; `$hsa_contract_version` semver | `schema_version` const `helios.strategy_package/1.0.0` | `schema_semantic_version` (a field inside the fingerprint); A-007.4 shows a conceptual `"schema_version": "1.0"`; `PLAN_SCHEMA_VERSION` `"1"`; separate `serialization_schema_version` |
| Identity | `strategy_id` `^[a-z][a-z0-9_]{2,63}$`; `strategy_version` strict semver | same patterns (`identity.py` 53-73) | `strategy_version_id` any non-empty string (`validation.py` 596-597); semantic identity is the fingerprint |
| Composition | closed enum `ALL ANY SEQUENCE CONTEXT_TRIGGER`; flat, no chain-of-chain | same four; `SEQUENCE` needs unique contiguous indices and an ordering window (`ChainSpec` 381) | typed composition; `ALL`, `ANY` directly compatible, `SEQUENCE` and `CONTEXT_TRIGGER` "compilable with versioned adapter" (archaeology study rows 2-5) |
| Atomic condition | prose plus `deterministic_test_cases`; HSA's own reuse assessment: typed conditions DO_NOT_REUSE (row 6) | declarative wrapper bound by registry to **hand-written Python atoms** | typed expressions and fact references (`expressions.py`, `facts.py`) |
| Lifecycle | `lifecycle.status` inside the package; promoted versions immutable, enforced by diff (`versioning.py` 575, `refuse_in_place_mutation`) | no lifecycle field; `assert_promotion_immutable` compares fingerprints | status outside the semantic document; immutable frozen dataclass |
| Provenance | `provenance` and `cer_references` (required) | `metadata` (title, description, authored_by, authored_at_utc); excluded from fingerprint | `provenance` excluded from `semantic_fingerprint` (`domain.py` 151-153) |
| Canonical JSON | none defined; `json.dumps(sort_keys=True, default=str)` appears incidentally (`hsa/semantics.py` 323) | `canonical_dumps` (`serialisation.py` 120): sorted keys, `ensure_ascii=False`, normalised decimal strings, microsecond `Z`, `null` preserved | `canonicalize`/`canonical_json` (`fingerprint.py` 28-61): sorted keys, `__type__` tags, `Decimal` via `str()`, datetime via `isoformat()`; lossless tagged form in `serialization.py` |
| Semantic fingerprint | **none** (N9) | `definition_fingerprint` (`cer_boundary.py` 120): SHA-256 hex of canonical package minus `metadata` and `identity.strategy_version`; **includes** `strategy_id` | `semantic_fingerprint` over 11 named fields (`domain.py` 132-144), excludes all ids; plan has a separate `fingerprint` and carries `source_semantic_fingerprint` |
| Emits or consumes | authoring side; schema describes the deliverable "FORGE implements inside HELIOS" | consumed by HELIOS; schema description says "emitted by HSA" | A-007.7: one route into research; JSON is interchange, typed model is authority |

### 8.2 Compatibility matrix (labels with citations)

| Id | Pair and dimension | Label | Evidence |
|---|---|---|---|
| SD-1 | HSA to HELIOS, identity shape | PROVEN identical | `common.defs.json` 13, `semver`; `identity.py` 53, 73 |
| SD-2 | HSA to HELIOS, document shape | PROVEN incompatible: HSA has 29 properties (`lifecycle`, `cer_references`, `thesis`, `deterministic_test_cases`, ...) the closed HELIOS schema refuses; HELIOS requires `schema_version`, `metadata`, `inputs`, `parameters` | both schema files |
| SD-3 | HSA to HELIOS, emitter | MISSING: no code in HSA produces `helios.strategy_package` (N8) | `negative-searches.sh` N8 |
| SD-4 | HELIOS to HSA, round trip | MISSING | same |
| SD-5 | HSA to DARWIN, identity | PROVEN mismatch: DARWIN `strategy_version_id` is a free string; archaeology rates HSA identity "REUSE_WITH_ADAPTATION" | `HSA-PID004A-REUSE-ASSESSMENT.md` rows 1-2 |
| SD-6 | HELIOS to DARWIN, composition semantics | PARTIAL: DARWIN's own study classifies `ALL`, `ANY` direct and `SEQUENCE`, `CONTEXT_TRIGGER` as versioned-adapter; no adapter code was found | `HELIOS-PID004A-SEMANTIC-COMPATIBILITY.md` summary table at `bf1142b`; N-searches over `darwin` found only descriptive references to HELIOS |
| SD-7 | HELIOS to DARWIN, document import | MISSING: DARWIN has no JSON Schema file for A-007 (N10) and `serialization.py` reads only DARWIN's own tagged form | `serialization.py` 769-865; N10 |
| SD-8 | DARWIN to HELIOS, compilation | MISSING: `ExecutableStrategyPlan` is consumed by APOLLO only | `compiler.py` 77; `plan_adapter.py` |
| SD-9 | Atomic condition meaning across the three | PROVEN divergent: prose, Python, typed | rows in 8.1 |
| SD-10 | Fingerprint across the three | PROVEN not comparable (inputs, id inclusion, number and instant forms, hex prefix, `__type__` tags); no cross-system canonical form is published | AC-30 and C-1 |
| SD-11 | Canonical JSON requirement | PARTIAL: required by A-007.3 in principle, specified only inside HELIOS (`canonical_dumps`) and DARWIN (`canonicalize`, differently) | rows in 8.1 |
| SD-12 | Versioning rules | PARTIAL agreement: promoted versions immutable in all three; the marker of the schema version differs (8.1) | `versioning.py`, `identity.py`, A-007.8 |
| SD-13 | Timeframe tokens | PARTIAL: HSA `4H`, `15M` style parses in HELIOS through the HERMES-code path for six values, wider grammar refused | `common.defs.json` timeframe; `timeframe.py` 100-122 |
| SD-14 | Reproducibility vectors | MISSING in all three | no vectors found |

### 8.3 Findings

| Id | Finding | Label |
|---|---|---|
| AC-29 | HSA defines no fingerprint and no canonical serialisation of its package; immutability is enforced by a diff, not a hash | PROVEN (N9) |
| AC-30 | HELIOS includes `strategy_id` in its fingerprint, DARWIN excludes ids; the two use different digest forms (see C-1) | PROVEN |
| AC-31 | No HSA to HELIOS emitter exists although the HELIOS schema describes its packages as emitted by HSA | PROVEN absent (N8) |
| AC-32 | No adapter exists between the HSA or HELIOS package and DARWIN's document, nor the reverse; the A-007 JSON Schema does not exist | PROVEN absent (N10) |
| AC-33 | Three condition semantics (prose, Python, typed) mean a mechanical path from HSA blueprint to a HELIOS atom to a DARWIN expression does not exist; each crossing is a human or FORGE step | PROVEN |
| AC-34 | Timeframe grammars differ (HSA wide suffix style; HELIOS six codes; FALCON eight; HERMES legacy `D`) | PROVEN |
| AC-35 | Lifecycle status lives inside HSA's package but outside DARWIN's semantic document and nowhere in HELIOS's | PROVEN |

### 8.4 Intended consumers and their references to a strategy identity

| Consumer | How it references a strategy | Label | Evidence |
|---|---|---|---|
| HSA | produces `(strategy_id, strategy_version)` and carries CER identities as opaque; no fingerprint | PROVEN | `hsa/cer.py`, `versioning.py` 334 |
| CER | logical `strategy_id`, `strategy_version` supplied by the caller and shape-validated only; four generated evidence ids; no strategy fingerprint field (CER does carry an artifact-content digest, which is unrelated to a strategy definition) | PROVEN. Consequence: evidence binds to `(id, version)` only, so the immutability rule is the only link to the definition (AC-36, PARTIAL) | `src/cer/contract/identity.py` 45, 64 |
| Private consumer (not published) | not audited in this document | UNVERIFIED; mapping to the GOAL identity MISSING (AC-37) | n/a |
| APOLLO | consumes the compiled `ExecutableStrategyPlan`; recomputes `StrategyVersion.semantic_fingerprint` independently and refuses a plan whose `source_semantic_fingerprint` or `source_strategy_version_id` differs; capability-blocks unknown `schema_semantic_version` | PROVEN | `preflight.py` 120, 254-270; `plan_adapter.py` 31 |
| ATHENA | the package contains only `__init__.py` at this revision: no strategy reference exists to inspect | PROVEN stub (AC-38); behaviour UNVERIFIED | `darwin/athena/__init__.py` |

### 8.5 Missing adapters (list, none specified)

HSA package to HELIOS package (SD-3); HELIOS package to HSA lineage (SD-4); HELIOS or HSA package to DARWIN document (SD-7); DARWIN StrategyVersion to HELIOS package (SD-8); a cross-system fingerprint computed beside each internal one (C-1); private-consumer and CER mappings to the shared identity (AC-36, AC-37); ATHENA's reference (AC-38).

### 8.6 Options, listed only (no recommendation adopted, nothing frozen)

* **O-A:** keep three definitions with explicit versioned adapters, each proven by fixtures in both directions before use.
* **O-B:** designate one interchange document (HELIOS package, a DARWIN-derived schema, or a new one) and treat the others as authoring or research views, with a published conformance suite.
* **O-C:** converge identity and fingerprint first (the canonical-form and strategy-identity decisions of the unpublished contract candidate) and defer document convergence until adapters have been proven.
* Independent of the option: any choice needs published reproducibility vectors (SD-14) and a decision on where lifecycle status lives (AC-35).

## 9. Minimum recommended changes and offered register rows (CA items 7 and 8)

See `DISPOSITION.md` for reuse verdicts. Minimum changes, each owned by a component architect and none made here:

1. HELIOS: reconcile the advertised fact schema version with its configuration and fixtures (AC-2); add the future-dated rule to the published rule list (AC-12); provide machine-readable rejection codes or adopt the CP-1 codes (AC-3).
2. HERMES: register the candle and indicator contracts in the manifest with a schema file (AC-1); decide the numeric form on the wire (D-C5).
3. Adapter owner (HELIOS-T2): implement against CP-1 conformance tests; own regime and session decisions with ARES (AC-6).
4. Trigger authority owner: publish the candidate through its own governed PR before any conformance package for the path is rebuilt (AC-26); the withheld findings are available to the owner through the private record.
5. TRON-T4 and FALCON-T3: reconcile to the published trigger authority once it exists (AC-17, AC-18).
6. Strategy definitions: decide an option in 8.6 with CA/PO; publish vectors.

## 10. Safety, constraints, tests and open items (CA item 9)

* Read-only; no deployment, no service touched, no broker or DEMO contact, no Redis, database, bridge or MT5 service contacted; no GitHub write; nothing pushed.
* Public-repository safety: CP-1 fixtures use canonical instruments and SHA-256 digests only; no key material of any kind is held in this change. Key families, if any, are described by pattern; no hostnames, addresses, accounts or credentials. `tests/test_cp_packages_common.py` runs the sanitisation grep and the forbidden-vocabulary test over the packages, support code and this directory.
* Not run: any component code (HELIOS, HERMES, TRON, FALCON, DARWIN, HSA). The consumer-side obligations (CB-1 to CB-6 against a real component) are therefore unproven; the CP-1 reference model and two checkers prove the package's internal consistency only.
* Independence limit of the two CP-1 checkers, stated exactly: checker B (standard library) and checker A (`jsonschema` plus `datetime`/`Decimal`) were written by the same engineer, B first; they share only `cp_common.py` (JSON loading and the `Num` number type), so rule logic, instant arithmetic and decimal conversion are separate code. A third, genuinely independent implementation is recommended for the auditor (A-2).
* CI limit: the repository CI installs only `pyyaml` and `pytest`. The A-versus-B equality tests need `jsonschema` and are reported as skipped where it is missing; checker B and every fixture, scenario and package test run with the standard library alone. Adding the package to CI is a workflow change outside this lane (non-goal).
* Open decisions, by reference: those of the unpublished trigger and contract candidates (identifiers held in the private record) and D-C1, D-C3, D-C5 of the lane PID. None is decided here.
* UNVERIFIED list: live HERMES PROD publication and history depth; the existence of an adapter outside the searched repositories; strategy dependence on regime, session and method tokens; FALCON Decision 16 text; ATHENA behaviour; the operational frequency of clock-order refusals (AC-13); the HELIOS engine's verdict on the CP-1 frames (not executed).
* Test and tool results are recorded in `AUDIT-VERDICT.md` for the head commit.

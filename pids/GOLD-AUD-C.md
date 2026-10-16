# GOLD-AUD-C — Shared contract reconciliation and consumer/provider packages (CP-1, CP-2)

**Lane:** research  
**Target repository:** `maff0000/GOAL`  
**Evidence:** primary PR in `maff0000/GOAL`, branch `wo/GOLD-AUD-C-evidence`, path `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-C/`; contract packages under `contracts/packages/`; matrix rows are contributed into `audits/2026-10-15/gold-mvp/COMPATIBILITY-MATRIX.md`, which `GOLD-MVP-001` owns  
**Priority:** P0  
**Risk:** Medium  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE -> FORGE  
**depends_on:** `GOAL-DCP-001` only  
**Complements:** `GOAL-CONTRACT-001`, `GOAL-TRIGGER-001`  

**Header notes:** Risk Medium: specification only, no runtime change. Matt gate No: D-3 of `GOAL-TRIGGER-001` keeps its own Matt gate and this item does not decide it. Delivery: evidence and contract PRs into `maff0000/GOAL`. `GOAL-DCP-001` is CLOSED. `GOAL-CONTRACT-001` and `GOAL-TRIGGER-001` are the approval owners of their contracts and this item freezes nothing (amendment fallback in D-C2). Evidence location follows programme-controller rulings 1 to 4 (`PORTFOLIO.md` appendix).

Header values are PROVISIONAL: the item is not in `backlog/backlog.yaml`; the backlog patch is specified, not applied, in
`audits/2026-10-15/gold-mvp/PORTFOLIO.md` section 11. Lane vocabulary is the backlog set {shared, research, trading, ops}; `research` is used for all
six audits (CA frame). Priority, lane and risk follow the CA/PO adjudication 2026-10-15 (recorded in `PORTFOLIO.md`, not in this PID); approval is not yet recorded and is entered by CA/PO only.
This item is a read-only audit; the contract packages it produces are specifications marked PROPOSED.

## Status

DRAFT CANDIDATE for Central Architecture review. Not approved. Not DELIVERY_READY.

**Form decision: option (ii), a thin new item.** It is justified in the section "Form decision" below. It does not amend, supersede or compete with
`GOAL-CONTRACT-001` or `GOAL-TRIGGER-001` (candidates on branch `wo/GOAL-CONTRACT-TRIGGER`, `64c843b`, with
`decisions/ADR-CONTRACT-001-STRATEGY-SEMANTICS.md`; the `GOAL-TRIGGER-001` backlog item is on `main` since GOAL PR #5 merged (`90323b3`); the PID
candidate is not on `main`, and no `pid_path` is set). Facts below were read on 2026-10-15 unless marked UNVERIFIED. Fabric is memory, not authority
(ADR-DELIVERY-001).

## Purpose

CA directive, Lane C: reconcile the two contract PIDs with the implementations that already exist, and produce governed consumer/provider contracts
for (CP-1) HERMES Redis -> HELIOS input and (CP-2) HELIOS signed trigger -> durable outbox -> TRON inbox, with explicit versioning, golden fixtures,
rejection behaviour and failure-recovery semantics. GOAL owns cross-system contract approval; component architects may propose changes but cannot
independently freeze incompatible versions.

**CA guidance 2026-10-15 applied (items 1 and 2).** (1) HERMES owns Redis publication. A HELIOS-side EXTERNAL ADAPTER, outside the pure
HELIOS engine (execution-blind, deterministic, no Redis or network imports), owns consumption and translation. GOAL approves the interface:
CP-1 is that interface. The `v1` to HELIOS fact-schema mapping belongs to the adapter; HERMES supplies a `HERMES-FACT-001`-style contract of
what it publishes. (2) `GOAL-TRIGGER-001` alone owns signed-trigger, outbox and inbox semantics; HELIOS, TRON and FALCON hold no competing
trigger contract, so CP-2 is a conformance and reconciliation package over that contract and every competing intake or evidence shape found
(FALCON `strategy_trigger`, TRON `falcon.trade_action.v1`) is recorded as a conflict to be reconciled to it, never as a second authority.

The two PIDs already specify the strategy envelope and the trigger envelope. What they do not contain, and what this item adds, is (a) a field-level
reconciliation against what HERMES, HELIOS, FALCON and TRON actually emit or assume today, (b) a consumer/provider conformance package per boundary,
and (c) golden fixtures with expected rejection codes that both sides can run. CP-1 is not covered by either PID at all.

## Form decision (amend versus new)

Option (ii), a thin new item, because:

1. **CP-1 has no home.** `GOAL-CONTRACT-001` Non-goals exclude "fact names or payload schema (HERMES-FACT-001)"; `HERMES-FACT-001` has no PID.
   Amending the trigger or strategy PID to carry a Redis input contract would break their scope statements and mix an upstream data boundary into a
   strategy-semantics freeze.
2. **Different approval risk profiles.** `GOAL-TRIGGER-001` is High risk, Matt-gated (D-3) and carries blocker decisions D-1..D-4, D-12. A CP-1 or
   conformance increment inside it would inherit those blockers and stall.
3. **Size.** Both PIDs are 362 and 364 lines and each has a long contradiction register; a third increment each duplicates evidence or pushes them
   past the PID size convention (D-11 of GOAL-TRIGGER-001 already contemplates a split).
4. **Different nature.** The deliverable is a read-only reconciliation audit plus conformance material; the PIDs deliver normative specifications.
   Research-lane evidence can land and be reviewed before either contract's draft-freeze, and informs them.
5. **No competing freeze, by construction.** This item has no authority to freeze anything (see Interaction rules). CP-2 is a conformance and
   reconciliation package over `goal.strategy-trigger/v1`; its normative text is `GOAL-TRIGGER-001`'s. CP-1 freezes only through the owner chosen in
   D-C1.

An amendment (option i) is preferable only if CA wants one approval gate; D-C2 records that choice. (RESOLVED by CA/PO adjudication 2026-10-15: option ii; a separate audit work item, not an amendment.)

## Current state

### Existing contract PIDs (read)

- `GOAL-CONTRACT-001` (`goal.strategy/v1`): register C-1..C-14, `goal-canon/1` (S-2), fact references grammar only (C-12, O-4).
- `GOAL-TRIGGER-001` (`goal.strategy-trigger/v1`): register T-1..T-11, decisions D-1..D-13, closed outcome vocabulary, outbox then inbox semantics,
  Ed25519.
- **TradingTriggerInbox specification status:** a prior search (recorded in `GOAL-TRIGGER-001` Current state 1) found no written specification
  anywhere: zero hits for `TradingTriggerInbox`; `TriggerInbox` appears only in the backlog as the TRON-T4 title. Re-checked for this item in the TRON
  D1 branch (`wo/WO-TRON-D1`), TRON main (`5577039`), HELIOS main (`7f7193d`) and FALCON main (`8f218ec`): `git grep -i "inbox\|outbox"` finds no
  inbox or outbox design, only the `action_id` ingestion and dedupe steps below. Status: **CA statement only; the contract is a proposal pending
  D-12.**

### CP-1 existing implementations: HERMES Redis -> HELIOS input

HERMES (`maff0000/hermes` main `ca19017`):
1. **Published surface.** `docs/architecture/redis-consumer-integrity-boundary.md`: consumers read `hermes:*` read-only (read commands, subscribe, no
   mutation), writer is HERMES only. `docs/contracts/hermes_redis_contract_manifest.md` registers only tick contracts and states that
   `hermes:candle_*`, `hermes:indicators:*` are "separately designed ... (different WOs)". **No registered manifest entry or schema file exists for
   the candle or indicator keys HELIOS needs.**
2. **Candle contract** (`utils/candle_contract_v1.py`): envelope `schema_version "v1"`, `contract "hermes.candles.latest"`, `contract_version "v1"`;
   timestamps UTC with millisecond `Z`; OHLC are JSON numbers quantised from floats (`round(float(v), dp)`); closure flag is `is_closed`; extra fields
   (`body_*`, `wick_*`, `range_size`, `candle_direction`, coverage and gap fields); source in `provenance`. Keys: `latest` and a history family with a
   ZSET index (`hermes:candles:{instrument}:{timeframe}:history:v1:...`).
3. **Indicator contract** (`utils/hermes_indicators_v1.py`): key `hermes:indicators:{instrument}:{timeframe}:v1` (latest-only) plus a designed history
   family `...:history:v1:{open_epoch}` with ZSET index (`ops/work_orders/WO-HERMES-INDICATOR-HISTORY-CONTRACT-0001.md`); a larger indicator set than
   HELIOS knows (MACD, Bollinger, ADX, `ema_12`, `ema_26`); declared `methods` (RSI = Cutler SMA-14, ATR = SMA-14); `regime` and risk tokens are
   forbidden in the payload (ARES-owned).
4. **Readiness.** `docs/governance/PID-HERMES-MVP-001.md` records production indicator-history activation as outstanding; HELIOS evidence below shows D1 and H4 incomplete on PROD at 2026-09-05. Current PROD state: UNVERIFIED
   here; Lane A owns it.

HELIOS (`maff0000/HELIOS` main `7f7193d`):
5. **Input model.** `helios/contracts/market_fact.py` `MarketFactFrame` (one instrument, timeframe, bar-open instant) with `Candle` (7 fields incl.
   `complete`, `source`), `IndicatorSet` (8 optional fields: `rsi_14`, `ema_9/21/50/200`, `atr_14`, `regime`, `session`) and `Provenance` (`source`,
   `schema_version`, `observed_at_utc`, `ingested_at_utc`). Closed world: any unknown field is refused; binary floats are refused
   (`helios/contracts/_fields.py`); ordering strictly ascending; freshness from bar close; incomplete bar refused unless policy allows
   (`helios/integration/hermes_boundary.py`, `INPUT_REJECTION_RULES`).
6. **No Redis client was found in HELIOS `main` `7f7193d` (search: `git grep` and the import-ban test below), and none can be added to the pure engine:** `tests/test_execution_blind.py` bans importing `redis` and networking modules
   under `helios/`; `docs/INTEGRATION.md` section 2 says "data contract, not a client". Facts come from `fixtures/hermes/` (15 malformed fixtures, 2
   stale, valid XAU_USD set).
7. **Version-string inconsistency inside HELIOS:** `MARKET_FACT_SCHEMA_VERSION = "helios.market_fact/1.0.0"` is what `describe_input_contract()`
   advertises, while fixtures, config and tests use and accept `hermes.market_fact/1.0.0` (`helios/integration/exemplars.py`, `tests/test_config.py`).
8. **Prior integration attempt.** Branch `wo/WO-HELIOS-HERMES-PROD-INTEGRATION-PROOF-0001` (`84d3772`): recorded verdict (proof incomplete at the time); records
   the live schema_version `v1` versus `hermes.market_fact/1.0.0` mismatch and leaves open whether mapping is transport or semantic reinterpretation.
   Group E report item 7 lists "HELIOS to HERMES contract version reconciliation and Redis reader" as blocking HELIOS-T2. Bounded conclusion (CA/PO adjudication 2026-10-15): lane B's search (HELIOS, GOLD-STRATEGY-RUNTIME, falcon and TRADER trees, branches, `gh repo list`, units and timers, container labels, fabric key names, HERMES consumer docs, legacy archive manifests) found no completed integration in the searched locations; absence elsewhere is UNVERIFIED, and lane B re-runs and extends the search. Under CA guidance
   2026-10-15 (item 1) that reader and reconciliation sit in the HELIOS-side external adapter, outside the pure engine.

**Reconciliation findings for CP-1 (all to be turned into mapping rows with a fixture each):** HERMES `v1` versus HELIOS `<namespace>/<x.y.z>`; ms
versus microsecond instants; JSON number versus exact decimal text; `is_closed` versus `complete`; two Redis keys (candles, indicators) joined on
`(instrument, timeframe, open)` versus one frame; HERMES-only indicators versus a closed-world refusal; `regime`/`session` supplier (HERMES forbids
regime, ARES owns it); RSI/ATR method naming; `ingested_at_utc` has no HERMES source (reader supplies it); fixture D1 token handling (`D` legacy
versus `D1`); FALCON `hermes/market_fact.v1` is a third, evidence-side fact shape (`fact_id`, `series_id`, `value_decimal`), not an input.

### CP-2 existing implementations: HELIOS trigger -> outbox -> TRON inbox

1. **HELIOS has no trigger, signing or outbox code.** `grep -ril "outbox|ed25519|hmac|strategy_trigger"` over HELIOS main finds no source; its sinks
   are file, stream and memory only (`helios/publish/sink.py`: "no network sink, no state service"); it publishes `strategy_state` (JSON Lines, schema
   negotiation in `helios/publish/negotiation.py`), never a trigger.
2. **FALCON** (`8f218ec`; its registered trigger payload is an evidence shape, not a trigger contract, CA guidance 2026-10-15 item 2): registered payload `schemas/payloads/helios/strategy_trigger.v1.schema.json` (required: `trigger_id`,
   `semantic_fingerprint`, `parameter_set_id`, `direction` incl. `FLAT`, `action_type` incl. `EXIT/ADJUST`, `reference_price_decimal`,
   `signing_key_id`, `signature`; `additionalProperties:false`); signing doctrine `docs/security/FALCON-HELIOS-TRIGGER-SIGNING.md` ("Ed25519, subject
   to implementation proof", canonical form unspecified); event registry `registry/event_family_registry.v1.json`. No outbox code in FALCON (matches
   only mention failure replay and observability docs).
3. **TRON** (`wo/WO-TRON-D1`; a competing intake model under CA guidance 2026-10-15 item 2, to be reconciled to `GOAL-TRIGGER-001`, not a contract): intake is `falcon.trade_action.v1` keyed by `action_id` (required `contract_version, action_id, action, instrument,
   valid_until_ms, strategy_ref`); ingestion steps RECEIVED, VALIDATE, EXPIRE, DEDUPLICATE; terminals `REJECTED, EXPIRED, DUPLICATE, NEGOTIATED`;
   HR-08 (journal before submit) and HR-13 (idempotent on action identity) in `PID.md` and `docs/04-TRADE-LIFECYCLE.md`; time is epoch milliseconds;
   identifiers `^[A-Za-z0-9_.:-]+$`, 1-128 chars (`docs/05-CONTRACTS.md`). No inbox.
4. **Reconciliation findings for CP-2:** three different identity names (`trigger_id` free string in FALCON, `trg1_` deterministic in
   `GOAL-TRIGGER-001`, `action_id` in TRON) and fingerprint names (`semantic_fingerprint` versus `strategy_fingerprint`); `parameter_set_id` versus
   `binding_id`; `trigger_at_utc` versus the bar-close and validity fields; ms (TRON) versus fixed-width UTC strings; the `trg1_` id pattern fits the
   TRON identifier pattern and length (to be proven by fixture); TRON's closed terminal set has no `CONFLICT`, `SUPERSEDED` or `ABANDONED_UNRESOLVED`
   (TRON-T4 owns final names).

## Target outcome

At closure `maff0000/GOAL` holds, under one evidence directory and two contract-package directories, a reviewed reconciliation audit and two packages:
`CP-1` (HERMES Redis -> HELIOS input) and `CP-2` (HELIOS trigger -> outbox -> TRON inbox), each marked PROPOSED and each referencing, not restating,
the freeze owner of its normative text. A component architect can write a consumer or provider conformance test from a package alone and get the same
accept/reject verdict as the other side.

## Scope

Exactly CP-1 and CP-2. For each package:

1. **Explicit semver and compatibility:** package version `cp-1/0.1.0` and `cp-2/0.1.0`; wire schema versions as named by the owning contract
   (`goal.strategy-trigger/v1`; for CP-1 the HERMES `v1` contracts and the HELIOS fact version, with the mapping between them, see D-C3); additive
   versus breaking rules; a compatibility-matrix contribution (rows per provider version, consumer version, status COMPATIBLE / ADAPTER /
   INCOMPATIBLE).
2. **Field-level schema and mapping table:** every field on both sides, each row `MAPPED`, `DERIVED` (with rule) or `UNSUPPORTED` (with the
   fail-closed behaviour and error name); no empty cell, no `TBD`.
3. **Canonical form (CP-1: adapter duties):** CP-2 uses `goal-canon/1` (GOAL-CONTRACT-001, S-2) for ids, digest and signature; CP-1 states the canonical decimal and instant
   forms the external adapter must emit to HELIOS (exact decimal text; fixed-width UTC microsecond `Z`), and the adapter's duty to derive `ingested_at_utc`.
4. **Golden fixtures:** valid and invalid, each invalid naming its expected rejection code; CP-1 reuses the 15 HELIOS malformed cases and adds
   HERMES-shaped cases (float number, `v1` schema string, millisecond instant, unknown indicator, regime present, `is_closed` false, stale latest, gap
   in history, missing indicator key, duplicate frame); CP-2 includes valid trigger and invalidation, tampered, unsigned, unknown key, expired, future
   `valid_from`, over-long window, id collision with different digest, forbidden key (stop-loss etc.).
5. **Rejection behaviour:** a rejection matrix per boundary (code, side that rejects, effect: refuse frame / block entry / quarantine / alert);
   consumer never repairs, defaults or re-sorts.
6. **Failure and recovery semantics:** CP-2: duplicate delivery, replay of an occurrence key, expired trigger, clock skew, publisher outbox crash and
   restart, inbox down, partial publication (outbox written, delivery or receipt lost), poison message (repeatedly rejected entry: bounded retry,
   quarantine, no head-of-line block), FALCON sink down (no effect on dispositions). CP-1: Redis unavailable, key absent, latest older than history,
   reader restart (re-read, no replay of an already-evaluated bar), out-of-order or duplicate bars, history gap, incomplete bar, schema bump. Each as
   a scenario with the required observable outcome.
7. **Consumer and provider conformance test obligations:** per package, the list of tests each side must pass, written so they can run offline from
   fixtures (provider: emits only valid fixtures and never an invalid one; consumer: accepts valid, rejects invalid with the stated code).
8. **Reconciliation audit** of C-1..C-14 and T-1..T-11 against current commits (CONFIRMED / CHANGED / NEW), with new rows offered to the owning PIDs
   as proposals.

## Non-goals

- No change to HERMES, HELIOS, FALCON, TRON, HSA, DARWIN or CER. No Redis client, signer, outbox, inbox or reader is written, including in test
  tooling beyond in-repo reference models used only by tests.
- No new transport: `TradingTriggerInbox` is the authoritative trigger transport (CA); FALCON is an asynchronous, non-blocking evidence consumer and
  never on a decision path (CA guidance 2026-10-15, item 3); Graylog is never a transport.
- No competing trigger contract (CA guidance 2026-10-15, item 2): CP-2 introduces no envelope, id, signing, outbox or inbox rule of its own;
  `GOAL-TRIGGER-001` owns them, and HELIOS, TRON and FALCON hold none.
- No specification or build of the external adapter (CA guidance 2026-10-15, item 1): CP-1 is the interface the adapter conforms to.
- No freeze of `goal.strategy/v1` or `goal.strategy-trigger/v1` (their PIDs own that); no restatement of D-xx decisions; no key material; no fact
  names (HERMES-FACT-001 owns names and payloads).
- No edit to `backlog/backlog.yaml`, `MANIFEST.md`, tools or workflows; no `pid_path`; no approvals.

## Dependencies and interfaces

- **Hard backlog dependency:** `GOAL-DCP-001` (CLOSED) only.
- **Ordering (programme-controller ruling 5; no hard cycle).** C's inputs are A and B (CP-1 reality), D's TRON intake facts (soft) and E's FALCON registry
  facts (soft). C reads a soft input only after that lane's facts are committed; otherwise C records an assumption and flags UNVERIFIED. D does not depend
  on C (D uses its own assumption register until `GOAL-TRIGGER-001` exists). No lane waits on C except `GOLD-MVP-001`, which consumes C's matrix rows.
- **Lane A** (HERMES surface reality): the live key inventory and PROD readiness are inputs to CP-1; this item cites Lane A evidence when merged and
  flags UNVERIFIED where it is not.
- **Lane B** (existing HELIOS adapter and the legacy integration): input to the CP-1 external-adapter rows (the adapter sits outside the pure engine, CA guidance
  2026-10-15 item 1) and whether a prior reader exists. No dependency on Lane B timing; a missing Lane B result leaves the CP-1 adapter row UNVERIFIED.
- **Lane D** (TRON inbox facts, SOFT): input to CP-2 inbox rows and terminal-state mapping; TRON-T4 owns final names. Read after D's facts are committed;
  otherwise record the assumption.
- **Lane E** (FALCON registry facts, SOFT): input to the CP-2 evidence-event rows (registered `helios.strategy_trigger` and `tron.*` shapes); read after E's
  facts are committed; otherwise record the assumption.
- **GOAL-CONTRACT-001 draft-freeze** is required before any CP freeze that uses `goal-canon/1` or the strategy identity triple; CP drafting may
  proceed against its DRAFT.
- **GOAL-TRIGGER-001:** CP-2 draft-freeze requires its DRAFT-FREEZE; D-12 (authority of the trigger contract) must be decided first, otherwise CP-2 is
  a proposal against no authority.
- **HERMES-FACT-001:** no PID exists; CP-1 supplies a reconciliation input and a proposed grammar-compatible mapping, never fact names. Under CA guidance
  2026-10-15 (item 1) HERMES publishes against a `HERMES-FACT-001`-style contract of what it publishes; CP-1 is the interface GOAL approves between that
  publication and the HELIOS-side external adapter.
- **Rule:** component architects (HERMES, HELIOS, TRON, FALCON) may propose changes to a package through a PR or comment; only GOAL (CA/PO) freezes. A
  package version is frozen only when every provider and consumer row is COMPATIBLE or ADAPTER with a named owner; no incompatible pair may be frozen
  by either side.

## Interaction with GOAL-CONTRACT-001 and GOAL-TRIGGER-001 (no competing freezes)

1. This item freezes nothing. Packages carry status PROPOSED; their normative text is by reference.
2. CP-2 normative authority is `GOAL-TRIGGER-001` (and, through it, `GOAL-CONTRACT-001`). CP-2 freezes with, never before, the trigger contract's
   freeze, and any disagreement is raised as a change request to that PID, not resolved in CP-2.
3. CP-1 is the interface that GOAL approves (CA guidance 2026-10-15, item 1). HERMES owns what is published and the external adapter owns consumption and
   translation, so neither side freezes it alone. The mechanics of the freeze (which PID carries it) remain D-C1. Until then CP-1 is a DRAFT with no frozen field.
4. New contradictions are offered to the owning PID as register-row proposals; this item keeps its own ids `AC-n` and never edits those PIDs. If a PID
   changes, affected rows are re-based.
5. A matrix row cannot read COMPATIBLE unless both sides' fixtures pass.

## Safety boundaries

- Public repository: fixtures carry no credentials, tokens, hostnames, addresses, accounts, broker symbols or real private keys; canonical instrument
  ids only; signatures use ephemeral or published test public keys.
- Read-only on all systems except the item's own worktree; no production mutation; no broker or DEMO contact; no live Redis write; any live read is by
  an authorised read-only consumer identity and limited to key names and non-secret sample envelopes (Lane A).
- Fixtures are illustrative, non-production, with no stop-loss, take-profit, quantity, order, account or `confidence` field and no trading advice.
- `./tools/secret-scan` stays CLEAN; `./tools/goal-validate` stays OK.

## Deliverables

Paths proposed for the evidence PR (fixed in the first PL step); all inside `maff0000/GOAL` (evidence under `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-C/`, packages under `contracts/packages/`):

1. `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-C/RECONCILIATION.md`: base SHAs, commands, findings AC-n, status of C-1..C-14 and T-1..T-11, TradingTriggerInbox
   specification status.
2. `contracts/packages/cp-1-hermes-helios-input/` and `contracts/packages/cp-2-trigger-outbox-inbox/`, each: `PACKAGE.md` (versioning, mapping tables,
   canonical form, rejection matrix, failure/recovery scenarios, conformance obligations), `schema/`, `fixtures/valid/`, `fixtures/invalid/` (each
   file names rule and code), `conformance/PROVIDER-TESTS.md`, `conformance/CONSUMER-TESTS.md`.
3. Matrix rows for CP-1 and CP-2, prepared in each package and contributed into `audits/2026-10-15/gold-mvp/COMPATIBILITY-MATRIX.md` by a separate GOAL PR after this lane's evidence PR is accepted (one lane per PR; `GOLD-MVP-001` owns the file and its single writer is the `GOLD-MVP-001` PL; there is no second matrix).
4. Offline deterministic tests under `tests/` validating fixtures against schemas with two independent validators (schema validator and a hand-written
   second checker).
5. One primary evidence PR to `maff0000/GOAL` (branch `wo/GOLD-AUD-C-evidence`) mapped to CA's ten evidence items using the checklist below.

### Evidence PR checklist (CA's ten mandatory evidence items, CA numbering)

CA's ten mandatory evidence items, in CA's numbering (the numbering is CA's and is not to be changed by a lane): (1) PID/WO identifier and exact audited scope; (2) source repositories, revisions and relevant documentation references; (3) existing implementation: proven, partially proven, unverified or missing; (4) actual versus expected contract comparison; (5) tests, fixtures and evidence references; (6) specific defects and compatibility gaps; (7) reusable code and documentation; (8) minimum recommended implementation changes; (9) safety and deployment constraints; (10) independent audit verdict and any unresolved findings.

| CA # | CA evidence item | This audit puts it in | Proof method |
|---|---|---|---|
| 1 | PID/WO identifier and exact audited scope | Evidence PR header: quoted scope (exactly CP-1 and CP-2) and the Interaction statement (no competing freeze) | Quote equals approved PID |
| 2 | Source repositories, revisions and documentation references | `RECONCILIATION.md`: base SHAs of every cited repository and branch (working trees unmodified), documentation references | Script lists every cited file and commit and re-reads it at the recorded SHA |
| 3 | Existing implementation: proven, partially proven, unverified or missing | `RECONCILIATION.md`: HERMES published-surface inventory, HELIOS input contract and rejection rules, trigger / signing / outbox search results (negative results with scope and commands), TRON intake assumptions and terminal states, FALCON registry and trigger-schema delta, TradingTriggerInbox specification status; each classified proven / partially proven / unverified / missing | Negative results state scope and commands |
| 4 | Actual versus expected contract comparison | Mapping tables (no empty cell, no `TBD`) and the re-test of C-1..C-14 and T-1..T-11 as CONFIRMED / CHANGED / NEW | Two independent validators agree; every C and T row covered |
| 5 | Tests, fixtures and evidence references | CP-1 and CP-2 packages: golden valid and invalid fixtures with declared rejection codes, rejection matrices, failure and recovery scenarios, offline tests | `python3 -m pytest tests/ -q` exits 0; no fixture has an undeclared code |
| 6 | Specific defects and compatibility gaps | Findings AC-n and the compatibility-matrix rows to contribute (rows per provider / consumer version, status COMPATIBLE / ADAPTER / INCOMPATIBLE) | No row reads COMPATIBLE where a fixture fails |
| 7 | Reusable code and documentation | Reusable fixtures (the 15 HELIOS malformed cases), schemas and the reference-model tooling used only by tests | Each reuse entry cites path and revision |
| 8 | Minimum recommended implementation changes | Conformance test obligations per side and register-row proposals offered to the owning PIDs (never edited here) | Each NEW finding offered to its owning PID |
| 9 | Safety and deployment constraints | Safety section: public-repo sanitisation (no credentials, hosts, accounts, broker symbols, real keys), no runtime contact, forbidden-content test, open-decision list | `./tools/secret-scan` CLEAN; forbidden-content test passes |
| 10 | Independent audit verdict and unresolved findings | Independent auditor (AUD-2) verdict file plus `goal-validate`, `secret-scan` and test output | Fresh auditor GREEN with exact SHAs; PO acceptance recorded |

## Acceptance

Mechanical; each states its proof method.

A-1. Every valid fixture passes and every invalid fixture fails with its declared code: `python3 -m pytest tests/ -q` exits 0.
A-2. Each fixture set validates under two independent implementations (JSON Schema validator and a second, hand-written checker written from
     `PACKAGE.md` alone); verdicts and codes byte-identical; diff recorded.
A-3. Rejection matrix completeness: every `INPUT_REJECTION_RULES` entry of HELIOS and every CP-2 outcome has at least one invalid fixture, and no
     fixture has an undeclared code (script check).
A-4. Failure scenarios: every scenario in Scope item 6 has a fixture sequence and an expected outcome table; a reference model run (tests only)
     reproduces it, including crash-between-outbox-and-receipt without double execution, and logically equivalent dispositions (same trigger dispositions and terminal states; FALCON-side counters and timestamps excluded) with the FALCON sink disabled.
A-5. Mapping tables contain no empty cell and no `TBD`; each `UNSUPPORTED` row names fail-closed behaviour and error name; every cited source file and
     commit is re-read at the recorded SHA (script lists them).
A-6. Forbidden-content test: none of stop-loss, take-profit, quantity, order, account, broker symbol, `confidence`, host or address in packages and
     fixtures.
A-7. Compatibility matrix rows (prepared in the packages, contributed to `COMPATIBILITY-MATRIX.md` after acceptance) exist for every provider/consumer version pair; none reads COMPATIBLE where a fixture fails; no package is marked
     FROZEN.
A-8. Reconciliation covers every C and T row and offers each NEW finding to its owning PID; `./tools/goal-validate` prints OK; `./tools/secret-scan` CLEAN (tree and history); no existing test fails.
A-9. Independent FORGE Auditor GREEN with exact SHAs; PO acceptance recorded per the state machine.

### Disposition table

**Disposition table (REQUIRED; CA/PO legacy application doctrine 2026-10-15).** The evidence PR contains `DISPOSITION.md` (format: `PORTFOLIO.md` section 7.4): one row per reusable component in scope — existing contract and fixture assets (the 15 HELIOS malformed cases, FALCON's registered trigger payload and signing doctrine, TRON D1's intake schemas, the HERMES candle and indicator contract modules), each with its generation — each with generation (legacy / newer canonical / currently deployed), the criteria assessed (architecture fit, code quality, determinism, test evidence, maintainability, contracts, operational dependencies, integration cost), a verdict REUSE | REFACTOR | REPLACE | RETIRE, evidence, and the approximate comparative engineering cost of reuse versus refactor versus a clean build. A verdict is a recommendation only: nothing is retired, shut down or mutated, and the lane cannot be accepted without this table (it is part of CA evidence items 7 and 8).

## Stop conditions

Stop and return to the PO if:
- a package would need to restate or alter a normative rule of `GOAL-CONTRACT-001` or `GOAL-TRIGGER-001` (raise a change request instead);
- CA does not confirm D-12 (authority of the trigger contract) and the item would otherwise freeze a transport;
- reconciliation shows two components cannot be made compatible without changing one model (that is CA/PO);
- a fixture or sample would need a secret, address, account identifier or production payload;
- live HERMES inspection is needed beyond key names and a non-secret sample, or any write path would be required;
- the two independent validators disagree and the text cannot settle which is right.

## Open decisions

Owner PO unless stated; none needs Matt from this item. D-xx and C/S/O/T decisions are by reference to the two PIDs and are NOT restated here.

- **D-C1 (RESOLVED by CA/PO adjudication 2026-10-15): who owns the CP-1 freeze mechanics.** `HERMES-FACT-001` owns HERMES publication semantics; GOAL approves the CP-1 interface using the A/B/C reconciliation. Earlier text, kept: **who owns the CP-1 freeze mechanics.** Narrowed by CA guidance 2026-10-15 (item 1): GOAL approves the CP-1 interface,
  HERMES owns publication, the HELIOS-side external adapter owns consumption and translation. Still open: which PID carries the freeze and the
  `HERMES-FACT-001`-style publication contract. Options: a `HERMES-FACT-001` PID; a small GOAL item for the interface; or a section of
  `GOAL-CONTRACT-001` (rejected here: its Non-goals exclude fact payloads). Recommendation: `HERMES-FACT-001` PID for the publication contract, with this
  package as its input and GOAL approval of the CP-1 interface.
- **D-C2 (PO; blocks approval): form.** (ii) thin item (recommended) versus (i) amendment of both PIDs.
- **D-C3 (re-assigned by CA guidance 2026-10-15, item 1; blocks CP-1 freeze, not approval): the `v1` to HELIOS fact-schema mapping belongs to the
  HELIOS-side external adapter**, with GOAL approving the interface and a `HERMES-FACT-001`-style contract of what HERMES publishes. What stays open is the
  fix of the HELIOS version-string inconsistency (advertised `helios.market_fact/1.0.0`; fixtures, config and tests also accept `hermes.market_fact/1.0.0`),
  which is a HELIOS-side change (DR-27). Related: GOAL-CONTRACT-001 C-12/O-4; Group E item 7.
- **D-C4 (RESOLVED by CA guidance 2026-10-15, item 1): reader placement.** The reader is a HELIOS-side external adapter outside the pure engine (which keeps its
  `redis` and network import ban). Still open and new: whether that adapter lives in the HELIOS repository or a separate one, and who authors its PID
  (DR-34, DR-35: both RESOLVED by CA/PO adjudication 2026-10-15: the adapter lives in the HELIOS repository outside the pure engine; `HELIOS-T2` owns the implementation; the HELIOS architect authors the bounded work orders).
- **D-C5 (PO; later): numeric form on the Redis wire** (HERMES number versus decimal text); recommendation: the external adapter converts via the contract's
  exact-decimal rule with a stated quantisation.
- **Dependencies on existing decisions (by reference):** D-12, D-1, D-2, D-3 (Matt), D-4, D-5, D-6, D-8 of `GOAL-TRIGGER-001`; S-1, S-2, O-2, O-4 of
  `GOAL-CONTRACT-001`. CP-2 cannot freeze while any blocker among them is open; CP-1 cannot freeze while C-12 is open.

## Evidence

- GOAL base `1739e742154c77e9e2a96927dc40d4978b9cd798` (historical read base; baseline now `90323b3`; main; PID draft branch `wo/GOAL-GOLD-AUD-C` created from it; the evidence branch is `wo/GOLD-AUD-C-evidence`).
- `wo/GOAL-CONTRACT-TRIGGER` `64c843b`: `pids/GOAL-CONTRACT-001.md`, `pids/GOAL-TRIGGER-001.md`, `decisions/ADR-CONTRACT-001-STRATEGY-SEMANTICS.md`.
- HERMES main `ca19017`: `docs/contracts/hermes_redis_contract_manifest.md`, `docs/architecture/redis-consumer-integrity-boundary.md`,
  `docs/governance/PID-HERMES-MVP-001.md`, `utils/candle_contract_v1.py`, `utils/hermes_indicators_v1.py`,
  `ops/work_orders/WO-HERMES-INDICATOR-HISTORY-CONTRACT-0001.md`.
- HELIOS main `7f7193d`: `helios/contracts/{market_fact,_fields}.py`, `helios/integration/hermes_boundary.py`, `helios/publish/{sink,negotiation}.py`,
  `docs/INTEGRATION.md` section 2, `fixtures/hermes/`, `tests/test_execution_blind.py`; branch `wo/WO-HELIOS-HERMES-PROD-INTEGRATION-PROOF-0001`
  `84d3772`.
- FALCON main `8f218ec`: `schemas/payloads/helios/strategy_trigger.v1.schema.json`, `docs/security/FALCON-HELIOS-TRIGGER-SIGNING.md`,
  `registry/event_family_registry.v1.json`.
- TRON main `5577039`, branch `wo/WO-TRON-D1`: `PID.md`, `docs/04-TRADE-LIFECYCLE.md`, `docs/05-CONTRACTS.md`.
- Reports: RECON-F, RECON-H1, RECON-H2, Wave 1 Groups B and E (`wo/GOAL-*` branches).
- Lane A, B, D branches held no commits beyond main at drafting; nothing relies on them. Not read: live HERMES PROD, TRON runtime, private repos.

## Approval

PENDING. No approval has been recorded for this PID candidate. Approval is recorded here by Central Architecture/PO only.

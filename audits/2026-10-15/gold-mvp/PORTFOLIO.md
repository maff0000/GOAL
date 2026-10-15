# GOLD MVP portfolio for approval

**Work order:** `GOAL-GOLD-MVP`. **Baseline:** GOAL `main` @ `1739e742154c77e9e2a96927dc40d4978b9cd798`. **Date:** 2026-10-15.
**Author role:** architecture author for the cross-lane structure, working for ROGUE under Central Architecture (CA).
**Nature:** a proposal for approval. It records no approval, sets no `pid_path`, moves nothing to `DELIVERY_READY`, edits no backlog, and dispatches nothing. The backlog patch in section 11 is specified, not applied.
**Companion:** `pids/GOLD-MVP-001.md` (integration and acceptance PID candidate) and the six audit PID candidates `pids/GOLD-AUD-A.md` to `pids/GOLD-AUD-F.md`. `audits/2026-10-15/gold-mvp/DECISION-REGISTER.md` consolidates every open decision (it supersedes the PD list in section 12, whose ids it keeps).
**Revision note (consolidation):** this document was first drafted before the lane PIDs existed. The consolidation edit has read all six lane PIDs and reconciled the amend-versus-new answers, the evidence numbering, the lane findings (section 3a), the backlog patch and the decisions to what the lane drafters concluded. Where the lane PIDs contradict each other or this document, the contradiction is recorded in the consolidation report and the decision register, not resolved silently.

## 1. Objective and frame

Objective (CA directive): a verified reusable integration foundation for ONE XAUUSD strategy, Vantage DEMO execution, FALCON evidence and subsequent NEO review.

Critical path: HERMES PROD XAUUSD Redis → HELIOS one governed strategy → signed durable trigger outbox → TRON inbox + risk gates → MT5 gateway / Vantage DEMO → FALCON evidence; then NEO → CER → HSA/DARWIN → approved HELIOS version.

Not prerequisites: additional HERMES feeds, broad research-platform expansion, new third-party services. No live capital execution.

Operating model: one ROGUE, many parallel FORGE workers, up to six concurrent workstreams, each worker in its own worktree, each with an independent auditor; no two workers write the same authoritative source, contract, shared database or running service. PID first: amend existing PIDs or add bounded audit increments rather than duplicate.

How "amend versus new" was applied. Every audit is tracked as its own backlog item, because a read-only audit must be dispatchable before the existing component PIDs are approved and must carry its own independent auditor and acceptance. Two forms were offered to the lane drafters:

- **(i) amendment:** the existing PID already covers the scope. The audit item is a declared increment of that PID: the audit PID states `Amends: <ID>`, the existing PID's next revision lists the audit as a named deliverable, and audit closure satisfies that deliverable. The audit PID restates no scope the existing PID owns.
- **(ii) new bounded audit item:** no existing PID covers the scope, or the existing PID is engineering while this is research. The audit PID states `Complements: <IDs>` and the existing PIDs are not edited.

**Outcome after the lane drafters read the existing PIDs: all six lanes concluded (ii).** Each is a new bounded read-only audit item with a documented amendment fallback (section 3). The original draft expected (i) for A, C and E; that expectation is withdrawn.

## 2. The portfolio

Seven items: one integration PID and six read-only audit items. All audits: backlog lane `research` (read-only work; provisional, PO sets final), `depends_on: [GOAL-DCP-001]` only, `po_gate: true`, proposed state `PID_DRAFT`, proposed priority P0 (lane PIDs E and F state P1; see DECISION-REGISTER DR-13). The `amend vs new` column states what each lane drafter concluded after reading the existing PIDs.

| id | lane (area) | scope sentence | amend vs new (existing PID) | evidence PR goes to | read-only permissions (section 6) | gate | collisions (section 5) | independent auditor |
|---|---|---|---|---|---|---|---|---|
| `GOLD-MVP-001` | trading (integration) | Own the cross-component integration architecture, evidence index, contract compatibility matrix and the single end-to-end Vantage DEMO acceptance of one governed XAUUSD strategy with FALCON evidence; no component implementation. | new (overlaps `PAPER-E2E-001`, decision PD-1) | `maff0000/GOAL` | none beyond reading audit outputs until the acceptance run, which has its own approvals | PO + Matt (proposed) | reads outputs of all six audits; writes only `audits/2026-10-15/gold-mvp/` in GOAL | AUD-3 plus CA acceptance |
| `GOLD-AUD-A` | research (area A HERMES) | Audit the existing PROD XAUUSD Redis publication: keys, schemas, indicator coverage, timeframes, freshness, timestamps, warm-up, validation and status, and compare it with the documented Redis contracts, without mutating production. | **(ii) new bounded item**: a strict subset ("Increment A") of `HERMES-CUR-001` scope item 1 (Redis key inventory), complements `HERMES-CUR-001`; the lane PID carries proposed amendment text for CUR-001 (not applied); fallback: fold in as CUR-001 Increment A unchanged. `HERMES-FACT-001` is the downstream consumer | `maff0000/hermes` | repo read; PROD Redis non-blocking read protocol (section 6.2); container labels only | PO + **Matt (production read access; decision PD-5)** | the only audit that touches PROD Redis; HERMES repo shared read with B and E | AUD-1 |
| `GOLD-AUD-B` | research (area B HELIOS) | Locate the previously completed HERMES Redis to HELIOS GOLD integration (external adapter, deployment wiring, legacy), reconcile it with the new HELIOS runtime and the MarketFactFrame, recommend minimum reuse or adaptation, and review HSA strategy packages for a compatible first GOLD strategy. | **(ii) new**: a pre-increment of `HELIOS-T2` (the live-transport owner), complements `HELIOS-T1` and `GOLD-STRATEGY-RUNTIME`; no second market-data reader may be built or prototyped by the audit. The lane PID states no explicit fallback; the implied one is to fold it into the HELIOS-T2 PID as a named pre-deliverable (DR-14) | `maff0000/HELIOS` | repos read (HELIOS, GOLD-STRATEGY-RUNTIME, HSA, legacy HELIOS lineage); no PROD Redis (uses A's output and fixtures) | PO | shares HSA read with F; HELIOS repo single evidence writer | AUD-2 |
| `GOLD-AUD-C` | research (area C shared contracts) | Reconcile `GOAL-CONTRACT-001` and `GOAL-TRIGGER-001` with existing implementations and produce governed consumer/provider contracts for HERMES Redis to HELIOS input and for HELIOS signed trigger to durable outbox to TRON inbox: versioning, golden fixtures, rejection behaviour, recovery. | **(ii) new thin item**: CP-1 (HERMES Redis to HELIOS input) has no home in either PID or in `HERMES-FACT-001` (no PID); `GOAL-CONTRACT-001` / `GOAL-TRIGGER-001` remain the approval owners of the normative text and their blockers (D-3 Matt gate); `GOLD-AUD-C` freezes nothing (packages are PROPOSED); fallback: amendment of both PIDs (decision D-C2); CP-1 freeze owner is D-C1 | `maff0000/GOAL` | repos read (GOAL branches, HELIOS, HERMES, TRON D1 branch, FALCON contracts); no runtime | PO (contracts carry Matt gate in `GOAL-TRIGGER-001` itself) | single owner of the compatibility matrix and the GOAL evidence index; reads outputs of A, B, D, E | AUD-2 |
| `GOLD-AUD-D` | research (area D TRON / MT5) | Audit the TRON D1 design and implementation candidates, risk rules, journal and trigger-intake assumptions; coordinate with `MT5-GW-001`; identify the smallest missing capabilities for one DEMO execution path. | **(ii) new thin item**: composes `TRON-D1-RATIFY` and the merged / open MT5 work (`MT5-GW-001`, PR #9, readiness, DEMO-verify) into one six-hop gap matrix without redoing them; fallback: the same deliverables become an appendix to the ratification package plus a stub item (PD-3) | `maff0000/GOAL` (audit record) with mirror PRs in `maff0000/tron` and `maff0000/mt5-gateway` (lane PID position; the first draft of this table named `tron` primary: DR-15) | repos read (TRON incl. unmerged D1 branch, MT5 gateway, instance template records); docker labels only; **no broker call** | PO | two repos; MT5 instances never touched; TRON D1 branch is `TRON-D1-RATIFY`'s subject | AUD-3 |
| `GOLD-AUD-E` | research (area E FALCON) | Audit the delivered FALCON registry and running ingestion and define the minimum remaining HELIOS and TRON event publication, keeping FALCON outside the executable trigger path. | **(ii) new thin item**: a carve-out from `FALCON-T1` (T1 excludes exactly the `strategy_trigger` and `tron.*` families this audit must cover; T1 writes registry files, E is read-only); composes RECON-F's FALCON-T2/T3; fallback: append the deliverables to FALCON-T1 as a verification increment (cost: reverses T1's carve-out, mixes risk postures) | `maff0000/falcon` | repo read; FALCON running ingestion read via its own query interface (read-only); no write to the registry | PO | reads FALCON runtime; reads A/D outputs for event-source facts | AUD-1 |
| `GOLD-AUD-F` | research (area F CER / HSA / DARWIN / NEO) | Define how one GOLD strategy is qualified, registered, executed and reviewed (strategy versioning, evidence storage, causal testing, promotion, NEO review architecture) without rebuilding delivered functions, including earlier external repository/SaaS evaluations and reuse recommendations only where they materially reduce MVP engineering. | **(ii) new thin item**: complements `CER-R1`, `NEO-R1`, `HSA-C1`, `DARWIN-R2` (none amended; Deliverable 8 holds ready-to-apply amendment text; fallback: apply it and cancel the item after one audit PR) | `maff0000/GOAL` (audit record, cross-index) with evidence PRs in `maff0000/CER`, `HSA`, `DARWIN` and (PO-approved, private) `neo` (lane PID position; the first draft named CER primary with companion notes: DR-15) | repos read (CER, HSA, DARWIN, neo, earlier evaluation records); no runtime | PO | four repos read; shares HSA read with B | AUD-3 |

Notes on the table.

- Branch naming in the evidence repository: `wo/GOLD-AUD-<L>-<slug>`. The lane drafters' PID-authoring branches in GOAL already exist as `wo/GOAL-GOLD-AUD-<L>`; those carry PID text only, not evidence.
- Gate columns are proposals for the backlog. `matt_gate` is false except `GOLD-MVP-001` (risk `capital`, PAPER rule) and `GOLD-AUD-A`, whose Matt gate is **true pending the production-access decision** (PD-5 / lane A decision D1): if Matt waives it in one line before the patch is applied, flip it to false; otherwise it stays true.
- Auditor identities are roles AUD-1, AUD-2, AUD-3 (section 9.1), not named individuals; ROGUE binds them at dispatch.

## 3. Amend versus new, as concluded by the lane drafters

All six lane drafters read the existing PIDs and concluded **(ii) new bounded audit item**. The per-lane reasoning and the fallback route (kept documented so the PO can still choose an amendment) are:

| lane | conclusion | existing PID relationship | why not an amendment | fallback route if PO prefers the other answer |
|---|---|---|---|---|
| A | new bounded item: strict subset ("Increment A") of `HERMES-CUR-001` scope item 1 | complements `HERMES-CUR-001` | CUR-001 is DEV+PROD, SQL+Redis, git graph, image identity; its open decisions (snapshot timing, who probes, HMT-2) would hold the audit hostage; A is narrower and deeper (XAU_USD publication, fixtures); CUR-001 blocks `HERMES-FACT-001` | proposed CUR-001 amendment text is in the lane PID (not applied); or fold A into CUR-001 as Increment A unchanged |
| B | new: pre-increment of `HELIOS-T2` | complements `HELIOS-T1`, `HELIOS-T2`, `GOLD-STRATEGY-RUNTIME` | `HELIOS-T1` is a refactor to a contract not yet frozen; live transport belongs to T2; an audit would couple to an unfrozen contract | not stated in the lane PID; implied: name it a pre-deliverable of the `HELIOS-T2` PID |
| C | new thin item | complements `GOAL-CONTRACT-001`, `GOAL-TRIGGER-001` (remain approval owners) | CP-1 has no home (CONTRACT-001 excludes fact payloads; `HERMES-FACT-001` has no PID); TRIGGER-001 is High risk, Matt-gated, with its own blockers; both PIDs are about 360 lines; `GOLD-AUD-C` freezes nothing | amendment of both PIDs (lane decision D-C2); CP-1 freeze owner is D-C1 |
| D | new thin item | composes `TRON-D1-RATIFY`, `MT5-GW-001` and existing MT5 records | `TRON-D1-RATIFY` is a Matt-facing decision package for one artefact; folding in would put a programme audit behind a Matt decision | the same deliverables as one appendix to the ratification package plus a stub item; matrix and increment list are written to be transplantable |
| E | new thin item | complements `FALCON-T1` (carve-out) and RECON-F's FALCON-T2/T3 | T1 explicitly excludes the `strategy_trigger` and `tron.*` families E must cover; T1 writes, E is read-only; E needs running-ingestion checks | append deliverables to `FALCON-T1` as a verification increment (reverses the carve-out, mixes risk postures) |
| F | new thin item | complements `CER-R1`, `NEO-R1`, `HSA-C1`, `DARWIN-R2` | those rows are build-shaped, single-repository and partly mis-described or undefined (RECON-G, RECON-H1); amending four PIDs at once is four competing writes | Deliverable 8 holds the ready-to-apply amendment text; apply it and cancel the item after one audit PR |

The first draft of this section expected (i) for A, C and E (amendment with an `Amends:` line). That is withdrawn: the lane PIDs state `Complements:` lines, and no existing PID is edited by any audit.

## 3a. Lane findings that change the plan

Each lane PID recorded discoveries during drafting (all read-only; marked in the PIDs as proven, partial or UNVERIFIED). They change the plan as follows. Cited PID in brackets.

- **A, HERMES publication** (`pids/GOLD-AUD-A.md`). The documented tick contracts are the only registered contracts in the HERMES manifest and are marked "designed, publisher not built"; the candle, indicator, feed-health and catalog key families exist only in Memory Fabric (no repository document registers them), and the two fabric sources disagree on key counts by about 250 times (about 1,107 versus about 284,000), so which instance is "PROD" is itself open. Plan effect: A's job is to establish what is actually published and make the first repository record of it; `HERMES-FACT-001` cannot be written against documents that do not exist.
- **B, HELIOS reader** (`pids/GOLD-AUD-B.md`). No completed HERMES Redis to new-HELIOS integration was found: HELIOS has no Redis client (and the pure engine bans one); `GOLD-STRATEGY-RUNTIME` is wiring only (its own delta record says HELIOS has no live HERMES transport); the deployed GOLD stack is fixture-fed; branch `WO-HELIOS-HERMES-PROD-INTEGRATION-PROOF-0001` ended `WAITING_FOR_HERMES_BACKFILL` with no code; legacy HELIOS and the trading-host bridge read databases, not Redis. HSA's first-GOLD candidate `gold_context_breakout` 1.0.0 needs simple moving averages while HELIOS facts carry EMAs (SMA versus EMA naming), and HSA says `XAUUSD` where HERMES and HELIOS say `XAU_USD`. Plan effect: **the HERMES to HELIOS reader is a BUILD item inside `HELIOS-T2` scope**, not an adaptation; the B audit's output is the reuse inventory, gap list and minimum adaptation plan that scope that build, and a claim of "not found" carries a recorded negative-search method.
- **C, contracts** (`pids/GOLD-AUD-C.md`). The TradingTriggerInbox specification exists nowhere (re-checked in TRON D1, TRON main, HELIOS main, FALCON main). CP-1 mismatches to reconcile: HERMES `schema_version` `v1` versus HELIOS `<namespace>/<x.y.z>` (and HELIOS itself uses `helios.market_fact/1.0.0` in one place and `hermes.market_fact/1.0.0` in fixtures and tests), millisecond versus microsecond timestamps, JSON float versus exact decimal, `is_closed` versus `complete`, two Redis keys (candles, indicators) versus one frame, indicator sets (HERMES publishes more, HELIOS refuses unknown), `regime` (HERMES forbids it, ARES owns it, HELIOS wants it), RSI method naming (HERMES documents Cutler SMA-14; the HELIOS method, Wilder per the portfolio brief, is not stated in any lane PID), and `ingested_at_utc` having no HERMES source. CP-2 mismatches: three identity names (`trigger_id` free string in FALCON, deterministic `trg1_` in `GOAL-TRIGGER-001`, `action_id` in TRON), fingerprint and parameter-set naming, millisecond versus UTC strings, and TRON's closed terminal set lacking the outcomes the trigger contract names. HELIOS has no trigger, signing or outbox code. Plan effect: the compatibility matrix cannot be filled from documents; both boundaries need adapters or renames before `HELIOS-T3` and `TRON-T4` can be proven together.
- **D, TRON / MT5** (`pids/GOLD-AUD-D.md`). TRON has no runtime code on `main`; the D1 branch is 20 commits of documents, schemas and one docs test (148 tests prove consistency, not execution), with no PR; D1 has no exposure, position-count, order-size, loss or risk-lock checks and its kill-switch check has no setter; the typed MT5 gateway is not built (raw RPyC bridge only); PR #9 (instance template) is open. Plan effect: a TRON runtime, its risk gates and the typed gateway are builds; D's gap matrix sizes them to the one-order path.
- **E, FALCON** (`pids/GOLD-AUD-E.md`). FALCON is delivered (28 registered families; ingestion containers running), but only HERMES and ARES market-status events are actually emitted; HELIOS publication is synchronous and blocking (a sink failure exits the process); TRON has no claim/disposition or reconcile family; HELIOS and TRON ingestion inputs are deliberately not published; and about 15 documents carry stale "Graylog as trigger transport" language. Plan effect: minimum publication work (P-H1..P-F2) is small but real and sequences after `GOAL-TRIGGER-001`; FALCON stays outside the executable trigger path.
- **F, qualification to review** (`pids/GOLD-AUD-F.md`). A 10-hop path matrix is the unit of work: the running DARWIN production image is not an ancestor of `main` and lacks APOLLO and migrations 0006 to 0013; no `APOLLO_PROOF` run exists (006B emits `APOLLO_RESULT` only, single timeframe, ATOMIC, LONG only, so the chained two-timeframe gold candidate may be out of scope); `EdgeProfileVersion` is defined nowhere; the NEO observer fails every cycle (missing fabric config key since 2026-07-17); NEO has no CER client. External repository and SaaS evaluations: recommend **adopting none for the MVP** (the backtrader and backtesting.py reviews predate APOLLO; GPL and AGPL licence posture unresolved). Plan effect: the MVP review step is a read-only NEO report, not the full evidence gateway.

**Effect on the critical path.** The audits do not add scope, but they change what the serial chains consist of. (1) The strategy chain gets longer in its middle: `HELIOS-T2` is a build of a Redis reader plus a contract adapter (CP-1 reconciliation), not an adaptation, so the reader build is a long pole alongside `GOAL-CONTRACT-001` and `HELIOS-T3`. (2) The trigger path is a long pole: no inbox specification, no HELIOS signer or outbox, no TRON runtime, no typed gateway; `GOAL-TRIGGER-001` (Matt gate, blockers D-1..D-4, D-12) and `TRON-D1-RATIFY` (Matt gate) gate it. (3) The MT5 gateway chain remains four serial items before `TRON-T2`. (4) Evidence (FALCON) and the review step (F) are shorter than first feared and sequence after the trigger path. The earlier hope in section 8.3 that audit B might shrink `HELIOS-T2` to adaptation is not supported by the evidence found.

## 4. Dependency and ownership matrix

### 4.1 Components by what they own

| component | repo | contract it provides | contract it consumes | source of truth for | runtime state it owns | shared datastore it writes | single writer of |
|---|---|---|---|---|---|---|---|
| HERMES | `maff0000/hermes` | market facts (`goal.market-fact/v1` via `HERMES-FACT-001`; PROD Redis publication as built) | vendor feeds (not touched) | market-truth data and its publication | publisher process | PROD HERMES Redis (and its historical store) | the PROD HERMES Redis keyspace |
| HELIOS | `maff0000/HELIOS` | strategy state; signed trigger (`GOAL-TRIGGER-001`) | market-fact input; `goal.strategy/v1` | deterministic evaluation | evaluator state; the trigger outbox (proposed) | its own state and outbox store | the signed trigger outbox |
| TRON | `maff0000/tron` | inbox intake and outcomes (`GOAL-TRIGGER-001`); execution journal | signed trigger; gateway typed API | sizing, hard risk, kill, execution decisions | inbox, journal, kill state | Trading Postgres (`TRON-T1`) | inbox and execution journal; the only caller of the gateway |
| MT5 gateway | `maff0000/mt5-gateway` | typed allow-list API (`MT5-GW-003`) | broker (via the terminal) | terminal and instance control | instance containers, DEMO guard | none shared | the MT5 instances |
| FALCON | `maff0000/falcon` | event registry; evidence ingestion | event families from HERMES, ARES, HELIOS, TRON | evidence mirror | registry and ingestion | its registry store and Graylog stream | the registry |
| CER | `maff0000/CER` | evidence containers; `EdgeProfileVersion` (`CER-R1`) | HSA/DARWIN evidence references | empirical evidence and lineage | CER store | CER store | CER evidence store |
| HSA | `maff0000/HSA` | strategy package; (`HSA-C1`) `goal.strategy/v1` | fact catalogue | strategy engineering | none (CLI) | none | strategy package authoring |
| DARWIN | `maff0000/DARWIN` | research results, `StrategyVersion` | `goal.strategy/v1` (`DARWIN-R2`) | causal backtests | research DB | DARWIN DB | DARWIN DB |
| NEO | `maff0000/neo` | read-only review of evidence (`NEO-R1`) | evidence interface | observation only | review records | none in the trade path | its review records |
| GOAL | `maff0000/GOAL` | contracts of record, backlog, PIDs, evidence index, compatibility matrix | component evidence | programme state | none | the repository | `backlog/backlog.yaml` (PO-approved changes via ROGUE); contract text (CA/PO) |
| GOLD-STRATEGY-RUNTIME | `maff0000/GOLD-STRATEGY-RUNTIME` | composition and deployment of HSA + HELIOS + CER | those products unmodified | deployment composition | compose stack | none | the compose stack, if adopted (PD-7) |

### 4.2 Shared resources and their single writer

| shared resource | single writer | readers permitted during the audits | enforcement |
|---|---|---|---|
| PROD HERMES Redis | the HERMES publisher | `GOLD-AUD-A` only, non-blocking read protocol | allow-list wrapper (6.2); no other audit connects |
| HERMES historical store | HERMES | none (docs and repo only) | not in any permission set |
| HELIOS signed trigger outbox | HELIOS signer/publisher (to be fixed by `GOAL-TRIGGER-001`; PROPOSED, the inbox spec was not found) | TRON intake (read of delivered triggers) | contract |
| TRON TriggerInbox and execution journal | TRON | FALCON/NEO via published events or read-only interface | contract |
| Trading Postgres | TRON (`TRON-T1`) | none during audits | not in any permission set |
| MT5 instances (including the DEMO instance) | the MT5 gateway | none during audits (no broker call) | explicit write-forbidden list (5.3) |
| Legacy executors / legacy MT5 services | their existing owners; untouched (ADR-MT5-002) | none | explicit write-forbidden |
| FALCON registry / Graylog | FALCON ingestion | `GOLD-AUD-E` through the query interface, read-only | permission set |
| CER evidence store | CER | `GOLD-AUD-F` repo read only | permission set |
| DARWIN DB | DARWIN | none | permission set |
| `backlog/backlog.yaml`, `MANIFEST.md`, `MASTER-BACKLOG.md` | ROGUE integration (generated regions via `goal-docs --write`) | all | audits and PID drafters never edit |
| Cross-component evidence index and compatibility matrix | `GOLD-AUD-C` worker (during audits); `GOLD-MVP-001` (during integration) | all (read) | file ownership (5.2) |
| Memory Fabric | each persona writes only its own namespace | read-only orientation | audit workers do not write fabric |

### 4.3 Contract ownership

| contract / interface | provider | consumer | owning PID | approval |
|---|---|---|---|---|
| HERMES Redis publication (as built) | HERMES | HELIOS adapter, FALCON | `HERMES-CUR-001` (as-built), `GOLD-AUD-A` | GOAL |
| `goal.market-fact/v1` (to-be) | HERMES | HELIOS, HSA | `HERMES-FACT-001` | GOAL |
| HERMES → HELIOS input compatibility (as-is versus to-be) | HERMES | HELIOS-T2 | `GOLD-AUD-C` (matrix), `HERMES-FACT-001` | GOAL |
| `goal.strategy/v1` | GOAL | HSA, HELIOS, DARWIN, CER | `GOAL-CONTRACT-001` | GOAL (CA/PO) |
| signed trigger + inbox semantics | GOAL | HELIOS (producer), TRON (consumer), FALCON (observer) | `GOAL-TRIGGER-001` | GOAL (Matt gate) |
| TRON → gateway typed API | MT5 gateway | TRON | `MT5-GW-003` | GOAL |
| FALCON event families | FALCON | HERMES, HELIOS, TRON as emitters | `FALCON-T1` plus an increment (PD-4) | GOAL |
| EdgeProfileVersion | CER | TRON (sizing, later), NEO | `CER-R1` | GOAL |

### 4.4 Dependency graph (engineering edges only)

```text
GOAL-DCP-001 (CLOSED)
 ├─ GOLD-AUD-A..F (read-only; no engineering edges; feed matrix)
 ├─ HERMES-CUR-001 ─ HERMES-FACT-001 ─┐
 ├─ GOAL-CONTRACT-001 ─ GOAL-CORE-001 ─ HELIOS-T1 ─ HELIOS-T2 ─ HELIOS-T3 ──────┐
 │      └─ GOAL-TRIGGER-001 ───────────────────────────┘ (also feeds TRON-T4)  │
 ├─ TRON-D1-RATIFY (Matt) ─ TRON-T1 ─ TRON-T3, TRON-T4 (needs TRIGGER-001) ─────┤
 ├─ MT5-GW-001 ─ -002 ─ -003 ─ -004 ─ TRON-T2 ───────────────────────────────────┤
 ├─ FALCON-T1 (+ minimum event publication, PD-4)                                │
 └─ (fixed-size sizing, PD-4/D-3)                                                ▼
                                                                         GOLD-MVP-001
```

Audits shorten this graph by turning assumed work into verified reuse (section 8.3); they add no engineering edge.

## 5. Collision matrix

### 5.1 Who reads what (R) and who writes what (W, own worktree only)

| resource | A | B | C | D | E | F | MVP |
|---|---|---|---|---|---|---|---|
| GOAL repo (own `audits/2026-10-15/gold-aud-<l>/` and `pids/GOLD-AUD-<L>.md` on own branch) | W | W | W | W | W | W | W (`gold-mvp/`) |
| GOAL `main`, `backlog.yaml`, `MANIFEST.md` | R | R | R | R | R | R | R |
| `maff0000/hermes` | R + evidence PR | R | R | | R | | |
| `maff0000/HELIOS` | | R + evidence PR | R | | R | R | |
| `GOLD-STRATEGY-RUNTIME` | | R | | | R | R | |
| `maff0000/tron` (incl. unmerged D1 branch) | | | R | R + evidence PR | R | R | |
| `maff0000/mt5-gateway` | | | | R (+ note PR if needed) | | | |
| `maff0000/falcon` | R | | R | R | R + evidence PR | | |
| `maff0000/CER`, `HSA`, `DARWIN`, `neo` | | R (HSA) | R | | | R (+ evidence PR in CER) | |
| PROD HERMES Redis | **R (protocol)** | | | | | | |
| FALCON running query interface | | | | | R | | |
| MT5 instances / broker | | | | | | | W only in the approved acceptance run |
| Memory Fabric | R | R | R | R | R | R | R |

### 5.2 File-level single writers inside GOAL

| path | single writer |
|---|---|
| `pids/GOLD-MVP-001.md` | this work order (then PL under the approved PID) |
| `pids/GOLD-AUD-<L>.md` | lane `<L>` PID drafter |
| `audits/2026-10-15/gold-mvp/PORTFOLIO.md` | this work order |
| `audits/2026-10-15/gold-aud-<l>/INDEX-ENTRY.md` (a fixed-format summary per audit) | lane `<L>` worker |
| `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md`, `COMPATIBILITY-MATRIX.md` | `GOLD-AUD-C` worker (aggregates the six INDEX-ENTRY files after they merge) |
| `MANIFEST.md`, `backlog/MASTER-BACKLOG.md`, `backlog/backlog.yaml` | ROGUE at integration; never a lane |

Merge-conflict classes: the only expected conflict is `MANIFEST.md` (generated); ROGUE regenerates it. All other paths are disjoint by construction.

### 5.3 Explicit write-forbidden list (every audit, every drafter)

1. Production HERMES Redis: no `SET`, `DEL`, `EXPIRE`, `FLUSH*`, `CONFIG`, `PUBLISH`, stream writes, `ACL`, `SCRIPT`, `EVAL`, `DEBUG`, `MONITOR`, `SUBSCRIBE`, `KEYS`, blocking reads.
2. The MT5 instances (DEMO and others) and any broker connection; the legacy executors and the legacy dell MT5 container (ADR-MT5-002); no start, stop, restart, exec that mutates.
3. GOAL `main`; any branch other than the worker's own; any force-push; any direct commit to a component `main`; any auto-merge.
4. `backlog/backlog.yaml`, `MANIFEST.md`, `MASTER-BACKLOG.md`, tools, tests, workflows, `README.md`; no `pid_path`, no `DELIVERY_READY`, no approval records, no dispatch.
5. Production services of HERMES, HELIOS, TRON, FALCON, ARES, NEO: no restart, no config edit, no database write.
6. Shared databases (Trading Postgres, HERMES stores, DARWIN DB, CER store, MariaDB): no connection by default; if a lane needs a count, it is requested as a PO decision, not taken.
7. Credentials: no rotation, no creation of a principal (including a Redis ACL user), no reading of secret files.
8. `/srv/forge` and other workers' worktrees: not touched.
9. Memory Fabric: not written by audit workers.

## 6. Read-only permission matrix

### 6.1 Global rules (apply to every lane)

- Hosts: read-only shell on the dell host and the local host; `docker ps`, `docker image inspect`, `docker inspect --format` limited to labels, mounts and network names. Never an environment dump, never `docker exec`, never `docker logs` of a broker-facing (MT5) container. Logs of non-broker containers only with a bounded `--tail`/`--since`, filtered before use, never committed raw.
- Never print, copy or write a secret value. If one is seen, record only "a plaintext credential exists at `<path>`, key `<name>`". Show config as key names with `KEY=***`.
- GitHub: `gh` GET calls and `git` read operations on repositories; writes only to the worker's own evidence branch in the designated repository, through a PR; never push to a default branch.
- Fabric: read-only orientation; GitHub and repo evidence outrank it; fabric-only claims are labelled.
- Every command that touches a running system is logged (command, time, count of results) in the evidence; values are not logged unless sanitised.

### 6.2 PROD HERMES Redis protocol (lane A only)

Preconditions: PO decision PD-5 recorded; a window agreed with the HERMES owner; a wrapper script written in the worker's worktree, reviewed by the auditor before first use, that rejects every command not on the allow-list and enforces a rate cap and a result cap.

| allowed | forbidden |
|---|---|
| `SCAN`, `HSCAN`, `SSCAN`, `ZSCAN` with `MATCH` and `COUNT <= 200`, cursor loop with a pause | `KEYS`, `FLUSHALL`, `FLUSHDB`, `SET`, `DEL`, `UNLINK`, `EXPIRE`, `PERSIST`, `RENAME`, `HSET`, any write command |
| `TYPE`, `TTL`, `PTTL`, `EXISTS`, `STRLEN`, `HLEN`, `LLEN`, `SCARD`, `ZCARD`, `XLEN` | `CONFIG` (any), `ACL`, `DEBUG`, `SAVE`, `BGSAVE`, `SHUTDOWN`, `CLIENT KILL`, `SCRIPT`, `EVAL`, `FUNCTION` |
| `GET` only when `TYPE` is string and `STRLEN` is under a cap (suggest 64 KiB) | `MONITOR`, `SUBSCRIBE`, `PSUBSCRIBE`, `XREAD BLOCK`, `BLPOP`, any blocking call |
| `HGET`, `HMGET`, `HGETALL` only when `HLEN` is under a cap (suggest 500); otherwise `HSCAN` | `MIGRATE`, `REPLICAOF`, `PUBLISH` |
| `LRANGE` / `XREVRANGE` / `ZRANGE` bounded to a small count | `OBJECT FREQ`, `MEMORY DOCTOR` and anything that mutates LFU/LRU state |
| `INFO keyspace`, `INFO memory`, `INFO stats` (sections only) | `INFO` unrestricted (may include secrets) |

Handling: the Redis credential is supplied to the client only through an environment variable set inside the wrapper process from a root-only file; it never appears in a command line, a log or evidence (standing rule: never echo `--requirepass`-style arguments). Values read are sanitised before any repo copy. One connection, rate cap (suggest 50 commands per second), total command budget stated in the audit PID. Prefer a window away from peak market activity. The audit may not create a read-only ACL principal (that is a mutation); if a read-only principal exists it is used, otherwise the wrapper is the control and the auditor reviews it first.

### 6.3 Per-lane read permissions

| lane | may read | may not read |
|---|---|---|
| A | `hermes` repo, docs, contracts; HERMES-related GOAL branches; container labels for HERMES services; PROD Redis per 6.2; the HELIOS and FALCON repos for consumer expectations | HERMES historical store contents; vendor credentials; any other Redis |
| B | `HELIOS`, `GOLD-STRATEGY-RUNTIME`, `HSA`, legacy HELIOS lineage repo(s) and branches, deployment files (names only for env keys), image labels; fixtures | PROD Redis; any broker; env values |
| C | GOAL branches (contract, trigger, recon, wave-1 reports); `HELIOS`, `hermes`, `tron` (incl. D1 branch), `falcon` contracts; fixtures | runtime systems (none needed) |
| D | `tron` (main and the unmerged D1 branch), `mt5-gateway` (all branches), GOAL MT5 records (template, readiness, DEMO-verify), instance directory listings with modes only, image labels | broker, the MT5 instances' runtime, logs of MT5 containers, credential files, the legacy executors' runtime |
| E | `falcon` repo, contracts, PIDs, the running registry through its read-only query interface and its documented health endpoint; HELIOS/TRON event definitions | FALCON write APIs, Graylog admin, credentials |
| F | `CER`, `HSA`, `DARWIN`, `neo` repos; earlier external repository/SaaS evaluation records on the hosts and in fabric (read-only, labelled as fabric) | runtime stores, databases, NEO's legacy executor runtime |
| MVP (before the acceptance run) | the six audits' outputs and component PIDs | everything runtime |

## 7. GitHub evidence requirements

### 7.1 Ten-item checklist (every audit PR; the PR body links each item to a section/file)

The numbering and wording below are CA's. Each lane PID's "Evidence PR checklist" maps its own deliverables to these ten numbers; no lane may renumber them.

1. [ ] PID/WO identifier and exact audited scope.
2. [ ] Source repositories, revisions and relevant documentation references (full SHA, captured at audit start; later movement of a source noted).
3. [ ] Existing implementation: proven, partially proven, unverified or missing (with the proof method for each).
4. [ ] Actual versus expected contract comparison (field by field, for each interface in scope).
5. [ ] Tests, fixtures and evidence references (paths, commands, results; nothing fabricated; non-runnable items labelled).
6. [ ] Specific defects and compatibility gaps (each with severity BLOCKER / MAJOR / MINOR and an id).
7. [ ] Reusable code and documentation (path and revision, with the reuse boundary).
8. [ ] Minimum recommended implementation changes (each tied to an existing or proposed item and its owner).
9. [ ] Safety and deployment constraints (what must not be touched; what changes would need a gate).
10. [ ] Independent audit verdict (GREEN / AMBER / RED) and any unresolved findings, with auditor identity role and what the verdict does not cover.

### 7.2 Naming, checks and rules

| item | rule |
|---|---|
| PR title | `[GOLD-AUD-<L>] <short outcome>`; integration PRs `[GOLD-MVP-001] ...` |
| Branch | `wo/GOLD-AUD-<L>-<slug>` in the component repo; GOAL INDEX-ENTRY branch `wo/GOLD-AUD-<L>-index` |
| Evidence location | component repo: `docs/evidence/GOLD-AUD-<L>/`; GOAL: `audits/2026-10-15/gold-aud-<l>/INDEX-ENTRY.md` (fixed format: ids, repo, PR URL, head SHA, verdict, open findings, matrix rows contributed) |
| Required checks | repository CI where it exists; for GOAL, `./tools/goal-validate` and `./tools/secret-scan` clean and the control-plane workflow green; where a component repo has no CI, the PR records a secret scan (full history) and a link-check as manual checks, and says so |
| Merge | no direct-to-main, no auto-merge; a merge needs the independent auditor verdict, CA acceptance and the PO gate; a regular (non-squash) merge |
| Evidence is not acceptance | acceptance needs: approved PID and bounded WO; evidence committed to the correct repo; accessible PR; required checks; independent auditor review; CA acceptance |
| Commit message | `[GOLD-AUD-<L>] ...` with the attribution trailer the programme uses |

### 7.3 Public-repository sanitisation rule

GOAL is public, and some component repositories are public or may become so (the MT5 gateway repository is recorded as public in MT5-READINESS, contradicting an earlier statement). Therefore, for any evidence that originates from a private repository or from a running system:

- Evidence PRs in a **private** component repo may name internal key families, service names and schema fields, but never secret values, account numbers, login identifiers, internal IPs or hostnames of sensitive services, tokens or customer data.
- Anything copied into **GOAL** (INDEX-ENTRY, matrix, index) is generalised one more level: "the dell host", "the PROD HERMES Redis", key families by pattern without hostnames, broker "account `<redacted>`"; no copied payloads, only field names, types and counts.
- Evidence destined for a **public** component repo (HELIOS, mt5-gateway, GOAL) is treated as GOAL-level.
- Each PR runs a sanitisation grep (addresses, key-like strings, account-like numbers, token prefixes) and attaches the empty result; the auditor repeats it.
- If sanitisation would destroy the evidence value, the evidence stays in the private repo and GOAL holds only a pointer (repo, path, SHA).

## 8. Dispatch-eligibility analysis

### 8.1 What can start the moment PIDs are approved

- **All six audits** can start as soon as each audit PID is approved and its item is `DELIVERY_READY`: each depends only on `GOAL-DCP-001` (CLOSED, accepted terminal), needs no engineering predecessor, and writes only its own branch. Mechanically, once the backlog patch (part 1) is merged they appear in `./tools/goal-ready --pid-wave` as PID-drafting candidates, and in `./tools/goal-ready --with-pid` after approval.
- `GOLD-AUD-A` additionally needs PD-5 (production read access) and a reviewed wrapper; it is the only one with a pre-start action beyond approval. Until PD-5, A can do its repo-only half.
- `GOLD-MVP-001` is **not** dispatchable until its prerequisites are accepted (it is the last item on the critical path). Its architecture document and runbook skeleton may be drafted early by the PL under the approved PID only when the PO releases them; they must not block anything.

### 8.2 Ordering and feeds

| order | audits | rationale |
|---|---|---|
| wave 0, parallel | A, B, C, D, E, F | independent reads; six concurrent workstreams allowed |
| feeds into C | A (as-built publication), B (adapter and strategy findings), D (intake assumptions), E (event families) | C's compatibility matrix and index aggregate them; C starts concurrently and finalises last |
| feeds into B | A (key, timeframe and warm-up inventory) | B's compatibility conclusions need it; B can complete the locate-and-reconcile half first |
| feeds into F | B (candidate strategy), D (what TRON consumes from an edge profile) | F's qualification path ends at the chosen strategy |
| feeds into E | A and D (what HERMES, HELIOS and TRON emit) | E's minimum publication list |
| consolidation | C's final EVIDENCE-INDEX and COMPATIBILITY-MATRIX; then `GOLD-MVP-001` | after all six verdicts |

To keep concurrency safe, each audit freezes a source-revision table at start (7.1 item 2); a source that moves mid-audit is recorded, not chased.

### 8.3 The critical path and where audits shorten it

Serial engineering chains (after PID approvals, from the backlog as it stands with PR #5 applied):

- Strategy chain: `GOAL-CONTRACT-001` → `GOAL-CORE-001` → `HELIOS-T1` → `HELIOS-T2` → `HELIOS-T3` (also needs `GOAL-TRIGGER-001`) → `TRON-T4` intake proof with a real HELIOS.
- Execution chain: `MT5-GW-001` → `-002` → `-003` → `-004` → `TRON-T2`; and `TRON-D1-RATIFY` → `TRON-T1` → `TRON-T3`/`TRON-T4`.
- Evidence chain: `FALCON-T1` plus the minimum publication increment.
- Convergence: `GOLD-MVP-001`.

The long poles are the MT5 gateway chain (four serial items before TRON-T2) and the strategy chain (five). Audits shorten them by:

1. **A** shows whether the PROD publication already satisfies the fact set one strategy needs, so `HERMES-FACT-001` can be an adaptation or declaration of what exists, and no new feed is requested (the lane PID found that the candle and indicator families are documented only in fabric, so the repository record starts with this audit).
2. **B** was expected to find an earlier HERMES to HELIOS integration that could shrink `HELIOS-T2` from construction to adaptation. The lane PID found none (section 3a), so `HELIOS-T2` stays a construction; B still scopes it to a minimum adaptation plan, and picks the first strategy so `GOAL-CONTRACT-001` is validated against a real package.
3. **C** freezes the minimum contracts early, which unlocks `GOAL-CORE-001`, `HELIOS-T3` and `TRON-T4` authoring in parallel.
4. **D** states the smallest DEMO path, so `MT5-GW-003/-004` and `TRON-T2/T3` are scoped to the minimum rather than the full gateway ambition, and confirms whether the sizing gap needs its own item.
5. **E** confirms what FALCON already carries (28 registered families, only two emitting), so only the missing HELIOS and TRON publication work is built.
6. **F** confirms CER/HSA/DARWIN already cover registration and qualification, so none of `CER-R1`, `HSA-C1`, `DARWIN-R2` becomes a prerequisite of the MVP.

No audit shortens the path by adding scope; if one finds the path longer (a BLOCKER), it says so.

## 9. Audit acceptance checklist

### 9.1 Independent auditor assignment

Three independent auditor roles, each covering two lanes and independent of those lanes' workers and PID drafters:

| auditor | covers | rationale |
|---|---|---|
| AUD-1 | A and E | both centre on emitted events and runtime publication; shared vocabulary (keys, event families) |
| AUD-2 | B and C | HELIOS reconciliation and contract reconciliation need one reviewer who can see where they agree |
| AUD-3 | D, F, and the `GOLD-MVP-001` acceptance | execution and strategy-lifecycle reviewer; acceptance run reviewer is independent of the lane workers |

Rules: an auditor is never the drafter or worker of the lane; an auditor reviews the permission wrapper (lane A) and the sanitisation grep (all) before the evidence PR; the auditor writes only review comments and a verdict file in the PR, never edits the evidence.

### 9.2 Checklist (each audit; the auditor ticks, ROGUE and CA verify)

- [ ] Approved audit PID and bounded WO exist; the audit stayed inside the quoted scope.
- [ ] The ten evidence items present (7.1); every factual claim cites a source actually read; unverified claims labelled UNVERIFIED.
- [ ] Source-revision table present; sources unchanged or movement recorded.
- [ ] Every command against a running system is in the log, within the permission set (section 6); allow-list wrapper reviewed (lane A).
- [ ] Nothing written outside the worker's own branch; write-forbidden list (5.3) respected (the auditor checks reflogs, PR file list and system state snapshots where they exist).
- [ ] No secrets, internal addresses, account identifiers or key material in the PR; sanitisation grep empty; `./tools/secret-scan` clean for GOAL content.
- [ ] Actual versus expected contract comparison is field-level, not narrative.
- [ ] Each defect has severity and an owner; each recommended change maps to an existing or proposed item (no new scope hidden in prose).
- [ ] The INDEX-ENTRY file present in GOAL with the fixed fields; the matrix rows contributed are consistent with the evidence.
- [ ] Accessible PR; required checks green; no direct-to-main; no auto-merge.
- [ ] Verdict recorded (GREEN/AMBER/RED) with unresolved findings; CA acceptance recorded separately by CA/PO.

## 10. Risks

| # | risk | mitigation |
|---|---|---|
| R-1 | A lane audit touches production state | read-only protocol and wrapper (6.2), reviewed first; PD-5; single lane |
| R-2 | The previously completed HERMES to HELIOS integration is not found (B) | realised in B's drafting (section 3a): the reader is a build item in `HELIOS-T2` scope; B's stop condition holds (no second reader may be built or prototyped by the audit; a negative result needs a recorded search method) |
| R-3 | Contract drift while six audits run | source-revision tables; C owns one matrix; contract changes after acceptance restart affected rows |
| R-4 | Duplicate scope with existing PIDs (`HERMES-CUR-001`, `FALCON-T1`, `TRON-D1-RATIFY`) | all six lanes are new bounded items with `Complements:` lines and a documented amendment fallback (section 3); no existing PID is edited |
| R-5 | `GOLD-MVP-001` overlaps `PAPER-E2E-001` | PD-1; recommended option keeps both with a clear dependency |
| R-6 | Hidden missing items (fixed-size sizing, FALCON event publication, MT5 typed API) | listed in the gap register and PD-3/PD-4; audits D and E confirm shape |
| R-7 | Simulation mistaken for DEMO proof; PAPER set early | GOLD-MVP-001 AC-9 to AC-11 and S-6; title and ADR-MT5-001 reference |
| R-8 | Public-repo leakage from private evidence | 7.3 rule, sanitisation grep, auditor repeat, `secret-scan` |
| R-9 | `MT5 gateway` repository is public while a prior record says private (MT5-READINESS) | flagged for owner decision outside this portfolio; lane D treats mt5-gateway evidence as public-level |
| R-10 | Price-basis mismatch (live feed vs futures truth vs CFD) invalidates a performance claim | label the MVP a plumbing proof (GOLD-MVP-001 D-6) |
| R-11 | Six concurrent PR streams create merge noise on `MANIFEST.md` | ROGUE regenerates; disjoint paths (5.2) |
| R-12 | TRON D1 and its three trigger models are not ratified (Matt gate) | audit D consumes `TRON-D1-RATIFY`; MVP waits for the ratification |
| R-13 | Audit scope creeps into implementation | each audit PID carries a no-implementation non-goal; auditor checks the file list |
| R-14 | Auditor independence eroded when one auditor covers two lanes | pairing chosen to avoid reviewing one's own lane; CA acceptance is separate |

## 11. Backlog patch description (specified, NOT applied here)

**This section is a specification only.** The consolidation work order did not edit `backlog/backlog.yaml`, set any `pid_path`, move any item to `DELIVERY_READY`, record any approval or dispatch anything. The patch is applied later, by ROGUE, after the PO approves.

**Ordering and expected counts.** The patch is applied **after GOAL PR #5 merges** (PR #5 takes the backlog from 40 to 43 items by adding `GOAL-TRIGGER-001`, `TRON-D1-RATIFY`, `HSA-C1`). Expected pinned item counts: 40 on `main` today; 43 after PR #5; **49 after part 1** (43 + 6 audit items); **50 after part 2** (49 + `GOLD-MVP-001`). If part 1 were applied on today's `main` before PR #5 the count would be 46, and PR #5 would then have to be rebased onto it (not recommended). The count-pinning tests (`tests/test_cli.py`, `tests/test_model.py`, `tests/test_first_wave.py`) must be updated in the same change as each patch part. Part 2 additionally waits for the PO ruling on PD-1.

**Lane A matt gate.** `GOLD-AUD-A` carries `matt_gate: true` pending the production-access decision (PD-5; lane decision D1). It is the only audit with a Matt gate.

### 11.1 Interaction with GOAL PR #5 and PR #6

- **PR #5** (`wo/GOAL-RECON-PR`, OPEN) takes the backlog from 40 to 43 items (adds `GOAL-TRIGGER-001`, `TRON-D1-RATIFY`, `HSA-C1`) and edits `backlog/backlog.yaml`, `MASTER-BACKLOG.md`, `MANIFEST.md` and three tests that pin the item count (`tests/test_cli.py`, `tests/test_model.py`, `tests/test_first_wave.py`). This portfolio's `GOLD-MVP-001` depends on `GOAL-TRIGGER-001` and `TRON-D1-RATIFY` (transitively), which exist only on #5. Therefore **part 2 (GOLD-MVP-001 and the PAPER-E2E-001 edge) must be applied after #5 merges**. **Part 1 (the six audit items, depending only on `GOAL-DCP-001`) is independent of #5** and may be applied on `main` first or after #5; applied after #5 it is simplest because both edit the same file and the same count-pinning tests.
- Both patches touch `backlog/backlog.yaml`: apply serially, never as two concurrent writers. The pinned item count becomes 49 after part 1 on top of #5 and 50 after part 2 (43 + 6 + 1); on today's `main` it would be 46 after part 1 alone. The count-pinning tests must be updated in the same change (as #5 does). Lane values below were normalised to `research` for all six audits and risk to `medium` for C and D, to match the lane PIDs; priority is kept P0 pending DR-13.
- **PR #6** (`wo/GOAL-BACKUP-PLAN`, OPEN) is documentation only (`MANIFEST.md`, two `operations/` files). No backlog interaction; the only collision is `MANIFEST.md` with #5 and with any later change, resolved by `./tools/goal-docs --write` at integration.
- Generated documents (`MASTER-BACKLOG.md`, `MANIFEST.md`) are regenerated by ROGUE at integration; this work order did not run `goal-docs --write`.

### 11.2 Part 1: six audit items (all 13 fields explicit; `pid_path` stays `null` until the PO approves each PID)

```yaml
  # GOLD MVP read-only audit items (CA directive 2026-10-15). Read-only, no engineering dependency.
  - id: GOLD-AUD-A
    title: "GOLD MVP audit A: HERMES PROD XAUUSD Redis publication (read-only; strict subset of HERMES-CUR-001 scope item 1)"
    lane: research
    component: HERMES
    target_repository: maff0000/hermes
    priority: P0
    risk: medium
    state: PID_DRAFT
    depends_on:
      - GOAL-DCP-001
    po_gate: true
    matt_gate: true   # true pending the production-access decision (PD-5)
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md

  - id: GOLD-AUD-B
    title: "GOLD MVP audit B: locate and reconcile the HERMES Redis to HELIOS GOLD integration and review HSA packages (read-only)"
    lane: research
    component: HELIOS
    target_repository: maff0000/HELIOS
    priority: P0
    risk: low
    state: PID_DRAFT
    depends_on:
      - GOAL-DCP-001
    po_gate: true
    matt_gate: false
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md

  - id: GOLD-AUD-C
    title: "GOLD MVP audit C: shared contract reconciliation, compatibility matrix and evidence index (read-only; complements GOAL-CONTRACT-001 and GOAL-TRIGGER-001)"
    lane: research
    component: GOAL
    target_repository: maff0000/GOAL
    priority: P0
    risk: medium
    state: PID_DRAFT
    depends_on:
      - GOAL-DCP-001
    po_gate: true
    matt_gate: false
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md

  - id: GOLD-AUD-D
    title: "GOLD MVP audit D: TRON design, risk rules, journal, trigger intake and the smallest MT5 DEMO execution path (read-only)"
    lane: research
    component: TRON/MT5
    target_repository: maff0000/GOAL
    priority: P0
    risk: medium
    state: PID_DRAFT
    depends_on:
      - GOAL-DCP-001
    po_gate: true
    matt_gate: false
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - decisions/ADR-MT5-001-REUSE-CONTAINER-REPLACE-BRIDGE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md

  - id: GOLD-AUD-E
    title: "GOLD MVP audit E: FALCON registry and ingestion, minimum HELIOS and TRON event publication (read-only; complements FALCON-T1)"
    lane: research
    component: FALCON
    target_repository: maff0000/falcon
    priority: P0
    risk: low
    state: PID_DRAFT
    depends_on:
      - GOAL-DCP-001
    po_gate: true
    matt_gate: false
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md

  - id: GOLD-AUD-F
    title: "GOLD MVP audit F: strategy qualification, registration, execution and NEO review across CER, HSA, DARWIN and NEO (read-only)"
    lane: research
    component: CER/HSA/DARWIN/NEO
    target_repository: maff0000/GOAL
    priority: P0
    risk: low
    state: PID_DRAFT
    depends_on:
      - GOAL-DCP-001
    po_gate: true
    matt_gate: false
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md
```

### 11.3 Part 2: integration item and edge (apply only after PR #5 has merged and the PO has ruled PD-1)

```yaml
  - id: GOLD-MVP-001
    title: "GOLD MVP integration and acceptance: one governed XAUUSD strategy end to end on Vantage DEMO with FALCON evidence (state PAPER only after DEMO proof)"
    lane: trading
    component: GOAL
    target_repository: maff0000/GOAL
    priority: P0
    risk: capital
    state: PID_DRAFT
    depends_on:
      - GOLD-AUD-A
      - GOLD-AUD-B
      - GOLD-AUD-C
      - GOLD-AUD-D
      - GOLD-AUD-E
      - GOLD-AUD-F
      - GOAL-CONTRACT-001
      - GOAL-TRIGGER-001
      - HELIOS-T3
      - TRON-T2
      - TRON-T3
      - TRON-T4
      - FALCON-T1
    po_gate: true
    matt_gate: true
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - decisions/ADR-MT5-001-REUSE-CONTAINER-REPLACE-BRIDGE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md
```

Edge change (needs PD-1 option (b)): `PAPER-E2E-001.depends_on` gains `GOLD-MVP-001`. Later, after audits D and E: add the minimum sizing item and the minimum FALCON publication item to `GOLD-MVP-001.depends_on` once those items exist (PD-4).

State is `PID_DRAFT` for all seven because their PID candidates are drafted (`pids/GOLD-AUD-A.md` to `-F.md` and `pids/GOLD-MVP-001.md` exist in the consolidated branch, unapproved); none may carry a `pid_path` until CA/PO approval, none is `DELIVERY_READY`. The `target_repository` of D and F is `maff0000/GOAL` as in their lane PIDs (evidence mirrors go to component repositories; DR-15). `./tools/goal-validate` on the patched backlog is expected clean (all ids resolve; part 2 requires #5). ROGUE regenerates generated documents and updates the item-count tests in the same change.

## 12. PO decisions needed (original PD list; superseded by `DECISION-REGISTER.md`)

The register consolidates PD-1 to PD-12 with every lane PID's open decisions and the PR #5 and #6 items, de-duplicated and ranked. The PD ids below are kept as references. Lane drafters' conclusions on PD-3 (D is a new item) and the amend-or-new questions of A, B, C, E, F are recorded in section 3; the PO confirms them in the register.

| id | decision | options | recommendation | blocks |
|---|---|---|---|---|
| PD-1 | `GOLD-MVP-001` versus `PAPER-E2E-001` | (a) supersede; (b) keep both, `PAPER-E2E-001` depends on `GOLD-MVP-001`; (c) keep independent | (b) | approval of `GOLD-MVP-001` |
| PD-2 | Header gates of `GOLD-MVP-001` | risk `capital` + Matt gate; or `high` with Matt gate at PAPER only | `capital`, Matt gate true | approval of `GOLD-MVP-001` |
| PD-3 | Is lane D a new item or an increment of `TRON-D1-RATIFY` | new (lane D drafter concluded new) or fold in | new: keeps the audit outside a Matt-gated ratification | dispatch of D |
| PD-4 | Add the missing MVP items: minimum fixed-size sizing (TRON-owned) and minimum FALCON `strategy_trigger`/`tron.*` publication | add after audits D and E confirm shape; fold into TRON-T3/T2 and FALCON-T3/T4 subset; wait for TRON-T5 | add bounded items after D and E report; do not wait for TRON-T5/CER-R1 | acceptance, not approval |
| PD-5 | Read-only production Redis access for lane A | allow under 6.2 with Matt notification; require Matt gate; repo-only audit | allow under the 6.2 protocol; Matt informed and may waive the gate in one line; gate true by default until waived | start of A's runtime half |
| PD-6 | Are all six audits dispatched concurrently | all six in wave 0; stagger C last | all six (the permission design makes them collision-free) | ROGUE scheduling |
| PD-7 | Composition vehicle (`GOLD-STRATEGY-RUNTIME`) and the deferred `PLATFORM-RT-001` | adopt; adapt; compose per component | decide after audit B; do not rebuild a delivered runtime | acceptance |
| PD-8 | First strategy and its qualification threshold | PO fixes before the run | simplest single-timeframe HSA package already satisfiable from the PROD publication (audit B and F) | acceptance |
| PD-9 | Price basis for the MVP | accept difference for a plumbing proof; require HMT-3H alignment first | accept, with a no-performance-claim label | acceptance |
| PD-10 | Order of applying backlog changes | #5 first, then parts 1 and 2 serially; part 1 on `main` ahead of #5 | #5 first; then part 1; then part 2 after PD-1 | integration |
| PD-11 | Visibility of `maff0000/mt5-gateway` (public today per MT5-READINESS; an earlier record says private) | owner confirms | owner decision, outside this portfolio; lane D evidence is treated as public-level meanwhile | none (flagged) |
| PD-12 | Evidence PR spread for lanes D and F (one primary PR plus companion notes versus one PR per repo) | primary + companion notes | primary + companion notes, to bound the PR count | lane PIDs |

## 13. Method and limits

Read, read-only, on 2026-10-15: GOAL `main` @ `1739e74` documents listed in `pids/GOLD-MVP-001.md` Evidence; PR #5 and #6 file lists via `gh`; branch diffs and the reconciliation summary; the contract/trigger PIDs' headings and Current state; MT5 readiness headings and PR topology; TRON D1 ratification package head; GROUP-E, RECON-H1 and RECON-H2 excerpts; local git logs of the HELIOS and GOLD-STRATEGY-RUNTIME clones. Consolidation edit (later the same day): the seven drafted branches were merged into one branch and all six lane PIDs were read; sections 1 to 3a, 7.1, 8.3, 10, 11 and 12 were reconciled to them. Not done: no production system, Redis, broker, container or database was accessed; component repositories beyond the cited excerpts were not audited (that is what the audits are for). Statements about the content of the PROD XAUUSD publication, the location of the earlier HERMES to HELIOS integration, and the TRON/MT5 implementation candidates are UNVERIFIED here by design. No `goal-docs --write`, no backlog edit, no `pid_path`, no approval record, no dispatch, no push.

# GOLD-AUD-F — Lane F audit: CER / HSA / DARWIN / NEO qualification-to-review path

**Lane:** research  
**Target repository:** `maff0000/GOAL`  
**Priority:** P1  
**Risk:** Low  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE (read-only audit; evidence PRs into component repositories, GOAL cross-index)  
**Complements:** `CER-R1`, `NEO-R1`, `HSA-C1`, `DARWIN-R2` (none amended; Deliverable 8 holds ready-to-apply amendment text)

Header values are PROVISIONAL: the item is not in `backlog/backlog.yaml`; the backlog patch is specified, not applied, in
`audits/2026-10-15/gold-mvp/PORTFOLIO.md` section 11. Lane vocabulary is the backlog set {shared, research, trading, ops}; `research` is used for all
six audits (CA frame). The PO sets final values.


## Status

DRAFT CANDIDATE for Central Architecture review. Not approved. Not DELIVERY_READY. No backlog row, `pid_path` or state change is made or implied by this document.

Frame (from the GOLD MVP master PID `GOLD-MVP-001`, drafted separately): audit id `GOLD-AUD-F`; lane research (read-only); `depends_on` `GOAL-DCP-001` only (CLOSED).

## Amend or new item (decision, justified)

**Decision: (ii) a thin new item, `GOLD-AUD-F`. Not an amendment of CER-R1, NEO-R1, HSA-C1 or DARWIN-R2.**

1. **The deliverable is a cross-component path, and no existing item owns a path.** DARWIN-R1/R2/R3, CER-R1, NEO-R1, HSA-C1 and LEAN-P1 each name one component repository and one build-shaped output. The CA question spans four repositories and one chain (qualify, register, execute, review). Amending any one row would make that row a cross-repository audit it was not sized or targeted for.
2. **The existing rows are not safe amendment hosts today.** RECON-G found NEO-R1 and CER-R1 mis-described (NEO exists and is not read-only; CER v1 is built and deployed; `EdgeProfileVersion` is defined nowhere). RECON-H1 found DARWIN-R2 ("ResearchEngineAdapter") and LEAN-P1 undefined in every repository, HSA-C1 not on `main`, and HSA absent from the backlog. Folding an audit into undefined or stale items would inherit their ambiguity.
3. **Duplication is avoided by composition, not restatement.** This item does not re-derive RECON-G/H1. It cites them by id, verifies what is still true at its own base SHA, adds only what they did not examine (the end-to-end GOLD path, evidence-class sufficiency for one strategy, the NEO read path, external evaluations), and **emits amendment text as a proposal** for CER-R1, NEO-R1, HSA-C1 and DARWIN-R2 (Deliverable 8). Whether to apply it stays a CA/PO act.
4. **It is cheap to retire.** If CA prefers amendments, Deliverable 8 is already the amendment text and this item can be cancelled after its single audit PR.

## Purpose

Establish, from evidence, how **one** GOLD (XAUUSD) strategy can be qualified, registered, executed and reviewed using functions that are already delivered, and exactly which hops are missing, so the MVP builds only the gaps and rebuilds nothing. Record the earlier external repository and SaaS evaluations and make a reuse recommendation only where it materially reduces MVP engineering. Define the minimum the first strategy needs, given that the learning loop closes only after the trigger path works.

## Current state

Read-only discovery 2026-10-15. Base: GOAL `main` at `1739e742154c77e9e2a96927dc40d4978b9cd798`. Labels: `[repo@sha]` read in a repository; `FABRIC-ONLY` rests on Memory Fabric and, per ADR-DELIVERY-001, repository evidence outranks it; `UNVERIFIED` not checked. No addresses, accounts or credentials are recorded.

**Reconciliation inputs (cited, not restated).** RECON-G (NEO, CER, SKEPTIC; analysis only, 2026-10-14) and RECON-H1 (data chain; analysis only, 2026-10-14), both on GOAL branches over base `1739e74`. Their findings F1-F12 (G) and the three-representation finding (H1) are inputs; their decisions D1-D7 (G) and D-1..D-5 (H1) are referenced by id below and not re-argued.

**Strategy versioning.** Three live representations with no shared contract (RECON-H1): HSA `strategy_package` (authoring), HELIOS `helios.strategy_package/1.0.0` (runtime), DARWIN A-007 canonical JSON to immutable `StrategyVersion` with semantic fingerprint (research). HSA enforces immutable-once-promoted in code and has `derive_candidate` and lineage [HSA@279ec18 `hsa/versioning.py`, `docs/VERSIONING.md`]. DARWIN holds `strategy_versions` and compiled plan tables [DARWIN@bf1142b migrations 0001, 0006, 0012]. CER has `Strategy` and `StrategyVersion` records, write-only through the API [CER@60eae45]. The only GOLD candidate found is HSA `gold_context_breakout` 1.0.0 (XAUUSD; 4H moving-average cross context, 5M breakout trigger), `lifecycle.status = CANDIDATE`, with `evidence.json` beside it.

**Evidence storage.** CER v1.0.0 is merged (PR #1), independently audited PRODUCT_GREEN, and deployed as two instances (dev, prod), prod empty (RECON-G). It has 20 controlled evidence classes (research, historical BACKTEST / OUT_OF_SAMPLE / WALK_FORWARD / MONTE_CARLO / PARAMETER_SWEEP / ABLATION, forward SHADOW / PAPER / MT5_DEMO / PLUTUS, live, and NEO_OBSERVATION / NEO_HYPOTHESIS / REGIME_ANALYSIS / DRIFT_ALERT / STRATEGY_HEALTH), hash-addressed artifacts, idempotent writes, provenance-completeness marking, 10 promotion states, 5 health states, and endpoints for evidence, artifacts, promotions and health records. Known limits [CER `docs/KNOWN-LIMITATIONS.md`]: runs, experiments and strategies are write-only; evidence citations are not resolved (ADR-001: unresolved is not verified support). DARWIN keeps its own `evidence_records` and `research_runs` tables.

**Causal-testing capability.** DARWIN APOLLO core (PID-006B, PR #24, merged 2026-10-02, `GREEN_DARWIN_PID006B_XAUUSD_CAUSAL_CORE_ACCEPTED`): deterministic next-bar-open replay, stop-first same-bar, wick touches, MAE/MFE, mark-to-market equity, preflight identity checks, persistence [DARWIN `darwin/apollo/*`, about 2,700 lines]. Bounded scope: one XAUUSD timeframe, one dataset, ATOMIC entry composition, LONG only, single position, fixed research quantity [WO-PID006B-001]. Every 006B run is `APOLLO_RESULT`, never `APOLLO_PROOF`. PID-006C (execution completeness) onward is not delivered. `darwin/athena` and `darwin/qualification` are 4-line placeholders. The gold candidate above is multi-timeframe and chained, so it appears **outside** the 006B scope (to be confirmed by the audit, not assumed).

**Deployment gap.** The running DARWIN image is the 2026-09 hotfix build, byte-identical to `8def7a1`, which is not an ancestor of `main`; it lacks the workshop, research-contract and APOLLO packages and migrations 0006-0013 (DARWIN-R1 PID draft, evidence read 2026-10-14). Applied live migrations UNVERIFIED by this item.

**Promotion.** CER carries the `PromotionTransition` record and state vocabulary; HSA refuses in-place mutation of a promoted version; DARWIN PID defers CER registration until about five promising XAUUSD candidates exist (DARWIN PID section 22). No document states **who authorises a transition or what evidence a transition must cite**. `EdgeProfileVersion` is defined nowhere (RECON-G F5; decision D2).

**Execution.** HELIOS v1 (PR #1, PRODUCT_GREEN) loads HSA package sets through `helios/integration/hsa_boundary.py` and refuses unresolved chain components and nearest-version binding. GOLD-STRATEGY-RUNTIME (RUNTIME_PRODUCT_GREEN, assurance-tooling residual) deploys HSA, HELIOS and CER together. HELIOS publishes to FALCON; the GOAL design routes the trigger through TRON, which has no runtime (RECON-G F9; PLATFORM-RT-001 candidate). Whether HELIOS checks a CER promotion state before loading a version is UNVERIFIED.

**NEO (private repository `maff0000/neo`, checkout on the Trinity host).** Last commit 2026-05-26 `3d92152`; working tree has two modified tracked scripts and one untracked script (RECON-G). Components: observer, scorers, auditor, coach, librarian, competition, session close, regime audit, strategy-health consumer (reads only R2D2 health envelopes, advisory, no execution authority). **Observer failing:** re-observed 2026-10-15 15:39 UTC, the per-minute cycle logs `FATAL: neo:config:observer not found in Memory Fabric`; the key is absent from Fabric (`neo:config:*` holds only mode, coach, errors, structural_events); first failure 2026-07-17 (RECON-G, FABRIC-ONLY). Why the key vanished is UNVERIFIED. **Execution:** a Practice-account order bridge and dispatcher exist in the scripts; the practice account was auto-paused 2026-09-22 (FABRIC-ONLY). **Not present:** any CER client, MCP server, or GOAL contract usage. The practice executor is not to be run by this item.

**External repository and SaaS evaluations found (read-only).** Search covered `/srv` component repositories (DARWIN, CER, HSA, HELIOS, GOLD-STRATEGY-RUNTIME, tron, GOAL) and Fabric key names on both hosts. Findings:

| Evaluated | Kind | Source | Date | Verdict recorded | Reuse recommendation recorded | New third-party service? |
|---|---|---|---|---|---|---|
| cloudQuant fork of backtrader (GPL-3.0) | library | Fabric `trinity:repo_review:backtrader:v1` (FABRIC-ONLY) | 2026-09-19 | ADOPT as backtest and live engine under R2D2 | Verify its test claims before gating capital | No (library); live-capable, so execution use is out of scope here |
| kernc/backtesting.py (AGPL-3.0) | library | `trinity:repo_review:backtesting_py:v1` | 2026-09-19 | ADOPT as fast-iteration front end | Sketch only; passing is never validation | No |
| OpenBB (AGPL-3.0) | data platform | `trinity:repo_review:openbb:v1` | 2026-09-19 | ADOPT for macro and fundamentals data | Context only, not a live feed; default price feed is an unofficial scraper | Yes if used (data provider) |
| FinceptTerminal (AGPL-3.0) | desktop app | `trinity:repo_review:fincept_terminal:v1` | 2026-09-19 | ADOPT as personal research console | Not wired to pipeline | No |
| TradingAgents (Apache-2.0) | multi-agent LLM | `trinity:repo_review:tradingagents:v1` | 2026-09-19 | ADOPT on demand for due diligence | One opinion, never a signal | Implies external model calls (provider UNVERIFIED) |
| ai-hedge-fund (MIT) | multi-agent LLM | `trinity:repo_review:ai_hedge_fund:v1` | 2026-09-19 | ADOPT for long-horizon only; wrong tool for day trading | Not applicable to GOLD | Implies external model calls |
| Alpaca MCP server | vendor SaaS | `trinity:repo_review:alpaca_mcp:v1` | 2026-09-19 | SKIP | None (duplicates governed paper stack; conversational orders bypass governance) | Yes |
| daily_stock_analysis; macro-monitoring; recession-radar; macro-regime-nowcaster | repos | `trinity:repo_review:SYNTHESIS:v1` | 2026-09-19 | reject / park (methodology only) | None for GOLD | No |
| Risk and position-sizing open source | gap search | `trinity:repo_review:risk_management_position_sizing_gap:v1` | 2026-09-19 | No credible candidate; build in-house | Build as governed WO | n/a |
| Internal legacy reuse assessments (HSA, HELIOS, ATHENA, DIKE) | internal code | DARWIN `docs/archaeology/*` | 2026-09 | Per-function REUSE / ADAPT / DO_NOT_REUSE | HSA identity, immutability, versioning, validation reuse; atomic conditions do not | No |

Not found: any evaluation of QuantConnect or LEAN, vectorbt, zipline, freqtrade, nautilus, qlib, MLflow or any experiment-tracking SaaS. `LEAN-P1` is defined nowhere and whether it means an external engine is UNVERIFIED (RECON-H1 P-10). The backtrader and backtesting.py reviews predate APOLLO core (merged 2026-10-02), so their "engine under APOLLO" premise is stale. Detail was read for seven of the twelve reviews; the other five are taken from the index and synthesis only.

## Target outcome

At closure the component repositories and GOAL hold a dated, reproducible audit record that:

1. Names the existing function for every hop of the one-GOLD-strategy path and marks it **exists / partial / missing**, with citations and a re-runnable command or file reference per mark.
2. States which delivered functions the MVP must reuse unchanged, and lists "do not rebuild" items.
3. States the MVP minimum for the first strategy and its sequence relative to the trigger path.
4. Records every external evaluation with source, date, verdict and reuse recommendation, and flags any third-party service.
5. Gives CA ready-to-apply amendment text for CER-R1, NEO-R1, HSA-C1 and DARWIN-R2, and a list of undefined terms needing a ruling.
6. Changes no runtime, no backlog, and no repository other than by evidence documents.

## Scope

1. Versioning audit: map HSA, HELIOS, DARWIN and CER strategy identity for `gold_context_breakout` 1.0.0; test whether the same identity and fingerprint survive each hop; list representation gaps (RECON-H1 D-1).
2. Evidence audit: for one GOLD strategy, which CER evidence classes are required at each promotion state, which already have a writer, and which have none.
3. Causal-testing audit: whether APOLLO 006B scope can test the gold candidate; what `APOLLO_RESULT` can and cannot claim; deployment gap to the running DARWIN.
4. Promotion audit: transition authority, evidence citation rule (ADR-001), HSA immutability versus CER state, and whether HELIOS refuses an unpromoted version.
5. NEO review audit: observer failure cause class (read-only), read path to CER, the strategy-health authority split (RECON-G D4), and the practice executor assessed by reading only.
6. Path matrix and MVP minimum (Deliverables 2 and 3).
7. External evaluation register and reuse recommendations (Deliverable 4).
8. Cross-index in GOAL: a pointer record to the component evidence PRs.

## Non-goals

- No research platform expansion: no new backtest engine, no ATHENA, no experiment-tracking platform, no UI.
- No new third-party service, repository dependency or SaaS as a prerequisite for the MVP (CA).
- No strategy design, tuning, or claim about edge or performance.
- No backlog edit, `pid_path`, `DELIVERY_READY`, approval, or state change; no `goal-docs --write`.
- No deployment, migration, restart or repair, including the NEO observer and the DARWIN runtime.
- No definition of `EdgeProfileVersion`, `ResearchEngineAdapter` or `LEAN`; the audit only records that they are undefined and what depends on them.
- No broker contact and no run of NEO's practice executor or of any order path.

## Dependencies and interfaces

- **Hard dependency (backlog):** `GOAL-DCP-001` (CLOSED). Nothing else.
- **Reads, does not depend on:** RECON-G, RECON-H1; DARWIN-R1 PID draft (deployment truth); GOAL-STRAT-ADR-001 and HSA-C1 (proposed, not on `main`); the TRON and HELIOS-T3 design for the trigger path.
- **Component repositories receiving evidence PRs:** `maff0000/CER`, `maff0000/HSA`, `maff0000/DARWIN`, `maff0000/neo`. Each PR is documents only. The `neo` PR needs PO approval because the repository is private and carries an order bridge.
- **Needs authority outside FORGE:** read access on the dell host and Trinity host held by HELM; Fabric reads under read-only use.
- **Collisions:** `/srv/NEO` holds uncommitted work; the audit works from its own clone and never edits that checkout. RECON-G NEO-R0 (reconciliation) and DARWIN-R1 may run in parallel; findings are cross-referenced, not merged.

## Safety boundaries

- Read-only on all systems except the audit's own worktree and clones. No production mutation, no database write, no container action.
- NEO never makes a discretionary live trade, sizing or risk action (RECON-G prohibitions 1-6). The NEO practice executor is **assessed from source, never run, imported or scheduled**.
- No broker calls. No credentials printed, read or recorded; report credential-bearing paths as path and mode only.
- GOAL is public: no addresses, hostnames of internal services, ports, accounts or credentials in any committed file; say "the dell host" and "the Trinity host". Component evidence for private repositories stays in those repositories.
- Run `./tools/secret-scan` and a manual grep for address and key-like strings before every commit.
- External repositories are read as documents only: nothing is installed, executed or called.

## Deliverables

1. **Audit record** (`audits/<date>/gold-aud-f/AUDIT-F.md` in GOAL, sanitised) with, per CA evidence item below, the finding, citation and verdict.
2. **Qualification-to-review path matrix.** Hops (each marked exists / partial / missing with evidence):

| # | Hop | Existing function | Preliminary mark (to be proven) |
|---|---|---|---|
| 1 | Author candidate | HSA `gold_context_breakout` 1.0.0, CANDIDATE | exists |
| 2 | Canonical identity (`StrategyVersion` fingerprint) | DARWIN A-007 doctrine, finalise; no HSA-to-DARWIN importer | partial |
| 3 | Causal test | APOLLO 006B (single timeframe, ATOMIC, LONG); gold candidate is chained, two timeframes | partial |
| 4 | Qualification verdict (proof-grade) | `APOLLO_PROOF` gate, `darwin/qualification`, ATHENA placeholders | missing |
| 5 | Deployed qualification runtime | live image lacks APOLLO and migrations 0006-0013 | missing |
| 6 | Register in CER (strategy, version, evidence) | CER write endpoints; no DARWIN or HSA writer; read-back absent | partial |
| 7 | Promotion transition and authority | CER promotions, HSA immutability; no authority or citation rule | partial |
| 8 | Execute approved version | HELIOS loads HSA package; promotion check UNVERIFIED; trigger path to TRON missing | partial |
| 9 | Review (NEO) | NEO scripts exist; observer failing; no CER read path | partial |
| 10 | Feedback to research (hypothesis intake) | `NEO_HYPOTHESIS` class exists; DARWIN intake absent | missing |

3. **MVP minimum for the first GOLD strategy** (proposal for CA, sequenced after the trigger path works): one frozen identity (`strategy_id@version` plus package hash) recorded in CER; one clearly non-proof backtest evidence record with artifact hash from an engine that already exists; one PO-recorded promotion transition citing that evidence; HELIOS running exactly that version; and a **read-only NEO review report** (human-readable, one strategy, CER plus fires) rather than the full evidence gateway. Deferred beyond MVP: ATHENA, DARWIN-to-CER automation, hypothesis intake, `EdgeProfileVersion`, SKEPTIC. The audit states, with evidence, which of these items are truly needed before the first live-like trigger and which only after.
4. **External evaluation register** (the table above, re-verified, with licence-compatibility and service-dependency flags) and **reuse recommendations**, each stating the engineering saved or "none", the licence constraint, and whether it adds a third-party service. Default recommendation: no external engine is adopted for the MVP; an optional independent cross-check against APOLLO is recorded only if it saves work, using a library with no service dependency.
5. **No-rebuild register:** delivered functions the MVP must reuse (HSA versioning and validation, DARWIN StrategyVersion and APOLLO core, CER registry and promotion records, HELIOS HSA boundary, GOLD-STRATEGY-RUNTIME, NEO strategy-health consumer).
6. **Gap list** with owner, mapped to existing backlog ids or marked "no home".
7. **Cross-index** in GOAL listing the four component evidence PRs and their merge SHAs.
8. **Amendment text proposals** (not applied) for CER-R1, NEO-R1, HSA-C1 and DARWIN-R2, plus candidate rows only where a gap has no home. Informed by RECON-G S1-S8 and RECON-H1 P-14.

CA's ten mandatory evidence items, in CA's numbering, as carried by `AUDIT-F.md`:

CA's ten mandatory evidence items, in CA's numbering (the numbering is CA's and is not to be changed by a lane): (1) PID/WO identifier and exact audited scope; (2) source repositories, revisions and relevant documentation references; (3) existing implementation: proven, partially proven, unverified or missing; (4) actual versus expected contract comparison; (5) tests, fixtures and evidence references; (6) specific defects and compatibility gaps; (7) reusable code and documentation; (8) minimum recommended implementation changes; (9) safety and deployment constraints; (10) independent audit verdict and any unresolved findings.

| CA # | CA evidence item | This audit puts it in | Proof method |
|---|---|---|---|
| 1 | PID/WO identifier and exact audited scope | AUDIT-F section 0: quoted scope (qualify, register, execute, review one GOLD strategy) | Quote equals approved PID |
| 2 | Source repositories, revisions and documentation references | Base SHAs for GOAL, DARWIN, CER, HSA, HELIOS, GOLD-STRATEGY-RUNTIME and neo; documentation references; the external evaluation sources (Deliverable 1 and 4) | Auditor re-reads each at the SHA |
| 3 | Existing implementation: proven, partially proven, unverified or missing | Path matrix of 10 hops, each exists / partial / missing with a re-runnable citation (Deliverable 2): strategy versioning, evidence storage, causal testing, promotion, NEO review | Every hop has a mark and a citation |
| 4 | Actual versus expected contract comparison | Representation comparison HSA / HELIOS / DARWIN / CER for `gold_context_breakout` 1.0.0 (identity and fingerprint across hops), evidence-class sufficiency per promotion state, APOLLO 006B scope versus the candidate | Same identity and fingerprint tested hop to hop |
| 5 | Tests, fixtures and evidence references | Re-runnable commands, count checks (10 hops; every `trinity:repo_review:*` key and archaeology document in the register), before and after identity snapshots | Snapshots equal; counts match |
| 6 | Specific defects and compatibility gaps | Gap list with owner or 'no home' (Deliverable 6): deployment gap, undefined `EdgeProfileVersion`, NEO observer failure, no APOLLO_PROOF runs | Each missing mark names an owner or 'no home' |
| 7 | Reusable code and documentation | No-rebuild register (Deliverable 5) and external evaluation register with reuse recommendations, licence and service flags (Deliverable 4) | Each reuse recommendation names the engineering saved and any new service |
| 8 | Minimum recommended implementation changes | MVP minimum for the first GOLD strategy and sequencing against the trigger path (Deliverable 3); amendment text proposals for CER-R1, NEO-R1, HSA-C1, DARWIN-R2 (Deliverable 8), not applied | Each change maps to an existing item or 'no home' |
| 9 | Safety and deployment constraints | Safety and deployment constraints: NEO practice executor assessed from source only, no broker call, no installation of evaluated code, licence posture (D9), no third-party service as a prerequisite | No outbound call to any evaluated service in the record; secret-scan clean |
| 10 | Independent audit verdict and unresolved findings | Independent auditor (AUD-3) verdict file with unresolved findings; evidence PR list with SHAs | Fresh auditor GREEN with exact SHAs; PO acceptance recorded |

## Acceptance

GREEN requires, mechanically:

1. Every matrix hop carries an exists / partial / missing mark and at least one citation (repository path with commit SHA, or a command with its captured output) that an auditor re-runs and reproduces.
2. A count check passes: the matrix has 10 hops, the evidence table has CA items 1 to 10, the external register lists every Fabric key under `trinity:repo_review:*` and every legacy reuse document under DARWIN `docs/archaeology/`.
3. `./tools/goal-validate` and `./tools/secret-scan` are GREEN on every GOAL commit; a grep for IPv4 addresses, ports and key-like strings over all committed files returns nothing.
4. Before and after each inspected system, identity is unchanged: git HEAD of each inspected checkout, container ids and start times, and `git status` are recorded and equal. No file under `/srv/NEO`, `/srv/DARWIN`, `/srv/CER` or `/srv/HSA` changed.
5. No external code was installed or executed; no outbound call to any evaluated service is in the record.
6. No backlog, `pid_path` or state change in the diff; `./tools/goal-docs` reports no write.
7. Each missing mark names an owner or "no home"; each "reuse" recommendation names the engineering saved and any new service.
8. Fresh independent FORGE Auditor GREEN; evidence PR list with exact SHAs; PO acceptance recorded in GitHub.

## Stop conditions

Return to the PO if:

- the audit needs a write to any live system, database, Fabric key or broker;
- reading `maff0000/neo` or a private store would expose a credential;
- the running DARWIN or HELIOS provenance cannot be established read-only;
- a recommendation would require a third-party service as an MVP prerequisite;
- the audit finds a second order-placing path reachable by NEO that is not already recorded;
- evidence contradicts RECON-G or RECON-H1 materially (report the contradiction, do not resolve it).

Do not invent around a stop condition.

## Open decisions

**D1 — Amend or new item (blocks approval).** Recommended: new thin item (section above). Alternative: apply Deliverable 8 as amendments and cancel this item. Owner PO.

**D2 — Which strategy is "the first GOLD strategy" (blocks approval).** `gold_context_breakout` 1.0.0 is the only candidate found and may sit outside APOLLO 006B scope; a simpler single-timeframe candidate may be the MVP choice. Owner PO; Matt if it is a capital-risk choice.

**D3 — Strategy representation authority (RECON-H1 D-1; blocks hop 2 conclusions, not this audit).** Owner PO.

**D4 — `EdgeProfileVersion` (RECON-G D2; blocks CER-R1 and TRON-T5).** Defined nowhere. The audit reports whether the MVP needs it. Owner PO.

**D5 — NEO legacy practice executor and boundary wording (RECON-G D1; blocks the `neo` evidence PR scope).** Assessed only; disposition is not decided here. Owner PO.

**D6 — Strategy-health authority (RECON-G D4; blocks hop 9 design, not audit).** Owner PO.

**D7 — Meaning or fate of `LEAN-P1` and `DARWIN-R2` (RECON-H1 D-5, P-10; later).** Owner PO.

**D8 — Retired.** CA's numbered evidence list has been supplied and applied (see Deliverables); no decision remains.

**D9 — Licence posture for GPL / AGPL libraries (blocks any reuse recommendation being acted on).** backtrader fork is GPL-3.0 and backtesting.py is AGPL-3.0; compatibility with the repository visibility and licence of DARWIN and GOAL is UNVERIFIED. Owner PO.

**D10 — Evidence PR into private `maff0000/neo` (blocks that PR).** Owner PO.

## Evidence

- GOAL `main` at `1739e742154c77e9e2a96927dc40d4978b9cd798`: `backlog/backlog.yaml`, `backlog/SCHEMA.md`, `pids/GOAL-DCP-001.md`, tool validator source (PID format).
- RECON-G and RECON-H1 (analysis records, 2026-10-14), DARWIN-R1 PID draft (2026-10-14).
- DARWIN `bf1142b` (`main`): `PID.md`, amendment A-007, PID-006, WO-PID006B-001, `darwin/apollo/*`, migrations 0001-0013 (table names only), `docs/archaeology/*`.
- CER `60eae45`: `PID.md`, `src/cer/contract/enums.py`, `src/cer/api/routes.py` (route list), `docs/KNOWN-LIMITATIONS.md`.
- HSA `279ec18`: `strategies/gold_context_breakout/1.0.0/package.json` (lifecycle only), `docs/VERSIONING.md`.
- HELIOS `7f7193d`: `helios/integration/hsa_boundary.py`; GOLD-STRATEGY-RUNTIME `5891415`: `docs/ARCHITECTURE.md`.
- NEO on the Trinity host: `git log`, `git status`, scheduler table (names only), tail of the observer log, script names; Fabric key names under `neo:config:*`.
- Fabric key reads (read-only, FABRIC-ONLY): `trinity:repo_review:*` (12 reviews, index, synthesis).
- Not accessed: live databases, credential files and `.env` contents, TRON runtime (none), NEO Practice account state, any broker, any external service.

## Evidence PR checklist

- [ ] `maff0000/DARWIN`: strategy identity, APOLLO scope, deployment-gap record (documents only). PR link and SHA: ____
- [ ] `maff0000/CER`: evidence-class sufficiency, promotion authority and citation record (documents only). PR link and SHA: ____
- [ ] `maff0000/HSA`: gold candidate identity, handoff and immutability record (documents only). PR link and SHA: ____
- [ ] `maff0000/neo`: review architecture, observer failure class, executor assessment (documents only; PO-approved, D10). PR link and SHA: ____
- [ ] `maff0000/GOAL`: audit record, matrix, external register, amendment proposals, cross-index. PR link and SHA: ____
- [ ] Each PR passes secret-scan; no address, port, account or credential text
- [ ] Before and after identity snapshots attached and equal (Acceptance 4)
- [ ] CA evidence items 1 to 10 each present in `AUDIT-F.md` in CA numbering
- [ ] Fresh independent FORGE Auditor verdict recorded

## Approval

PENDING. No approval has been recorded for this PID candidate. Approval is recorded here by Central Architecture/PO only.

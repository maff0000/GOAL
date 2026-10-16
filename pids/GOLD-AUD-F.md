# GOLD-AUD-F — Lane F audit: CER / HSA / DARWIN / NEO qualification-to-review path

**Lane:** research  
**Target repository:** `maff0000/GOAL`  
**Evidence:** primary PR in `maff0000/GOAL`, branch `wo/GOLD-AUD-F-evidence`, path `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/`; mirror notes on branch `wo/GOLD-AUD-F-evidence` in each of `CER`, `HSA`, `DARWIN` and `neo`, path `docs/evidence/GOLD-AUD-F/`  
**Priority:** P1  
**Risk:** Low  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  
**Complements:** `CER-R1`, `NEO-R1`, `HSA-C1`, `DARWIN-R2`  

**Header notes:** GOAL is the primary repository, with mirror notes in CER, HSA, DARWIN and neo (the `neo` note is sanitised because that repository is private). Delivery is a read-only audit: one primary GOAL evidence PR, mirror notes into the component repositories, then a GOAL index entry. None of the complemented items is amended (Deliverable 8 holds ready-to-apply amendment text). Evidence location follows programme-controller rulings 1 to 3 (`PORTFOLIO.md` appendix).

Header values match the registered backlog item (`backlog/backlog.yaml`, `pid_path: pids/GOLD-AUD-F.md`). Lane vocabulary is the backlog set {shared, research, trading, ops}; `research` is used for all
six audits (CA frame). Priority, lane and risk follow the CA/PO adjudication 2026-10-15 (recorded in `PORTFOLIO.md`, not in this PID); approval is recorded in the Approval section below.


## Status

APPROVED (Central Architecture, 16 October 2026; see Approval). Registered in the backlog as DELIVERY_READY by the governed amendment.

Frame (from the GOLD MVP master PID `GOLD-MVP-001`, drafted separately): audit id `GOLD-AUD-F`; lane research (read-only); `depends_on` `GOAL-DCP-001` only (CLOSED).

## Amend or new item (decision, justified)

**Decision: (ii) a thin new item, `GOLD-AUD-F`. Not an amendment of CER-R1, NEO-R1, HSA-C1 or DARWIN-R2.**

1. **The deliverable is a cross-component path, and no existing item owns a path.** DARWIN-R1/R2/R3, CER-R1, NEO-R1, HSA-C1 and LEAN-P1 each name one component repository and one build-shaped output. The CA question spans four repositories and one chain (qualify, register, execute, review). Amending any one row would make that row a cross-repository audit it was not sized or targeted for.
2. **The existing rows are not safe amendment hosts today.** RECON-G found NEO-R1 and CER-R1 mis-described (NEO exists and is not read-only; CER v1 is built and deployed; `EdgeProfileVersion` is defined nowhere). RECON-H1 found DARWIN-R2 ("ResearchEngineAdapter") and LEAN-P1 undefined in every repository, HSA-C1 not on `main`, and HSA absent from the backlog. Folding an audit into undefined or stale items would inherit their ambiguity.
3. **Duplication is avoided by composition, not restatement.** This item does not re-derive RECON-G/H1. It cites them by id, verifies what is still true at its own base SHA, adds only what they did not examine (the end-to-end GOLD path, evidence-class sufficiency for one strategy, the NEO read path, external evaluations), and **emits amendment text as a proposal** for CER-R1, NEO-R1, HSA-C1 and DARWIN-R2 (Deliverable 8). Whether to apply it stays a CA/PO act.
4. **It is cheap to retire.** If CA prefers amendments, Deliverable 8 is already the amendment text and this item can be cancelled after its single audit PR.

## Purpose

Establish, from evidence, how **one** GOLD (XAUUSD) strategy can be qualified, registered, executed and reviewed using functions that are already delivered, and exactly which hops are missing, so the MVP builds only the gaps and rebuilds nothing. Record the earlier external repository and SaaS evaluations as **information only**. Define the minimum the one governed strategy needs, given that the learning loop closes only after the trigger path works.

**CA guidance 2026-10-15 applied (items 4 and 6).** (4) Binding constraint: the MVP takes no new third-party engine or SaaS dependency. The external evaluations in this PID are information only; none is an MVP option, none is recommended for adoption, and the licence-posture question (former D9) is moot for the MVP. (6) This audit selects no strategy and does not assume one. The path matrix is strategy-neutral: it is evaluated for each HSA candidate under review (currently `gold_context_breakout` 1.0.0 and `wick_rejection_sequence` 0.1.0, as listed by lane B; neither is selected, preferred or implied). Strategy selection is a PO decision taken only after audit A (PROD facts) and audit B (candidate requirements versus PROD facts) have reported and been reconciled.

## Current state

Read-only discovery 2026-10-15. Base read: GOAL `main` at `1739e742154c77e9e2a96927dc40d4978b9cd798`; baseline now `90323b3`. Labels: `[repo@sha]` read in a repository; `FABRIC-ONLY` rests on Memory Fabric and, per ADR-DELIVERY-001, repository evidence outranks it; `UNVERIFIED` not checked. No addresses, accounts or credentials are recorded.

**Reconciliation inputs (cited, not restated).** RECON-G (NEO, CER, SKEPTIC; analysis only, 2026-10-14) and RECON-H1 (data chain; analysis only, 2026-10-14), both on GOAL branches over base `1739e74`. Their findings F1-F12 (G) and the three-representation finding (H1) are inputs; their decisions D1-D7 (G) and D-1..D-5 (H1) are referenced by id below and not re-argued.

**Strategy versioning.** Three live representations with no shared contract (RECON-H1): HSA `strategy_package` (authoring), HELIOS `helios.strategy_package/1.0.0` (runtime), DARWIN A-007 canonical JSON to immutable `StrategyVersion` with semantic fingerprint (research). HSA enforces immutable-once-promoted in code and has `derive_candidate` and lineage [HSA@279ec18 `hsa/versioning.py`, `docs/VERSIONING.md`]. DARWIN holds `strategy_versions` and compiled plan tables [DARWIN@bf1142b migrations 0001, 0006, 0012]. CER has `Strategy` and `StrategyVersion` records, write-only through the API [CER@60eae45]. HSA holds two XAUUSD candidates under review, both `lifecycle.status = CANDIDATE` and neither selected: `gold_context_breakout` 1.0.0 (4H moving-average cross context, 5M breakout trigger, with `evidence.json` beside it) and `wick_rejection_sequence` 0.1.0 (15M location and confirmation, 5M trigger; lane B).

**Evidence storage.** CER v1.0.0 is merged (PR #1), independently audited PRODUCT_GREEN, and deployed; the audit establishes what is deployed (RECON-G). It has 20 controlled evidence classes (research, historical BACKTEST / OUT_OF_SAMPLE / WALK_FORWARD / MONTE_CARLO / PARAMETER_SWEEP / ABLATION, forward SHADOW / PAPER / MT5_DEMO / PLUTUS, live, and NEO_OBSERVATION / NEO_HYPOTHESIS / REGIME_ANALYSIS / DRIFT_ALERT / STRATEGY_HEALTH), hash-addressed artifacts, idempotent writes, provenance-completeness marking, 10 promotion states, 5 health states, and endpoints for evidence, artifacts, promotions and health records. Known limits [CER `docs/KNOWN-LIMITATIONS.md`]: runs, experiments and strategies are write-only; evidence citations are not resolved (ADR-001: unresolved is not verified support). DARWIN keeps its own `evidence_records` and `research_runs` tables.

**Causal-testing capability.** DARWIN APOLLO core (PID-006B, PR #24, merged 2026-10-02, `GREEN_DARWIN_PID006B_XAUUSD_CAUSAL_CORE_ACCEPTED`): deterministic next-bar-open replay, stop-first same-bar, wick touches, MAE/MFE, mark-to-market equity, preflight identity checks, persistence [DARWIN `darwin/apollo/*`, about 2,700 lines]. Bounded scope: one XAUUSD timeframe, one dataset, ATOMIC entry composition, LONG only, single position, fixed research quantity [WO-PID006B-001]. Every 006B run is `APOLLO_RESULT`, never `APOLLO_PROOF`. PID-006C (execution completeness) onward is not delivered. `darwin/athena` and `darwin/qualification` are 4-line placeholders. Both HSA candidates under review use two timeframes and a composed entry, so each appears **outside** the 006B scope (to be confirmed by the audit per candidate, not assumed).

**Deployment gap.** The audit establishes what is deployed and how it relates to `main` (deployment gap to be audited). Applied live migrations UNVERIFIED by this item.

**Promotion.** CER carries the `PromotionTransition` record and state vocabulary; HSA refuses in-place mutation of a promoted version; DARWIN PID defers CER registration until about five promising XAUUSD candidates exist (DARWIN PID section 22). No document states **who authorises a transition or what evidence a transition must cite**. `EdgeProfileVersion` is defined nowhere (RECON-G F5; decision D2).

**Execution.** HELIOS v1 (PR #1, PRODUCT_GREEN) loads HSA package sets through `helios/integration/hsa_boundary.py` and refuses unresolved chain components and nearest-version binding. GOLD-STRATEGY-RUNTIME (RUNTIME_PRODUCT_GREEN, assurance-tooling residual) deploys HSA, HELIOS and CER together. HELIOS publishes to FALCON; the GOAL design routes the trigger through TRON, which has no runtime (RECON-G F9; PLATFORM-RT-001 candidate). Whether HELIOS checks a CER promotion state before loading a version is UNVERIFIED.

**NEO (private repository `maff0000/neo`).** Components: observer, scorers, auditor, coach, librarian, competition, session close, regime audit, strategy-health consumer (reads only R2D2 health envelopes, advisory, no execution authority). **Observer and execution:** the audit establishes the operating state of the observer and whether any execution-capable tooling exists (source text only; nothing is run). **Not present:** any CER client, MCP server, or GOAL contract usage. The legacy practice-account tooling is not to be run by this item.

**External repository and SaaS evaluations found (read-only; information only, CA guidance 2026-10-15 item 4: none is an MVP option and none is recommended).** The verdict columns below record what the 2026-09-19 reviews said at the time; they are not recommendations of this item. Search covered the component repositories (DARWIN, CER, HSA, HELIOS, GOLD-STRATEGY-RUNTIME, tron, GOAL) and Fabric key names. Findings:

| Evaluated | Kind | Source | Date | Verdict recorded | Reuse note recorded (historical, 2026-09) | New third-party service? |
|---|---|---|---|---|---|---|
| cloudQuant fork of backtrader (GPL-3.0) | library | the memory-fabric review record identified in the audit (FABRIC-ONLY) | 2026-09-19 | ADOPT as backtest and live engine under R2D2 | Verify its test claims before gating capital | No (library); live-capable, so execution use is out of scope here |
| kernc/backtesting.py (AGPL-3.0) | library | the memory-fabric review record identified in the audit | 2026-09-19 | ADOPT as fast-iteration front end | Sketch only; passing is never validation | No |
| OpenBB (AGPL-3.0) | data platform | the memory-fabric review record identified in the audit | 2026-09-19 | ADOPT for macro and fundamentals data | Context only, not a live feed; default price feed is an unofficial scraper | Yes if used (data provider) |
| FinceptTerminal (AGPL-3.0) | desktop app | the memory-fabric review record identified in the audit | 2026-09-19 | ADOPT as personal research console | Not wired to pipeline | No |
| TradingAgents (Apache-2.0) | multi-agent LLM | the memory-fabric review record identified in the audit | 2026-09-19 | ADOPT on demand for due diligence | One opinion, never a signal | Implies external model calls (provider UNVERIFIED) |
| ai-hedge-fund (MIT) | multi-agent LLM | the memory-fabric review record identified in the audit | 2026-09-19 | ADOPT for long-horizon only; wrong tool for day trading | Not applicable to GOLD | Implies external model calls |
| Alpaca MCP server | vendor SaaS | the memory-fabric review record identified in the audit | 2026-09-19 | SKIP | None (duplicates governed paper stack; conversational orders bypass governance) | Yes |
| daily_stock_analysis; macro-monitoring; recession-radar; macro-regime-nowcaster | repos | the memory-fabric review record identified in the audit | 2026-09-19 | reject / park (methodology only) | None for GOLD | No |
| Risk and position-sizing open source | gap search | the memory-fabric review record identified in the audit | 2026-09-19 | No credible candidate; build in-house | Build as governed WO | n/a |
| Internal legacy reuse assessments (HSA, HELIOS, ATHENA, DIKE) | internal code | DARWIN `docs/archaeology/*` | 2026-09 | Per-function REUSE / ADAPT / DO_NOT_REUSE | HSA identity, immutability, versioning, validation reuse; atomic conditions do not | No |

Not found: any evaluation of QuantConnect or LEAN, vectorbt, zipline, freqtrade, nautilus, qlib, MLflow or any experiment-tracking SaaS. `LEAN-P1` is defined nowhere and whether it means an external engine is UNVERIFIED (RECON-H1 P-10). The backtrader and backtesting.py reviews predate APOLLO core (merged 2026-10-02), so their "engine under APOLLO" premise is stale. Licence posture of the GPL and AGPL entries is not assessed: it is moot for the MVP (CA guidance 2026-10-15, item 4). Detail was read for seven of the twelve reviews; the other five are taken from the index and synthesis only.

## Target outcome

At closure the component repositories and GOAL hold a dated, reproducible audit record that:

1. Names the existing function for every hop of the one-GOLD-strategy path and marks it **exists / partial / missing**, with citations and a re-runnable command or file reference per mark.
2. States which delivered functions the MVP must reuse unchanged, and lists "do not rebuild" items.
3. States the MVP minimum for the one governed strategy (strategy-neutral) and its sequence relative to the trigger path.
4. Records every external evaluation with source, date and recorded verdict as information only, and flags any third-party service; recommends none for the MVP.
5. Gives CA ready-to-apply amendment text for CER-R1, NEO-R1, HSA-C1 and DARWIN-R2, and a list of undefined terms needing a ruling.
6. Changes no runtime, no backlog, and no repository other than by evidence documents.

## Scope

1. Versioning audit: map HSA, HELIOS, DARWIN and CER strategy identity for each HSA candidate under review (no selection implied); test whether the same identity and fingerprint survive each hop; list representation gaps (RECON-H1 D-1).
2. Evidence audit: for one governed GOLD strategy (whichever the PO later selects), which CER evidence classes are required at each promotion state, which already have a writer, and which have none.
3. Causal-testing audit: whether APOLLO 006B scope can test each candidate under review; what `APOLLO_RESULT` can and cannot claim; deployment gap to the running DARWIN.
4. Promotion audit: transition authority, evidence citation rule (ADR-001), HSA immutability versus CER state, and whether HELIOS refuses an unpromoted version.
5. NEO review audit: observer cause class (read-only; recorded in the private record), read path to CER, the strategy-health authority split (RECON-G D4), and legacy practice-account tooling assessed by reading only.
6. Path matrix and MVP minimum (Deliverables 2 and 3).
7. External evaluation register, information only (Deliverable 4).
8. Index entry: after acceptance, one GOAL PR contributes a pointer record to the primary and mirror PRs into `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md` (owned by `GOLD-MVP-001`).

## Non-goals

- No research platform expansion: no new backtest engine, no ATHENA, no experiment-tracking platform, no UI.
- No new third-party engine, service, repository dependency or SaaS for the MVP (binding constraint, CA guidance 2026-10-15, item 4); no recommendation to adopt any evaluated item, and no licence-posture ruling.
- No strategy selection, ranking or recommendation (CA guidance 2026-10-15, item 6).
- No strategy design, tuning, or claim about edge or performance.
- No backlog edit, `pid_path`, `DELIVERY_READY`, approval, or state change; no `goal-docs --write`.
- No deployment, migration, restart or repair, including the NEO observer and the DARWIN runtime.
- No definition of `EdgeProfileVersion`, `ResearchEngineAdapter` or `LEAN`; the audit only records that they are undefined and what depends on them.
- No broker contact and no run of legacy practice-account tooling or of any order path.

## Dependencies and interfaces

- **Hard dependency (backlog):** `GOAL-DCP-001` (CLOSED). Nothing else.
- **Reads, does not depend on:** RECON-G, RECON-H1; DARWIN-R1 PID draft (deployment truth); GOAL-STRAT-ADR-001 and HSA-C1 (proposed, not on `main`); the TRON and HELIOS-T3 design for the trigger path.
- **Component repositories receiving mirror-note PRs:** `maff0000/CER`, `maff0000/HSA`, `maff0000/DARWIN`, `maff0000/neo`. Each PR is documents only, under `docs/evidence/GOLD-AUD-F/`. The `neo` mirror note is sanitised before anything is placed in GOAL and needs PO approval because the repository is private and carries legacy practice-account tooling (open decision D10).
- **Needs authority outside FORGE:** read access to the estate hosts held by HELM; Fabric reads under read-only use.
- **Collisions:** the NEO repository may hold uncommitted work; the audit works from its own clone and never edits an existing checkout. RECON-G NEO-R0 (reconciliation) and DARWIN-R1 may run in parallel; findings are cross-referenced, not merged.

## Safety boundaries

- Read-only on all systems except the audit's own worktree and clones. No production mutation, no database write, no container action.
- NEO never makes a discretionary live trade, sizing or risk action (RECON-G prohibitions 1-6). Legacy practice-account tooling and the legacy trading executors are **assessed from source (inspection permitted, CA/PO adjudication 2026-10-15), never run, modified, imported or scheduled**.
- No broker calls. No credentials printed, read or recorded; report credential-bearing paths as path and mode only.
- GOAL is public: no addresses, hostnames of internal services, ports, accounts or credentials in any committed file; use generic role names only. Component evidence for private repositories stays in those repositories.
- Run `./tools/secret-scan` and a manual grep for address and key-like strings before every commit.
- External repositories are read as documents only: nothing is installed, executed or called.

## Deliverables

1. **Audit record** (`audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/AUDIT-F.md` in GOAL, sanitised, primary evidence PR on branch `wo/GOLD-AUD-F-evidence`) with, per CA evidence item below, the finding, citation and verdict.
2. **Qualification-to-review path matrix.** Hops (each marked exists / partial / missing with evidence):

| # | Hop | Existing function | Preliminary mark (to be proven) |
|---|---|---|---|
| 1 | Author candidate | HSA candidates under review (none selected), CANDIDATE | exists |
| 2 | Canonical identity (`StrategyVersion` fingerprint) | DARWIN A-007 doctrine, finalise; no HSA-to-DARWIN importer | partial |
| 3 | Causal test | APOLLO 006B (single timeframe, ATOMIC, LONG); each candidate under review is chained, two timeframes | partial |
| 4 | Qualification verdict (proof-grade) | `APOLLO_PROOF` gate, `darwin/qualification`, ATHENA placeholders | missing |
| 5 | Deployed qualification runtime | what is deployed and its relation to `main` to be audited | to be audited |
| 6 | Register in CER (strategy, version, evidence) | CER write endpoints; no DARWIN or HSA writer; read-back absent | partial |
| 7 | Promotion transition and authority | CER promotions, HSA immutability; no authority or citation rule | partial |
| 8 | Execute approved version | HELIOS loads HSA package; promotion check UNVERIFIED; trigger path to TRON missing | partial |
| 9 | Review (NEO) | NEO scripts exist; observer state to be audited; no CER read path | partial |
| 10 | Feedback to research (hypothesis intake) | `NEO_HYPOTHESIS` class exists; DARWIN intake absent | missing |

3. **MVP minimum for the one governed strategy** (strategy-neutral proposal for CA, sequenced after the trigger path works; it applies to whichever strategy the PO later selects): one frozen identity (`strategy_id@version` plus package hash) recorded in CER; one clearly non-proof backtest evidence record with artifact hash from an engine that already exists; one PO-recorded promotion transition citing that evidence; HELIOS running exactly that version; and a **read-only NEO review report** (human-readable, one strategy, CER plus fires) rather than the full evidence gateway. Deferred beyond MVP: ATHENA, DARWIN-to-CER automation, hypothesis intake, `EdgeProfileVersion`, SKEPTIC. The audit states, with evidence, which of these items are truly needed before the first live-like trigger and which only after.
4. **External evaluation register** (the table above, re-verified, with service-dependency flags), **information only**. It carries no reuse recommendation and no licence ruling: under CA guidance 2026-10-15 (item 4) the MVP takes no new third-party engine or SaaS dependency, so no external engine is adopted and none is offered as an MVP option.
5. **No-rebuild register:** delivered functions the MVP must reuse (HSA versioning and validation, DARWIN StrategyVersion and APOLLO core, CER registry and promotion records, HELIOS HSA boundary, GOLD-STRATEGY-RUNTIME, NEO strategy-health consumer).
6. **Gap list** with owner, mapped to existing backlog ids or marked "no home".
6a. **Disposition table** (`DISPOSITION.md`, REQUIRED; CA/PO legacy application doctrine 2026-10-15; format `PORTFOLIO.md` section 7.4). It keeps NEO's parts apart, one set of rows each: (a) NEO's legacy runtime; (b) legacy practice-account tooling (source inspection only); (c) the observer, scorer, auditor and coach; (d) the deployed NEO scheduled service. For each: generation (legacy / newer canonical / currently deployed), criteria (architecture fit, code quality, determinism, test evidence, maintainability, contracts, operational dependencies, integration cost), a verdict REUSE | REFACTOR | REPLACE | RETIRE, evidence, and the approximate comparative engineering cost of reuse versus refactor versus a clean build. **Explicit assessment required:** is a clean, read-only intelligence service (consuming CER evidence, no order path) preferable to rehabilitating the previous NEO runtime? State the answer with the cost comparison, evidence from the observer failure class and the tests actually proven, and the algorithms, tested logic, contracts and research findings worth retaining either way. The same table covers the CER, HSA and DARWIN components in the path (HSA package and versioning, DARWIN StrategyVersion and APOLLO core, CER registry and promotion records, GOLD-STRATEGY-RUNTIME). Obsolete application architecture is not preserved merely because time was invested. Verdicts are recommendations only: nothing is retired, stopped, migrated or mutated, and any physical retirement needs a separate authorised work order.
7. **Index entry** listing the primary PR and the four mirror-note PRs and their merge SHAs, contributed to `EVIDENCE-INDEX.md` by one GOAL PR after acceptance (single writer of the file: the `GOLD-MVP-001` PL).
8. **Amendment text proposals** (not applied) for CER-R1, NEO-R1, HSA-C1 and DARWIN-R2, plus candidate rows only where a gap has no home. Informed by RECON-G S1-S8 and RECON-H1 P-14.

CA's ten mandatory evidence items, in CA's numbering, as carried by `AUDIT-F.md`:

CA's ten mandatory evidence items, in CA's numbering (the numbering is CA's and is not to be changed by a lane): (1) PID/WO identifier and exact audited scope; (2) source repositories, revisions and relevant documentation references; (3) existing implementation: proven, partially proven, unverified or missing; (4) actual versus expected contract comparison; (5) tests, fixtures and evidence references; (6) specific defects and compatibility gaps; (7) reusable code and documentation; (8) minimum recommended implementation changes; (9) safety and deployment constraints; (10) independent audit verdict and any unresolved findings.

| CA # | CA evidence item | This audit puts it in | Proof method |
|---|---|---|---|
| 1 | PID/WO identifier and exact audited scope | AUDIT-F section 0: quoted scope (qualify, register, execute, review one GOLD strategy) | Quote equals approved PID |
| 2 | Source repositories, revisions and documentation references | Base SHAs for GOAL, DARWIN, CER, HSA, HELIOS, GOLD-STRATEGY-RUNTIME and neo; documentation references; the external evaluation sources (Deliverable 1 and 4) | Auditor re-reads each at the SHA |
| 3 | Existing implementation: proven, partially proven, unverified or missing | Path matrix of 10 hops, each exists / partial / missing with a re-runnable citation (Deliverable 2): strategy versioning, evidence storage, causal testing, promotion, NEO review | Every hop has a mark and a citation |
| 4 | Actual versus expected contract comparison | Representation comparison HSA / HELIOS / DARWIN / CER for each HSA candidate under review (identity and fingerprint across hops), evidence-class sufficiency per promotion state, APOLLO 006B scope versus the candidate | Same identity and fingerprint tested hop to hop |
| 5 | Tests, fixtures and evidence references | Re-runnable commands, count checks (10 hops; every memory-fabric review record identified in the audit and archaeology document in the register), before and after identity snapshots | Snapshots equal; counts match |
| 6 | Specific defects and compatibility gaps | Gap list with owner or 'no home' (Deliverable 6): deployment gap, undefined `EdgeProfileVersion`, NEO observer state, no APOLLO_PROOF runs | Each missing mark names an owner or 'no home' |
| 7 | Reusable code and documentation | No-rebuild register (Deliverable 5) and external evaluation register, information only, with service flags (Deliverable 4) | The register states that no external item is an MVP option |
| 8 | Minimum recommended implementation changes | MVP minimum for the one governed strategy and sequencing against the trigger path (Deliverable 3); amendment text proposals for CER-R1, NEO-R1, HSA-C1, DARWIN-R2 (Deliverable 8), not applied | Each change maps to an existing item or 'no home' |
| 9 | Safety and deployment constraints | Safety and deployment constraints: legacy practice-account tooling assessed from source only, no broker call, no installation of evaluated code, no new third-party service or engine for the MVP (CA guidance 2026-10-15, item 4) | No outbound call to any evaluated service in the record; secret-scan clean |
| 10 | Independent audit verdict and unresolved findings | Independent auditor (AUD-3) verdict file with unresolved findings; evidence PR list with SHAs | Fresh auditor GREEN with exact SHAs; PO acceptance recorded |

## Acceptance

GREEN requires, mechanically:

1. Every matrix hop carries an exists / partial / missing mark and at least one citation (repository path with commit SHA, or a command with its captured output) that an auditor re-runs and reproduces.
2. A count check passes: the matrix has 10 hops, the evidence table has CA items 1 to 10, the external register lists every memory-fabric review record identified in the audit and every legacy reuse document under DARWIN `docs/archaeology/`.
3. `./tools/goal-validate` and `./tools/secret-scan` are GREEN on every GOAL commit; a grep for IPv4 addresses, ports and key-like strings over all committed files returns nothing.
4. Before and after each inspected system, identity is unchanged: git HEAD of each inspected checkout, container ids and start times, and `git status` are recorded and equal. No file in any inspected checkout changed.
5. No external code was installed or executed; no outbound call to any evaluated service is in the record.
6. No backlog, `pid_path` or state change in the diff; `./tools/goal-docs` reports no write.
7. Each missing mark names an owner or "no home"; the external register is marked information only and contains no recommendation to adopt an external engine or SaaS for the MVP (grep check); no strategy is ranked, recommended or marked as selected.
8. `DISPOSITION.md` is present and complete: every NEO part and every CER / HSA / DARWIN component in the path has generation, criteria, a REUSE / REFACTOR / REPLACE / RETIRE verdict, evidence and a comparative cost, and the clean-read-only-service-versus-rehabilitation question is answered with a cost comparison. The lane cannot be accepted without it.
9. Fresh independent FORGE Auditor GREEN; evidence PR list with exact SHAs; PO acceptance recorded in GitHub.

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

**D2 — Strategy selection (restated by CA guidance 2026-10-15, item 6; does not block approval).** No strategy is selected, recommended or implied here. Selection is a PO decision taken after audits A and B have reported and been reconciled (DR-23); this audit supplies the per-candidate path facts as an input. Owner PO; Matt if it is a capital-risk choice.

**D3 — Strategy representation authority (RECON-H1 D-1; blocks hop 2 conclusions, not this audit).** Owner PO.

**D4 — `EdgeProfileVersion` (RECON-G D2; blocks CER-R1 and TRON-T5).** Defined nowhere. The audit reports whether the MVP needs it. Owner PO.

**D5 — NEO legacy practice-account tooling and boundary wording (RECON-G D1; blocks the `neo` evidence PR scope).** Source text only may be read; no running, no execution, no modification, no connection (CA/PO adjudication 2026-10-15). The disposition table carries a recommendation only; who adjudicates verdicts is DR-37. Owner PO.

**D6 — Strategy-health authority (RECON-G D4; blocks hop 9 design, not audit).** Owner PO.

**D7 — Meaning or fate of `LEAN-P1` and `DARWIN-R2` (RECON-H1 D-5, P-10; later).** Owner PO.

**D8 — Retired.** CA's numbered evidence list has been supplied and applied (see Deliverables); no decision remains.

**D9 — RETIRED (moot for the MVP) by CA guidance 2026-10-15, item 4.** The MVP takes no new third-party engine or SaaS dependency, so the GPL / AGPL licence posture of the evaluated libraries is not decided here.

**D10 — Evidence PR into private `maff0000/neo` (blocks that PR).** Owner PO.

## Evidence

- GOAL `main` at `1739e742154c77e9e2a96927dc40d4978b9cd798` (historical read base; baseline now `90323b3`): `backlog/backlog.yaml`, `backlog/SCHEMA.md`, `pids/GOAL-DCP-001.md`, tool validator source (PID format).
- RECON-G and RECON-H1 (analysis records, 2026-10-14), DARWIN-R1 PID draft (2026-10-14).
- DARWIN `bf1142b` (`main`): `PID.md`, amendment A-007, PID-006, WO-PID006B-001, `darwin/apollo/*`, migrations 0001-0013 (table names only), `docs/archaeology/*`.
- CER `60eae45`: `PID.md`, `src/cer/contract/enums.py`, `src/cer/api/routes.py` (route list), `docs/KNOWN-LIMITATIONS.md`.
- HSA `279ec18`: `strategies/gold_context_breakout/1.0.0/package.json` (lifecycle only), `docs/VERSIONING.md`.
- HELIOS `7f7193d`: `helios/integration/hsa_boundary.py`; GOLD-STRATEGY-RUNTIME `5891415`: `docs/ARCHITECTURE.md`.
- The NEO checkout: `git log`, `git status`, scheduler table (names only), a bounded read of the observer log, script names; the memory-fabric records identified in the audit (names only).
- Memory-fabric record reads (read-only, FABRIC-ONLY): the review records identified in the audit.
- Not accessed: live databases, credential files and `.env` contents, TRON runtime (none), legacy practice-account state, any broker, any external service.

## Evidence PR checklist

- [ ] `maff0000/GOAL` (PRIMARY, branch `wo/GOLD-AUD-F-evidence`): audit record, matrix, external register, amendment proposals. PR link and SHA: ____
- [ ] `maff0000/DARWIN` mirror note (`docs/evidence/GOLD-AUD-F/`): strategy identity, APOLLO scope, deployment-gap record (documents only). PR link and SHA: ____
- [ ] `maff0000/CER` mirror note: evidence-class sufficiency, promotion authority and citation record (documents only). PR link and SHA: ____
- [ ] `maff0000/HSA` mirror note: gold candidate identity, handoff and immutability record (documents only). PR link and SHA: ____
- [ ] `maff0000/neo` mirror note: review architecture, observer cause class, legacy tooling assessment (documents only; sanitised; private repository; PO-approved, D10). PR link and SHA: ____
- [ ] After acceptance: one GOAL PR adding F's entry to `EVIDENCE-INDEX.md` (owned by GOLD-MVP-001)
- [ ] Each PR passes secret-scan; no address, port, account or credential text
- [ ] Before and after identity snapshots attached and equal (Acceptance 4)
- [ ] CA evidence items 1 to 10 each present in `AUDIT-F.md` in CA numbering
- [ ] Fresh independent FORGE Auditor verdict recorded

## Approval

APPROVED. Recorded 2026-10-16 by ROGUE on the written authority of Central Architecture/PO.

1. Central Architecture adjudication of the GOLD MVP Portfolio, 15 October 2026 (APPROVED WITH CORRECTIONS AND GOVERNED MERGE CONDITIONS; approves the architecture and scope of this audit PID).
2. Central Architecture formal approval, 16 October 2026, Decision: OPTION 1. The previous adjudication is confirmed as the formal approval of record for the seven GOLD PIDs, including this one. No further approval of this PID scope is required unless a substantive change is proposed.

Scope of this approval: the read-only audit scope in this PID. It authorises no deployment, production mutation, broker order, contract freeze or live-capital action.

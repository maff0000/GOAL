# GOLD MVP portfolio for approval

**Work order:** `GOAL-GOLD-MVP`. **Baseline:** GOAL `main` @ `1739e742154c77e9e2a96927dc40d4978b9cd798`. **Date:** 2026-10-15.
**Author role:** architecture author for the cross-lane structure, working for ROGUE under Central Architecture (CA).
**Nature:** a proposal for approval. It records no approval, sets no `pid_path`, moves nothing to `DELIVERY_READY`, edits no backlog, and dispatches nothing. The backlog patch in section 11 is specified, not applied. **Status after the CA/PO adjudication of 2026-10-15 (APPROVED WITH CORRECTIONS):** the corrections are applied in this revision (section 0a, section 14, appendices C and D). The document still records no approval on CA's behalf: approval records are entered by CA/PO only, in the PID approval flow, and every PID Approval section remains PENDING.
**Companion:** `pids/GOLD-MVP-001.md` (integration and acceptance PID candidate) and the six audit PID candidates `pids/GOLD-AUD-A.md` to `pids/GOLD-AUD-F.md`. `audits/2026-10-15/gold-mvp/DECISION-REGISTER.md` consolidates every open decision (it supersedes the PD list in section 12, whose ids it keeps).
**Revision note (consolidation):** this document was first drafted before the lane PIDs existed. The consolidation edit has read all six lane PIDs and reconciled the amend-versus-new answers, the evidence numbering, the lane findings (section 3a), the backlog patch and the decisions to what the lane drafters concluded. A second pass applied the programme controller's delivery-coordination rulings 1 to 9 (appendix at the end of this document, verbatim, so that CA can overrule any of them) to resolve the mechanical contradictions between the lane PIDs and this document: evidence location, branch naming, evidence paths, index and matrix ownership, the C and D ordering, the lane A protocol, the `GOAL-TRIGGER-001` status, the RSI method statement and the HELIOS schema string. Genuine PO calls remain in `DECISION-REGISTER.md` (ruling 10). A third pass applied Central Architecture's binding architectural guidance of 2026-10-15 (appendix B, recorded as "CA guidance 2026-10-15", not as a controller ruling): HELIOS-side external adapter, `GOAL-TRIGGER-001` as the sole trigger authority, FALCON evidence-only and non-blocking, no new third-party engine or SaaS for the MVP, the named gap `GAP-TRON-FIXED-SIZE-DEMO-RISK`, and no strategy selection before audits A and B are reconciled. CA's instruction is to return the final PID portfolio and decision register for PO approval; both documents are in that state, still unapproved.

**Revision note (adjudication pass):** a fourth pass applied the CA/PO adjudication of 2026-10-15 (appendix C) and the CA/PO legacy application doctrine of 2026-10-15 (appendix D, section 1a item 8, section 7.4). Historical audit evidence and findings were not altered to conceal anything: where a statement was wrong or stale (MT5 gateway heads, a universal absence claim, byte identity for the FALCON outage test, run_id as a mutation proof) it is corrected in place and the correction is labelled. Still no backlog edit, no `pid_path`, no approval record, no dispatch and no push.

## 0a. Adjudication record (CA/PO adjudication 2026-10-15)

Central Architecture (PO) adjudicated GOAL PR #7 on 2026-10-15: **APPROVED WITH CORRECTIONS** (full statement, appendix C). This section is the per-PID adjudication record; no PID Approval section was edited and every one remains PENDING.

| PID | Adjudication record | priority | lane / risk | gates |
|---|---|---|---|---|
| `GOLD-MVP-001` | PO adjudication 2026-10-15: architecture and scope approved; approval record to be entered by CA/PO at PID approval | P0 | trading / capital | PO; Matt: capital-risk, Matt-gated for its FINAL DEMO acceptance (not for the six audits) |
| `GOLD-AUD-A` | PO adjudication 2026-10-15: architecture and scope approved as a separate audit work item; approval record to be entered by CA/PO at PID approval | P0 | research / medium | PO; Matt's express permission for production Redis read only (DR-4); GitHub/source analysis may proceed meanwhile |
| `GOLD-AUD-B` | same wording | P0 | research / low | PO |
| `GOLD-AUD-C` | same wording | P0 | research / medium | PO (`GOAL-TRIGGER-001` keeps its own Matt gate) |
| `GOLD-AUD-D` | same wording | P0 | research / medium | PO |
| `GOLD-AUD-E` | same wording (priority raised from P1 to P0) | P0 | research / low | PO |
| `GOLD-AUD-F` | same wording | P1 | research / low | PO |

The six audits are separate audit work items, NOT amendments of component implementation PIDs (the amendment fallbacks in section 3 are not taken). Six-way parallel FORGE audit dispatch is authorised once approved PIDs, backlog readiness, evidence requirements and safety gates are satisfied (section 14). Each audit returns a GitHub evidence PR, the source SHA, a contract matrix, reusable implementation findings, specific gaps, a disposition table (section 7.4) and a fresh independent audit verdict; ROGUE returns results individually as each lane finishes.

Where the corrections landed: Gate A and stale mt5-gateway references (sections 1, 3a, 7.3, 11.1, appendix B); bounded no-integration conclusion (section 3a lane B, 3a effect paragraph, 8.3 point 2, R-2); FALCON-outage logical equivalence and isolated FALCON (sections 2, 5.3, 6.3, R-17); run_id versus mutation (section 6.2); decision rulings (`DECISION-REGISTER.md` Resolved section); merge sequence (section 14).

## 1. Objective and frame

Objective (CA directive): a verified reusable integration foundation for ONE XAUUSD strategy, Vantage DEMO execution, FALCON evidence and subsequent NEO review.

Critical path: HERMES PROD XAUUSD Redis → HELIOS one governed strategy → signed durable trigger outbox → TRON inbox + risk gates → MT5 gateway / Vantage DEMO → FALCON evidence; then NEO → CER → HSA/DARWIN → approved HELIOS version.

Not prerequisites: additional HERMES feeds, broad research-platform expansion, new third-party services. No live capital execution. **Binding constraint (CA guidance 2026-10-15, item 4):** the MVP takes no new third-party engine or SaaS dependency; external evaluations (lane F) are information only and are not MVP options.

### 1a. CA guidance 2026-10-15 in one view, and other CA decisions of the day

Full statements are in appendix B. Each is recorded as CA guidance, not as a controller ruling, and has been applied in the PIDs and in `DECISION-REGISTER.md` (which keeps ids stable and lists what the guidance resolved).

| # | guidance | where applied |
|---|---|---|
| 1 | HERMES owns Redis publication. A HELIOS-side external adapter, outside the pure HELIOS engine (execution-blind, deterministic, no Redis or network imports), owns consumption and translation. GOAL approves the interface (CP-1) | lanes A, B, C; `GOLD-MVP-001`; sections 3a, 4, 8.3, 10 here |
| 2 | `GOAL-TRIGGER-001` owns signed-trigger, outbox and inbox semantics; no competing trigger contract in HELIOS, TRON or FALCON | lanes C, D, E; `GOLD-MVP-001`; sections 4.3 |
| 3 | FALCON is evidence-only and must not block execution (asynchronous, non-blocking, bounded queue; execution completes with FALCON ingestion stopped) | lane E (acceptance 6, EP-9); `GOLD-MVP-001` (AC-12, S-10) |
| 4 | No new third-party engine or SaaS dependency for the MVP; lane F external evaluations are information only | lane F; `GOLD-MVP-001` (AC-17); this section |
| 5 | `GAP-TRON-FIXED-SIZE-DEMO-RISK` recorded as a named gap | section 3b; lane D; `GOLD-MVP-001`; section 11.4 |
| 6 | No strategy is selected before the PROD facts (audit A) and candidate requirements (audit B) are reconciled | lanes A, B, F; `GOLD-MVP-001` D-5; sections 8.2, 12 (PD-8) |
| 7 | Return the final PID portfolio and decision register for PO approval | `DECISION-REGISTER.md` |
| 8 | **Legacy application doctrine** (CA/PO legacy application doctrine 2026-10-15; binding, full text appendix D): HELIOS and NEO have significant pre-GOAL history and their existing implementations have no automatic right to remain part of THE GOAL. Each audit distinguishes legacy generations, newer canonical implementations and currently deployed services, and ends every reusable component with a REUSE, REFACTOR, REPLACE or RETIRE recommendation and a comparative cost. Objective: the strongest achievable GOLD MVP architecture, not maximum legacy code reuse. Verdicts are recommendations only; nothing is retired, shut down or mutated | every lane (disposition table, section 7.4); lanes B and F especially; register DR-37 |

**Sequence (CA guidance 2026-10-15, item 6).** Audits A and B, then reconciliation of PROD facts against candidate requirements, then strategy selection (a PO decision taken with those inputs), then `GOLD-MVP-001` acceptance planning. No strategy is recommended, preferred or implied as selected anywhere in this portfolio; the HSA packages are candidates under review only.

**Other CA decisions of 2026-10-15, for context (none changes the scope of this portfolio).** MT5 Gateway Gate A is CLOSED GREEN WITH NOTICES at the canonical `maff0000/mt5-gateway` `main` @ `6263d61f4cb0d4d5b16337e67c30f409bc9c5051` (PR #9 merged; this corrects the earlier statement that placed the SHA on GOAL `main`, CA/PO adjudication 2026-10-15). Follow-up issue #10 tracks the template-hardening notices, including secrets ownership and symlink handling, to be resolved before the template is used. The unrestricted RPyC bridge is not to be connected to TRON. The functional Vantage DEMO proof remains a separate gated workstream. The GitHub PRIVATE visibility change for that repository is now eligible for Matt's authorisation (DR-32). No production or broker mutation is authorised. No audit dispatch and no backlog change occurs until approved PIDs, backlog readiness, evidence requirements and safety gates are satisfied (section 14).

### 1b. Status update 2026-10-15 (later)

Current-state facts that supersede earlier statements in this document where they conflict; historical sections (rulings and adjudication appendices, revision notes) are left as written and annotated where needed.

- **GOAL PR #5 is MERGED.** Merge commit `90323b3e1171cdafaeff9612d51307a41000a13a` on `main` (audited head `e2671ff256e5bb02c7c72082fee7184eac2e26a3`; independent audit GREEN-WITH-NOTICE; merge record posted on the PR). `main` now has **43 backlog items**, including `GOAL-TRIGGER-001` (lane `shared`, `matt_gate` true, dependencies `GOAL-DCP-001` and `GOAL-CONTRACT-001`), `TRON-D1-RATIFY` and `HSA-C1`; `HELIOS-T1` is `PID_DRAFT`. The PID candidates for `GOAL-TRIGGER-001` and `TRON-D1-RATIFY` are still drafts; the `GOAL-TRIGGER-001` PID candidate remains on branch `wo/GOAL-CONTRACT-TRIGGER` commit `64c843b`; no `pid_path` is set. Expected counts: 43 on `main` today, 49 after part 1, 50 after part 2. Part 2 is no longer blocked by #5 (it still waits for the portfolio merge and approved PIDs; PD-1 is resolved).
- **GOAL PR #6 (head `84fc7ce`) is superseded in practice by a clean replacement PR #8** (branch `wo/GOAL-BACKUP-PLAN-CLEAN`, head `096673e64751429edc67ce7a03a5a51b3a7531ad`): an earlier draft contained more detailed operational text than is appropriate for a public repository. The merge decision on #6 / #8 is pending CA. Sequence: PR #5 (merged), then the backup-plan documentation PR (#6, being replaced by #8 pending CA's decision), then this PR. Heads are current at time of writing.
- **This PR's branch was reconciled with `main`:** true merge `cbd4df9` of `main` @ `90323b3`, `MANIFEST.md` regenerated.
- **MT5 Gateway Gate A is closed** at `maff0000/mt5-gateway` `main` @ `6263d61f4cb0d4d5b16337e67c30f409bc9c5051`; issue #10 tracks the template-hardening notices.

Operating model: one ROGUE, many parallel FORGE workers, up to six concurrent workstreams, each worker in its own worktree, each with an independent auditor; no two workers write the same authoritative source, contract, shared database or running service. PID first: amend existing PIDs or add bounded audit increments rather than duplicate.

How "amend versus new" was applied. Every audit is tracked as its own backlog item, because a read-only audit must be dispatchable before the existing component PIDs are approved and must carry its own independent auditor and acceptance. Two forms were offered to the lane drafters:

- **(i) amendment:** the existing PID already covers the scope. The audit item is a declared increment of that PID: the audit PID states `Amends: <ID>`, the existing PID's next revision lists the audit as a named deliverable, and audit closure satisfies that deliverable. The audit PID restates no scope the existing PID owns.
- **(ii) new bounded audit item:** no existing PID covers the scope, or the existing PID is engineering while this is research. The audit PID states `Complements: <IDs>` and the existing PIDs are not edited.

**Outcome after the lane drafters read the existing PIDs: all six lanes concluded (ii).** Each is a new bounded read-only audit item with a documented amendment fallback (section 3). The original draft expected (i) for A, C and E; that expectation is withdrawn.

## 2. The portfolio

Seven items: one integration PID and six read-only audit items. All audits: backlog lane `research` (read-only work; adjudicated), `depends_on: [GOAL-DCP-001]` only, `po_gate: true`, proposed state `PID_DRAFT`, priority P0 for A to E and P1 for F, risk as each lane PID states (A medium, B low, C medium, D medium, E low, F low) (CA/PO adjudication 2026-10-15, resolving DR-13 and DR-33). The `amend vs new` column states what each lane drafter concluded after reading the existing PIDs.

| id | lane (area) | scope sentence | amend vs new (existing PID) | evidence PR goes to | read-only permissions (section 6) | gate | collisions (section 5) | independent auditor |
|---|---|---|---|---|---|---|---|---|
| `GOLD-MVP-001` | trading (integration) | Own the cross-component integration architecture, evidence index, contract compatibility matrix and the single end-to-end Vantage DEMO acceptance of one governed XAUUSD strategy with FALCON evidence; no component implementation. | new; kept alongside `PAPER-E2E-001`, which becomes a subsequent broader qualification (PD-1 resolved, CA/PO adjudication 2026-10-15) | `maff0000/GOAL` | none beyond reading audit outputs until the acceptance run, which has its own approvals | PO + Matt: capital-risk, Matt-gated for its FINAL DEMO acceptance, not for the six audits | reads outputs of all six audits; writes only `audits/2026-10-15/gold-mvp/` in GOAL; owns `EVIDENCE-INDEX.md` and `COMPATIBILITY-MATRIX.md` (single writer: its PL) | AUD-3 plus CA acceptance |
| `GOLD-AUD-A` | research (area A HERMES) | Audit the existing PROD XAUUSD Redis publication: keys, schemas, indicator coverage, timeframes, freshness, timestamps, warm-up, validation and status, and compare it with the documented Redis contracts, without mutating production. | **(ii) new bounded item**: a strict subset ("Increment A") of `HERMES-CUR-001` scope item 1 (Redis key inventory), complements `HERMES-CUR-001`; the lane PID carries proposed amendment text for CUR-001 (not applied); fallback: fold in as CUR-001 Increment A unchanged. `HERMES-FACT-001` is the downstream consumer | `maff0000/hermes` (primary; GOAL index entry only) | repo read; PROD Redis non-blocking read protocol (section 6.2); container labels only | PO + **Matt's express permission for production Redis read only (DR-4); GitHub/source analysis proceeds meanwhile** | the only audit that touches PROD Redis; HERMES repo shared read with B and E | AUD-1 |
| `GOLD-AUD-B` | research (area B HELIOS) | Search the recorded locations for any previously completed HERMES Redis to HELIOS GOLD integration (external adapter, deployment wiring, legacy), distinguish legacy HELIOS generations, the newer deterministic engine and the deployed stack, reconcile what is found with the new HELIOS runtime and the MarketFactFrame, recommend minimum reuse or adaptation for the HELIOS-side external adapter, and tabulate HSA candidate requirements against the PROD facts of audit A (no ranking, no selection). | **(ii) new**: a separate audit item that is an input to `HELIOS-T2` (the live-transport owner, which owns the adapter implementation), not an increment or amendment of it; complements `HELIOS-T1` and `GOLD-STRATEGY-RUNTIME`; no second market-data reader may be built or prototyped by the audit. The fold-in fallback is not taken (adjudication 2026-10-15) | `maff0000/HELIOS` (primary; GOAL index entry only) | repos read (HELIOS, GOLD-STRATEGY-RUNTIME, HSA, legacy HELIOS lineage); no PROD Redis (uses A's output and fixtures) | PO | shares HSA read with F; HELIOS repo single evidence writer | AUD-2 |
| `GOLD-AUD-C` | research (area C shared contracts) | Reconcile `GOAL-CONTRACT-001` and `GOAL-TRIGGER-001` with existing implementations and produce governed consumer/provider contracts for HERMES Redis to the HELIOS-side external adapter (CP-1, the interface GOAL approves) and for HELIOS signed trigger to durable outbox to TRON inbox (CP-2, a conformance package over `GOAL-TRIGGER-001`, which alone owns the semantics): versioning, golden fixtures, rejection behaviour, recovery. | **(ii) new thin item**: CP-1 (HERMES Redis to HELIOS input) has no home in either PID or in `HERMES-FACT-001` (no PID); `GOAL-CONTRACT-001` / `GOAL-TRIGGER-001` remain the approval owners of the normative text and their blockers (D-3 Matt gate); `GOLD-AUD-C` freezes nothing (packages are PROPOSED); fallback: amendment of both PIDs (decision D-C2); CP-1 freeze owner is D-C1 | `maff0000/GOAL` (primary; packages under `contracts/packages/`) | repos read (GOAL branches, HELIOS, HERMES, TRON D1 branch, FALCON contracts); no runtime | PO (contracts carry Matt gate in `GOAL-TRIGGER-001` itself) | contributes matrix rows to the single `COMPATIBILITY-MATRIX.md` owned by `GOLD-MVP-001` (after its own evidence PR is accepted); inputs A and B, soft inputs D and E (section 8.2); no second matrix | AUD-2 |
| `GOLD-AUD-D` | research (area D TRON / MT5) | Audit the TRON D1 design and implementation candidates, risk rules, journal and trigger-intake assumptions; coordinate with `MT5-GW-001`; identify the smallest missing capabilities for one DEMO execution path, including the named gap `GAP-TRON-FIXED-SIZE-DEMO-RISK` (section 3b), and validate the scope of the approved `TRON-T3A` (section 3b). | **(ii) new thin item**: composes `TRON-D1-RATIFY` and the merged MT5 work (`MT5-GW-001`, merged PR #9 and follow-up issue #10, readiness, DEMO-verify) into one six-hop gap matrix without redoing them; fallback: the same deliverables become an appendix to the ratification package plus a stub item (PD-3) | `maff0000/GOAL` (primary: TRON and MT5 facts) with mirror notes in `maff0000/tron` and `maff0000/mt5-gateway` (ruling 1) | repos read (TRON incl. unmerged D1 branch, MT5 gateway, instance template records); docker labels only; **no broker call**; legacy trading executors may be inspected as source text, never run or modified | PO | two repos; MT5 instances never touched; TRON D1 branch is `TRON-D1-RATIFY`'s subject | AUD-3 |
| `GOLD-AUD-E` | research (area E FALCON) | Audit the delivered FALCON registry and running ingestion and define the minimum remaining HELIOS and TRON event publication, keeping FALCON evidence-only, asynchronous and non-blocking, outside the executable trigger path (execution must complete with FALCON ingestion stopped). | **(ii) new thin item**: a carve-out from `FALCON-T1` (T1 excludes exactly the `strategy_trigger` and `tron.*` families this audit must cover; T1 writes registry files, E is read-only); composes RECON-F's FALCON-T2/T3; fallback: append the deliverables to FALCON-T1 as a verification increment (cost: reverses T1's carve-out, mixes risk postures) | `maff0000/falcon` (primary; GOAL index entry only) | repo read; FALCON running ingestion read via its own query interface (read-only); no write to the registry; running Graylog is never mutated or interrupted, and if authenticated read-only inspection is unavailable that part is recorded UNVERIFIED; FALCON-outage rehearsals only against an isolated DEV/test FALCON | PO | reads FALCON runtime; reads A/D outputs for event-source facts | AUD-1 |
| `GOLD-AUD-F` | research (area F CER / HSA / DARWIN / NEO) | Define how one GOLD strategy is qualified, registered, executed and reviewed (strategy versioning, evidence storage, causal testing, promotion, NEO review architecture) without rebuilding delivered functions, recording earlier external repository/SaaS evaluations as information only (no new third-party engine or SaaS for the MVP; none is an MVP option). | **(ii) new thin item**: complements `CER-R1`, `NEO-R1`, `HSA-C1`, `DARWIN-R2` (none amended; Deliverable 8 holds ready-to-apply amendment text; fallback: apply it and cancel the item after one audit PR) | `maff0000/GOAL` (primary) with mirror notes in `maff0000/CER`, `HSA`, `DARWIN` and `neo` (private: sanitised; PO approval of the `neo` note is DR-18) (ruling 1) | repos read (CER, HSA, DARWIN, neo, earlier evaluation records); no runtime | PO | four repos read; shares HSA read with B | AUD-3 |

Notes on the table.

- Branch naming (ruling 2): audit evidence branches are `wo/GOLD-AUD-<L>-evidence` in the primary repository (for example `wo/GOLD-AUD-A-evidence`), and the same name in a mirror repository. The PID-authoring branches already named `wo/GOAL-GOLD-AUD-<L>` are PID drafts, not evidence branches.
- Evidence paths (ruling 3): `docs/evidence/GOLD-AUD-<L>/` in the primary repository; GOAL uses `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-<L>/` for the GOAL-primary lanes C, D and F and for index entries.
- `GOAL-TRIGGER-001` status (ruling 7): the drafted PID candidate is on branch `wo/GOAL-CONTRACT-TRIGGER` (commit `64c843b`), its backlog item is on `main` since GOAL PR #5 merged on 2026-10-15 (merge commit `90323b3`; see 1b), while the PID candidate remains on that branch and no `pid_path` is set. Lanes C, D and E treat it as a candidate, not an authority.
- Gate columns are proposals for the backlog. `matt_gate` is false for B to F. `GOLD-MVP-001` is capital-risk and Matt-gated for its FINAL DEMO acceptance (PAPER rule), not for the six audit investigations. `GOLD-AUD-A` keeps `matt_gate: true` solely as the production-read gate: production Redis read requires Matt's express permission and a HELM-operated bounded protocol (DR-4), and stays TRUE until Matt expressly permits; GitHub/source analysis for lane A may proceed meanwhile.
- Priorities (adjudicated): A to E P0, F P1. Lane `research` for all six audits.
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

The CA/PO adjudication of 2026-10-15 confirms all six as separate audit work items, NOT amendments to component implementation PIDs: the amendment fallbacks above are recorded for history and are not taken.

The first draft of this section expected (i) for A, C and E (amendment with an `Amends:` line). That is withdrawn: the lane PIDs state `Complements:` lines, and no existing PID is edited by any audit.

## 3a. Lane findings that change the plan

Each lane PID recorded discoveries during drafting (all read-only; marked in the PIDs as proven, partial or UNVERIFIED). They change the plan as follows. Cited PID in brackets.

- **A, HERMES publication** (`pids/GOLD-AUD-A.md`). The documented tick contracts are the only registered contracts in the HERMES manifest and are marked "designed, publisher not built"; the candle, indicator, feed-health and catalog key families exist only in Memory Fabric (no repository document registers them), and the two fabric sources disagree on key counts by about 250 times (about 1,107 versus about 284,000), so which instance is "PROD" is itself open. Plan effect: A's job is to establish what is actually published and make the first repository record of it; `HERMES-FACT-001` (the `HERMES-FACT-001`-style contract of what HERMES publishes, CA guidance 2026-10-15 item 1) cannot be written against documents that do not exist. A's PROD facts are also the first input to the strategy-selection sequence (item 6).
- **B, HELIOS reader** (`pids/GOLD-AUD-B.md`). *Bounded conclusion (corrected by CA/PO adjudication 2026-10-15; the earlier text read as a universal absence claim).* Searched (lane B Scope 1 and Current state): the HELIOS, GOLD-STRATEGY-RUNTIME, falcon and TRADER trees; worktrees and branches; `gh repo list` for the owner; systemd units and timers; container names and labels (never environment); fabric key names (labelled fabric-only); HERMES consumer docs; legacy archive manifests. Found, in those locations: HELIOS has no Redis client (and the pure engine bans one); `GOLD-STRATEGY-RUNTIME` is wiring only (its own delta record says HELIOS has no live HERMES transport); the deployed GOLD stack is fixture-fed; branch `WO-HELIOS-HERMES-PROD-INTEGRATION-PROOF-0001` ended `WAITING_FOR_HERMES_BACKFILL` with no code; legacy HELIOS and the trading-host bridge read databases, not Redis. **No completed integration was found in the searched locations; absence elsewhere is UNVERIFIED**, and the lane B acceptance item that re-runs and extends the search is kept (a negative is a claim, not a finding). One HSA candidate under review, `gold_context_breakout` 1.0.0, needs simple moving averages while HELIOS facts carry EMAs (SMA versus EMA naming), and HSA says `XAUUSD` where HERMES and HELIOS say `XAU_USD`; this is a requirement of that candidate, recorded without preference (the other candidate under review is `wick_rejection_sequence` 0.1.0). Plan effect: **the HERMES to HELIOS reader is a BUILD item: the HELIOS-side external adapter outside the pure engine (CA guidance 2026-10-15, item 1)**, not an adaptation of the engine; resolved by CA/PO adjudication 2026-10-15 (DR-34, DR-35): the HERMES Redis reader and adapter belong in the HELIOS repository outside the pure engine, `HELIOS-T2` owns the implementation, and the HELIOS architect authors the bounded work orders. The B audit's output is the reuse inventory, gap list and minimum adaptation plan that scope that build, plus a candidate-requirements matrix against A's PROD facts (an input to the later selection, not a selection), and a claim of "not found" carries a recorded negative-search method.
- **C, contracts** (`pids/GOLD-AUD-C.md`). The TradingTriggerInbox specification exists nowhere (re-checked in TRON D1, TRON main, HELIOS main, FALCON main). CP-1 mismatches to reconcile: HERMES `schema_version` `v1` versus HELIOS `<namespace>/<x.y.z>` (and HELIOS itself advertises `helios.market_fact/1.0.0` while its fixtures, config and tests also accept `hermes.market_fact/1.0.0`), millisecond versus microsecond timestamps, JSON float versus exact decimal, `is_closed` versus `complete`, two Redis keys (candles, indicators) versus one frame, indicator sets (HERMES publishes more, HELIOS refuses unknown), `regime` (HERMES forbids it, ARES owns it, HELIOS wants it), RSI method naming (HERMES documents Cutler SMA-14, as sourced from lane C; HELIOS's RSI method is not stated in any lane PID, so audits B and C confirm it), and `ingested_at_utc` having no HERMES source. CP-2 mismatches: three identity names (`trigger_id` free string in FALCON, deterministic `trg1_` in `GOAL-TRIGGER-001`, `action_id` in TRON), fingerprint and parameter-set naming, millisecond versus UTC strings, and TRON's closed terminal set lacking the outcomes the trigger contract names. HELIOS has no trigger, signing or outbox code. Plan effect: the compatibility matrix cannot be filled from documents; both boundaries need adapters or renames before `HELIOS-T3` and `TRON-T4` can be proven together. Under CA guidance 2026-10-15 the CP-1 mapping is owned by the HELIOS-side external adapter (D-C3 re-assigned, D-C4 resolved), and every competing intake or evidence shape found at CP-2 is reconciled to `GOAL-TRIGGER-001` as the sole trigger authority (item 2).
- **D, TRON / MT5** (`pids/GOLD-AUD-D.md`). TRON has no runtime code on `main`; the D1 branch is 20 commits of documents, schemas and one docs test (148 tests prove consistency, not execution), with no PR; D1 has no exposure, position-count, order-size, loss or risk-lock checks and its kill-switch check has no setter; the typed MT5 gateway is not built (raw RPyC bridge only); the MT5 gateway state is Gate A CLOSED GREEN WITH NOTICES at canonical `maff0000/mt5-gateway` `main` @ `6263d61f4cb0d4d5b16337e67c30f409bc9c5051` (PR #9 merged; follow-up issue #10 tracks template-hardening notices; no TRON connection to the unrestricted RPyC bridge; the functional Vantage DEMO proof is a separate gated workstream). Plan effect: a TRON runtime, its risk gates and the typed gateway are builds; D's gap matrix sizes them to the one-order path. D also confirms the shape of the named gap `GAP-TRON-FIXED-SIZE-DEMO-RISK` (section 3b).
- **E, FALCON** (`pids/GOLD-AUD-E.md`). FALCON is delivered (28 registered families; ingestion containers running), but only HERMES and ARES market-status events are actually emitted; HELIOS publication is synchronous and blocking (a sink failure exits the process); TRON has no claim/disposition or reconcile family; HELIOS and TRON ingestion inputs are deliberately not published; and about 15 documents carry stale "Graylog as trigger transport" language. Plan effect: minimum publication work (P-H1..P-F2) is small but real and sequences after `GOAL-TRIGGER-001`; FALCON stays outside the executable trigger path.
- **F, qualification to review** (`pids/GOLD-AUD-F.md`). A 10-hop path matrix is the unit of work: the running DARWIN production image is not an ancestor of `main` and lacks APOLLO and migrations 0006 to 0013; no `APOLLO_PROOF` run exists (006B emits `APOLLO_RESULT` only, single timeframe, ATOMIC, LONG only, so the chained two-timeframe gold candidate may be out of scope); `EdgeProfileVersion` is defined nowhere; the NEO observer fails every cycle (missing fabric config key since 2026-07-17); NEO has no CER client. External repository and SaaS evaluations: information only, **none is an MVP option and none is recommended** (CA guidance 2026-10-15, item 4: no new third-party engine or SaaS dependency; the backtrader and backtesting.py reviews also predate APOLLO; the licence-posture question is moot). Plan effect: the MVP review step is a read-only NEO report, not the full evidence gateway.

**Effect on the critical path.** The audits do not add scope, but they change what the serial chains consist of. (1) The strategy chain gets longer in its middle: the HELIOS-side external adapter (a Redis reader plus a contract adapter, CP-1 reconciliation, outside the pure engine; carried by `HELIOS-T2` or a separate adapter item, DR-34 and DR-35) is a build, not an adaptation, so it is a long pole alongside `GOAL-CONTRACT-001` and `HELIOS-T3`. (1a) The strategy itself is not on the engineering chain until the PO selects it, after audits A and B are reconciled (CA guidance 2026-10-15, item 6); acceptance planning follows the selection. (2) The trigger path is a long pole: no inbox specification, no HELIOS signer or outbox, no TRON runtime, no typed gateway; `GOAL-TRIGGER-001` (Matt gate, blockers D-1..D-4, D-12) and `TRON-D1-RATIFY` (Matt gate) gate it. (3) The MT5 gateway chain remains four serial items before `TRON-T2`; and the named gap `GAP-TRON-FIXED-SIZE-DEMO-RISK` (section 3b) is a TRON item on the same path with no owner today: until it exists, no DEMO order can be sized or gated, so it is on the critical path to `GOLD-MVP-001` and `PAPER-E2E-001` acceptance. (4) Evidence (FALCON) and the review step (F) are shorter than first feared and sequence after the trigger path. The earlier hope in section 8.3 that audit B might shrink `HELIOS-T2` to adaptation is not supported by the evidence found in the searched locations (section 3a, lane B); that conclusion is bounded and audit B re-runs and extends the search.

## 3b. Named gaps

### GAP-TRON-FIXED-SIZE-DEMO-RISK (recorded explicitly by the consolidation, CA guidance 2026-10-15, item 5)

**Statement.** No backlog item owns a minimum fixed-size DEMO risk and sizing policy. `TRON-T5` pulls in `CER-R1` (it is the edge-profile-driven sizing, not a minimum); `TRON-T5A` exists only as a deferred candidate (RECON-H2 F-6); and the D1 design's MVP check set contains no exposure, position-count, order-size, loss or drawdown gate, and its kill-switch check (CHK-074) has no setter (D1 ratification package; `pids/GOLD-AUD-D.md` Current state). TRON cannot place a DEMO order without a quantity and without gates that run before submit.

| field | value |
|---|---|
| id | `GAP-TRON-FIXED-SIZE-DEMO-RISK` |
| owner | TRON (`maff0000/tron`); credential-free (provable with a simulated adapter, deterministic gates and an in-memory journal port) |
| required content | (1) a fixed DEMO base quantity read from configuration; (2) a per-instrument one-position rule; (3) a maximum number of open positions; (4) a maximum daily loss and trade-count guard; (5) a kill switch, with a setter; (6) hard gates before submit, evaluated fail-closed |
| candidate backlog item | `TRON-T3A` (section 11.4): APPROVED by CA/PO adjudication 2026-10-15 as a proposed P0 / high-risk, credential-free minimum DEMO sizing and risk item, subject to Lane D scope validation (DR-36 resolved with that condition). A single kill switch exists: no competing TRON kill switches; `TRON-T3A` must reuse or extend the `TRON-T3` hard-risk / kill-switch design and must not create a second one. Its backlog entry is not applied here (a later serial governed change, section 14) |
| audit input | `GOLD-AUD-D` validates the scope of `TRON-T3A` and confirms or corrects its shape (H3 row, `INCREMENTS.md`), including that it reuses or extends the `TRON-T3` design with one kill switch, and does not close the gap |
| acceptance linkage | `PAPER-E2E-001` and `GOLD-MVP-001` acceptance require it (`GOLD-MVP-001` AC-8 and AC-16, S-9) |

## 4. Dependency and ownership matrix

### 4.1 Components by what they own

| component | repo | contract it provides | contract it consumes | source of truth for | runtime state it owns | shared datastore it writes | single writer of |
|---|---|---|---|---|---|---|---|
| HERMES | `maff0000/hermes` | market facts (`goal.market-fact/v1` via `HERMES-FACT-001`; PROD Redis publication as built) | vendor feeds (not touched) | market-truth data and its publication | publisher process | PROD HERMES Redis (and its historical store) | the PROD HERMES Redis keyspace |
| HELIOS | `maff0000/HELIOS` | strategy state; signed trigger (`GOAL-TRIGGER-001`) | market-fact input through the external adapter (the pure engine has no Redis or network import); `goal.strategy/v1` | deterministic evaluation | evaluator state; the trigger outbox (proposed) | its own state and outbox store | the signed trigger outbox |
| TRON | `maff0000/tron` | inbox intake and outcomes (`GOAL-TRIGGER-001`); execution journal | signed trigger; gateway typed API | sizing, hard risk, kill, execution decisions | inbox, journal, kill state | Trading Postgres (`TRON-T1`) | inbox and execution journal; the only caller of the gateway |
| HELIOS-side external adapter (CA guidance 2026-10-15, item 1) | the HELIOS repository, in a package outside the pure engine (CA/PO adjudication 2026-10-15; DR-34); implementation owned by `HELIOS-T2`, bounded work orders authored by the HELIOS architect (DR-35) | translated `MarketFactFrame` input for HELIOS | HERMES Redis publication (read-only) | consumption and translation of HERMES facts, including the `v1` mapping | adapter state only (none shared) | none | none (read-only consumer) |
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
| PROD HERMES Redis | the HERMES publisher | `GOLD-AUD-A` only, non-blocking read protocol, after Matt's express permission (DR-4) | allow-list wrapper (6.2); no other audit connects |
| HERMES historical store | HERMES | none (docs and repo only) | not in any permission set |
| HELIOS signed trigger outbox | HELIOS signer/publisher (to be fixed by `GOAL-TRIGGER-001`; PROPOSED, the inbox spec was not found) | TRON intake (read of delivered triggers) | contract |
| TRON TriggerInbox and execution journal | TRON | FALCON/NEO via published events or read-only interface | contract |
| Trading Postgres | TRON (`TRON-T1`) | none during audits | not in any permission set |
| MT5 instances (including the DEMO instance) | the MT5 gateway | none during audits (no broker call) | explicit write-forbidden list (5.3) |
| Legacy executors / legacy MT5 services | their existing owners; untouched (ADR-MT5-002) | none | explicit write-forbidden |
| FALCON registry / Graylog | FALCON ingestion | `GOLD-AUD-E` through the query interface, read-only; the running Graylog is never mutated or interrupted | permission set |
| CER evidence store | CER | `GOLD-AUD-F` repo read only | permission set |
| DARWIN DB | DARWIN | none | permission set |
| `backlog/backlog.yaml`, `MANIFEST.md`, `MASTER-BACKLOG.md` | ROGUE integration (generated regions via `goal-docs --write`) | all | audits and PID drafters never edit |
| Cross-component evidence index and compatibility matrix | the `GOLD-MVP-001` PL, at all times (ruling 4); lanes contribute by PR after their own evidence PR is accepted, one lane per PR | all (read) | file ownership (5.2) |
| Memory Fabric | each persona writes only its own namespace | read-only orientation | audit workers do not write fabric |

### 4.3 Contract ownership

| contract / interface | provider | consumer | owning PID | approval |
|---|---|---|---|---|
| HERMES Redis publication (as built) | HERMES | HELIOS-side external adapter, FALCON | `HERMES-CUR-001` (as-built), `GOLD-AUD-A` | GOAL |
| `goal.market-fact/v1` (to-be) | HERMES | HELIOS, HSA | `HERMES-FACT-001` | GOAL |
| HERMES → HELIOS input compatibility (as-is versus to-be), CP-1 | HERMES (publication, with a `HERMES-FACT-001`-style contract) | HELIOS-side external adapter (translation); the pure engine receives validated frames only | `GOLD-AUD-C` (rows contributed into the matrix `GOLD-MVP-001` owns), `HERMES-FACT-001` (owns HERMES publication semantics), `HELIOS-T2` (adapter implementation) | GOAL approves the CP-1 interface using the A/B/C reconciliation (CA/PO adjudication 2026-10-15) |
| `goal.strategy/v1` | GOAL | HSA, HELIOS, DARWIN, CER | `GOAL-CONTRACT-001` | GOAL (CA/PO) |
| signed trigger + inbox semantics | GOAL | HELIOS (producer), TRON (consumer), FALCON (observer) | `GOAL-TRIGGER-001` (sole owner; no competing trigger contract in HELIOS, TRON or FALCON, CA guidance 2026-10-15, item 2) | GOAL (Matt gate) |
| TRON → gateway typed API | MT5 gateway | TRON | `MT5-GW-003` | GOAL |
| FALCON event families (evidence only; asynchronous, non-blocking, bounded queue; execution completes with FALCON ingestion stopped, CA guidance 2026-10-15, item 3) | FALCON | HERMES, HELIOS, TRON as emitters | `FALCON-T1` plus an increment (PD-4) | GOAL |
| EdgeProfileVersion | CER | TRON (sizing, later), NEO | `CER-R1` | GOAL |

### 4.4 Dependency graph (engineering edges only)

```text
GOAL-DCP-001 (CLOSED)
 ├─ GOLD-AUD-A..F (read-only; no engineering edges; feed matrix)
 ├─ HERMES-CUR-001 ─ HERMES-FACT-001 ─┐
 ├─ GOAL-CONTRACT-001 ─ GOAL-CORE-001 ─ HELIOS-T1 ─ HELIOS-T2 (+ HELIOS-repo external adapter) ─ HELIOS-T3 ─┐
 │      └─ GOAL-TRIGGER-001 ───────────────────────────┘ (also feeds TRON-T4)  │
 ├─ TRON-D1-RATIFY (Matt) ─ TRON-T1 ─ TRON-T3, TRON-T4 (needs TRIGGER-001) ─────┤
 ├─ MT5-GW-001 ─ -002 ─ -003 ─ -004 ─ TRON-T2 ───────────────────────────────────┤
 ├─ FALCON-T1 (+ minimum event publication, PD-4)                                │
 └─ (GAP-TRON-FIXED-SIZE-DEMO-RISK: proposed item, DR-36; not applied)           ▼
                                                                         GOLD-MVP-001
```

Audits shorten this graph by turning assumed work into verified reuse (section 8.3); they add no engineering edge.

## 5. Collision matrix

### 5.1 Who reads what (R) and who writes what (W, own worktree only)

| resource | A | B | C | D | E | F | MVP |
|---|---|---|---|---|---|---|---|
| GOAL repo (index-entry and matrix contribution PRs after acceptance; lanes C, D, F also `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-<L>/`; `pids/GOLD-AUD-<L>.md` on the PID draft branch) | W (index PR) | W (index PR) | W (primary, packages) | W (primary) | W (index PR) | W (primary) | W (`gold-mvp/`, single writer of index and matrix) |
| GOAL `main`, `backlog.yaml`, `MANIFEST.md` | R | R | R | R | R | R | R |
| `maff0000/hermes` | R + primary evidence PR | R | R | | R | | |
| `maff0000/HELIOS` | | R + primary evidence PR | R | | R | R | |
| `GOLD-STRATEGY-RUNTIME` | | R | | | R | R | |
| `maff0000/tron` (incl. unmerged D1 branch) | | | R | R + mirror note | R | R | |
| `maff0000/mt5-gateway` | | | | R + mirror note | | | |
| `maff0000/falcon` | R | | R | R | R + primary evidence PR | | |
| `maff0000/CER`, `HSA`, `DARWIN`, `neo` | | R (HSA) | R | | | R + mirror notes (neo sanitised) | |
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
| `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-<L>/` (lanes C, D, F: primary evidence) | lane `<L>` worker, on `wo/GOLD-AUD-<L>-evidence` |
| `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md`, `COMPATIBILITY-MATRIX.md` | the `GOLD-MVP-001` PL (single writer). Lane PRs contribute entries only after their own evidence PR is accepted, one lane per PR, merged one at a time |
| `contracts/packages/` | `GOLD-AUD-C` worker |
| `MANIFEST.md`, `backlog/MASTER-BACKLOG.md`, `backlog/backlog.yaml` | ROGUE at integration; never a lane |

Merge-conflict classes: the only expected conflict is `MANIFEST.md` (generated); ROGUE regenerates it. All other paths are disjoint by construction; the two shared files (`EVIDENCE-INDEX.md`, `COMPATIBILITY-MATRIX.md`) have one writer and take one lane per PR.

### 5.3 Explicit write-forbidden list (every audit, every drafter)

1. Production HERMES Redis: no `SET`, `DEL`, `EXPIRE`, `FLUSH*`, `CONFIG`, `PUBLISH`, stream writes, `ACL`, `SCRIPT`, `EVAL`, `DEBUG`, `MONITOR`, `SUBSCRIBE`, `KEYS`, blocking reads.
2. The MT5 instances (DEMO and others) and any broker connection; the legacy executors and the legacy dell MT5 container (ADR-MT5-002); no start, stop, restart, exec that mutates. Source inspection of legacy trading executors is permitted (text only); running or modifying them is not.
3. GOAL `main`; any branch other than the worker's own; any force-push; any direct commit to a component `main`; any auto-merge.
4. `backlog/backlog.yaml`, `MANIFEST.md`, `MASTER-BACKLOG.md`, tools, tests, workflows, `README.md`; no `pid_path`, no `DELIVERY_READY`, no approval records, no dispatch.
5. Production services of HERMES, HELIOS, TRON, FALCON, ARES, NEO: no restart, no config edit, no database write. The running Graylog / production FALCON is never mutated or interrupted, and FALCON-outage rehearsals run only against an isolated DEV/test FALCON.
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

This section and `pids/GOLD-AUD-A.md` S1 to S4 are identical on every limit (ruling 6: the stricter value of each limit applies).

Preconditions: Matt's express permission recorded (DR-4; the gate stays TRUE until he expressly permits) and a HELM-operated bounded protocol; a window agreed with the HERMES owner; a wrapper script written in the worker's worktree, reviewed by the auditor before first use, that rejects every command not on the allow-list and enforces the rate cap and the size caps. Who runs it: a HELM-lane operator with approved production read access (not the FORGE worker; ROGUE supervises and does not connect).

| allowed | forbidden |
|---|---|
| `SCAN` with `MATCH` and `COUNT <= 200`, cursor loop with a pause of at least 1 s between pages | `KEYS`, unbounded `SCAN` (no `COUNT` or no `MATCH`), `FLUSHALL`, `FLUSHDB`, `SET`, `DEL`, `UNLINK`, `EXPIRE`, `PEXPIRE`, `PERSIST`, `RENAME`, `HSET`, any write command |
| `TYPE`, `TTL`, `PTTL`, `EXISTS`, `STRLEN`, `HLEN`, `ZCARD`, `SCARD`, `DBSIZE`, `PING` | `CONFIG` (any form), `ACL` (any form, including creating a principal), `DEBUG`, `SAVE`, `BGSAVE`, `SHUTDOWN`, `CLIENT KILL`, `SCRIPT`, `EVAL`, `FUNCTION`, `SLOWLOG RESET` |
| `GET` only when `TYPE` is string and `STRLEN` is at most 64 KiB | `MONITOR`, `SUBSCRIBE`, `PSUBSCRIBE`, `XREAD`, `XREADGROUP`, `XACK`, `XDEL`, `BLPOP` and any blocking call |
| `HGET`; `HGETALL` only when `HLEN` is at most 200 (otherwise record `HLEN` and sample with `HGET`) | `MIGRATE`, `REPLICAOF`, `PUBLISH` |
| `ZRANGE` bounded to 100 and only when `ZCARD` is at most 200; `LRANGE` bounded to 100 | `OBJECT FREQ`, `MEMORY DOCTOR` and anything that mutates LFU/LRU state |
| `SMEMBERS` only after a size pre-check shows `SCARD` is at most 200 | `SMEMBERS` without the pre-check or above 200 members |
| `INFO` with section `server`, `clients` or `persistence` only (`memory` or any other section only if the PO adds it to the approved PID) | `INFO` without a permitted section, `INFO keyspace`, `INFO memory`, `INFO stats`, `INFO all`, `CONFIG GET` (may include secrets) |

Handling: one connection, sequential commands, at most 10 commands per second, at least 1 s between `SCAN` pages, total payload read at most 50 MB, no single reply above 64 KiB (skip and record `STRLEN`); the time-box is the lane PID's S7 (the lane PID states no separate command-count budget). The Redis credential, if the approved read path supplies one (fabric records PROD Redis as open, so none is expected), reaches the client only through an environment variable set inside the wrapper process; it never appears in a command line, a log or evidence (standing rule: never echo `--requirepass`-style arguments), and the operator does not search for one: if authentication is required and none is supplied, stop. No ACL principal is created (that is a mutation); if a read-only principal already exists it is used, otherwise the wrapper is the control and the auditor reviews it first. Values read are sanitised before any repo copy. Prefer a window away from peak market activity.

**What the before/after check does and does not prove (CA/PO adjudication 2026-10-15).** An unchanged Redis `run_id` establishes that there was no restart. It is NOT proof of no data mutation. Data-mutation checks use the audit's own before/after comparison of the sampled keys (key existence, `TTL`/`PTTL` and a hash of each sampled value), taken within this read-only protocol and its caps; changes are explained by normal HERMES publishing only.

### 6.3 Per-lane read permissions

| lane | may read | may not read |
|---|---|---|
| A | `hermes` repo, docs, contracts; HERMES-related GOAL branches; container labels for HERMES services; PROD Redis per 6.2 (only after Matt's express permission; repository and source analysis proceed meanwhile); the HELIOS and FALCON repos for consumer expectations | HERMES historical store contents; vendor credentials; any other Redis |
| B | `HELIOS`, `GOLD-STRATEGY-RUNTIME`, `HSA`, legacy HELIOS lineage repo(s) and branches, deployment files (names only for env keys), image labels; fixtures | PROD Redis; any broker; env values |
| C | GOAL branches (contract, trigger, recon, wave-1 reports); `HELIOS`, `hermes`, `tron` (incl. D1 branch), `falcon` contracts; fixtures | runtime systems (none needed) |
| D | `tron` (main and the unmerged D1 branch), `mt5-gateway` (all branches), GOAL MT5 records (template, readiness, DEMO-verify), instance directory listings with modes only, image labels | broker, the MT5 instances' runtime, logs of MT5 containers, credential files, the legacy executors' runtime (their source text may be read) |
| E | `falcon` repo, contracts, PIDs, the running registry through its read-only query interface and its documented health endpoint; HELIOS/TRON event definitions | FALCON write APIs, Graylog admin, credentials; nothing that mutates or interrupts the running Graylog (authenticated read-only inspection unavailable means UNVERIFIED) |
| F | `CER`, `HSA`, `DARWIN`, `neo` repos; earlier external repository/SaaS evaluation records on the hosts and in fabric (read-only, labelled as fabric) | runtime stores, databases, NEO's legacy executor runtime (source text may be read) |
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
7. [ ] Reusable code and documentation (path and revision, with the reuse boundary), including the REQUIRED disposition table (7.4): every reusable component with generation, criteria, a REUSE / REFACTOR / REPLACE / RETIRE verdict, evidence and comparative engineering cost.
8. [ ] Minimum recommended implementation changes (each tied to an existing or proposed item and its owner), consistent with the disposition verdicts (recommendations only; nothing retired or mutated).
9. [ ] Safety and deployment constraints (what must not be touched; what changes would need a gate).
10. [ ] Independent audit verdict (GREEN / AMBER / RED) and any unresolved findings, with auditor identity role and what the verdict does not cover.

### 7.2 Naming, checks and rules

| item | rule |
|---|---|
| PR title | `[GOLD-AUD-<L>] <short outcome>`; integration PRs `[GOLD-MVP-001] ...` |
| Branch | `wo/GOLD-AUD-<L>-evidence` in the primary repository (same name for a mirror note in another repository); a later GOAL index-contribution PR uses `wo/GOLD-AUD-<L>-index`; `wo/GOAL-GOLD-AUD-<L>` is the PID draft branch, not evidence |
| Evidence location | one primary evidence PR per audit (A hermes, B HELIOS, C GOAL, D GOAL, E falcon, F GOAL), at `docs/evidence/GOLD-AUD-<L>/` in the primary repository (GOAL-primary lanes C, D, F: `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-<L>/`); mirror notes at `docs/evidence/GOLD-AUD-<L>/` in the other named repositories (sanitised for private ones); GOAL holds the cross-component index and compatibility matrix (`EVIDENCE-INDEX.md`, `COMPATIBILITY-MATRIX.md`, owned by `GOLD-MVP-001`), to which each lane contributes an entry (ids, repo, PR URL, head SHA, verdict, open findings, matrix rows) by one PR after its own evidence PR is accepted |
| Required checks | repository CI where it exists; for GOAL, `./tools/goal-validate` and `./tools/secret-scan` clean and the control-plane workflow green; where a component repo has no CI, the PR records a secret scan (full history) and a link-check as manual checks, and says so |
| Merge | no direct-to-main, no auto-merge; a merge needs the independent auditor verdict, CA acceptance and the PO gate; a regular (non-squash) merge |
| Evidence is not acceptance | acceptance needs: approved PID and bounded WO; evidence committed to the correct repo; accessible PR; required checks; independent auditor review; CA acceptance |
| Commit message | `[GOLD-AUD-<L>] ...` with the attribution trailer the programme uses |

### 7.3 Public-repository sanitisation rule

GOAL is public, and some component repositories are public or may become so (the MT5 gateway repository is recorded as public in MT5-READINESS, contradicting an earlier statement; the GitHub PRIVATE change is now eligible for Matt's authorisation, DR-32, and until it is made the repository is treated as public). Therefore, for any evidence that originates from a private repository or from a running system:

- Evidence PRs in a **private** component repo may name internal key families, service names and schema fields, but never secret values, account numbers, login identifiers, internal IPs or hostnames of sensitive services, tokens or customer data.
- Anything copied into **GOAL** (index entries, matrix rows) is generalised one more level: "the dell host", "the PROD HERMES Redis", key families by pattern without hostnames, broker "account `<redacted>`"; no copied payloads, only field names, types and counts.
- Evidence destined for a **public** component repo (HELIOS, mt5-gateway, GOAL) is treated as GOAL-level.
- Each PR runs a sanitisation grep (addresses, key-like strings, account-like numbers, token prefixes) and attaches the empty result; the auditor repeats it.
- If sanitisation would destroy the evidence value, the evidence stays in the private repo and GOAL holds only a pointer (repo, path, SHA).

### 7.4 Disposition table (REQUIRED in every audit; CA/PO legacy application doctrine 2026-10-15)

Every audit's evidence PR contains a **Disposition table** (`DISPOSITION.md`, in the lane's evidence directory). No lane can be accepted without it, and it is part of CA evidence items 7 and 8 (reusable code and documentation; minimum recommended changes). Doctrine in appendix D: the objective is the strongest achievable GOLD MVP architecture, not maximum legacy code reuse.

One row per reusable component in the lane's scope (for example: HELIOS legacy generations, the newer deterministic HELIOS engine, the deployed GOLD stack, `helios_bridge`; NEO's legacy runtime, practice-execution bridge, observer / scorer / auditor / coach and the deployed cron service; FALCON publishers; TRON candidates; legacy executors by source inspection only; CER, HSA and DARWIN components; HERMES contracts and fixtures).

| column | content |
|---|---|
| component | name, repository, path, revision |
| generation | `legacy`, `newer canonical` or `currently deployed` (a component may need more than one row) |
| criteria assessed | architecture fit with the current architecture; code quality; determinism; test evidence (what is proven, not claimed); maintainability; contracts; operational dependencies; integration cost; each with a short evidenced note |
| verdict | exactly one of `REUSE`, `REFACTOR`, `REPLACE`, `RETIRE` |
| evidence | citations (path and SHA, command and output) for the verdict |
| comparative engineering cost | approximate cost of reuse versus refactor versus a clean build, in the same unit, with the basis stated |
| retained value | algorithms, tested logic, contracts and research findings worth keeping whatever the verdict |

Rules. (1) A verdict is a **recommendation only**: nothing is retired, shut down, migrated or mutated by an audit, and any physical retirement needs a separate authorised work order. (2) A clean implementation is acceptable and preferable where it materially simplifies THE GOAL and reduces long-term technical debt; obsolete application architecture is not preserved merely because time was invested. (3) The newer deterministic HELIOS engine is evaluated independently of the legacy HELIOS generations. (4) For NEO, the lane F table explicitly assesses whether a clean read-only intelligence service is preferable to rehabilitating the previous runtime, with the cost comparison. (5) Who adjudicates the verdicts is DR-37 (recommended: CA/PO, per component, after the audit's independent verdict). (6) The independent auditor checks the table is complete and that each verdict follows from its evidence.

## 8. Dispatch-eligibility analysis

### 8.1 What can start the moment PIDs are approved

- **All six audits** can start as soon as each audit PID is approved and its item is `DELIVERY_READY`: each depends only on `GOAL-DCP-001` (CLOSED, accepted terminal), needs no engineering predecessor, and writes only its own branch. Mechanically, once the backlog patch (part 1) is merged they appear in `./tools/goal-ready --pid-wave` as PID-drafting candidates, and in `./tools/goal-ready --with-pid` after approval.
- `GOLD-AUD-A` additionally needs Matt's express permission for production read access (DR-4) and a reviewed wrapper; it is the only one with a pre-start action beyond approval. Until that permission, A proceeds with its GitHub / source analysis half only.
- Six-way parallel FORGE audit dispatch is authorised by the CA/PO adjudication of 2026-10-15 once the conditions in section 14 are satisfied (approved PIDs, backlog readiness, evidence requirements, safety gates).
- `GOLD-MVP-001` is **not** dispatchable until its prerequisites are accepted (it is the last item on the critical path). Its architecture document and runbook skeleton may be drafted early by the PL under the approved PID only when the PO releases them; they must not block anything.

### 8.2 Ordering and feeds

| order | audits | rationale |
|---|---|---|
| wave 0, parallel | A, B, C, D, E, F | independent reads; six concurrent workstreams allowed |
| feeds into C | A (as-built publication) and B (adapter and strategy findings): inputs for CP-1 reality; D (TRON intake facts) and E (FALCON registry facts): SOFT inputs | C reads a soft input only after that lane's facts are committed, otherwise records an assumption. D does not depend on C (ruling 5), so there is no cycle. C starts concurrently, finalises last, and contributes matrix rows to the matrix `GOLD-MVP-001` owns |
| feeds into B | A (key, timeframe and warm-up inventory) | B's compatibility conclusions need it; B can complete the locate-and-reconcile half first |
| feeds into F | B (candidate requirements versus PROD facts), D (what TRON consumes from an edge profile) | F's path matrix is strategy-neutral (evaluated per candidate under review); no lane selects a strategy |
| strategy selection (CA guidance 2026-10-15, item 6) | A (PROD facts) and B (candidate requirements versus PROD facts), reconciled | a PO decision with those inputs (DR-23); only then `GOLD-MVP-001` acceptance planning. Sequence: A and B, reconciliation, selection, acceptance planning |
| feeds into E | A and D (what HERMES, HELIOS and TRON emit; read after committed, otherwise an assumption) | E's minimum publication list |
| consolidation | the `GOLD-MVP-001` PL merges the six lane contribution PRs, one at a time, into `EVIDENCE-INDEX.md` and `COMPATIBILITY-MATRIX.md` | after each lane's evidence PR is accepted; `GOLD-MVP-001` acceptance after all six verdicts |

To keep concurrency safe, each audit freezes a source-revision table at start (7.1 item 2); a source that moves mid-audit is recorded, not chased.

### 8.3 The critical path and where audits shorten it

Serial engineering chains (after PID approvals, from the backlog as it stands on `main` since PR #5 merged, 43 items):

- Strategy chain: `GOAL-CONTRACT-001` → `GOAL-CORE-001` → `HELIOS-T1` → `HELIOS-T2` → `HELIOS-T3` (also needs `GOAL-TRIGGER-001`) → `TRON-T4` intake proof with a real HELIOS.
- Execution chain: `MT5-GW-001` → `-002` → `-003` → `-004` → `TRON-T2`; and `TRON-D1-RATIFY` → `TRON-T1` → `TRON-T3`/`TRON-T4`.
- Evidence chain: `FALCON-T1` plus the minimum publication increment.
- Convergence: `GOLD-MVP-001`.

The long poles are the MT5 gateway chain (four serial items before TRON-T2) and the strategy chain (five). Audits shorten them by:

1. **A** shows what the PROD publication actually carries, so the candidate requirements can be set against it and `HERMES-FACT-001` (the contract of what HERMES publishes) can be an adaptation or declaration of what exists, and no new feed is requested (the lane PID found that the candle and indicator families are documented only in fabric, so the repository record starts with this audit).
2. **B** was expected to find an earlier HERMES to HELIOS integration that could shrink the reader build from construction to adaptation. The lane PID found no completed integration in the searched locations (section 3a; absence elsewhere is UNVERIFIED and B re-runs and extends the search), so the HELIOS-side external adapter stays a construction; B still scopes it to a minimum adaptation plan, and tabulates candidate requirements against A's PROD facts so that the later PO selection (not B) can validate `GOAL-CONTRACT-001` against a real package.
3. **C** freezes the minimum contracts early, which unlocks `GOAL-CORE-001`, `HELIOS-T3` and `TRON-T4` authoring in parallel.
4. **D** states the smallest DEMO path, so `MT5-GW-003/-004` and `TRON-T2/T3` are scoped to the minimum rather than the full gateway ambition, and confirms the shape of the named gap `GAP-TRON-FIXED-SIZE-DEMO-RISK` (section 3b), which needs its own item (proposed, section 11.4).
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
- [ ] After acceptance, the lane's index-entry and matrix-row contribution PR exists against `EVIDENCE-INDEX.md` and `COMPATIBILITY-MATRIX.md` (one lane per PR; single writer the `GOLD-MVP-001` PL); the rows are consistent with the evidence.
- [ ] Accessible PR; required checks green; no direct-to-main; no auto-merge.
- [ ] Disposition table present (section 7.4): every reusable component has generation, criteria, a REUSE / REFACTOR / REPLACE / RETIRE verdict, evidence and a comparative cost; no component was retired, stopped or mutated.
- [ ] Verdict recorded (GREEN/AMBER/RED) with unresolved findings; CA acceptance recorded separately by CA/PO.

### 9.3 Return package and reporting

Each audit returns: (a) a GitHub evidence PR; (b) the source SHA of every repository read; (c) a contract matrix; (d) reusable implementation findings; (e) specific gaps; (f) the disposition table (section 7.4); (g) a fresh independent audit verdict. ROGUE returns results individually as each lane finishes, not as a batch. A lane cannot be accepted without its disposition table.

## 10. Risks

| # | risk | mitigation |
|---|---|---|
| R-1 | A lane audit touches production state | read-only protocol and wrapper (6.2), reviewed first; Matt's express permission (DR-4); single lane |
| R-2 | No previously completed HERMES to HELIOS integration is found in the searched locations (B); absence elsewhere is UNVERIFIED | realised in B's drafting (section 3a, bounded conclusion): the reader is a build item, the HELIOS-side external adapter outside the pure engine (CA guidance 2026-10-15, item 1); B's stop condition holds (no second reader may be built or prototyped by the audit; a negative result needs a recorded search method) |
| R-3 | Contract drift while six audits run | source-revision tables; one matrix owned by `GOLD-MVP-001`; contract changes after acceptance restart affected rows |
| R-4 | Duplicate scope with existing PIDs (`HERMES-CUR-001`, `FALCON-T1`, `TRON-D1-RATIFY`) | all six lanes are new bounded items with `Complements:` lines and a documented amendment fallback (section 3); no existing PID is edited |
| R-5 | `GOLD-MVP-001` overlaps `PAPER-E2E-001` | PD-1; recommended option keeps both with a clear dependency |
| R-6 | Hidden missing items (the named gap `GAP-TRON-FIXED-SIZE-DEMO-RISK`, FALCON event publication, MT5 typed API) | listed in section 3b, the gap register and PD-3/PD-4; audits D and E confirm shape; `GOLD-MVP-001` AC-8 and AC-16 require the TRON gap closed |
| R-7 | Simulation mistaken for DEMO proof; PAPER set early | GOLD-MVP-001 AC-9 to AC-11 and S-6; title and ADR-MT5-001 reference |
| R-8 | Public-repo leakage from private evidence | 7.3 rule, sanitisation grep, auditor repeat, `secret-scan` |
| R-9 | `MT5 gateway` repository is public while a prior record says private (MT5-READINESS) | flagged for owner decision (DR-32; the GitHub PRIVATE change is eligible for Matt's authorisation); lane D treats mt5-gateway evidence as public-level until changed |
| R-10 | Price-basis mismatch (live feed vs futures truth vs CFD) invalidates a performance claim | label the MVP a plumbing proof (GOLD-MVP-001 D-6) |
| R-11 | Six concurrent PR streams create merge noise on `MANIFEST.md` | ROGUE regenerates; disjoint paths (5.2) |
| R-12 | TRON D1 and its three trigger models are not ratified (Matt gate) | audit D consumes `TRON-D1-RATIFY`; MVP waits for the ratification |
| R-13 | Audit scope creeps into implementation | each audit PID carries a no-implementation non-goal; auditor checks the file list |
| R-14 | Auditor independence eroded when one auditor covers two lanes | pairing chosen to avoid reviewing one's own lane; CA acceptance is separate |
| R-15 | A strategy is chosen, or appears chosen, before the PROD facts and candidate requirements are reconciled | CA guidance 2026-10-15, item 6: no lane selects or ranks; the HSA packages are candidates under review; selection is a PO decision (DR-23) after audits A and B; `GOLD-MVP-001` AC-16 and S-9 |
| R-16 | A third-party engine or SaaS enters the MVP through an external evaluation | CA guidance 2026-10-15, item 4: binding constraint; lane F evaluations are information only; `GOLD-MVP-001` AC-17 and S-5 |
| R-17 | FALCON becomes a dependency of execution | CA guidance 2026-10-15, item 3: lane E EP-9 tests, `GOLD-MVP-001` AC-12 and S-10 (execution completes with FALCON ingestion stopped; acceptance is deterministic LOGICAL decision and reconciliation equivalence, not byte identity; rehearsals only against an isolated DEV/test FALCON) |
| R-18 | A legacy implementation is kept only because effort was invested in it, or is retired without authority | CA/PO legacy application doctrine 2026-10-15: disposition table in every audit (7.4); verdicts are recommendations; adjudication by DR-37; physical retirement needs a separate authorised work order |

## 11. Backlog patch description (specified, NOT applied here)

**This section is a specification only.** The consolidation work order did not edit `backlog/backlog.yaml`, set any `pid_path`, move any item to `DELIVERY_READY`, record any approval or dispatch anything. The patch is applied later, by ROGUE, after the PO approves.

**Ordering and expected counts.** GOAL PR #5 has merged (2026-10-15, merge commit `90323b3`; see 1b), taking the backlog from 40 to 43 items by adding `GOAL-TRIGGER-001`, `TRON-D1-RATIFY`, `HSA-C1`. Expected pinned item counts: **43 on `main` today**; **49 after part 1** (43 + 6 audit items); **50 after part 2** (49 + `GOLD-MVP-001`). The former '46 if part 1 were applied on the pre-#5 `main`' alternative is moot. The count-pinning tests (`tests/test_cli.py`, `tests/test_model.py`, `tests/test_first_wave.py`) must be updated in the same change as each patch part. Part 2 additionally waited for the PO ruling on PD-1, which is resolved; it now waits only for the portfolio merge and approved PIDs.

**Lane A matt gate.** `GOLD-AUD-A` carries `matt_gate: true` as the production-read gate only: it stays TRUE until Matt expressly permits production Redis read (DR-4). It is the only audit with a Matt gate, and the gate does not apply to its GitHub / source analysis. `GOLD-MVP-001` is Matt-gated for its FINAL DEMO acceptance (capital risk), not for the audits.

**Adjudicated values (CA/PO adjudication 2026-10-15).** Priority P0 for A to E and P1 for F; lane `research` for all six; risk as the lane PIDs. The YAML below carries these values; it is still NOT applied.

### 11.1 Interaction with GOAL PR #5 (merged) and PR #6 / #8

- **PR #5** (`wo/GOAL-RECON-PR`, **MERGED** 2026-10-15 as `90323b3`; audited head `e2671ff`) took the backlog from 40 to 43 items (added `GOAL-TRIGGER-001`, `TRON-D1-RATIFY`, `HSA-C1`) and edited `backlog/backlog.yaml`, `MASTER-BACKLOG.md`, `MANIFEST.md` and three tests that pin the item count (`tests/test_cli.py`, `tests/test_model.py`, `tests/test_first_wave.py`). This portfolio's `GOLD-MVP-001` depends on `GOAL-TRIGGER-001` and `TRON-D1-RATIFY` (transitively), which are now on `main`. Therefore **part 2 (GOLD-MVP-001 and the PAPER-E2E-001 edge) is no longer blocked by #5**; it still waits for the portfolio merge and approved PIDs. Part 1 (the six audit items, depending only on `GOAL-DCP-001`) was always independent of #5 and applies on top of the 43-item `main`.
- Both patches touch `backlog/backlog.yaml`: apply serially, never as two concurrent writers. The pinned item count becomes 49 after part 1 (on the 43-item `main`) and 50 after part 2 (43 + 6 + 1). The count-pinning tests must be updated in the same change (as #5 did). Lane values below were normalised to `research` for all six audits and risk to `medium` for C and D, to match the lane PIDs; priority is kept P0 pending DR-13.
- **PR #6** (`wo/GOAL-BACKUP-PLAN`, OPEN, head `84fc7ce`) is documentation only (`MANIFEST.md`, two `operations/` files) and is superseded in practice by the clean replacement **PR #8** (`wo/GOAL-BACKUP-PLAN-CLEAN`, head `096673e64751429edc67ce7a03a5a51b3a7531ad`), because an earlier draft contained more detailed operational text than is appropriate for a public repository; the merge decision on #6 / #8 is pending CA. Heads are current at time of writing, reconcile at merge. No backlog interaction; the only collision is `MANIFEST.md` with any later change, resolved by `./tools/goal-docs --write` at integration.
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
    matt_gate: true   # production-read gate only: TRUE until Matt expressly permits production Redis read (DR-4)
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
    priority: P1
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

### 11.3 Part 2: integration item and edge (PR #5 has merged, so no longer blocked by it; applies after the portfolio merge and approved PIDs; PD-1 is resolved by the CA/PO adjudication of 2026-10-15)

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
    matt_gate: true   # capital risk: Matt-gated for the FINAL DEMO acceptance, not for the six audits
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - decisions/ADR-MT5-001-REUSE-CONTAINER-REPLACE-BRIDGE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md
```

Edge change (PD-1 resolved: both items kept; `PAPER-E2E-001` becomes a subsequent broader qualification): `PAPER-E2E-001.depends_on` gains `GOLD-MVP-001`. Later, after audits D and E: add the minimum FALCON publication item, and (approved by the adjudication, DR-36, subject to Lane D scope validation) the TRON fixed-size DEMO risk item of section 11.4, to `GOLD-MVP-001.depends_on` once those items exist (PD-4).

State is `PID_DRAFT` for all seven because their PID candidates are drafted (`pids/GOLD-AUD-A.md` to `-F.md` and `pids/GOLD-MVP-001.md` exist in the consolidated branch, unapproved); none may carry a `pid_path` until CA/PO approval, none is `DELIVERY_READY`. The `target_repository` of D and F is `maff0000/GOAL` as in their lane PIDs (mirror notes go to component repositories; ruling 1). `./tools/goal-validate` on the patched backlog is expected clean (all ids resolve; part 2's dependency targets are on `main` since PR #5 merged). ROGUE regenerates generated documents and updates the item-count tests in the same change.

### 11.4 Part 3: `TRON-T3A` for `GAP-TRON-FIXED-SIZE-DEMO-RISK` (APPROVED as proposed by CA/PO adjudication 2026-10-15, subject to Lane D scope validation; NOT applied here)

Parts 1 and 2 above are the patch as specified. `TRON-T3A` is APPROVED as a proposed P0 / high-risk, credential-free minimum DEMO sizing and risk item (DR-36 resolved with the condition that `GOLD-AUD-D` validates its scope). It is not applied here and not counted in the 49 and 50 above; it is a third serial governed backlog change after part 2 (item count 51), with the count-pinning tests updated in the same change (section 14). **A single kill switch exists: there are no competing TRON kill switches. `TRON-T3A` must reuse or extend the `TRON-T3` hard-risk / kill-switch design and must not create a second one.** The dependency link to `TRON-T3` is to be recorded at application; whether the id stays `TRON-T3A` is for CA/PO at that change.

```yaml
  # APPROVED AS PROPOSED (DR-36, CA/PO adjudication 2026-10-15), subject to Lane D scope validation. NOT APPLIED HERE.
  # GAP-TRON-FIXED-SIZE-DEMO-RISK. Must reuse/extend the TRON-T3 hard-risk / kill-switch design; no second kill switch.
  - id: TRON-T3A
    title: "TRON fixed-size DEMO risk and sizing policy: fixed base quantity from config, one position per instrument, max open positions, daily loss and trade-count guard, kill switch with setter, hard gates before submit (credential-free)"
    lane: trading
    component: TRON
    target_repository: maff0000/tron
    priority: P0
    risk: high
    state: ARCHITECTURE_REQUIRED
    depends_on:
      - TRON-T1
    po_gate: true
    matt_gate: true   # proposed: DEMO base quantity and loss limits are capital-adjacent parameters; PO may reduce to false
    pid_path: null
    architecture_refs:
      - architecture/DELIVERY-CONTROL-PLANE.md
      - audits/2026-10-15/gold-mvp/PORTFOLIO.md
```

Edges to record at application: `GOLD-MVP-001.depends_on` and `PAPER-E2E-001.depends_on` gain `TRON-T3A`. It must not depend on `CER-R1` (that is the point of the gap). It carries no broker credential and no DEMO session. Required content and acceptance linkage are in section 3b. Its PID would be authored by the TRON-owning persona after `GOLD-AUD-D` confirms the shape.

## 12. PO decisions needed (original PD list; superseded by `DECISION-REGISTER.md`)

The register consolidates PD-1 to PD-12 with every lane PID's open decisions and the PR #5 and #6 items, de-duplicated and ranked. The PD ids below are kept as references. Status after the CA/PO adjudication of 2026-10-15: PD-1 (keep both; subsequent broader qualification), PD-2 (`capital`, Matt-gated for final DEMO acceptance), PD-3 (all six new), PD-6 (six-way dispatch, conditions in section 14), PD-10 (merge and application order, section 14) are resolved; PD-5 stays gated (Matt's express permission, DR-4); PD-8 stays gated on audits A and B; PD-4, PD-7, PD-9 and PD-11 remain open as recorded in `DECISION-REGISTER.md`. The recommendation columns below are historical. PD-12 is resolved by ruling 1 (appendix); PD-3 is a confirmation (DR-3). Lane drafters' conclusions on PD-3 (D is a new item) and the amend-or-new questions of A, B, C, E, F are recorded in section 3; the PO confirms them in the register.

| id | decision | options | recommendation | blocks |
|---|---|---|---|---|
| PD-1 | `GOLD-MVP-001` versus `PAPER-E2E-001` | (a) supersede; (b) keep both, `PAPER-E2E-001` depends on `GOLD-MVP-001`; (c) keep independent | (b) | approval of `GOLD-MVP-001` |
| PD-2 | Header gates of `GOLD-MVP-001` | risk `capital` + Matt gate; or `high` with Matt gate at PAPER only | `capital`, Matt gate true | approval of `GOLD-MVP-001` |
| PD-3 | Is lane D a new item or an increment of `TRON-D1-RATIFY` | new (lane D drafter concluded new) or fold in | new: keeps the audit outside a Matt-gated ratification | dispatch of D |
| PD-4 | Add the missing MVP items: minimum FALCON `strategy_trigger`/`tron.*` publication (the sizing half is now the named gap `GAP-TRON-FIXED-SIZE-DEMO-RISK`, section 3b, with its own register item DR-36) | add after audits D and E confirm shape; fold into FALCON-T3/T4 subset | add bounded items after D and E report; do not wait for TRON-T5/CER-R1 | acceptance, not approval |
| PD-5 | Read-only production Redis access for lane A | allow under 6.2 with Matt notification; require Matt gate; repo-only audit | allow under the 6.2 protocol; Matt informed and may waive the gate in one line; gate true by default until waived | start of A's runtime half |
| PD-6 | Are all six audits dispatched concurrently | all six in wave 0; stagger C last | all six (the permission design makes them collision-free) | ROGUE scheduling |
| PD-7 | Composition vehicle (`GOLD-STRATEGY-RUNTIME`) and the deferred `PLATFORM-RT-001` | adopt; adapt; compose per component | decide after audit B; do not rebuild a delivered runtime | acceptance |
| PD-8 | Strategy selection and its qualification threshold (restated by CA guidance 2026-10-15, item 6) | PO decides after audits A and B have reported and been reconciled, with those inputs; threshold fixed before the run | no recommendation here; no strategy is selected or implied; HSA packages are candidates under review only | acceptance planning |
| PD-9 | Price basis for the MVP | accept difference for a plumbing proof; require HMT-3H alignment first | accept, with a no-performance-claim label | acceptance |
| PD-10 | Order of applying backlog changes | #5 first, then parts 1 and 2 serially; part 1 on `main` ahead of #5 | #5 first; then part 1; then part 2 after PD-1 | integration |
| PD-11 | Visibility of `maff0000/mt5-gateway` (public today per MT5-READINESS; an earlier record says private) | owner confirms | owner decision, outside this portfolio; lane D evidence is treated as public-level meanwhile | none (flagged) |
| PD-12 | Evidence PR spread for lanes D and F (one primary PR plus companion notes versus one PR per repo) | primary + companion notes | primary + companion notes, to bound the PR count | lane PIDs |

## 13. Method and limits

Read, read-only, on 2026-10-15: GOAL `main` @ `1739e74` documents listed in `pids/GOLD-MVP-001.md` Evidence; PR #5 and #6 file lists via `gh`; branch diffs and the reconciliation summary; the contract/trigger PIDs' headings and Current state; MT5 readiness headings and PR topology; TRON D1 ratification package head; GROUP-E, RECON-H1 and RECON-H2 excerpts; local git logs of the HELIOS and GOLD-STRATEGY-RUNTIME clones. Consolidation edit (later the same day): the seven drafted branches were merged into one branch and all six lane PIDs were read; sections 1 to 3a, 7.1, 8.3, 10, 11 and 12 were reconciled to them. Third pass (same day): CA guidance 2026-10-15 (appendix B) was applied to the portfolio, `GOLD-MVP-001`, lanes A to F and the register; sections 1, 1a, 2, 3a, 3b, 4, 8, 10, 11.4, 12 and appendix B changed. Still no backlog edit, no `pid_path`, no approval record, no dispatch and no push. Not done: no production system, Redis, broker, container or database was accessed; component repositories beyond the cited excerpts were not audited (that is what the audits are for). Statements about the content of the PROD XAUUSD publication, the location of the earlier HERMES to HELIOS integration, and the TRON/MT5 implementation candidates are UNVERIFIED here by design. No `goal-docs --write`, no backlog edit, no `pid_path`, no approval record, no dispatch, no push. Fourth pass (adjudication, same day): the CA/PO adjudication and the legacy application doctrine were applied to this document, `GOLD-MVP-001`, lanes A to F and the register; sections 0a, 1, 1a, 2, 3, 3a, 3b, 4, 5.3, 6.2, 6.3, 7.3, 7.4, 8, 9.3, 10, 11, 12, 14 and appendices B to D changed. Nothing was run against any production system.

## 14. Merge sequence and dispatch record

Recorded from the CA/PO adjudication of 2026-10-15. This is a record of the ordering CA set, not a merge or dispatch performed here.

**Governed GOAL merges, in CA's order.** GOAL PR #5, then PR #6, then the corrected PR #7 (this portfolio). **Current state (1b):** PR #5 is merged (`90323b3`; audited head `e2671ff`); the backup-plan documentation PR is #6 (head `84fc7ce`), being replaced by the clean PR #8 (head `096673e6`) pending CA's decision; then this PR. Heads are current at time of writing and are reconciled at merge.

**Per-merge gates.**

1. Independent audit GREEN, or an acceptable GREEN-WITH-NOTICE, at the exact head being merged.
2. CI and GOAL validation green (`./tools/goal-validate`, `./tools/secret-scan`, the test suite, `./tools/goal-docs --check`).
3. Reconcile with the current `main`.
4. Regenerate `MANIFEST.md` and the derived views (`./tools/goal-docs --write`, at integration only).
5. Verify the intended diff, and that there are no unintended backlog or delivery-state changes.
6. Preserve history and merge provenance (regular merge, no squash, no force push).
7. Stop on substantive changes or failed gates and return to CA.

**After the portfolio merge.** Backlog entries are applied in serial governed changes (never concurrent writers), each recording the exact IDs, the approved PID paths, the delivery states and the dependency links: part 1 (six audit items), part 2 (`GOLD-MVP-001` and the `PAPER-E2E-001` edge), part 3 (`TRON-T3A`). `pid_path` is set only for a PID that CA/PO has approved in the approval flow.

**Dispatch conditions.** Six-way parallel FORGE audit dispatch is authorised once: each audit PID is valid, approved and `DELIVERY_READY` before dispatch; the backlog entries exist; the evidence requirements (section 7, including the disposition table) are in the dispatched work order; and the safety gates hold (section 5.3 and 6; for lane A, Matt's express permission before any production read). ROGUE returns results individually as each lane finishes. Nothing in this section dispatches or approves anything.

## Appendix A: Resolved by programme-controller rulings

These are delivery-coordination rulings by the programme controller, not architecture decisions. They are recorded verbatim so that CA can overrule any of them. Each mechanical contradiction between the lane PIDs and this portfolio that they cover has been resolved in the lane PIDs, this document and the register. Ruling 10 lists what was deliberately left open.

1. EVIDENCE LOCATION (DR-15): each audit has ONE primary evidence PR; GOAL holds the cross-component index and compatibility matrix. Component-repo detailed evidence goes into the component repo as a mirror PR where the component repo is public or private-appropriate (private-repo evidence is sanitised before anything is placed in GOAL). Primary PR per lane: A: maff0000/hermes (evidence) with GOAL index entry; B: maff0000/HELIOS; C: maff0000/GOAL; D: maff0000/GOAL primary (TRON/MT5 facts) with mirror notes in tron and mt5-gateway; E: maff0000/falcon; F: maff0000/GOAL primary with mirror notes in CER/HSA/DARWIN/neo (neo is private: sanitised). Make every PID's header, Deliverables, checklist and the portfolio table consistent.
2. BRANCH NAMING: one convention everywhere: audit branches are wo/GOLD-AUD-<L>-evidence in the primary repo (e.g. wo/GOLD-AUD-A-evidence); PID-authoring branches already named wo/GOAL-GOLD-AUD-<L> are PID drafts, not evidence branches. Fix E and D checklists and the portfolio.
3. EVIDENCE PATHS: one convention: docs/evidence/GOLD-AUD-<L>/ in the primary repo (GOAL uses audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-<L>/ for the GOAL-primary lanes C, D, F and for index entries). Update A (docs/audits/gold-prod-redis/ -> docs/evidence/GOLD-AUD-A/), B (docs/evidence/GOLD-AUD-B.md -> docs/evidence/GOLD-AUD-B/), D, E, F consistently.
4. INDEX AND MATRIX OWNERSHIP: GOLD-MVP-001 owns audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md and COMPATIBILITY-MATRIX.md (single writer: the GOLD-MVP-001 PL). Lane PIDs contribute entries by PR to those files only AFTER their own evidence PR is accepted, one lane per PR to avoid conflicting writes; GOLD-AUD-C's contract packages live under contracts/packages/ (GOAL) and its matrix rows are contributed into COMPATIBILITY-MATRIX.md, not a second matrix. Fix C, D, E, F and the portfolio collision table.
5. CIRCULAR DEPENDENCY C<->D: ruling: D does not depend on C. D uses an assumption register for trigger-intake until GOAL-TRIGGER-001 exists; C consumes D's TRON intake facts as a SOFT input (read after D's facts are committed, otherwise records an assumption). C inputs: A and B (CP-1 reality), D's intake facts (soft), E's registry facts (soft; portfolio 8.2 must say soft). Remove any hard cycle; state the ordering explicitly.
6. LANE A PROTOCOL: apply the STRICTER value of each limit in portfolio 6.2 and PID A S1-S3: SCAN COUNT <= 200, rate <= 10 commands/s, HGETALL <= 200 fields; permit INFO sections server, clients, persistence only (memory and others only if the PO adds them); SMEMBERS only with a size pre-check (SCARD <= 200) else forbidden; who runs: a HELM-lane operator (not 'the worker'); credential via environment variable only; no ACL principal creation. Make the two documents identical on this.
7. GOAL-TRIGGER-001 STATUS: the drafted PID candidate is on branch wo/GOAL-CONTRACT-TRIGGER (commit 64c843b), a backlog item for it is added by GOAL PR #5 (open), neither is on main. (superseded: see 1b) Fix lane D's statement that it is 'not yet authored' and make C/D/E consistent.
8. RSI METHOD: keep 'HERMES RSI is Cutler SMA-14' as sourced from lane C; remove the unsourced claim that HELIOS uses Wilder (say: HELIOS's RSI method is not stated in any lane PID; audit B/C to confirm).
9. HELIOS SCHEMA STRING: state both facts (advertised helios.market_fact/1.0.0; fixtures/config/tests also accept hermes.market_fact/1.0.0) wherever it appears.
10. Leave as PO decisions (do NOT resolve): lane vocabulary (research for all six is the portfolio value; note the backlog vocabulary is shared/research/trading/ops), priorities (P0 vs P1 for E and F: DR-13), risk values, blocking status of F D2/A D1/E D-2, Lane B fallback (inference, DR-14), mt5-gateway visibility (DR-32). Update DECISION-REGISTER.md so every remaining open item appears once, remove entries resolved by rulings 1-9 (record them in a short 'Resolved by programme-controller rulings' appendix in PORTFOLIO.md with the rulings verbatim so CA can overrule), and fix the register's counts.

Register entries removed or reduced by these rulings: DR-15 (rulings 1 to 3, evidence PR location and spread; the question of the `neo` mirror note moves into DR-18) and DR-19 (ruling 5, the trigger-assumption area proceeds with an assumption register); also retired in the lane PIDs: E D-9 (rulings 1 to 3), D 5 (ruling 5). Ruling 6 closes the open protocol-limit differences between section 6.2 and PID A (no register entry existed).

## Appendix B: CA guidance 2026-10-15 (binding architectural guidance for the consolidation)

Central Architecture issued the following binding guidance. It is recorded here as CA guidance, not as a controller ruling, and as given to the consolidation editor (summarised faithfully; no wording is the editor's decision). The register lists what it resolved in its own appendix.

1. **HERMES owns Redis publication; a HELIOS-side external adapter owns consumption and translation.** The adapter sits outside the pure HELIOS engine, which stays execution-blind and deterministic with no Redis or network imports. GOAL approves the interface (CP-1). Effect: lane B, lane C, `GOLD-MVP-001` and this portfolio updated; the question where the reader lives (lane C D-C4) is resolved; the `v1` to `hermes.market_fact/1.0.0` mapping (D-C3) belongs to the adapter, with GOAL approving the interface and a `HERMES-FACT-001`-style contract of what HERMES publishes. Open at that time: who owns the CP-1 freeze mechanics, HELIOS's version-string inconsistency, the adapter's repository and PID author (DR-34, DR-35). Update (CA/PO adjudication 2026-10-15): DR-34 and DR-35 are resolved (the HELIOS repository outside the pure engine; `HELIOS-T2` implements; the HELIOS architect authors the bounded work orders), and `HERMES-FACT-001` owns HERMES publication semantics; the version-string fix stays open (DR-27).
2. **`GOAL-TRIGGER-001` owns signed-trigger, outbox and inbox semantics.** No competing trigger contract in HELIOS, TRON or FALCON. Lane C, D, E and `GOLD-MVP-001` wording checked and aligned.
3. **FALCON is evidence-only and must not block execution:** asynchronous, non-blocking, bounded queue; execution completes with FALCON ingestion stopped. Lane E and `GOLD-MVP-001` already said so; strengthened (EP-9, acceptance 6, AC-12, S-10).
4. **No new third-party engine or SaaS dependency for the MVP.** Binding constraint in this portfolio, `GOLD-MVP-001` (non-goals, AC-17, S-5) and lane F. Lane F's external evaluations are information only; the licence-posture decision (D9, DR-21) is moot and retired.
5. **Missing TRON fixed-size DEMO risk policy recorded explicitly** as `GAP-TRON-FIXED-SIZE-DEMO-RISK` (section 3b): required content, owner TRON, credential-free, candidate item listed as a proposed part-3 item for PO decision (section 11.4, DR-36), and required for `PAPER-E2E-001` and `GOLD-MVP-001` acceptance.
6. **Do not select the GOLD strategy before the actual HERMES PROD facts and candidate requirements are reconciled.** No strategy is recommended or implied as selected; the HSA packages are candidates under review. Sequence: audits A and B, reconciliation, strategy selection (PO decision), `GOLD-MVP-001` acceptance planning. PD-8, DR-23, lane F D2 and lane B first-strategy text restated.
7. **Return the final PID portfolio and decision register for PO approval.** Both documents are updated and returned; neither is approved, and no approval is recorded by this editor.

8. **Legacy application doctrine** (added by the CA/PO legacy application doctrine of 2026-10-15; full text appendix D): legacy HELIOS and NEO implementations have no automatic right to remain part of THE GOAL; every audit distinguishes legacy generations, newer canonical implementations and currently deployed services and ends each reusable component in REUSE, REFACTOR, REPLACE or RETIRE with evidence and a comparative cost; the strongest achievable GOLD MVP architecture is the objective, not maximum legacy reuse. Verdicts are recommendations only; no retirement, shutdown or production mutation is authorised.

Other CA decisions of 2026-10-15, for context only: MT5 Gateway Gate A accepted with notices (the original text read "merged (GOAL `main` at `6263d61f`)"; corrected by CA/PO adjudication 2026-10-15 to the canonical `maff0000/mt5-gateway` `main` @ `6263d61f4cb0d4d5b16337e67c30f409bc9c5051`, PR #9 merged, issue #10 tracking the template-hardening notices); the unrestricted bridge is not to be connected to TRON; no production or broker mutation is authorised; no audit dispatch and no backlog change until this portfolio is approved.

## Appendix C: CA/PO adjudication 2026-10-15 (APPROVED WITH CORRECTIONS)

Central Architecture (PO) adjudicated GOAL PR #7 on 2026-10-15 and returned it APPROVED WITH CORRECTIONS. Summarised faithfully; the wording of each ruling is CA/PO's. Provenance for everything below: 'CA/PO adjudication 2026-10-15'. PID Approval sections remain PENDING; approval is recorded by CA/PO only in the approval flow.

**A. PID decisions.** `GOLD-MVP-001` and `GOLD-AUD-A` to `-F`: architecture and scope approved. The six audits are separate audit work items, not amendments of component implementation PIDs. Priorities A to E P0, F P1; all six research lane with the risk levels in their PIDs. `GOLD-MVP-001` is capital-risk and Matt-gated for its FINAL DEMO acceptance, not for the six audit investigations; lane A keeps the production-read gate. Six-way parallel FORGE audit dispatch is authorised once approved PIDs, backlog readiness, evidence requirements and safety gates are satisfied.

**B. Rulings.** Keep `GOLD-MVP-001` and `PAPER-E2E-001`, the latter becoming a subsequent broader qualification (PD-1). `HERMES-FACT-001` owns HERMES publication semantics; GOAL approves the CP-1 interface using the A/B/C reconciliation. The HERMES Redis reader and adapter belong in the HELIOS repository outside the pure engine; `HELIOS-T2` owns the implementation; the HELIOS architect authors the bounded work orders (DR-34, DR-35). `GOAL-TRIGGER-001` is the sole trigger / outbox / inbox authority; its technical and Matt decision gates stay open. FALCON is evidence-only. No new trading engine or SaaS prerequisite. `TRON-T3A` is APPROVED as a proposed P0 / high-risk, credential-free minimum DEMO sizing and risk item subject to Lane D scope validation (DR-36); one kill switch exists, `TRON-T3A` reuses or extends the `TRON-T3` design and creates no second. No GOLD strategy is selected until audits A and B are accepted and reconciled (PD-8). Production Redis read for lane A requires Matt's express permission and a HELM-operated bounded protocol (DR-4 remains TRUE until he permits; GitHub / source analysis proceeds meanwhile). Lane E may not mutate or interrupt the running Graylog; where authenticated read-only inspection is unavailable the part is UNVERIFIED. Source inspection of legacy trading executors is permitted; running or modifying them is not (lane D decision 4 resolved with that boundary). Each audit returns a GitHub evidence PR, source SHA, contract matrix, reusable implementation findings, specific gaps and a fresh independent audit verdict; ROGUE returns results individually.

**C. Corrections.** (1) MT5 Gateway Gate A is CLOSED GREEN WITH NOTICES at canonical `maff0000/mt5-gateway` `main` @ `6263d61f4cb0d4d5b16337e67c30f409bc9c5051` (PR #9 merged; issue #10 tracks template-hardening notices including secrets ownership and symlink handling, to be resolved before the template is used; no TRON connection to the unrestricted RPyC bridge; functional Vantage DEMO proof remains a separate gated workstream; the GitHub PRIVATE change is eligible for Matt's authorisation); older mt5-gateway heads, 'PR #9 open' and 'stale clone' states are replaced; GOAL PR heads (#5 `e2671ff`, #6 `84fc7ce`) are 'current at time of writing, reconcile at merge' (superseded: see 1b). (2) Universal claims that no Redis-to-HELIOS integration exists become bounded conclusions: what was searched, what was found, 'no completed integration was found in the searched locations; absence elsewhere is UNVERIFIED', with the re-run / extend acceptance item kept. (3) FALCON-outage acceptance is deterministic LOGICAL decision and reconciliation equivalence (same trigger dispositions, same orders / fills / positions reconciliation outcome, same terminal states; FALCON-side counters and timestamps excluded), not byte identity; rehearsals run only against an isolated DEV/test FALCON. (4) An unchanged Redis `run_id` establishes no restart, not no data mutation; mutation checks use the audit's own before/after key / TTL / value-hash comparison of the sampled keys within the read-only protocol.

**D, E.** Historical audit evidence is not changed to conceal findings; existing sections are kept where unaffected; the merge sequence and dispatch record is section 14.

## Appendix D: CA/PO legacy application doctrine 2026-10-15 (binding)

Issued by CA/PO as an additional instruction on 2026-10-15; provenance 'CA/PO legacy application doctrine 2026-10-15'. Text as given:

HELIOS and NEO have significant pre-GOAL engineering history. Their existing implementations have no automatic right to remain part of THE GOAL. Each audit must distinguish legacy generations, the newer canonical implementations, and currently deployed services. Assess each reusable component objectively against current architecture, code quality, determinism, test evidence, maintainability, contracts, operational dependencies and integration cost. Every assessment must conclude REUSE, REFACTOR, REPLACE or RETIRE, with evidence and an approximate comparative engineering cost. Retain genuinely valuable algorithms, tested logic, contracts and research findings. Do not preserve obsolete application architecture merely because time was invested building it. A clean implementation is acceptable and preferable when it materially simplifies THE GOAL and reduces long-term technical debt. For HELIOS, evaluate the newer deterministic engine independently of legacy HELIOS generations. For NEO, explicitly assess whether a clean, read-only intelligence service is preferable to rehabilitating the previous runtime. No physical retirement, service shutdown or production mutation is authorised by this instruction. Objective: the strongest achievable GOLD MVP architecture, not maximum legacy code reuse.

Applied as: section 1a item 8; the REQUIRED disposition table, section 7.4 (evidence items 7 and 8, section 9 checklist and 9.3, every lane's acceptance); lane B (HELIOS generations), lane F (NEO and CER / HSA / DARWIN), lanes A, C, D, E and `GOLD-MVP-001`; register DR-37 (who adjudicates the verdicts; recommended CA/PO per component after the audit's independent verdict; any physical retirement needs a separate authorised work order).

# GOLD-MVP-001 — GOLD MVP cross-component integration and acceptance (one governed XAUUSD strategy on Vantage DEMO)

**Lane:** trading  
**Target repository:** `maff0000/GOAL`  
**Priority:** P0  
**Risk:** Capital (proposed; carries the explicit PAPER gate, see Open decisions D-2)  
**Matt gate:** Yes (proposed; see D-2)  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE

Header values are PROPOSED (lane vocabulary is the backlog set {shared, research, trading, ops}). `GOLD-MVP-001` is not yet in `backlog/backlog.yaml`; the exact
backlog patch is specified in `audits/2026-10-15/gold-mvp/PORTFOLIO.md` section 11 and is not applied.
Central Architecture/PO set the final values.

## Status

DRAFT CANDIDATE for Central Architecture review. Not approved. Not DELIVERY_READY.

This PID owns **cross-component integration and acceptance only**. It is not a component implementation PID:
every component change lands in the component's own PID (HERMES, HELIOS, TRON, MT5 gateway, FALCON, CER and
their neighbours) and is tracked by that PID's backlog item. This PID owns the single end-to-end acceptance
event, the cross-component evidence index, the consolidated contract compatibility matrix and the acceptance
runbook, and nothing else.

## Purpose

Deliver, and prove, one verified reusable integration foundation for a single XAUUSD strategy: a governed
strategy version consumes HERMES market facts, HELIOS evaluates it deterministically and emits a signed trigger
into a durable outbox, TRON receives it through an idempotent inbox, applies its own sizing and hard-risk gates and
executes on a Vantage DEMO account through the MT5 gateway, and FALCON records the evidence, after which NEO can
review the run. The purpose is the minimum safe route to deterministic strategy research, causal backtesting and
Vantage DEMO execution (programme direction), proven once end to end before anything is generalised.
The foundation must be reusable: a second strategy must be able to follow the same path by changing the strategy
version only, not by re-integrating components.

## Current state

Read 2026-10-15 from `main` @ `1739e74` and the cited branches. Fabric is memory, not authority (ADR-DELIVERY-001);
fabric-only claims are labelled. Anything not read in a source is UNVERIFIED. The six audit items
(`GOLD-AUD-A` to `GOLD-AUD-F`) exist to replace the UNVERIFIED rows below with proven ones.

| area | what exists (source) | status |
|---|---|---|
| Control plane | GOAL `main` @ `1739e74`, `GOAL-DCP-001` CLOSED (merged PR #2, #4); validator, readiness, secret scan | proven |
| Pending programme changes | GOAL PR #5 (`wo/GOAL-RECON-PR`, OPEN): factual corrections, adds `GOAL-TRIGGER-001`, `TRON-D1-RATIFY`, `HSA-C1`, re-points edges; GOAL PR #6 (`wo/GOAL-BACKUP-PLAN`, OPEN): documentation only | proven (`gh pr list`) |
| HERMES | Market-truth contracts and replay in `maff0000/hermes` (HMT-1, RECON-H1 table); a PROD XAUUSD Redis publication is stated to exist | publication contents UNVERIFIED here: audited by `GOLD-AUD-A` |
| HERMES data provenance | live facts come from one venue feed, microstructure truth is CME gold futures, execution is a Vantage MT5 gold CFD; the alignment basis is named only in an unauthorised HMT-3H candidate (RECON-H1 section 2.6) | proven as a gap; see D-6 |
| HELIOS | `maff0000/HELIOS` `main` @ `7f7193d` (PR #1, independent PRODUCT_GREEN, 1005 tests per GROUP-E-REPORT), execution-blind enforced by a vocabulary test, HSA package loader, FALCON publication boundary, Docker runtime | proven for v1; live HERMES client is a file-feed fixture source only (RECON-H2 table); an earlier Redis-to-HELIOS proof branch stops at `WAITING_FOR_HERMES_BACKFILL` |
| Earlier HERMES-to-HELIOS GOLD integration | `GOLD-STRATEGY-RUNTIME` `main` @ `5891415` composes HSA + HELIOS + CER as one platform (RUNTIME_PRODUCT_GREEN, assurance-tooling residual); its architecture predates TRON and the trigger (RECON-H1 section 1) | located and negative: no completed HERMES Redis to new-HELIOS integration exists (HELIOS has no Redis client; the deployed GOLD stack is fixture-fed; the proof branch ended `WAITING_FOR_HERMES_BACKFILL`), so the HERMES to HELIOS reader is a build item in `HELIOS-T2` scope (GOLD-AUD-B Current state; PORTFOLIO section 3a); to be proven by `GOLD-AUD-B` |
| Strategy contract | `GOAL-CONTRACT-001` and `GOAL-TRIGGER-001` PID candidates on `wo/GOAL-CONTRACT-TRIGGER` @ `64c843b`, plus `ADR-CONTRACT-001`; the `GOAL-TRIGGER-001` backlog item is added by GOAL PR #5 (OPEN); none on `main`, none approved; three live strategy representations with no shared contract (HSA package, HELIOS package, DARWIN `StrategyVersion`) | candidates only |
| Trigger transport | the TradingTriggerInbox specification was searched for and NOT found (GOAL-TRIGGER-001 Current state 1); three incompatible inbound models exist (FALCON discovery, TRON D1 Redis board, backlog titles) | missing |
| TRON | `maff0000/tron` `main` @ `5577039` is `PID.md` + scripts only; the D1 design baseline is on an unmerged branch (20 commits) pending `TRON-D1-RATIFY` (Matt gate); no runtime code | design only |
| MT5 gateway | 8 stacked open PRs, linear, 27 commits, no CI, no typed service; a DEMO instance exists and is healthy; one earlier record shows a broker-reported DEMO trade mode; raw `SlaveService` is the only control surface (MT5-READINESS headlines 3 to 6) | partially proven; `MT5-GW-001` to `-004` are the engineering chain |
| FALCON | delivered registry and ingestion; `strategy_trigger` and `tron.*` families are excluded from `FALCON-T1` and have no frozen contract (RECON-F, RECONCILIATION-SUMMARY section 2 row 7) | partially proven |
| CER / HSA / DARWIN / NEO | CER v1.0.0 delivered; HSA PRODUCT_GREEN with 11 atomic entries and 2 example packages; DARWIN APOLLO causal core merged (PID-006B); NEO-R1 undefined beyond its title; no one maps a qualified strategy to a registered, executed, reviewed one | partially proven; `GOLD-AUD-F` |
| Sizing | no item owns a minimal fixed-size SizingPolicy; `TRON-T5` pulls in `CER-R1`; the split is a deferred candidate (RECON-H2 F-6) | missing |
| Overlap | `PAPER-E2E-001` already exists as the full paper-lane proof on Vantage DEMO (not satisfiable by simulation) with the same critical-path dependencies | overlap to rule on: D-1 |

## Target outcome

At closure all of the following are true, each with GitHub evidence:

1. One XAUUSD strategy exists as a governed, versioned `goal.strategy/v1` artifact with a stable fingerprint,
   registered with its evidence references, and the identical fingerprint is the one HELIOS loaded and the one every
   downstream record cites.
2. HERMES-published XAUUSD facts reach HELIOS through one governed consumer/provider contract, with no second
   market-data reader and no additional HERMES feed.
3. HELIOS emits a signed trigger into a durable outbox; TRON receives it through an idempotent inbox, verifies it
   itself, and records exactly one terminal outcome per trigger.
4. TRON, not HELIOS, applies sizing, hard risk and kill, and executes through the MT5 gateway on a Vantage DEMO
   account whose DEMO identity was verified by the broker before the first order.
5. One full order lifecycle on the DEMO account reconciles to zero difference between the TRON execution journal and
   the broker as system of record, and survives restart of TRON and reconnect of the gateway.
6. FALCON holds correlated evidence of the strategy state, trigger and execution outcome for the run, and FALCON
   unavailability demonstrably does not block an entry.
7. The run's evidence package is readable by NEO through a read-only interface for review.
8. A cross-component evidence index, dependency graph and consolidated contract compatibility matrix exist in GOAL.
9. The state `PAPER` is recorded for this item only after the Vantage DEMO proof is accepted; never on a simulation.

## Scope

In scope (integration and acceptance only):

1. **Integration architecture of record:** the sequence, interfaces and ownership of the critical path
   (HERMES PROD XAUUSD Redis, HELIOS, signed durable trigger outbox, TRON inbox and risk gates, MT5 gateway and
   Vantage DEMO, FALCON evidence, then NEO review) as one document, derived from the six audits.
2. **Cross-component evidence index:** one GOAL file listing, per audit and per component PID, the repository, PR,
   revision, verdict and unresolved findings.
3. **Consolidated contract compatibility matrix:** per interface (market-fact input, strategy contract, signed
   trigger, inbox, execution journal, FALCON event families), the provider version, consumer version, status
   (compatible, adapter needed, incompatible, unverified) and the owning PID that closes each gap.
4. **Acceptance runbook and harness definition:** the exact ordered procedure, fixtures, fault injections and
   evidence capture for the single acceptance event, written so an independent auditor can re-run it.
5. **The acceptance run itself** on the Vantage DEMO account, executed under TRON's authority and the MT5 gateway's
   DEMO guard, with the evidence package committed to GitHub.
6. **Gap register:** any capability the audits find missing, each assigned to an existing or proposed owning item;
   this PID does not implement any of them.

Contribution rule for items 2 and 3 (programme-controller ruling 4). Each lane PID contributes its index entry and its matrix rows by one GOAL PR per lane, only AFTER that lane's own evidence PR is accepted, so that writes never conflict. The `GOLD-MVP-001` PL is the single writer of the two files and merges those PRs one at a time. Lane evidence lives at `docs/evidence/GOLD-AUD-<L>/` in the primary repository (`audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-<L>/` in GOAL for lanes C, D and F); `GOLD-AUD-C`'s contract packages stay under `contracts/packages/` and its matrix rows are contributed into `COMPATIBILITY-MATRIX.md`.

Integration glue that belongs to no component (for example a cross-repository acceptance driver script that only
orchestrates public interfaces) lives in `maff0000/GOAL` under a path the approved PID names; it must contain no
strategy, risk, sizing or execution logic.

## Non-goals

1. No component implementation (HERMES, HELIOS, TRON, MT5 gateway, FALCON, CER, HSA, DARWIN, NEO changes belong to their own PIDs).
2. No additional HERMES feeds, no broad research-platform expansion, no new third-party service as a prerequisite.
3. No live capital execution, no LIVE state, no LIVE credentials anywhere in the acceptance stack.
4. No ARES event risk (enters later through TRON, `TRON-T3`), no DIKE research, no LEAN, no SKEPTIC.
5. No second strategy, no strategy portfolio, no parameter search; qualification of the one strategy only.
6. No NEO discretionary action; NEO review is read-only and after the fact.
7. No simulation milestone that carries state `PAPER`.
8. No change to legacy executors (ADR-MT5-002) and no use of them.
9. No dispatch automation (`GOAL-DCP-002/003`) and no auto-merge.

## Dependencies and interfaces

Hard engineering prerequisites of the acceptance run (canonical ids; the backlog edges proposed in PORTFOLIO section 11):

| prerequisite | why |
|---|---|
| `GOLD-AUD-A` to `GOLD-AUD-F` | read-only audits whose accepted verdicts convert UNVERIFIED rows to proven and feed the compatibility matrix |
| `GOAL-CONTRACT-001`, `GOAL-TRIGGER-001` | frozen strategy and trigger contracts (on GOAL PR #5 for the latter) |
| `HELIOS-T3` (and transitively `HELIOS-T2`, `HELIOS-T1`, `GOAL-CORE-001`, `HERMES-FACT-001`) | live HERMES adapter and signed durable trigger |
| `TRON-T2`, `TRON-T3`, `TRON-T4` (and transitively `TRON-T1`, `TRON-D1-RATIFY`, `MT5-GW-001` to `-004`) | Vantage DEMO adapter, hard risk and kill, trigger inbox |
| `FALCON-T1` plus a minimum FALCON event-publication increment for `strategy_trigger` and `tron.*` | evidence; the increment has no item yet (D-4) |
| a minimum fixed-size SizingPolicy owned by TRON | no item owns it yet (D-3) |

Interfaces (each owned by exactly one contract owner; this PID verifies them, it does not define them):
HERMES Redis to HELIOS input (provider HERMES-FACT-001, consumer HELIOS-T2); `goal.strategy/v1`
(`GOAL-CONTRACT-001`); signed trigger and inbox delivery semantics (`GOAL-TRIGGER-001`); TRON to gateway typed API
(`MT5-GW-003`); FALCON event families (`FALCON-T1` and its increment).

What may proceed in parallel: all six audits start the moment their PIDs are approved (read-only, depend only on
`GOAL-DCP-001`). PID authoring of the component items proceeds against declared draft interfaces (the schema has no
authoring-versus-dispatch edge; state `PID_DRAFT` expresses it). What this PID blocks: nothing; it is the last item
on the critical path.

## Safety boundaries

1. Vantage DEMO only. Before any order, the gateway must report the broker-confirmed DEMO account mode; any other
   result, or an unreadable result, aborts the run (stop condition S-1).
2. Neither HELIOS nor FALCON may hold an order, sizing, account or broker concept in this path; TRON alone sizes,
   risks and executes. FALCON is an asynchronous evidence consumer outside the executable trigger path.
3. The broker is the system of record; TRON keeps an execution journal and reconciles to the broker.
4. No secrets, internal addresses, account numbers, login identifiers or key material in GOAL (public). Evidence in
   private repositories is sanitised before any copy or citation in GOAL (PORTFOLIO section 7).
5. Production HERMES Redis is read-only for every audit and for the acceptance run's read side; no component other
   than the HERMES publisher writes it.
6. The legacy executors and any other MT5 instance are untouched; the acceptance run uses the one designated DEMO
   instance only.
7. Fault injection (restart, disconnect, FALCON outage) is performed on the DEMO acceptance stack only, never on
   production services, and never against a LIVE instance.
8. Position size on the DEMO account is the TRON-owned minimum policy; an order that exceeds the approved cap is a stop.
9. No deployment, merge, or state change occurs without the PO gate; the PAPER transition additionally needs the Matt gate.

## Deliverables

1. `audits/2026-10-15/gold-mvp/INTEGRATION-ARCHITECTURE.md`: the sequence, interfaces, owners and failure behaviour of the critical path.
2. `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md`: cross-component evidence index (owned by this PID; single writer: the `GOLD-MVP-001` PL).
3. `audits/2026-10-15/gold-mvp/COMPATIBILITY-MATRIX.md`: consolidated contract compatibility matrix with an owner and closing PID per gap (owned by this PID; single writer: the `GOLD-MVP-001` PL; no second matrix).
4. `audits/2026-10-15/gold-mvp/GAP-REGISTER.md`: capabilities missing for the MVP, each with owner and proposed item.
5. `audits/2026-10-15/gold-mvp/ACCEPTANCE-RUNBOOK.md` plus fixtures and the orchestration-only driver named in the approved PID.
6. `audits/2026-10-15/gold-mvp/ACCEPTANCE-EVIDENCE/`: the executed run's evidence package (sanitised), with a manifest of hashes.
7. A GOAL PR carrying 1 to 6 with the ten evidence items of PORTFOLIO section 7 and an independent auditor verdict.
8. A reusability note stating what a second strategy changes (strategy version only) and what it must not change.

## Acceptance

Each criterion has a proof method and is judged by an independent auditor re-running the stated check; none is
satisfiable by simulation unless it says so.

| # | criterion | proof method |
|---|---|---|
| AC-1 | All prerequisites in Dependencies are in an accepted terminal state and `GOLD-AUD-A` to `-F` verdicts are accepted by CA with no open BLOCKER finding | `./tools/goal-validate` OK; `./tools/goal-ready --assume-closed` projection; the evidence index lists each verdict |
| AC-2 | The compatibility matrix has zero rows with status incompatible or unverified on the critical path | auditor reads the matrix; script counts statuses |
| AC-3 | One `goal.strategy/v1` XAUUSD strategy version: fingerprint recorded once; the same fingerprint appears in the HELIOS loaded-strategy record, the trigger, the TRON journal row and the FALCON event | hash equality check across the four records in the evidence package |
| AC-4 | Recorded HERMES XAUUSD session replayed twice through the HELIOS input boundary yields byte-identical state and trigger sequences matching the committed golden file | run twice, diff, compare to golden fixture (simulation allowed; this is a determinism proof, not an execution proof) |
| AC-5 | Trigger durability: HELIOS restarted between signing and delivery loses no trigger and creates no duplicate | fault-injection log; dedupe key count equals trigger count |
| AC-6 | TRON rejects, with a recorded terminal outcome and no broker call, each of: bad signature, expired validity window, stale fact, duplicate dedupe key, unknown strategy version, replayed trigger | negative fixture run; journal rows; gateway call count zero for these |
| AC-7 | Execution-blindness: the HELIOS output and the trigger contain no sizing, order, account or broker vocabulary | the HELIOS forbidden-vocabulary test passes against the trigger schema and fixtures |
| AC-8 | TRON sizing, hard-risk and kill gates evaluated before the order; a kill-switch activation blocks a following entry | gate trace in the journal; blocked-entry record |
| AC-9 | Broker-confirmed DEMO identity recorded before the first order | gateway identity record precedes the first order timestamp; value masked in GOAL |
| AC-10 | One full lifecycle on the DEMO account: entry with broker-side protection, fill observed, close; resubmission of the same trigger creates no second position | broker position query before and after; journal; idempotency record |
| AC-11 | Reconciliation: TRON journal versus broker positions and deals shows zero difference after the lifecycle and after a TRON restart and a gateway reconnect mid-position | reconciliation report; restart and reconnect logs |
| AC-12 | FALCON holds events for strategy state, trigger and TRON outcome of the run, correlated by the trigger id; with FALCON ingestion stopped in the rehearsal, an entry still completes | FALCON query by trigger id; outage rehearsal log |
| AC-13 | Evidence package is readable through a read-only interface and the NEO review handoff manifest validates; no write path exists | manifest check; permission check; NEO review itself is a later separate item |
| AC-14 | `./tools/secret-scan` clean (tree and history) on every repository PR in the evidence set; no internal address, account or key in GOAL | scan output attached; grep log |
| AC-15 | GitHub evidence: PR with the ten items, required checks green, independent auditor review, CA acceptance; state `PAPER` is set only after AC-9 to AC-11 are accepted by the PO and the Matt gate | PR URL; recorded decisions |

## Stop conditions

- S-1: the broker-reported account mode is not DEMO, is unreadable, or the instance identity cannot be tied to the designated DEMO account: stop, no order.
- S-2: any component requires a LIVE credential, a LIVE instance or a legacy executor to complete the run: stop.
- S-3: a critical-path audit returns a BLOCKER (for example the PROD publication lacks a timeframe or indicator the strategy needs, or the contract cannot express the strategy): stop and return to CA; do not widen scope to fix it here.
- S-4: any evidence contains a secret, an internal address or an account identifier destined for GOAL: stop, sanitise, re-scan.
- S-5: the acceptance run would need a second HERMES feed, a new third-party service or a component code change from this PID: stop and raise a component item.
- S-6: a simulated result is offered as proof of AC-9 to AC-11: reject.
- S-7: reconciliation shows a non-zero difference or an unexplained position: stop trading on the DEMO account, report, do not retry blindly.
- S-8: a prerequisite PID changes a frozen contract after the matrix is accepted: stop, re-baseline the matrix.

## Open decisions

D-1 (blocks PID approval). **Relationship to `PAPER-E2E-001`.** Both are end-to-end DEMO proofs with the same
dependencies. Options: (a) supersede `PAPER-E2E-001` by this PID and re-point `LIVE-GATE-001` (clean, but edits a
Matt-gated item and breaks an edge); (b) keep both, with `PAPER-E2E-001` re-scoped as the later general paper-lane
proof depending on `GOLD-MVP-001` (no deletion; two items may reach `PAPER`); (c) keep both independent (duplicate
scope; rejected). Recommendation: (b). Owner PO. The edge change is part 2 of the backlog patch.

D-2 (blocks PID approval). **Header gates.** Risk `capital` plus Matt gate true (matches `PAPER-E2E-001` and the PAPER
rule), or risk `high` with Matt gate only at the PAPER transition. Recommendation: `capital` and Matt gate true,
because the run places real orders on a broker account (DEMO) and ends in a protected state. Owner PO, informs Matt.

D-3 (blocks acceptance, not approval). **Who owns minimum sizing.** TRON cannot order without a quantity. Options:
fold a fixed-size policy into `TRON-T3`/`TRON-T2`; add the deferred candidate `TRON-T5A`; wait for `TRON-T5` (pulls in
`CER-R1`). Recommendation: a small TRON-owned fixed-size increment (`TRON-T5A`), added after `GOLD-AUD-D` confirms the
shape. Owner PO.

D-4 (blocks acceptance, not approval). **FALCON minimum event publication.** `FALCON-T1` excludes `strategy_trigger`
and `tron.*`; no item publishes them. Options: a bounded increment of `FALCON-T3/T4`; publication by HELIOS and TRON
as emitters with FALCON schema only. Recommendation: decide after `GOLD-AUD-E`. Owner PO.

D-5 (blocks acceptance). **Which strategy.** The first strategy is chosen from existing HSA packages by `GOLD-AUD-B`
review (compatibility with the live fact set), then qualified by `GOLD-AUD-F` method. Recommendation: the simplest
single-timeframe package whose required facts the PROD publication already carries; qualification threshold set by
PO before the run, not after. Owner PO.

D-6 (blocks acceptance). **Price basis.** Live HERMES facts, the futures microstructure truth and the Vantage CFD
differ; the alignment basis is unauthorised. Options: accept the basis difference for plumbing proof only (the DEMO run
proves integration, not edge); or require the HMT-3H alignment first. Recommendation: accept for the MVP and label the
run as a plumbing proof; no performance claim. Owner PO.

D-7 (blocks acceptance). **Composition vehicle.** Whether `GOLD-STRATEGY-RUNTIME` is the deployment vehicle of the
acceptance stack or the stack is composed per component. The reconciliation (`PLATFORM-RT-001`) is a deferred
candidate. Recommendation: decide after `GOLD-AUD-B`; do not rebuild a delivered runtime. Owner PO.

## Evidence

Sources read 2026-10-15 (read-only): GOAL `README.md`, `architecture/DELIVERY-CONTROL-PLANE.md`,
`governance/DELIVERY-STATE-MACHINE.md`, `decisions/ADR-*`, `backlog/backlog.yaml`, `backlog/SCHEMA.md`,
`pids/GOAL-DCP-001.md` at `1739e74`; `wo/GOAL-RECON-PR` @ `e2671ff` (`RECONCILIATION-SUMMARY.md`);
`wo/GOAL-CONTRACT-TRIGGER` @ `64c843b`; `wo/GOAL-TRON-D1-RATIFY` @ `d5f6d32`; `wo/GOAL-MT5-READINESS` @ `fe43db3`;
`wo/GOAL-MT5-DEMO-VERIFY` @ `da2e4ea`; `wo/GOAL-PID-WAVE1-E-helios` (`GROUP-E-REPORT.md`);
`wo/GOAL-RECON-H1-datachain` and `-H2-tradechain` reports; `gh pr list` for GOAL; local `git log` of the HELIOS and
GOLD-STRATEGY-RUNTIME clones; `audits/2026-10-15/gold-mvp/PORTFOLIO.md` (this work order); the six lane PID candidates `pids/GOLD-AUD-A.md` to `-F.md` (their findings are summarised in PORTFOLIO section 3a). Not read: any production
service, Redis, broker or container; component repositories beyond the logs cited.

## Approval

PENDING. No approval has been recorded for this PID candidate. Approval is recorded here by Central Architecture/PO only.

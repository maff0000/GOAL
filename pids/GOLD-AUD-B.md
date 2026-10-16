# GOLD-AUD-B — Locate and reconcile the HERMES to HELIOS GOLD integration (audit)

**Lane:** research  
**Target repository:** `maff0000/HELIOS`  
**Evidence:** primary PR in `maff0000/HELIOS`, branch `wo/GOLD-AUD-B-evidence`, path `docs/evidence/GOLD-AUD-B/`  
**Priority:** P0  
**Risk:** low  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  
**Complements:** `HELIOS-T2`, `HELIOS-T1`, `HERMES-FACT-001`, `GOLD-STRATEGY-RUNTIME`  

**Header notes:** GOAL holds an index entry only; the primary evidence PR is in `maff0000/HELIOS`. Delivery is a read-only audit increment. `HELIOS-T2` is complemented as a separate audit item that is an input to it (`HELIOS-T2` owns the adapter implementation; this audit is not an increment or amendment of it). Evidence location follows programme-controller rulings 1 to 3 (`PORTFOLIO.md` appendix).

Header values match the registered backlog item (`backlog/backlog.yaml`, `pid_path: pids/GOLD-AUD-B.md`). Lane vocabulary is the backlog set {shared, research, trading, ops}; `research` is used for all
six audits (CA frame). Priority, lane and risk follow the CA/PO adjudication 2026-10-15 (recorded in `PORTFOLIO.md`, not in this PID); approval is recorded in the Approval section below.


## Status

APPROVED (Central Architecture, 16 October 2026; see Approval). Registered in the backlog as DELIVERY_READY by the governed amendment.

This is a bounded, read-only audit increment of GOLD MVP Lane B. It is drafted
as the Lane B member of the master `GOLD-MVP-001` frame (audit id `GOLD-AUD-B`,
`depends_on` `GOAL-DCP-001` only). It adds no backlog entry and no `pid_path`;
those are recorded by Central Architecture or the PO only.

## Purpose

Central Architecture directed Lane B to locate the previously completed HERMES
Redis to HELIOS GOLD integration, including any external adapter, deployment
wiring or legacy implementation; reconcile its actual source with the new
HELIOS runtime and the documented `MarketFactFrame` contract; determine the
minimum reuse or adaptation; and review HSA's existing strategy packages for a
compatible first GOLD strategy (as originally directed; restated below by
CA guidance 2026-10-15, item 6: candidate requirements are compared with PROD
facts and no strategy is selected here). No second market-data reader may be introduced
until the existing integration has been located and assessed.

This PID turns that directive into a mechanically checkable, read-only
increment whose output is a reuse inventory, a gap list and a minimum
adaptation plan. It decides nothing about building the reader.

**CA guidance 2026-10-15 (items 1 and 6) applied.** (1) HERMES owns Redis
publication. A HELIOS-side EXTERNAL ADAPTER, outside the pure HELIOS engine
(which stays execution-blind and deterministic, with no Redis or network
imports), owns consumption and translation; GOAL approves the interface
(CP-1, `GOLD-AUD-C`). This audit inventories what exists for that adapter to
reuse and what it must translate; it neither builds nor specifies the adapter
itself (the adapter PID is a later item, decisions DR-34 and DR-35 in
`DECISION-REGISTER.md`). (6) This audit selects no strategy. Its candidate
output is a requirements-versus-facts comparison: the data each HSA candidate
needs, set against what the PROD publication actually carries (audit A). The
sequence is audits A and B, then reconciliation, then strategy selection by
the PO, then `GOLD-MVP-001` acceptance planning.

## Current state

Read on 2026-10-15, read-only. Marks:
**PROVEN** (read directly, command or file named), **PARTIAL** (read in part),
**UNVERIFIED** (inferred or not opened). Internal addresses, accounts and
credentials are deliberately omitted because `maff0000/GOAL` is public.

**Headline finding (PARTIAL; bounded conclusion, corrected by CA/PO adjudication 2026-10-15).**
*Searched:* the HELIOS, GOLD-STRATEGY-RUNTIME, falcon and TRADER trees; worktrees and branches;
`gh repo list` for the owner; systemd units and timers; container names and labels (never
environment); fabric key names (labelled fabric-only); HERMES consumer docs; legacy archive
manifests (the methods of Scope 1, with the candidates of the inventory below).
*Found:* every candidate located is one of: a legacy path that read MariaDB rather than HERMES Redis
candles; a deployment that feeds HELIOS from a fact directory; an unmerged work-order branch that
stopped before writing code; or an untracked read-only probe.
*Conclusion:* **no completed HERMES Redis to new-HELIOS integration was found in the searched
locations; absence elsewhere is UNVERIFIED.** The belief that an integration was "previously
completed" is not supported by any artefact read in those locations. "Not found" is itself a claim
(see Stop conditions): the search inventory below is what the audit must re-run and extend before
the claim is accepted, and that re-run and extension remain an acceptance item.

### Candidate inventory

| # | Candidate | Where | Nature | Finding | Mark |
|---|---|---|---|---|---|
| 1 | New HELIOS v1 | `maff0000/HELIOS` (public), `main` = `7f7193d` (PR #1, independent PRODUCT_GREEN at `0bb9297`) | product, execution-blind | `helios/hermes/` holds one adapter, a fixture source; `helios/integration/hermes_boundary.py` is a data contract, "not a client"; no Redis or DB client, no network sink. Facts arrive as validated `MarketFactFrame` values. Advertised schema version is `helios.market_fact/1.0.0`; fixtures, config and tests also accept `hermes.market_fact/1.0.0`. | PROVEN |
| 2 | GOLD Strategy Runtime | `maff0000/GOLD-STRATEGY-RUNTIME` (private), `main` `5891415` (PR #1) | deployment wiring | Runs HSA, HELIOS and CER as containers on pinned digests. Its own records state that HELIOS has no live HERMES transport and reject a runtime-owned bridge; the delta is bounded as a HERMES transport source behind HELIOS's existing fact-source interface; a Redis sink is deferred, and v1 is kept free of shared Redis. | PROVEN |
| 3 | Deployed GOLD stack | the deployed instances built from the runtime repo images (deployment records held in the maintainers' private operations record) | deployed unit | The audit establishes what is deployed and how it relates to `main`. Evidence indicates the deployed HELIOS is fed from fixture-style inputs; content not opened. | PARTIAL |
| 4 | HELIOS to HERMES PROD proof | HELIOS branch `wo/WO-HELIOS-HERMES-PROD-INTEGRATION-PROOF-0001` (one commit `84d3772`, unmerged) | work-order evidence, no code | The work-order records a terminal verdict that the proof could not complete at the time (HERMES data not yet complete), and that HELIOS has no Redis client and validates a different fact schema family from the one live HERMES publishes. No harness was built. | PROVEN |
| 5 | Read-only compatibility probe | an untracked probe script and its captured-sample file, dated 2026-10-07 (locations recorded in the maintainers' private operations record) | evidence probe | Header says it is "not a proposal of adapter code": feeds real captured HERMES objects (candle, indicators, session) through HELIOS's `MarketFactFrame` validator in a no-network container to show which raw fields pass. Output was not re-run or located. Likely Lane A or earlier-lane input. | PARTIAL |
| 6 | Legacy HELIOS V2 / V3 | a legacy private repository tree (identified in the audit) | legacy, retired | Marked retired in its own records. The V3 daemon reads a database and publishes to the fabric HTTP gateway; no read of HERMES candle keys was found by grep. Not the new HELIOS lineage. Archived in a dated legacy archive. | PARTIAL |
| 7 | `helios_bridge` | a legacy bridge component (identified in the audit) | external adapter, legacy | Reads M1 candles, signals and levels from the HERMES SQL store and writes legacy records to the memory fabric. A database reader, not a Redis reader, and not feeding new HELIOS. | PROVEN |
| 8 | XAU watcher / gate compositor | the legacy XAU watcher and gate compositor components | legacy | No Redis or HERMES key reference found in watcher source by grep. Compositor not opened. Also unopened: other legacy private repositories (identified in the audit). | PARTIAL / UNVERIFIED |
| 9 | Legacy memory-fabric records | the memory-fabric records identified in the audit (names only, labelled fabric-only) | legacy state | Outputs of the legacy scanner and bridge; none are HERMES inputs. | PROVEN (existence), UNVERIFIED (values) |
| 10 | HERMES contract surface | a HERMES publisher manifest sample under a dated evidence directory (2026-10-07) | upstream authority | `schema_version` `v1`; canonical instrument `XAU_USD`; six timeframes ACTIVE for `candle_latest`; `candle_history_d1` BLOCKED until D1 latest is green; HERMES declares no regime ownership. | PROVEN (sample), live state UNVERIFIED |

### Contract reconciliation read so far

- **Frame shape (PROVEN).** `MarketFactFrame` binds instrument, timeframe,
  bar-open `timestamp_utc`, candle (`open high low close volume complete
  source`), indicators (`rsi_14 ema_9 ema_21 ema_50 ema_200 atr_14 regime
  session`, all optional, absent never zero) and provenance (`source`,
  `schema_version`, `observed_at_utc`, `ingested_at_utc`). Closed world: unknown
  field refused; binary floats refused; windows must be strictly ascending.
  Source: HELIOS `docs/CONTRACTS.md` and `helios/contracts/market_fact.py`.
- **Version gap (PROVEN).** HELIOS advertises `helios.market_fact/1.0.0` and its fixtures, config and tests also accept
  `hermes.market_fact/1.0.0` (accepted set `HELIOS_ACCEPTED_HERMES_SCHEMA_VERSIONS`); live HERMES publishes `v1` with a
  `hermes.candles.latest` envelope. Row 4 records the same gap.
- **Provenance gap (PROVEN, from the GOLD runtime delta records).** A fact `source` is a
  lowercase token, so DEV and PROD HERMES cannot be told apart in the frame.
  The runtime requires an explicit expected-environment setting with no silent fallback.
- **Completeness gap (UNVERIFIED).** Whether the H4 and D1 history
  the candidates need is complete is established by lane A. `gold_context_breakout`
  needs H4 for its `CONTEXT` role (a requirement of that candidate, not a selection).
- **Indicator gap (UNVERIFIED).** HELIOS carries EMA 9/21/50/200 and ATR 14;
  whether HERMES publishes the same names, and any SMA, was not read.

### HSA candidate read so far (candidates under review; none selected or implied)

`maff0000/HSA` (public) `main` `279ec18` holds two governed packages, both
`CANDIDATE`, both `XAUUSD`, neither with passing CER evidence. They are listed
as candidates under review only (CA guidance 2026-10-15, item 6); no
preference is expressed:

| Package | Shape | Roles / timeframes | Observations |
|---|---|---|---|
| `gold_context_breakout` 1.0.0 | `CONTEXT_TRIGGER`: `golden_cross` (context) then `range_breakout` (trigger) | CONTEXT 4H, TRIGGER 5M | Needs H4 and M5 only. Requires `ma.fast` / `ma.slow` as simple averages of close, plus `range.high` and `range.low` over a lookback; HELIOS facts carry EMAs, not SMAs. HELIOS has a same-named fixture chain (`gold_context_trigger`, H4/M5). |
| `wick_rejection_sequence` 0.1.0 | `SEQUENCE`: `rejection_wick`, `no_wick_candle`, optional `range_breakout` | LOCATION and CONFIRMATION 15M, TRIGGER 5M | Needs M15 and M5 only. Needs only raw candle fields (no indicator facts); evidence is "still owed before promotion". |

Mismatches seen by inspection (PROVEN): HSA uses `XAUUSD`, `4H`, `5M`, `15M` and
HERMES/HELIOS use `XAU_USD`, `H4`, `M5`, `M15` (the HELIOS enum parses both
timeframe spellings; the instrument spelling mapping was not found). HSA
packages name required fields in a `required_hermes_fields` list with
`ma.fast` style names that are not HELIOS fact-field names. Whether HELIOS
loads the HSA package files as-is, or only its own `helios.strategy_package/1.0.0`
fixtures, is UNVERIFIED. A `GOLD-STRATEGY-RUNTIME` strategies directory
contains HELIOS-format chain files for GOLD (names read, content not).

### Existing coverage

- Backlog: `HELIOS-T1` (`depends_on` `GOAL-CORE-001`), `HELIOS-T2` ("Live
  HERMES/ARES adapters"; `depends_on` T1, `HERMES-FACT-001`, `ARES-RISK-001`),
  `HELIOS-T3`, `HERMES-FACT-001` (no PID); all `pid_path: null`.
- The HELIOS-T1 candidate PID records the same absence of a Redis client.
  GOAL-RECON-H2 finds T2 "contradicts the HELIOS PID" on ARES risk. GOAL-RECON-H1
  F-2 warns `goal.market-fact/v1` overlaps `MarketFactFrame` and HERMES HMT-3A
  (risk of a sixth HERMES data contract). `GOAL-CONTRACT-001` (draft) owns only
  the fact reference grammar, not fact names.

## Target outcome

At closure, the evidence PR and the GOAL index let Central Architecture decide
Lane B without further discovery:

1. A signed-off inventory of every HERMES to HELIOS reader candidate, each
   marked PROVEN, PARTIAL or UNVERIFIED, with a recorded negative-search
   method (locations and commands) for the bounded "no completed integration
   was found in the searched locations" conclusion; absence elsewhere stays
   UNVERIFIED.
2. For each reader candidate: reuse, adapt or rewrite, with justification
   against `MarketFactFrame`.
3. A field-by-field mapping from live HERMES surfaces to `MarketFactFrame`
   with every gap named.
4. A minimum adaptation plan mapped to `HELIOS-T2` (and to `HERMES-FACT-001`
   where the gap belongs to HERMES).
5. A candidate-requirements matrix: for every HSA package (and the HELIOS and
   GOLD runtime packages for GOLD), the facts, timeframes and indicator names it
   needs against the PROD facts recorded by audit A, naming what would have to
   change for each. It ranks nothing and recommends no strategy; it is an input
   to the later PO selection (CA guidance 2026-10-15, item 6).
6. An explicit input for the adapter PID: which existing artefact, if any, the
   HELIOS-side external adapter extends, and what it must translate (CA
   guidance 2026-10-15, item 1).
7. A disposition table (Deliverables, below) covering each HELIOS generation.

## Scope

In scope, all read-only:

1. **Locate.** Re-run and extend the Current state search: HELIOS, GOLD
   runtime, falcon and TRADER trees; worktrees and branches; `gh repo list`
   for the owner; systemd units and timers; container names and labels
   (never environment); fabric key names (labelled fabric-only); HERMES
   consumer docs; legacy archive manifests. Record the exact commands.
2. **Inventory.** One row per candidate: path, repository, commit, nature
   (external adapter, legacy, deployed unit, probe, document), status,
   mark. Open and read the items marked UNVERIFIED above (candidate rows 3,
   5, 8), bounded to names, structure and commit history.
3. **Reconcile with `MarketFactFrame`.** Map each live HERMES candle,
   indicator, session and manifest surface to the frame; run HELIOS's own
   tests unchanged; reproduce the probe's accept and refuse results in a
   throwaway no-network container fed with captured, sanitised samples.
4. **Classify** each component of each candidate as reuse, adapt or rewrite,
   and give the minimum change.
5. **Map to `HELIOS-T2`.** Show which T2 requirements the findings satisfy,
   which they contradict (ARES scope, transport seam, Redis sink), and what
   is missing.
6. **HSA candidate-requirements review.** For every package in HSA `strategies/`
   (and the HELIOS and GOLD runtime packages for GOLD), tabulate: data needs
   against what the PROD publication carries (audit A output), timeframe
   completeness, indicator names, determinism, execution-blindness, evidence
   state, fit with the HELIOS package schema and with the `goal.strategy/v1`
   draft. Name what would have to change for each. Do not rank, do not
   recommend, do not select (CA guidance 2026-10-15, item 6): selection is a
   PO decision taken after audits A and B have reported and been reconciled.

## Non-goals

- No code, adapter, reader, sink, schema or fixture is written or changed in
  any product repository; documents only. No second reader is built,
  scripted or prototyped.
- No change to HERMES, ARES, FALCON, TRON, HSA, CER, the GOLD runtime, or any
  running unit, container, timer or fabric key.
- No strategy selection, ranking-to-selection or recommendation (CA guidance 2026-10-15, item 6).
- No change to the pure HELIOS engine and no Redis or network import into it; the
  external adapter is a later item (CA guidance 2026-10-15, item 1).
- No strategy promotion or evidence claim; no decision on `goal.market-fact/v1`,
  `goal.strategy/v1` or HELIOS-T3 trigger semantics.
- No backlog edit, `pid_path`, `DELIVERY_READY` state or approval record.

## Dependencies and interfaces

- **Hard dependency (backlog):** `GOAL-DCP-001` (CLOSED) only.
- **HERMES Lane A output:** the live HERMES surface inventory and completeness
  findings. This audit consumes it as input; if it is not available at
  delivery start, the HERMES side is read directly and marked UNVERIFIED
  where it cannot be proven (see Stop conditions).
- **GOAL-CONTRACT-001 fact grammar:** only the fact-reference shape is
  relevant; this audit may not freeze or invent fact names (owner
  `HERMES-FACT-001`). It records any mismatch as a gap.
- **HSA package schema:** `contracts/strategy_package.schema.json` in HSA and
  `docs/schema/strategy_package.schema.json` in HELIOS; the audit reports
  conformance between them and against the `goal.strategy/v1` draft, and
  proposes no schema change.
- **Downstream:** `HELIOS-T1` (strategy contract refactor), `HELIOS-T2` (live
  adapters), `HERMES-FACT-001`, and the master `GOLD-MVP-001` frame.

**Collision notes:** the audit writes only to a new branch `wo/GOLD-AUD-B-evidence` of `maff0000/HELIOS`
(`docs/evidence/GOLD-AUD-B/`). After that PR is accepted, one separate GOAL PR contributes B's entry to
`audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md` (owned by `GOLD-MVP-001`; one lane per PR; B's matrix rows go to
`COMPATIBILITY-MATRIX.md` the same way). The branch `wo/GOAL-GOLD-AUD-B` is the PID draft, not evidence. It does not touch product source,
`pids/HELIOS-T1.md` or `backlog/`.

## Safety boundaries

- Read-only on every system except the author's own worktree. No production
  mutation, no running-service change, no restart, no unmask, no enable.
- HELIOS stays execution-blind. No audit text or fixture may introduce broker,
  account, sizing, order or TRON vocabulary into HELIOS; the existing
  forbidden-vocabulary test must still pass unchanged.
- **No second reader.** The audit must not stand up, run or script a new
  HERMES reader (or the HELIOS-side external adapter) against live Redis. Captured samples are read through the
  existing Redis gateway read endpoints or existing evidence directories only.
- `maff0000/GOAL` and `maff0000/HELIOS` are public: no internal IPs, hostnames,
  accounts, credentials, tokens, environment
  dumps or private-repo contents. Evidence that cannot be sanitised goes to
  the private evidence location and is cited by identifier only.
- Never print secrets. `docker inspect` is restricted to names, images,
  labels and mount destinations; never `env`.
- Allowed commands: `git` read verbs, `ls`, `find`, `grep`, file reads,
  `gh repo list` and `gh api` GET, `systemctl list-units|list-unit-files|status`,
  `docker ps|images|inspect` (restricted above), `pytest -p no:cacheprovider`
  in a clean checkout, fabric key-name listing and single-key GET (fabric-only).
  Forbidden: any write, `set`, `delete`, mutating `docker exec`,
  `systemctl start|stop|enable|mask|unmask`, `git push`, `goal-docs --write`.

## Deliverables

1. **Primary evidence PR** into `maff0000/HELIOS` (branch `wo/GOLD-AUD-B-evidence`) containing
   `docs/evidence/GOLD-AUD-B/` (sanitised audit record and supporting tables), followed after acceptance by one GOAL index-entry PR
   (ruling 4). The checklist is CA's ten mandatory evidence items in CA's numbering:

   CA's ten mandatory evidence items, in CA's numbering (the numbering is CA's and is not to be changed by a lane): (1) PID/WO identifier and exact audited scope; (2) source repositories, revisions and relevant documentation references; (3) existing implementation: proven, partially proven, unverified or missing; (4) actual versus expected contract comparison; (5) tests, fixtures and evidence references; (6) specific defects and compatibility gaps; (7) reusable code and documentation; (8) minimum recommended implementation changes; (9) safety and deployment constraints; (10) independent audit verdict and any unresolved findings.

   | CA # | CA evidence item | This audit puts it in | Proof method |
   |---|---|---|---|
   | 1 | PID/WO identifier and exact audited scope | `docs/evidence/GOLD-AUD-B/` record header: quoted scope sentence; audit id | Quote equals approved PID |
   | 2 | Source repositories, revisions and documentation references | Search method and exact commands including the negative-search record; revisions (full SHA) of HELIOS, GOLD-STRATEGY-RUNTIME, HSA, legacy lineage; documentation references | Commands re-run to the recorded SHAs |
   | 3 | Existing implementation: proven, partially proven, unverified or missing | Candidate inventory (path, repo, commit, nature, status, mark) and source-level reading of each candidate touching HERMES data; reuse / adapt / rewrite classification per component; marks PROVEN / PARTIAL / UNVERIFIED map to proven / partially proven / unverified, absent artefacts to missing | Every row has a mark; every PROVEN row names a path or command and a commit or date |
   | 4 | Actual versus expected contract comparison | HERMES-to-`MarketFactFrame` field mapping, schema version and provenance reconciliation, HSA package field needs versus the mapping | Field-level, no narrative cells; every gap named |
   | 5 | Tests, fixtures and evidence references | Unchanged-HELIOS test result (baseline 1005 at `7f7193d`); throwaway no-network container reproduction of the probe's accept and refuse results using captured sanitised samples | Same pass count; no test or source file modified |
   | 6 | Specific defects and compatibility gaps | Gap list, each gap with an owner repository and a closing proof | Every gap has owner and closing proof |
   | 7 | Reusable code and documentation | Reuse inventory and HSA candidate-requirements matrix (no ranking, no selection) with what would have to change in each | Each GOLD-capable package has a requirements row |
   | 8 | Minimum recommended implementation changes | Minimum adaptation plan mapped to `HELIOS-T2` and `HERMES-FACT-001`: ordered, with target repository, owner persona, dependency and closing proof | Each step maps to an existing item |
   | 9 | Safety and deployment constraints | Sanitisation attestation; recorded command log (no write, no `docker exec`, no unit-state change); no second reader | Sanitisation grep empty; auditor repeats it |
   | 10 | Independent audit verdict and unresolved findings | Independent auditor (AUD-2) verdict file with unresolved findings | Fresh auditor GREEN / AMBER / RED with exact SHAs |

2. **Reuse inventory** (table, item 2 and 6) and **disposition table** (`DISPOSITION.md`, REQUIRED;
   CA/PO legacy application doctrine 2026-10-15, format `PORTFOLIO.md` section 7.4). The table keeps the
   HELIOS generations apart: (a) legacy HELIOS V2 and V3; (b) the legacy `helios_bridge`
   and the XAU watcher / gate compositor (legacy); (c) the newer deterministic engine
   `maff0000/HELIOS`, evaluated INDEPENDENTLY of every legacy generation on its own merits;
   (d) `GOLD-STRATEGY-RUNTIME` and the currently deployed GOLD stack; (e) the untracked probe and the
   proof branch. Each row: generation, criteria (architecture fit, code quality, determinism,
   test evidence, maintainability, contracts, operational dependencies, integration cost), a verdict
   REUSE | REFACTOR | REPLACE | RETIRE, evidence, and the approximate comparative engineering
   cost of reuse versus refactor versus a clean build. Valuable algorithms, tested logic, contracts
   and research findings are listed as retained value whatever the verdict. A clean implementation is
   acceptable and preferable where it materially simplifies THE GOAL. A verdict is a recommendation
   only: nothing is retired, stopped or mutated.
3. **Gap list** (item 7).
4. **Minimum adaptation plan** (item 8): ordered, each step with target
   repository, owner persona, dependency and the proof that would close it.

## Acceptance

Mechanical:

1. `./tools/secret-scan` exits 0 on the HELIOS evidence branch; on the later GOAL index-entry PR, `./tools/goal-validate`
   and `./tools/secret-scan` exit 0.
2. `git diff --name-only origin/main` on the HELIOS branch lists only
   `docs/evidence/GOLD-AUD-B/` paths; on the GOAL index-entry PR, only `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md` and
   `COMPATIBILITY-MATRIX.md`.
3. HELIOS `pytest -p no:cacheprovider -q` reports the same pass count as the
   baseline (1005 at `7f7193d`) with no test or source file modified.
4. Every row of the candidate inventory has a mark in {PROVEN, PARTIAL,
   UNVERIFIED}; every PROVEN row names a path or command and a commit or date.
5. A grep of the new documents for `[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+` (except
   version strings with a `v` or `/` prefix), for the words `password`,
   `secret`, `token` followed by a value, and for private hostnames returns no
   hit.
6. Each GOLD-capable package found (HSA, HELIOS fixture and runtime strategies) has a requirements row with
   its required timeframes and fields checked against the field mapping and the audit A facts; no row is ranked or marked as the selected strategy.
7. Every gap in the gap list has an owner repository and a closing proof.
8. No `docker exec`, write, unit-state or fabric write appears in the recorded
   command log.
9. The checklist in Deliverables is complete or each missing item states why.
10. `DISPOSITION.md` exists with a row for every component in the inventory, each with generation, criteria, a REUSE / REFACTOR / REPLACE / RETIRE verdict, evidence and a comparative cost; the newer deterministic engine has its own rows distinct from legacy generations; no component was retired, stopped or mutated. The lane cannot be accepted without it.

## Stop conditions

Return to the PO or Central Architecture if:
- a candidate reader is found to be running against live HERMES Redis (stop,
  report, do not touch it);
- the audit would need a write to any running system, a secret, or a new
  reader to make progress;
- HERMES Lane A output contradicts the negative-search result and the
  difference cannot be resolved read-only;
- evidence in a private repo is essential and cannot be sanitised;
- the bounded "no completed integration found in the searched locations" conclusion
  cannot be supported by the recorded search method (a negative is a claim, not a finding).

Do not invent around a stop condition.

## Open decisions

1. **RESOLVED by CA/PO adjudication 2026-10-15: a separate audit work item, not an
   amendment (and not a fold-in to `HELIOS-T2`); `HELIOS-T2` owns the adapter implementation.**
   Reasoning recorded earlier: a new bounded
   item. HELIOS-T1 is a refactor to a contract that is not yet frozen
   (`depends_on` `GOAL-CORE-001`); this audit concerns the live transport,
   which belongs to `HELIOS-T2` or to the adapter PID that CA guidance
   2026-10-15 (item 1) calls for (DR-34, DR-35). Amending T1 would couple a read-only audit
   to an unfrozen contract and would blur T1's single purpose. The audit is
   therefore framed as a separate audit item that is a hard input to the `HELIOS-T2` PID, not an
   amendment of T1 or of T2. Resolved; no longer blocks approval.
2. **Is `HELIOS-T2` in scope for ARES?** GOAL-RECON-H2 finds the T2 title
   contradicts HELIOS PID on ARES risk. This audit maps to the HERMES half
   only. Owner PO. Does not block this PID; blocks T2 PID.
3. **Where may sanitised samples live?** Evidence PR in the public repo
   versus a private evidence location cited by identifier. Recommendation:
   sanitised excerpts public, full captures private. Owner PO. Blocks approval.
4. **Spelling canon at the HERMES boundary** (`XAU_USD`/`H4` versus
   `XAUUSD`/`4H`): the audit reports the mapping; the ruling belongs to
   `HERMES-FACT-001` / `GOAL-CONTRACT-001`. Owner PO. Does not block approval.
5. **First GOLD strategy selection** is not made here and follows the
   reconciliation of audits A and B (CA guidance 2026-10-15, item 6). The audit
   supplies the requirements-versus-facts matrix as an input to that PO decision
   (DR-23). Owner PO. Does not block approval. Probe provenance (who authored the untracked
   probe, may its output be cited) is confirmed in the same step. Owner PO or
   ROGUE. Does not block approval.

## Evidence

Read on 2026-10-15, read-only: GOAL `main` at
`1739e742154c77e9e2a96927dc40d4978b9cd798` (historical read base; baseline now `90323b3`; verified; backlog entries, DCP-001
PID); the Wave 1 Group E HELIOS-T1 candidate PID (the `GROUP-E-REPORT.md` named
in the task was not found and not read); GOAL-RECON-H1/H2 notes; the
`GOAL-CONTRACT-001` draft; HELIOS `main` `7f7193d` (contract docs, boundary
module, fixture names, proof-branch evidence file); GOLD-STRATEGY-RUNTIME
`main` `5891415` (README, delta records, compose grep, PID relationship
section); HSA `main` `279ec18` (strategies, catalogue listing); the legacy
bridge source header; runtime state records of the deployed and legacy units (held in
the maintainers' private operations record); the legacy archive listing; and fabric key names.

Not read: FALCON PID-07/08 bodies, other legacy private repositories (identified in the audit), the gate compositor, the deployed fact files'
content, live HERMES state (2026-10-07 sample only), HERMES Lane A output.

## Approval

APPROVED. Recorded 2026-10-16 by ROGUE on the written authority of Central Architecture/PO.

1. Central Architecture adjudication of the GOLD MVP Portfolio, 15 October 2026 (APPROVED WITH CORRECTIONS AND GOVERNED MERGE CONDITIONS; approves the architecture and scope of this audit PID).
2. Central Architecture formal approval, 16 October 2026, Decision: OPTION 1. The previous adjudication is confirmed as the formal approval of record for the seven GOLD PIDs, including this one. No further approval of this PID scope is required unless a substantive change is proposed.

Scope of this approval: the read-only audit scope in this PID. It authorises no deployment, production mutation, broker order, contract freeze or live-capital action.

# GOLD-AUD-B — Locate and reconcile the HERMES to HELIOS GOLD integration (audit)

**Lane:** research  
**Target repository:** `maff0000/HELIOS` (evidence PR) with a `maff0000/GOAL` cross-component index  
**Priority:** P0  
**Risk:** low  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE (read-only audit increment)

## Status

DRAFT CANDIDATE for Central Architecture review. Not approved. Not DELIVERY_READY.

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
compatible first GOLD strategy. No second market-data reader may be introduced
until the existing integration has been located and assessed.

This PID turns that directive into a mechanically checkable, read-only
increment whose output is a reuse inventory, a gap list and a minimum
adaptation plan. It decides nothing about building the reader.

## Current state

Read on 2026-10-15 on two estate hosts (the trading host and the delivery host), read-only. Marks:
**PROVEN** (read directly, command or file named), **PARTIAL** (read in part),
**UNVERIFIED** (inferred or not opened). Internal addresses, accounts and
credentials are deliberately omitted because `maff0000/GOAL` is public.

**Headline finding (PARTIAL, strongly indicated).** No completed HERMES Redis
to new-HELIOS integration was found. Every candidate located is one of: a
legacy path that read MariaDB rather than HERMES Redis candles; a deployment
that feeds HELIOS from a fact directory; an unmerged work-order branch that
stopped before writing code; or an untracked read-only probe. The belief that
an integration was "previously completed" is not supported by any artefact
read. "Not found" is itself a claim (see Stop conditions): the search
inventory below is what the audit must re-run and extend before the claim is
accepted.

### Candidate inventory

| # | Candidate | Where | Nature | Finding | Mark |
|---|---|---|---|---|---|
| 1 | New HELIOS v1 | `maff0000/HELIOS` (public), clone on the delivery host, `main` = `origin/main` = `7f7193d` (PR #1, independent PRODUCT_GREEN at `0bb9297`) | product, execution-blind | `helios/hermes/` holds one adapter, a fixture source; `helios/integration/hermes_boundary.py` is a data contract, "not a client"; no Redis or DB client, no network sink. Facts arrive as validated `MarketFactFrame` values. Accepted schema version is `helios.market_fact/1.0.0`. | PROVEN |
| 2 | GOLD Strategy Runtime | `maff0000/GOLD-STRATEGY-RUNTIME` (private), clone on the delivery host, `main` `5891415` (PR #1) | deployment wiring | Runs HSA, HELIOS and CER as containers on pinned digests. Its own `docs/COMPONENT-DELTAS.md` CD-1 states HELIOS "has no live HERMES transport", rejects a runtime-owned bridge, and bounds the delta as "a HERMES transport source behind HELIOS's existing fact-source interface". CD-3 defers a Redis sink. ADR-001 Ruling 1 keeps v1 free of shared Redis. | PROVEN |
| 3 | Deployed GOLD stack | delivery host, DEV and PROD container sets (healthy, up about five weeks) built from the runtime repo images dated 2026-09-07 | deployed unit | HELIOS container mounts a host fact directory and a strategies directory read-only; the fact directory holds four files with fixture-style names (`xau_usd_aligned_*`). Evidence says it is fixture-fed. Content of the files was not opened. | PARTIAL |
| 4 | HELIOS to HERMES PROD proof | HELIOS branch `wo/WO-HELIOS-HERMES-PROD-INTEGRATION-PROOF-0001` (one commit `84d3772`, unmerged) | work-order evidence, no code | Terminal verdict `WAITING_FOR_HERMES_BACKFILL` (2026-09-05, a Saturday): D1 had 21 of 26 required bars and no `latest` key; H4 stale by days. Records that HELIOS has no Redis client and validates `hermes.market_fact/1.0.0` while live HERMES publishes `v1` / `hermes.candles.latest`. No harness was built. | PROVEN |
| 5 | Read-only compatibility probe | `/root/helios_compat_probe.py` and `/root/helios_cap.json` on the delivery host, dated 2026-10-07, untracked | evidence probe | Header says it is "not a proposal of adapter code": feeds real captured HERMES objects (candle, indicators, session) through HELIOS's `MarketFactFrame` validator in a no-network container to show which raw fields pass. Output was not re-run or located. Likely Lane A or earlier-lane input. | PARTIAL |
| 6 | Legacy HELIOS V2 / V3 | tradingProteus tree on the delivery host (`helios/`, `helios_v3/`); units `helios-shadow` and `helios-v3` both masked | legacy, retired | V2 marked RETIRED 2026-04-29 (`RETIRED.md`). V3 daemon reads a database and publishes to the fabric HTTP gateway; no read of HERMES candle keys was found by grep. Not the new HELIOS lineage. Archived with SHA256SUMS under a dated legacy archive directory on the delivery host. | PARTIAL |
| 7 | Trading-host helios_bridge | `/srv/TRADER/helios_bridge/bridge.py` (984 lines) on the trading host; unit `helios-bridge` disabled, inactive | external adapter, legacy | Reads M1 candles, signals and levels from the HERMES MariaDB schema (`tradingSignals`) and writes `helios:*` fabric keys for TRADER. Its docstring names it "tradingScalp/HERMES to Memory Fabric". A database reader, not a Redis reader, and not feeding new HELIOS. Carries an assurance extension (fabric flag key). | PROVEN |
| 8 | XAU watcher / gate compositor | `/srv/helios/trader-xau-watcher`, `/srv/helios/trader-gate-compositor` on the trading host; units disabled | legacy | No `redis` or `hermes:` key reference found in watcher source by grep. Compositor not opened. Also unopened: private repos `trading-helios` (skeleton, last push 2026-06-22), `tradingGOLD`, `trading-hermes`, and the tradingProteus deploy copy. | PARTIAL / UNVERIFIED |
| 9 | Fabric `helios:*` keys | delivery host fabric gateway, key names only, labelled fabric-only | legacy state | 207 keys: `helios:setup:history:*` (199), `helios:journal:*`, `helios:setup:current:XAU_USD`, `helios:signals:m1`, `helios:heat`, `helios:levels`; plus one `helios_bridge:assurance:task:state`. These are outputs of the legacy scanner and bridge, none are HERMES inputs. | PROVEN (names), UNVERIFIED (values) |
| 10 | HERMES contract surface | HERMES publisher manifest sample under a dated evidence directory on the delivery host (2026-10-07) | upstream authority | `schema_version` `v1`; canonical instrument `XAU_USD`; six timeframes ACTIVE for `candle_latest`; `candle_history_d1` BLOCKED until D1 latest is green; HERMES declares no regime ownership. | PROVEN (sample), live state UNVERIFIED |

### Contract reconciliation read so far

- **Frame shape (PROVEN).** `MarketFactFrame` binds instrument, timeframe,
  bar-open `timestamp_utc`, candle (`open high low close volume complete
  source`), indicators (`rsi_14 ema_9 ema_21 ema_50 ema_200 atr_14 regime
  session`, all optional, absent never zero) and provenance (`source`,
  `schema_version`, `observed_at_utc`, `ingested_at_utc`). Closed world: unknown
  field refused; binary floats refused; windows must be strictly ascending.
  Source: HELIOS `docs/CONTRACTS.md` and `helios/contracts/market_fact.py`.
- **Version gap (PROVEN).** HELIOS accepts `helios.market_fact/1.0.0` (set by
  `HELIOS_ACCEPTED_HERMES_SCHEMA_VERSIONS`); live HERMES publishes `v1` with a
  `hermes.candles.latest` envelope. Row 4 records the same gap.
- **Provenance gap (PROVEN, from GOLD runtime CD-2).** A fact `source` is a
  lowercase token, so DEV and PROD HERMES cannot be told apart in the frame.
  The runtime requires `HERMES_EXPECTED_ENVIRONMENT` with no silent fallback.
- **Completeness gap (PROVEN as of 2026-09-05, UNVERIFIED now).** The proof
  branch found H4 and D1 incomplete on HERMES PROD. HELIOS needs H4 for the
  `CONTEXT` role of the first GOLD template.
- **Indicator gap (UNVERIFIED).** HELIOS carries EMA 9/21/50/200 and ATR 14;
  whether HERMES publishes the same names, and any SMA, was not read.

### HSA first-strategy read so far

`maff0000/HSA` (public) `main` `279ec18` holds two governed packages, both
`CANDIDATE`, both `XAUUSD`, neither with passing CER evidence:

| Package | Shape | Roles / timeframes | Observations |
|---|---|---|---|
| `gold_context_breakout` 1.0.0 | `CONTEXT_TRIGGER`: `golden_cross` (context) then `range_breakout` (trigger) | CONTEXT 4H, TRIGGER 5M | Needs H4 and M5 only. Requires `ma.fast` / `ma.slow` as simple averages of close, plus `range.high` and `range.low` over a lookback; HELIOS facts carry EMAs, not SMAs. HELIOS has a same-named fixture chain (`gold_context_trigger`, H4/M5) that suggests the shape is already runnable. |
| `wick_rejection_sequence` 0.1.0 | `SEQUENCE`: `rejection_wick`, `no_wick_candle`, optional `range_breakout` | LOCATION and CONFIRMATION 15M, TRIGGER 5M | Needs M15 and M5 only. Needs only raw candle fields, so fewer indicator dependencies, but intraday freshness load is higher and evidence is "still owed before promotion". |

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
   method for the "no integration exists" claim.
2. For each reader candidate: reuse, adapt or rewrite, with justification
   against `MarketFactFrame`.
3. A field-by-field mapping from live HERMES surfaces to `MarketFactFrame`
   with every gap named.
4. A minimum adaptation plan mapped to `HELIOS-T2` (and to `HERMES-FACT-001`
   where the gap belongs to HERMES).
5. A ranked review of HSA packages for the first GOLD strategy, naming what
   must change in each.
6. An explicit ruling input on whether a new reader is justified, or exactly
   which existing artefact it extends.

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
6. **HSA review.** Rank every package in HSA `strategies/` (and the HELIOS and
   GOLD runtime packages for GOLD) for first-GOLD-strategy fitness: data
   needs against what HERMES publishes, timeframe completeness, indicator
   names, determinism, execution-blindness, evidence state, fit with the
   HELIOS package schema and with the `goal.strategy/v1` draft. Name what
   must change for each.

## Non-goals

- No code, adapter, reader, sink, schema or fixture is written or changed in
  any product repository; documents only. No second reader is built,
  scripted or prototyped.
- No change to HERMES, ARES, FALCON, TRON, HSA, CER, the GOLD runtime, or any
  running unit, container, timer or fabric key.
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

**Collision notes:** writes only to a new branch of `maff0000/HELIOS`
(`docs/evidence/` and an audit note) and `maff0000/GOAL` (an index entry under
`audits/`). It does not touch product source, `pids/HELIOS-T1.md` or
`backlog/`.

## Safety boundaries

- Read-only on every system except the author's own worktree. No production
  mutation, no running-service change, no restart, no unmask, no enable.
- HELIOS stays execution-blind. No audit text or fixture may introduce broker,
  account, sizing, order or TRON vocabulary into HELIOS; the existing
  forbidden-vocabulary test must still pass unchanged.
- **No second reader.** The audit must not stand up, run or script a new
  HERMES reader against live Redis. Captured samples are read through the
  existing Redis gateway read endpoints or existing evidence directories only.
- `maff0000/GOAL` and `maff0000/HELIOS` are public: no internal IPs, hostnames
  beyond generic role names, accounts, credentials, tokens, environment
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

1. **Evidence PR** into `maff0000/HELIOS` containing
   `docs/evidence/GOLD-AUD-B.md` (sanitised) and supporting tables, plus a
   `maff0000/GOAL` cross-component index entry. Checklist:

   | # | Evidence item | Present |
   |---|---|---|
   | 1 | Search method and exact commands, including the negative-search record | [ ] |
   | 2 | Candidate inventory (path, repo, commit, nature, status, mark) | [ ] |
   | 3 | Source-level reading of each candidate that touches HERMES data | [ ] |
   | 4 | HERMES-to-`MarketFactFrame` field mapping with gaps | [ ] |
   | 5 | Schema version and provenance reconciliation | [ ] |
   | 6 | Reuse / adapt / rewrite classification per component | [ ] |
   | 7 | Gap list, each gap with an owner repository | [ ] |
   | 8 | Minimum adaptation plan mapped to `HELIOS-T2` and `HERMES-FACT-001` | [ ] |
   | 9 | HSA package ranking and what must change | [ ] |
   | 10 | Sanitisation attestation and unchanged-HELIOS test result | [ ] |

   The ten items above are the evidence set for Central Architecture; if the
   CA's own numbering differs, this table is mapped to it in the PR body.
2. **Reuse inventory** (table, item 2 and 6).
3. **Gap list** (item 7).
4. **Minimum adaptation plan** (item 8): ordered, each step with target
   repository, owner persona, dependency and the proof that would close it.

## Acceptance

Mechanical:

1. `./tools/goal-validate` exits 0 on the GOAL branch; `./tools/secret-scan`
   exits 0 on both branches.
2. `git diff --name-only origin/main` on the HELIOS branch lists only
   `docs/evidence/` paths; on the GOAL branch, only `audits/` paths.
3. HELIOS `pytest -p no:cacheprovider -q` reports the same pass count as the
   baseline (1005 at `7f7193d`) with no test or source file modified.
4. Every row of the candidate inventory has a mark in {PROVEN, PARTIAL,
   UNVERIFIED}; every PROVEN row names a path or command and a commit or date.
5. A grep of the new documents for `[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+` (except
   version strings with a `v` or `/` prefix), for the words `password`,
   `secret`, `token` followed by a value, and for private hostnames returns no
   hit.
6. Each GOLD-capable package found (HSA, HELIOS fixture and runtime strategies) has a ranked row with
   its required timeframes and fields checked against the field mapping.
7. Every gap in the gap list has an owner repository and a closing proof.
8. No `docker exec`, write, unit-state or fabric write appears in the recorded
   command log.
9. The checklist in Deliverables is complete or each missing item states why.

## Stop conditions

Return to the PO or Central Architecture if:
- a candidate reader is found to be running against live HERMES Redis (stop,
  report, do not touch it);
- the audit would need a write to any running system, a secret, or a new
  reader to make progress;
- HERMES Lane A output contradicts the negative-search result and the
  difference cannot be resolved read-only;
- evidence in a private repo is essential and cannot be sanitised;
- the "no integration exists" claim cannot be supported by the recorded search
  method (a negative is a claim, not a finding).

Do not invent around a stop condition.

## Open decisions

1. **Amend HELIOS-T1 or new bounded item?** Recommendation: a new bounded
   item. HELIOS-T1 is a refactor to a contract that is not yet frozen
   (`depends_on` `GOAL-CORE-001`); this audit concerns the live transport,
   which belongs to `HELIOS-T2`. Amending T1 would couple a read-only audit
   to an unfrozen contract and would blur T1's single purpose. The audit is
   therefore framed as a **pre-increment of `HELIOS-T2`** (and a hard input
   to its PID), not an amendment of T1. Owner PO. Blocks approval of this PID.
2. **Is `HELIOS-T2` in scope for ARES?** GOAL-RECON-H2 finds the T2 title
   contradicts HELIOS PID on ARES risk. This audit maps to the HERMES half
   only. Owner PO. Does not block this PID; blocks T2 PID.
3. **Where may sanitised samples live?** Evidence PR in the public repo
   versus a private evidence location cited by identifier. Recommendation:
   sanitised excerpts public, full captures private. Owner PO. Blocks approval.
4. **Spelling canon at the HERMES boundary** (`XAU_USD`/`H4` versus
   `XAUUSD`/`4H`): the audit reports the mapping; the ruling belongs to
   `HERMES-FACT-001` / `GOAL-CONTRACT-001`. Owner PO. Does not block approval.
5. **First GOLD strategy selection** follows the audit's ranking. Owner PO.
   Does not block approval. Probe provenance (who authored the untracked
   probe, may its output be cited) is confirmed in the same step. Owner PO or
   ROGUE. Does not block approval.

## Evidence

Read on 2026-10-15 on two estate hosts, read-only: GOAL `main` at
`1739e742154c77e9e2a96927dc40d4978b9cd798` (verified; backlog entries, DCP-001
PID); the Wave 1 Group E HELIOS-T1 candidate PID (the `GROUP-E-REPORT.md` named
in the task was not found and not read); GOAL-RECON-H1/H2 notes; the
`GOAL-CONTRACT-001` draft; HELIOS `main` `7f7193d` (contract docs, boundary
module, fixture names, proof-branch evidence file); GOLD-STRATEGY-RUNTIME
`main` `5891415` (README, COMPONENT-DELTAS, compose grep, PID relationship
section); HSA `main` `279ec18` (strategies, catalogue listing); the trading-host
bridge source header and unit states; delivery-host unit states, container names,
images and mount destinations, legacy retirement marker and archive listing,
and fabric key names.

Not read: FALCON PID-07/08 bodies, the private `tradingGOLD` and
`trading-hermes` repositories, the gate compositor, the deployed fact files'
content, live HERMES state (2026-10-07 sample only), HERMES Lane A output.

## Approval

PENDING. No approval has been recorded for this PID candidate. Approval is recorded here by Central Architecture/PO only.

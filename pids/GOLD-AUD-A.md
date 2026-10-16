# GOLD-AUD-A — HERMES PROD XAUUSD Redis publication audit (GOLD MVP Lane A)

**Lane:** research  
**Target repository:** `maff0000/hermes`  
**Evidence:** primary PR in `maff0000/hermes`, branch `wo/GOLD-AUD-A-evidence`, path `docs/evidence/GOLD-AUD-A/`  
**Priority:** P0  
**Risk:** Medium  
**Matt gate:** Yes  
**PO gate:** Yes  
**Delivery:** ROGUE → HELM-lane operator → FORGE  
**Complements:** `HERMES-CUR-001`  

**Header notes:** The Matt gate applies to production Redis read access only (decision D1, since resolved: Matt gave his express permission on 16 October 2026, see Approval; the flag remains true as the manual production-read precondition and a HELM-operated bounded protocol; the gate stays TRUE until he expressly permits); no Matt gate applies to the GitHub / source analysis, which may proceed meanwhile. GOAL holds an index entry only; the primary evidence PR is in `maff0000/hermes`. The audit is a strict subset ('Increment A') of `HERMES-CUR-001` scope item 1 (amendment fallback below). Evidence location follows programme-controller rulings 1 to 3 (`PORTFOLIO.md` appendix). Delivery: the evidence run is performed by a HELM-lane operator; FORGE produces the docs and fixtures PR only.

Header values match the registered backlog item (`backlog/backlog.yaml`, `pid_path: pids/GOLD-AUD-A.md`). Lane vocabulary is the backlog set {shared, research, trading, ops}; `research` is used for all
six audits (CA frame). Priority, lane and risk follow the CA/PO adjudication 2026-10-15 (recorded in `PORTFOLIO.md`, not in this PID); approval is recorded in the Approval section below.


## Status

APPROVED (Central Architecture, 16 October 2026; see Approval). Registered in the backlog as DELIVERY_READY by the governed amendment.

`depends_on: GOAL-DCP-001` (CLOSED). Parent programme item: GOLD-MVP-001 (Lane A).

## Relationship to existing PIDs (amend vs new: decision and reason)

**Decision: GOLD-AUD-A is a new bounded item, defined as a strict subset ("Increment A") of
`HERMES-CUR-001` scope item 1 (Redis contract key inventory), not a duplicate of it.**

Why not an amendment of HERMES-CUR-001:

1. CUR-001 is DEV+PROD, SQL+Redis, git-graph, image identity, HMT-2 location, defect list. Its
   critical open decisions (D1 snapshot timing around a planned production change, D2 who probes,
   D7 HMT-2) are unresolved and would hold this audit hostage.
2. CA's directive for Lane A is narrower and deeper on one surface: the PROD **XAUUSD Redis
   publication** only (keys, schemas, indicators, timeframes, freshness, warm-up, validation,
   status, documented-vs-actual). CUR-001 only asks for key inventory and counts.
3. CUR-001 is a Shared-lane P0 that blocks HERMES-FACT-001 and through it GR-001, HELIOS-T2/T3.
   Adding a fixture and contract-comparison payload to it changes its risk and delivery shape.
4. Lane A needs sanitised golden fixtures; CUR-001 produces none.

Non-duplication (proposed CUR-001 amendment text for CA to apply; this PID does not edit it):
*"Scope item 1 key inventory is satisfied for XAU_USD by the GOLD-AUD-A evidence PR; CUR-001 keeps
all other Scope items and other instruments, and cites rather than re-runs that inventory."*
Fallback if CA prefers one item: fold this PID in as CUR-001 "Increment A" unchanged. (Not taken: the CA/PO adjudication 2026-10-15 confirms this as a separate audit work item, not an amendment.)

## Purpose

Record, from observation rather than memory, what the production HERMES instance actually
publishes in Redis for gold today, compare it with the documented Redis contracts, and give the
GOLD MVP a trustworthy, public-safe description and golden samples of the existing production
publication. This is the evidence base for the HELIOS `MarketFactFrame` consumer mapping and for
`HERMES-FACT-001`. The existing production implementation is preserved; nothing is changed.

**CA guidance 2026-10-15 applied (items 1 and 6).** HERMES owns Redis publication; a HELIOS-side external adapter, outside the pure HELIOS engine, owns
consumption and translation. This audit's output is therefore the first repository record of what HERMES publishes (the input to a
`HERMES-FACT-001`-style publication contract) and the PROD facts against which audit B compares candidate strategy requirements. It is the
first step of the sequence audits A and B, reconciliation, strategy selection (PO), `GOLD-MVP-001` acceptance planning; this audit selects no strategy.

CA directive (verbatim): *"Audit the existing PROD XAUUSD Redis publication, not the expanded
development feature programme. Record actual keys, schemas, indicator coverage, timeframes,
freshness, timestamps, historical warm-up, validation and status. Compare PROD reality with the
documented Redis contracts. Preserve the existing production implementation. No production
mutations."*

Naming: the key token is `XAU_USD` (canonical; `XAUUSD` is never a key form).

## Current state

Labels: **[repo]** committed GitHub content; **[fabric]** Memory Fabric only (memory, not
authority, ADR-DELIVERY-001); **UNVERIFIED** not proved by this PID's author. This PID was drafted
without touching production Redis; every PROD statement is UNVERIFIED and is established by this audit.

**Documented contracts [repo, `maff0000/hermes` `main` at `ca19017`, read 2026-10-15].**
- `docs/contracts/hermes_redis_contract_manifest.md` registers only two contracts:
  `hermes:ticks:{instrument}:latest:v1` and `hermes:ticks:latest:v1` (envelope with
  `generated_at_utc`, `valid_until_utc`, `ttl_seconds` 5 / Redis EX 10, `freshness_state`
  FRESH/DEGRADED/STALE/UNAVAILABLE, `status`, `provenance`, `seq` null). Their status text reads
  "DESIGNED (publisher not built)". It states `hermes:candle_features:*`, `hermes:candle_context:*`
  and `hermes:indicators:*` are "separately designed ... (different WOs)" and not in the manifest.
- `docs/contracts/hermes_redis_tick_contract_v1.md` (design only), builder/validator
  `utils/tick_contract_v1.py`, fixtures `tests/fixtures/tick_contract/`.
- `docs/architecture/environment-model.md` section 4a: Redis is the published consumer interface; canonical gold token
  `XAU_USD`; core contract = price, signal/indicator snapshot, M1/M5/M15/H1 latest+history; XAU_USD
  may add H4/D1, features, levels, sessions, gaps, quote/tick. It points to a "live key/catalog
  contract" held in fabric, i.e. **no repo
  document registers the candle, indicator, feed-health, catalog or manifest key families.** That
  gap is itself a primary finding to be confirmed.
- Consumer side [repo, HELIOS]: `helios/contracts/market_fact.py` fixes `FACT_FIELDS` = candle
  (open, high, low, close, volume, complete, source) + indicators (rsi_14, ema_9, ema_21, ema_50,
  ema_200, atr_14, regime, session), schema string advertised as `helios.market_fact/1.0.0` (fixtures, config and tests also
  accept `hermes.market_fact/1.0.0`).

**PROD observations.** None are stated as current facts in this public document. Earlier observations exist only as memory (fabric, not authority) and are held in the maintainers' private operations record; every PROD fact is established by this audit or labelled UNVERIFIED.

**UNVERIFIED (must be established by the audit).** Which Redis instance and logical DB is "PROD" for
Lane A (memory notes record PROD location and status as unverified; fabric sources disagree on key
counts); the live key list; any key whose registered contract differs from reality; actual
TTLs; actual indicator coverage per timeframe; real publish cadence; whether the tick key is live
though documented as unbuilt; whether there is an in-band validation or status field beyond
`freshness_state`/`status`; whether stale or missing data degrades status or is silently served.

**Access path and protection posture (no address, public repo).** Access is through the HELM-operated bounded protocol; credentials are never recorded. The audit records the result in the private evidence record.

## Target outcome

At closure `maff0000/hermes` holds a dated audit record, a machine-readable inventory, sanitised
golden samples and a documented-vs-actual comparison for the PROD `XAU_USD` Redis publication, such
that HERMES-FACT-001 and the HELIOS-side external adapter's mapping can be written against observed facts, every
PROD statement is either proved by the evidence bundle or labelled UNVERIFIED, and production is
provably unchanged.

## Scope

Read-only audit of the PROD `XAU_USD` publication only. One recorded observation window plus one
bounded sampling period (see Safety, S7). Each item names its method.

1. **Key inventory.** `SCAN MATCH hermes:*XAU_USD* COUNT 200` and the global (non-instrument) key patterns listed in the maintainers' private operations record. Per family: count, `TYPE`, `TTL`/`PTTL` distribution (min, median,
   max, persistent), key-name pattern, owning contract. Cross-check against `DBSIZE` only. Record keys of other instruments only as a count, not content.
2. **Schema per key.** One `GET`/`HGETALL` sample per family per timeframe; derive field list,
   types, nullability, nesting, `schema_version`, `contract`, `contract_version`.
3. **Indicator and timeframe coverage.** Matrix of timeframe (M1, M5, M15, M30, H1, H4, D1) by
   {latest candle, history objects, indicator key, candle_features} and per indicator
   (rsi_14, ema_9, ema_21, ema_50, ema_200, atr_14, plus every other published) present, NULL, or absent.
4. **Freshness and timestamps.** For each sampled key, record the four times separately and never
   merge them: bar open time (`timestamp_utc` / `value_open_time_utc`), publish time
   (`generated_at_utc` / `updated_at`), `valid_until_utc`, and the observer's receive time. Report
   publish lag, validity window, and per-timeframe publish cadence from repeated bounded samples.
5. **Warm-up and historical depth.** Per timeframe: history index length, first and last bar open
   time, expected vs present bar count over the trailing window, gaps (H4 explicitly), TTL horizon,
   and whether depth satisfies the indicator lookback (ema_200) per timeframe.
6. **Validation and status.** All validation/status fields and keys: `freshness_state`, `status`,
   `reason_codes`, feed health, publisher liveness and any other published
   health or status surface. Record allowed values observed and values never observed.
7. **TTL behaviour.** TTL of latest vs history vs index keys; compare to documented `ttl_seconds`
   and `EX` rules; observe TTL decrement and renewal between two samples.
8. **Failure and staleness semantics.** Observe only what occurs naturally during the window
   (e.g. weekend close, session gap): does a key expire, turn `STALE`/`UNAVAILABLE`, or keep serving
   an old value with a fresh-looking envelope. No fault injection of any kind.
9. **Documented-vs-actual table** for every documented contract and every observed key family,
   classifying each row MATCH, DIVERGENT, UNDOCUMENTED (live, no repo doc) or DOCUMENTED-NOT-LIVE.
10. **Fixtures and defects.** Sanitised golden samples and a defect list with proposed owner.

## Non-goals

- The expanded HERMES development feature programme (HMT-3, event/microstructure facts, GC data,
  indicator-history activation, new indicators, new timeframes).
- New feeds, new keys, new contracts, new publishers, any change to OANDA ingestion.
- Any write to any system other than the evidence worktree; any Redis write of any kind.
- Other instruments' content (only their existence as a count).
- Defining `goal.market-fact/v1` (HERMES-FACT-001), any production recreate or deploy, infrastructure
  hardening, credential rotation, branch protection, or repair of any defect found.
- DEV Redis and SQL audit (HERMES-CUR-001 owns it); the HMT-2 corpus.

## Dependencies and interfaces

- Hard: GOAL-DCP-001 (CLOSED). Soft: GOAL-CONTRACT-001 fact grammar (the audit reports against its
  field vocabulary; it does not wait for it).
- Consumer: HELIOS `MarketFactFrame` / `helios.market_fact/1.0.0` (advertised; `hermes.market_fact/1.0.0` also accepted by fixtures, config and tests) (candle + indicator fields
  above). The audit's mapping table states, per `FACT_FIELDS` entry, the PROD key and field that
  carries it, or "absent".
- Contract owners: HERMES owns the `hermes:*` contracts; GOAL-CONTRACT-001 owns the cross-component
  fact grammar; HELM owns PROD access and infrastructure.
- Feeds: HERMES-FACT-001, HERMES-GR-001 (fixtures as candidate replay inputs), HERMES-CUR-001.
- The one primary evidence PR lands in `maff0000/hermes` (branch `wo/GOLD-AUD-A-evidence`, path
  `docs/evidence/GOLD-AUD-A/`). After that PR is accepted, one separate GOAL PR contributes this lane's
  entry (path and SHA) to `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md`, which `GOLD-MVP-001` owns
  (single writer: the `GOLD-MVP-001` PL). The branch `wo/GOAL-GOLD-AUD-A` is the PID draft, not evidence.

## Safety boundaries

**S1 Allow-list (exhaustive; identical to `PORTFOLIO.md` section 6.2).** Every command goes through a
wrapper that rejects anything not listed. `SCAN` with `MATCH` and `COUNT` <= 200; `TYPE`; `TTL`, `PTTL`;
`EXISTS`; `STRLEN`; `GET` only when `TYPE` is string and `STRLEN` <= 64 KiB; `HLEN`; `HGET`; `HGETALL` only
when `HLEN` <= 200 (otherwise record `HLEN` and sample with `HGET`); `ZCARD`; `ZRANGE` bounded to 100 and
only when `ZCARD` <= 200; `SCARD`; `SMEMBERS` only after a size pre-check shows `SCARD` <= 200 (otherwise
forbidden); `LRANGE` bounded to 100; `INFO` with section `server`, `clients` or `persistence` only (the
`memory` section and any other section only if the PO adds them to the approved PID); `DBSIZE`; `PING`.

**S2 Forbidden.** `KEYS`, unbounded `SCAN` (no `COUNT`) or `SCAN` over the whole keyspace without
`MATCH`; `INFO` without a permitted section name, and `INFO keyspace`, `INFO memory`, `INFO stats`,
`INFO all`; `SMEMBERS` without the pre-check; `SET`, `DEL`, `UNLINK`, `EXPIRE`/`PEXPIRE`/`PERSIST`, `RENAME`,
`FLUSHDB`/`FLUSHALL`, `CONFIG` (any form, including `CONFIG GET`), `ACL` (any form, including creating a
principal), `SUBSCRIBE`/`PSUBSCRIBE` (no consuming streams), `XREAD`/`XREADGROUP`/`XACK`/`XDEL`,
`BLPOP`-family, `MONITOR`, `DEBUG`, `SLOWLOG RESET`, `CLIENT KILL`, `SAVE`/`BGSAVE`, `SHUTDOWN`,
`SCRIPT`/`EVAL`/`FUNCTION`, `MIGRATE`, `REPLICAOF`, `PUBLISH`, `OBJECT FREQ`, `MEMORY DOCTOR`, and any
`docker exec`/restart/compose on the PROD host.

**S3 Rate and size.** One connection at a time (a second operator's repeat runs after the first has finished, never concurrently), sequential commands, at most 10 commands/s, a pause of >= 1 s
between `SCAN` pages, total payload read <= 50 MB, no single reply > 64 KiB (skip and record `STRLEN`).
Abort on any latency or memory warning. Run only outside the HERMES publish-critical minutes if the operator
advises; never during a deploy window.

**S4 Credentials and access.** The operator uses the approved
read path only. No credential is created, copied, rotated or tested and no ACL principal is created.
Credentials are never recorded: if the approved read path itself supplies one, it reaches the client only
through an environment variable set inside the wrapper process, never on a command line, in a log or in
evidence. If authentication is required and none is supplied, stop. No `CONFIG GET` of any parameter, no
`INFO` section exposing config or `docker inspect` environment. Any credential-handling or exposure
question: stop and report privately to HELM.

**S5 No secrets; sanitisation.** Raw output stays private, referenced by SHA-256 in the PR. Before
anything reaches the public repo: remove host names and addresses (use "the production host"), ports
other than the standard Redis port, redis target strings, container ids, account identifiers, user
names, tokens; replace `provenance.runtime_instance`, `redis_target`, `service_identity` host parts
with `<REDACTED>`; keep market values (public OANDA-sourced prices) but round sample sets so that
no more than a bounded window is published. Then `./tools/secret-scan` and `gitleaks` on the PR, and
a grep for IPv4 patterns, `redis://`, `host`, `token`, `password` must return nothing.

**S6 Who runs it.** A HELM-lane operator with approved production read access. FORGE engineers
receive the sanitised bundle only, never production credentials or addresses. ROGUE supervises;
ROGUE does not itself connect to production.

**S7 Time-box.** Preflight (state the command list, recorded before use): 0.5 day. Observation
window: single run of <= 30 minutes for inventory and schema, plus a sampling period of <= 2 hours
covering at least one full M15 and one H1 boundary, plus (if D3 agrees) one H4 boundary: total
wall-clock <= 6 hours. Analysis and PR: <= 2 days. Overrun is a stop condition, not an extension.

**S8 Before/after proof.** Record `INFO server` (`uptime_in_seconds`, `run_id`) and `DBSIZE` before
and after. An unchanged `run_id` establishes that there was no restart; it is NOT proof that no data was
mutated (CA/PO adjudication 2026-10-15). Data-mutation checks use this audit's own before/after comparison of
the sampled keys (existence, `TTL`/`PTTL` and a hash of each sampled value), taken within this read-only
protocol and its caps. Key count may change only by normal HERMES publishing and must be explained.

**S9 Gate.** Production read access is not assumed. It requires Matt's express permission (D1) and a
HELM-operated bounded protocol, recorded in the PR description before the run. Until then only the
GitHub / source analysis half proceeds.

## Deliverables

Paths in `maff0000/hermes` (names proposed, final names by PL):

1. `docs/evidence/GOLD-AUD-A/AUDIT-<date>.md`: findings, sections matching Scope 1-9.
2. `docs/evidence/GOLD-AUD-A/inventory.json`: machine-readable key families, TYPE, TTL stats,
   field lists, coverage matrix, with `source` (command), `observed_utc`, `evidence_hash` per entry.
3. `docs/evidence/GOLD-AUD-A/contract-comparison.md`: documented-vs-actual table (Scope 9).
4. `docs/evidence/GOLD-AUD-A/fixtures/xau_usd/*.json`: sanitised golden samples, one per key family and
   timeframe, plus `MANIFEST.json` (SHA-256 per file, capture UTC, sanitisation record). Final
   location per D4.
5. `docs/evidence/GOLD-AUD-A/protocol.md`: the exact command allow-list run, with counts.
6. `docs/evidence/GOLD-AUD-A/defects.md`: defect list (id, evidence, severity, proposed owner,
   closing work item). Defects are listed, not fixed.
7. Private evidence bundle reference (hash and storage identifier only).
8. After the hermes evidence PR is accepted: one GOAL PR adding this lane's entry (pointer to the hermes PR and SHA) to `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md` (owned by `GOLD-MVP-001`; contributed one lane per PR).

## Evidence PR checklist (CA's ten mandatory evidence items, CA numbering)

CA's ten mandatory evidence items, in CA's numbering (the numbering is CA's and is not to be changed by a lane): (1) PID/WO identifier and exact audited scope; (2) source repositories, revisions and relevant documentation references; (3) existing implementation: proven, partially proven, unverified or missing; (4) actual versus expected contract comparison; (5) tests, fixtures and evidence references; (6) specific defects and compatibility gaps; (7) reusable code and documentation; (8) minimum recommended implementation changes; (9) safety and deployment constraints; (10) independent audit verdict and any unresolved findings.

| CA # | CA evidence item | This audit puts it in | Proof method |
|---|---|---|---|
| 1 | PID/WO identifier and exact audited scope | PR description header and AUDIT section 0: quoted scope sentence of the approved PID; D1 approval quoted | Quoted text equals the approved PID scope; approval timestamp precedes bundle capture |
| 2 | Source repositories, revisions and documentation references | AUDIT section 0 and `inventory.json` `sources[]`: full SHAs of hermes and HELIOS, documentation paths, PROD instance identification (D2) | Every SHA re-resolves; auditor re-reads each cited document |
| 3 | Existing implementation: proven, partially proven, unverified or missing | `inventory.json` `families[]` and the AUDIT coverage matrix (Scope 1, 3, 5, 6, 7, 8): each family, timeframe and indicator marked proven / partial / unverified / missing (PRESENT / NULL / ABSENT cells map to these) | Count per pattern reproduces from the protocol SCAN log; matrix of 8 `FACT_FIELDS` indicators x 7 timeframes has no empty cell; auditor re-runs SCAN |
| 4 | Actual versus expected contract comparison | `contract-comparison.md` (Scope 9): each documented key and each observed family classified MATCH, DIVERGENT, UNDOCUMENTED or DOCUMENTED-NOT-LIVE; field list, types, TTL, the four timestamps kept separate, freshness and status enumerations | Exactly one classification row per documented key and per observed family |
| 5 | Tests, fixtures and evidence references | `docs/evidence/GOLD-AUD-A/fixtures/xau_usd/` with `MANIFEST.json`; `protocol.md` command log; script checks (fixtures validate against recorded field lists; lag and warm-up figures recomputed) | SHA-256 in MANIFEST verifies; recomputed lag and warm-up equal reported values |
| 6 | Specific defects and compatibility gaps | `defects.md`: id, evidence, severity, proposed owner, closing work item | Every DIVERGENT or UNDOCUMENTED row has a defect entry |
| 7 | Reusable code and documentation | AUDIT section 'Reuse': `utils/tick_contract_v1.py`, candle and indicator builders, sanitised golden samples reusable by HERMES-FACT-001, HERMES-GR-001 and the HELIOS consumer mapping (path and revision, reuse boundary) | Each reuse entry cites path and revision |
| 8 | Minimum recommended implementation changes | AUDIT section 'Recommendations': minimum changes, each mapped to `HERMES-FACT-001`, `HERMES-CUR-001`, `HELIOS-T2` or another named owning item (listed, not fixed) | Each recommendation names an existing or proposed owning item |
| 9 | Safety and deployment constraints | `protocol.md` allow-list and S8 before/after (`run_id`, `DBSIZE`); sanitisation record; credential-handling or exposure questions reported privately to HELM only | Script asserts every logged command is allow-listed; `run_id` unchanged; S5 grep and secret-scan empty |
| 10 | Independent audit verdict and unresolved findings | Verdict file in the PR by the independent auditor (AUD-1) with unresolved findings and what the verdict does not cover | Fresh auditor GREEN / AMBER / RED with exact SHAs; PO acceptance recorded separately |

## Acceptance

GREEN requires all of the following; each has a proof method:

1. **Authorisation recorded.** D1 approval is quoted in the PR before the run. Proof: PR text and
   timestamp precede the bundle capture time.
2. **Allow-list compliance.** The protocol log contains only S1 commands. Proof: script in the PR
   asserts every logged command is in the allow-list and none in S2; independent auditor check.
3. **No restart and no mutation.** S8 before/after shows unchanged `run_id` (no restart; this alone is not
   proof of no data mutation) and, for the sampled keys, an unchanged key/TTL/value-hash comparison apart from
   explained normal HERMES publishing, and no unexpected keyspace change. Pass criteria: `run_id` equal before and after;
   every differing sampled key is in the allowed-diff set, fixed before the run as keys whose publish or bar timestamp advanced
   by the documented cadence or whose TTL elapsed, each difference listed; `DBSIZE` change no larger than the listed expiring and
   newly published keys; any other difference is a FAIL. Proof: bundle excerpts.
4. **Checklist complete.** All 10 rows present and each proof method succeeds; coverage matrix has
   no empty cell.
5. **Independent re-derivation.** A second operator or auditor repeats the inventory SCAN and a
   sample of 10 keys in the same window, sequentially after the first operator has finished and over the same bounded protocol (never concurrently, so S3 holds); Pass criteria: the second run's key set equals the first run's except keys listed as expired or republished in the interval, and each common sampled key has an equal value hash once the timestamp and TTL fields of the AC3 allowed-diff set are excluded; any other difference is a FAIL.
6. **Fixtures are public-safe and faithful.** `MANIFEST.json` SHA-256 verifies; `./tools/secret-scan`,
   `gitleaks` and the S5 grep return nothing; sampled fixtures byte-match the sanitised raw excerpt
   after a documented transformation.
7. **Labels.** Every PROD statement is proved by the bundle or marked UNVERIFIED; no statement
   relies on fabric alone.
8. **Hermes tests untouched and green.** Existing hermes CI passes; no source file outside
   `docs/evidence/GOLD-AUD-A/` changes (diff check).
9. **Defects.** Every DIVERGENT or UNDOCUMENTED row has a defect entry with owner and closing item.
10. Fresh independent auditor GREEN; exact SHAs in the PR; PO acceptance recorded.

### Disposition table

**Disposition table (REQUIRED; CA/PO legacy application doctrine 2026-10-15).** The evidence PR contains `DISPOSITION.md` (format: `PORTFOLIO.md` section 7.4): one row per reusable component in scope — the HERMES publication surfaces and contract documents, the builders and validators (`utils/tick_contract_v1.py`, candle and indicator builders), the existing fixtures, and the currently deployed publisher as observed — each with generation (legacy / newer canonical / currently deployed), the criteria assessed (architecture fit, code quality, determinism, test evidence, maintainability, contracts, operational dependencies, integration cost), a verdict REUSE | REFACTOR | REPLACE | RETIRE, evidence, and the approximate comparative engineering cost of reuse versus refactor versus a clean build. A verdict is a recommendation only: nothing is retired, shut down or mutated, and the lane cannot be accepted without this table (it is part of CA evidence items 7 and 8).

## Stop conditions

Stop and return to PO/CA (do not improvise) if:

- D1 production read access has no express Matt permission, or requires a credential to be created or handed to a
  FORGE engineer;
- any step would need a non-allow-listed command, a restart, or a code or config change;
- a command raises latency or memory warnings, or the time-box S7 is exceeded;
- the PROD instance cannot be identified unambiguously (D2) or two candidate instances disagree;
- an exposed secret or an active safety defect is observed: stop documentation of
  that item and report privately to HELM;
- sanitisation cannot be proved (secret-scan or grep non-empty);
- a production recreate or deploy occurs mid-window (decide: re-run).

## Open decisions

| # | Decision | Owner | Blocks |
|---|---|---|---|
| D1 | Production Redis read access. Per CA/PO adjudication 2026-10-15: requires Matt's express permission and a HELM-operated bounded protocol; the gate remains TRUE until Matt expressly permits; GitHub / source analysis proceeds meanwhile. Open: Matt's permission, and which HELM-lane operator and read path. | Matt (permission), HELM | the runtime half only (not approval, not the source half) |
| D2 | Which Redis instance is "PROD" for Lane A: the HERMES production cache, or another instance? Memory notes record PROD location/status as unverified and sources disagree. Recommendation: operator identifies it by a build-info environment match and records the evidence; if ambiguous, stop. | PO | approval |
| D3 | Sampling duration: minimum is one full M15 and H1 boundary; include an H4 boundary (up to 4 h) and a session close? Recommendation: M15+H1 now, H4 boundary only if it falls in the window, no deliberate wait. | PO | later (before run) |
| D4 | Public or private samples: the fixtures live under `docs/evidence/GOLD-AUD-A/fixtures/xau_usd/` in hermes (ruling 3). Open: sanitised excerpts public with full captures private by identifier (recommended), or all samples private. GOAL stays pointer-only. | PO | later |
| D5 | Run before or after any planned PROD change? Recommendation: now; a short delta afterwards is a separate small increment. | PO | approval |
| D6 | RESOLVED by CA/PO adjudication 2026-10-15: kept as a separate audit work item, not folded into CUR-001. | CA/PO | none |
| D7 | Authority for undocumented key families (candle, indicator, feed-health, catalog): should the audit's comparison table become the proposed contract registry in hermes docs? Recommendation: audit records only; registry belongs to HERMES-FACT-001. | PO | later |

## Evidence

Sources read for this draft (2026-10-15), all read-only:

- GOAL `main` at `1739e74` (historical read base; baseline now `90323b3`): backlog entries HERMES-CUR-001/FACT-001/GR-001, `pids/GOAL-DCP-001.md`.
- Draft PID `pids/HERMES-CUR-001.md` on `wo/GOAL-PID-WAVE1-B-research` (and its group report).
- `audits/2026-10-14/reconciliation/RECON-H1.md` on `wo/GOAL-RECON-H1-datachain` (sections 0-2.4).
- `maff0000/hermes` `main`: `docs/contracts/hermes_redis_contract_manifest.md`,
  `docs/contracts/hermes_redis_tick_contract_v1.md`, `docs/architecture/environment-model.md`.
- HELIOS `helios/contracts/market_fact.py` (consumer field vocabulary).
- Fabric, read-only GET (memory, not authority): entries recorded in the maintainers' private operations record, and facts quoted in the
  CUR-001 draft.
- Auto-memory notes recording PROD location/status as unverified.
- Not accessed: production Redis or host, hermes `docs/config/hermes-configuration-reference.md`, HMT-2 storage.

## Approval

APPROVED. Recorded 2026-10-16 by ROGUE on the written authority of Central Architecture/PO.

1. Central Architecture adjudication of the GOLD MVP Portfolio, 15 October 2026 (APPROVED WITH CORRECTIONS AND GOVERNED MERGE CONDITIONS; approves the architecture and scope of this audit PID).
2. Central Architecture formal approval, 16 October 2026, Decision: OPTION 1. The previous adjudication is confirmed as the formal approval of record for the seven GOLD PIDs, including this one. No further approval of this PID scope is required unless a substantive change is proposed.

Scope of this approval: the read-only audit scope in this PID. It authorises no deployment, production mutation, broker order, contract freeze or live-capital action.

Production Redis read: separately authorised by Matt on 16 October 2026 (DR-4 owner condition satisfied; relayed by Central Architecture; the dated authorisation is held in the private owner-authorisation record, with no connection details published). It additionally requires HELM to verify the authoritative instance and logical database, confirm a read-only connection and review the exact S1 to S9 command protocol. The `matt_gate` flag stays true and `goal-ready` does not read it (R-19), so this precondition is checked manually before the production-read phase is dispatched. Source and GitHub analysis may begin immediately.

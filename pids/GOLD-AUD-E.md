# GOLD-AUD-E — FALCON evidence audit and minimum HELIOS/TRON publication set (GOLD MVP Lane E)

**Lane:** research  
**Target repository:** `maff0000/falcon` (primary evidence PR; GOAL carries the index entry only)  
**Evidence:** primary PR in `maff0000/falcon`, branch `wo/GOLD-AUD-E-evidence`, path `docs/evidence/GOLD-AUD-E/` (programme-controller rulings 1 to 3; `PORTFOLIO.md` appendix)  
**Priority:** P1  
**Risk:** Low  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  
**Complements:** `FALCON-T1` (carve-out: the excluded `strategy_trigger` and `tron.*` families), RECON-F's FALCON-T2/T3; amendment fallback in Dependencies and interfaces


Header values are PROVISIONAL: the item is not in `backlog/backlog.yaml`; the backlog patch is specified, not applied, in
`audits/2026-10-15/gold-mvp/PORTFOLIO.md` section 11. Lane vocabulary is the backlog set {shared, research, trading, ops}; `research` is used for all
six audits (CA frame). The PO sets final values.

## Status

DRAFT CANDIDATE for Central Architecture review. Not approved. Not DELIVERY_READY.

Form decision: a **thin new audit item** (option ii), not an amendment of `FALCON-T1` (see Dependencies
and interfaces, "Amend or new"). It composes FALCON-T1 and RECON-F's FALCON-T2/T3 and duplicates none.

## Purpose

Execute CA directive for Lane E: review the delivered FALCON/Graylog event registry and verified running
ingestion; define the minimum remaining HELIOS and TRON event-publication work; keep FALCON outside the
executable trigger-delivery path. The output is evidence and a bounded work list, not an implementation.
The audit proves what runs, states what is registered versus what HELIOS and TRON would need, and
specifies, mechanically, what "FALCON outside the executable path" requires of each publisher, so the
follow-on items (FALCON-T2, FALCON-T3, HELIOS and TRON publisher work) are authored once, against facts.

## Current state

Read 2026-10-15, read-only, unless marked UNVERIFIED. Fabric is memory, not authority.

1. **FALCON is delivered, not missing.** `maff0000/falcon` main `8f218ec` (PR #20, 2026-10-07): PIDs 00 to
   06 delivered, PID-07 Stage 1 discovery merged, PIDs 08, 10 to 15 are design text only (`pids/`).
   Contract stack: `registry/event_family_registry.v1.json` (28 live families, version v1, 5 reserved
   ARES names), `registry/field_registry.v1.json`, `registry/system_component_registry.v1.json`,
   `schemas/falcon-event-envelope`, `schemas/payloads/{ares,helios,hermes,tron}`, fixtures
   `tests/fixtures/{valid,invalid}`, validator `tests/validator/`, CI `.github/workflows/ci.yml` (structure
   and manifest cross-check, internal link check, gitleaks, PID-01 validator suite and fixture report).
2. **Registry versus producers.** `status: "live"` means schema registered, not producer emitting
   (RECON-F section 1). Registered: HERMES 5, ARES 6, HELIOS 5 (`strategy_evaluated`, `strategy_state`,
   `chain_state`, `strategy_trigger`, `health`), TRON 12 (`trigger_observed`, `admission_decision`,
   `order_intent`, `order_submitted`, `order_update`, `fill`, `position_state`, `protection_state`,
   `exit`, `trade_outcome`, `execution_quality`, `health`). Producers emitting: HERMES and ARES
   `market_status.session_state` only (RECON-F 1.1; falcon PID-06 evidence doc section 3). HELIOS and TRON
   emit nothing to FALCON.
3. **HELIOS registry debt is already diagnosed.** `docs/architecture/PID07-HELIOS-STAGE1-DISCOVERY.md`
   section 12 (19-row table), section 15 (single-family candidate) and section 18 (6 blockers): the
   `strategy_evaluated`/`chain_state` split and the 4-value `chain_state` enum do not match real HELIOS
   (one schema, 7-value `state`); `evaluation_id` is a field HELIOS must not mint; `helios.health`
   cannot occur under HELIOS's no-network-sink design; `strategy_trigger` is "confirmed unimplemented".
4. **HELIOS publication is synchronous and blocking today** (same document, section 10): a failing sink
   propagates out of `publish_all()` and the process exits 1; no FALCON path exists; live "prod"/"dev"
   HELIOS replays fixture data (section 14). `PublicationSink` is a small Protocol, so a decoupled sink
   is additive.
5. **The non-blocking publisher pattern is proven for HERMES and ARES only.**
   `docs/operations/FALCON-PID06-RUNTIME-ACCEPTANCE-EVIDENCE.md` section 5: bounded queue, bounded retry
   (2 attempts), 0 scheduler failures, 0 restarts, 1 event lost by accepted best-effort design. Section
   12 states plainly that no durable outbox and no zero-loss guarantee was delivered.
6. **Running ingestion (names, status, labels only; no env, config or secret read).** Containers
   `graylog-falcon` (Up 10 days, healthy), `datanode-falcon` (Up 2 weeks, healthy), `mongodb-falcon`
   (Up 2 weeks, healthy); restart policy `unless-stopped`; compose project `falcon`, config file
   `/srv/falcon/deploy/docker-compose.yml` (container labels). No systemd unit manages GOAL FALCON.
   The host's `falcon-*` systemd units and the older `graylog`, `graylog-mongo`, `graylog-elasticsearch`
   containers belong to the legacy Falcon Ranger and an older Graylog stack and must not be conflated
   (falcon `README.md` identity section; RECON-F 1.1).
7. **Inputs and streams.** Content pack `deploy/content-packs/falcon-pid03-ingestion-v1.json` declares 5
   mTLS inputs (HERMES, ARES, HELIOS, TRON `tron.execution_engine`, TRON `tron.discovery_service`), 7
   streams (HERMES, ARES, HELIOS, HELIOS Trade Suggestions, TRON, Operational Health, Quarantine), one
   pipeline and 30 rules. Compose comment (`deploy/docker-compose.yml` lines 154 to 159): only the HERMES
   and ARES inputs are host-published; HELIOS and TRON inputs are "deliberately NOT published - each needs
   its own separate authorisation". PID-04 runbook records identity-spoof tests 4/4 PASS and correct
   identity 2/2 PASS across the five identities.
8. **Not verifiable without credentials: UNVERIFIED.** Message counts, live input and stream
   configuration, and index sizes need the authenticated Graylog API. No stored credential was read and
   no unauthenticated probe was made. Whether HERMES is publishing in steady state is UNVERIFIED
   (RECON-F 1.1). Volume and retention are unmeasured: `docs/engineering/FALCON-CAPACITY-MODEL.md` is a
   metric list without numbers, retention classes exist (`PERMANENT_TRADING_EVIDENCE`,
   `LONG_RESEARCH_EVIDENCE`, `MEDIUM_OPERATIONAL_EVIDENCE`, `SHORT_HEALTH_TELEMETRY`) but durations
   await PID-10 (`docs/graylog/FALCON-STREAM-INDEX-DESIGN.md`).
9. **Stale "Graylog as trigger transport" language (falcon@8f218ec; all in falcon, none in GOAL).**
   `docs/contracts/FALCON-TRON-TRIGGER-DISCOVERY.md` (all 33 lines);
   `docs/contracts/TRON-FALCON-CONTRACT.md` lines 3 to 30 (discovery, cadence, "no new entries");
   `docs/governance/FALCON-DECISION-REGISTER.md` Decision 16 lines 23 to 24;
   `docs/architecture/01-FALCON-ARCHITECTURE.md` line 45 and lines 169 to 170; `README.md` line 63;
   `pids/PID-05-HERMES-INTEGRATION.md` line 99; `pids/PID-08-HELIOS-SIGNED-TRIGGERS.md` lines 12 and 68;
   `pids/PID-09-TRON-PAPER-INTEGRATION.md` lines 1, 11, 32, 34, 62;
   `docs/operations/FALCON-OBSERVABILITY.md` line 14; `docs/engineering/FALCON-CAPACITY-MODEL.md` line 22;
   `pids/PID-13-OBSERVABILITY-CAPACITY.md` line 24; `docs/engineering/FALCON-PROD-PROMOTION-GATES.md`
   line 8; `docs/graylog/FALCON-STREAM-INDEX-DESIGN.md` lines 14 to 15 (stream label);
   `registry/system_component_registry.v1.json` line 35 (`tron.discovery_service`);
   `registry/field_registry.v1.json` lines 1960 and 1979 ("for TRON discovery").
10. **Existing coverage.** GOAL backlog FALCON-T1 (as re-pointed by the reconciliation PR #5 to depend on
    `GOAL-DCP-001`, excluding `strategy_trigger` and `tron.*`); RECON-F proposals FALCON-T2 to T6 (T2, T3
    minimum; not in the backlog); RECON-H2 F-1 (three inbound models); `wo/GOAL-CONTRACT-TRIGGER`
    `pids/GOAL-TRIGGER-001.md` (TradingTriggerInbox authoritative, deterministic `trigger_id`
    `trg1_` + SHA-256 of the occurrence key, evidence events `trigger_emitted`, `trigger_received`,
    `trigger_disposed`, "no component reads FALCON to decide anything"). The registered
    `helios.strategy_trigger` carries a free-string `trigger_id` and stop/target-style fields that the
    candidate contract removes; `tron.trigger_observed` carries `local_trigger_id` and `source_trigger_id`
    built for the discovery model. Neither fits the deterministic id without a reconciliation.

## Target outcome

At closure, one primary evidence PR in `maff0000/falcon` and, after acceptance, one entry in the GOAL GOLD-MVP evidence index show:

1. what is delivered and running, with the unverifiable parts named;
2. a registered-versus-needed matrix for HELIOS and TRON, family by family, against the evidence
   lifecycle (strategy evaluation, trigger evidence, claim, risk, order, fill, reconcile, outcome);
3. the minimum remaining HELIOS and TRON publication work, each item with owner, schema or registry
   delta, fixture and acceptance, sequenced against FALCON-T1, FALCON-T3 and GOAL-TRIGGER-001;
4. the mechanical definition of "FALCON outside the executable path" as testable publisher requirements;
5. a ruling-ready list of stale documents with exact lines and the amendment route.

## Scope

In scope: read-only audit of falcon main, the running FALCON stack's non-secret observable state, the HELIOS
and TRON publication surfaces (read-only; HELIOS `docs/INTEGRATION.md`, `docs/CONTRACTS.md`, TRON `PID.md`
and `wo/WO-TRON-D1` docs), registry and schema comparison, the stale-language inventory, volume and
retention estimate from design cadence (labelled estimate), and drafting the minimum publication work
list. The only write is the evidence document set in the audit worktree and its PR.

## Non-goals

- No registry or schema edit (FALCON-T1 owns the HELIOS/HERMES/ARES reconciliation; FALCON-T3 the trigger
  and `tron.*` freeze). No amendment of stale documents (listed, routed, not edited).
- No change to HELIOS, TRON, HERMES, ARES, GOAL backlog, `MANIFEST.md`, tools or workflows.
- No trigger contract design (GOAL-TRIGGER-001), no signing design (PID-08), no inbox design (TRON-T4).
- No event injection into the running Graylog or FALCON, no test events, no replay, no new input, no
  port publication, no stream, pipeline, retention or index change, no credential rotation.
- No claim that FALCON is production-ready; PIDs 10 to 15 are not in scope.

## Dependencies and interfaces

**Backlog dependency:** `GOAL-DCP-001` only (CLOSED).

**Amend or new (decision and justification).** Option (ii), a thin new item, because:
(a) FALCON-T1 is a low-risk delivery item whose PO-approved scope after PR #5 is registry reconciliation
for HERMES/ARES/HELIOS and it explicitly excludes `strategy_trigger` and `tron.*`; Lane E must cover
exactly those excluded families, so an amendment would reverse T1's carve-out;
(b) Lane E is research and read-only, T1 writes registry files; mixing them puts a write item behind a
research gate and gives one PID two risk postures;
(c) Lane E needs running-ingestion verification, which T1's inputs do not;
(d) the audit's output (minimum work list) is what FALCON-T2 and FALCON-T3 PIDs should be authored from,
so it must be independent of T1's timing. Not duplicated: GOLD-AUD-E does not reconcile the registry; it
cites T1 as the owner of items 1 to 3 in Deliverables, and defers the `strategy_trigger` and `tron.*`
freeze to FALCON-T3. If CA prefers one item, the fallback is to append Deliverables 1 to 10 as a T1
"verification increment"; the cost is the carve-out reversal and a mixed risk posture.

**Interfaces.** FALCON-T1 (registry reconciliation, soft; the audit reads T1's PID and branch if present
and states which findings T1 absorbs). GOAL-TRIGGER-001 (PID candidate on `wo/GOAL-CONTRACT-TRIGGER` @ `64c843b`; its backlog item is added by GOAL PR #5, OPEN; neither is on `main`): the audit reads its envelope
and evidence events and records the hook below; it does not depend on its approval. E's registry facts are a SOFT input to `GOLD-AUD-C` (ruling 5): E has no dependency on C. HELIOS-T3, TRON-T4
(authors of trigger publication and inbox), HELIOS-T2 (live feed; replay evidence must be labelled).
HELM owns runtime authorisation of any HELIOS or TRON input exposure; that is a later item.

**Trigger-id hook (to be verified, not designed).** Every evidence event concerning a trigger carries
`trigger_id` (the `trg1_` deterministic value) as a registered, searchable, exact-match field,
`tron_instance_id` where the event is TRON-side, and `signing_key_id`; the full signed envelope travels as
producer-owned payload preserved losslessly (Decision 32 pattern). FALCON assigns its own
`falcon_event_id`; it never mints, derives or validates `trigger_id`. Evidence events are idempotent on
`(trigger_id, event_kind, tron_instance_id)` at the reader, and FALCON provides no deduplication
authority (falcon Decision 15, `TRON-FALCON-CONTRACT.md` "Idempotency").

## Safety boundaries

- READ-ONLY on all systems except the audit worktree and its PR. Allowed runtime reads: `docker ps` and
  `docker inspect` of state, restart policy, health and labels; `systemctl list-units`; file reads of
  non-secret repository content.
- Forbidden: `docker exec` into FALCON containers, `docker logs` of FALCON containers, Graylog API calls
  that need stored credentials, reading `deploy/secrets/` or any env file, sending any event (including
  "test" or "heartbeat" events) to any FALCON input, changing any configuration.
- If a check needs authentication the result is recorded UNVERIFIED with the reason. Credential values
  are never read, printed, committed or described.
- GOAL and the evidence PR are public-safe: no IP addresses, account identifiers, credentials, key
  material, host secrets or tenant data. Hostnames are generic ("the delivery host").
- `./tools/secret-scan` clean on both repositories before any push of the evidence PR.

## Deliverables

One evidence PR into `maff0000/falcon` (docs only, under `docs/evidence/GOLD-AUD-E/`, with
`DOCUMENTATION-MANIFEST.json` updated as falcon CI requires), followed after acceptance by one GOAL PR contributing this lane's entry to `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md` (owned by `GOLD-MVP-001`; one lane per PR). Ten deliverable parts
(EP-1 to EP-10; their mapping to CA's evidence numbering follows the table below the parts list):

| # | Evidence item | Content |
|---|---|---|
| EP-1 | Delivered inventory | PIDs, PRs, merged SHAs, what is delivered versus design-only, with the PID-05 stale status header noted |
| EP-2 | Running ingestion record | Container names, status, restart policy, health, labels; systemd finding; legacy-stack exclusion; UNVERIFIED list with reason |
| EP-3 | Registry matrix | All 28 families by producer: registered, schema, fixture, emitting (yes/no), reconciliation owner (T1, T3, new) |
| EP-4 | HELIOS needs | Families HELIOS must emit versus registered; mismatches from PID07 sections 12 and 18; `helios.health` ruling options |
| EP-5 | TRON needs | Lifecycle gap analysis (below); mapping to registered `tron.*`; missing families |
| EP-6 | Ingestion contract | mTLS per-producer identity binding, five identities, spoof results, publication gating of HELIOS and TRON inputs, authorisation path |
| EP-7 | Volume and retention | Cadence-derived events per day per producer (estimate, labelled), retention class per family, UNMEASURED items |
| EP-8 | Trigger-id hook | Field-level mapping from GOAL-TRIGGER-001 to registered fields; conflicts with `helios.strategy_trigger` and `tron.trigger_observed` |
| EP-9 | Outside-the-path proof requirements | Mechanical publisher requirements (below) and a test per requirement |
| EP-10 | Stale-language inventory | The file and line list in Current state 9, verdict per row, amendment route (falcon PID/amendment process) |

**Mapping of the deliverable parts to CA's evidence numbering.**

CA's ten mandatory evidence items, in CA's numbering (the numbering is CA's and is not to be changed by a lane): (1) PID/WO identifier and exact audited scope; (2) source repositories, revisions and relevant documentation references; (3) existing implementation: proven, partially proven, unverified or missing; (4) actual versus expected contract comparison; (5) tests, fixtures and evidence references; (6) specific defects and compatibility gaps; (7) reusable code and documentation; (8) minimum recommended implementation changes; (9) safety and deployment constraints; (10) independent audit verdict and any unresolved findings.

| CA # | CA evidence item | This audit puts it in | Proof method |
|---|---|---|---|
| 1 | PID/WO identifier and exact audited scope | Evidence PR header: quoted scope; EP-1 delivered inventory | Quote equals approved PID |
| 2 | Source repositories, revisions and documentation references | Audited falcon SHA and every cited path and commit (EP-1, EP-3); stale-document list at the audited SHA (EP-10) | `grep -n` re-run at the audited SHA matches the line numbers |
| 3 | Existing implementation: proven, partially proven, unverified or missing | EP-1, EP-2 (running ingestion), EP-3 (28-family registry matrix), EP-4 / EP-5 (HELIOS and TRON versus registered); UNVERIFIED table with reasons | Matrix regenerated by a script from the registry; diff empty |
| 4 | Actual versus expected contract comparison | EP-4, EP-5, EP-6 (ingestion contract), EP-8 (trigger-id hook mapping from `GOAL-TRIGGER-001` to registered fields; conflicts with `helios.strategy_trigger` and `tron.trigger_observed`) | Field-level mapping, no narrative cells |
| 5 | Tests, fixtures and evidence references | EP-9 outside-the-path requirements, each with a test; regeneration script; fixtures named in the work list; audit log of runtime commands | Each requirement has a test; command log within allowed list |
| 6 | Specific defects and compatibility gaps | Conflicts and registry debt in EP-3, EP-4, EP-5, EP-8; stale Graylog-as-transport language (EP-10) | Each gap with owner (T1, T3, new) |
| 7 | Reusable code and documentation | Reusable: registry, fixtures, validator, non-blocking publisher pattern of PID-06 for HERMES and ARES (EP-1, EP-9) | Path and commit cited |
| 8 | Minimum recommended implementation changes | Minimum publication work list P-H1..P-H4, P-T1, P-T2, P-F1, P-F2 with owner, delta, fixture, acceptance and sequencing (EP-4, EP-5, EP-7) | No row makes FALCON a precondition of a HELIOS or TRON decision |
| 9 | Safety and deployment constraints | Safety: read-only runtime reads only, no event injection, no credential read; EP-6 authorisation path; EP-7 volume and retention (estimate labelled) | `git diff --stat` docs only; secret-scan clean |
| 10 | Independent audit verdict and unresolved findings | Independent auditor (AUD-1) verdict file with unresolved findings | falcon CI green; fresh auditor GREEN with exact SHAs |

**TRON lifecycle gap analysis (EP-5, audit to confirm).** CA lifecycle: claim, risk, order, fill, reconcile.
Registered closest matches: claim to `tron.trigger_observed` (observed, not claimed: no claim or
disposition family, no inbox receipt); risk to `tron.admission_decision`; order to `order_intent`,
`order_submitted`, `order_update`; fill to `fill`, `position_state`, `protection_state`, `exit`,
`trade_outcome`; reconcile: no family. Candidate additions for FALCON-T3 to rule on: trigger disposition
(`trigger_received`, `trigger_disposed` with the closed outcome vocabulary of GOAL-TRIGGER-001) and broker
reconciliation result. Decision: extend by registered type within an existing family, or add families.

**Minimum remaining publication work (EP-4/EP-5 output; owner is the component repository's persona, FALCON
side by Rogue):**

| ID | Work | Owner | Schema / registry delta | Fixture | Sequencing |
|---|---|---|---|---|---|
| P-H1 | Non-blocking evidence sink: bounded queue, bounded retry, drop-on-full with counter, never raises into the evaluation loop | HELIOS | none | fault-injection test: sink raising, blocked, slow | independent; first |
| P-H2 | Publish `StrategyStateEnvelope` as one family, envelope as lossless payload, replay/fixture-feed events labelled so they are excluded from evidence | HELIOS + FALCON | FALCON-T1 collapses the three-way split | real envelope fixtures; replay-marked fixture | after FALCON-T1 |
| P-H3 | Rule on `helios.health` (retire, or local file only) and on `evaluation_id` | FALCON architect | T1 registry delta | none | with T1 |
| P-H4 | Trigger evidence: after the durable publisher outbox commit, emit `trigger_emitted` with the signed envelope | publisher (HELIOS-T3 decision D-10) | FALCON-T3 reshapes `helios.strategy_trigger` to the frozen contract | signed vector fixtures from GOAL-TRIGGER-001 | after GOAL-TRIGGER-001 freeze |
| P-T1 | Evidence emitter: durable local journal first, then bounded asynchronous emission through a local spool; nothing in the decision path reads FALCON | TRON | none | outage and recovery test as PID-06 section 5 | with TRON-T1/T4 |
| P-T2 | Emit the lifecycle families: trigger received and disposed, risk, order, fill, reconcile, outcome, each carrying `trigger_id` and `tron_instance_id` | TRON | FALCON-T3: missing disposition and reconcile types; replace `local_trigger_id` semantics | one fixture per type | after GOAL-TRIGGER-001 and TRON-T1 |
| P-F1 | Retire the discovery model in falcon documents (Current state 9); one supersession decision (new Decision, not an edit of Decision 16) | FALCON (falcon amendment route) | none | link-check and manifest pass | docs-only, may run first |
| P-F2 | Authorise and expose HELIOS and TRON inputs one at a time, with PID-06-style acceptance each | HELM + Rogue | none | mTLS accept and spoof-reject records | after P-H1 or P-T1 per input |

## Acceptance

Mechanical; every row passes or the audit is not accepted.

1. EP-1 to EP-10 exist in the evidence PR, each with at least one cited repository path and commit SHA.
2. The registry matrix in EP-3 has exactly 28 rows and is reproducible: a script in the PR regenerates it
   from `registry/event_family_registry.v1.json` and a diff against the committed table is empty.
3. Every claim in EP-2 carries its command (read-only) and output excerpt without secrets; every
   unavailable fact appears in an UNVERIFIED table with the reason.
4. The stale inventory lists at least the Current state 9 rows, re-verified by `grep -n` at the audited
   SHA, line numbers matching.
5. The minimum work table has, per row: owner, delta, fixture, acceptance test and sequencing, and no row
   makes FALCON a precondition of a HELIOS or TRON decision.
6. EP-9 states these requirements and a test for each: publication is asynchronous and non-blocking; the
   queue is bounded and drop-on-full is counted; FALCON unreachable, slow, rejecting or full leaves
   evaluation, claim, risk, order and reconcile outcomes byte-identical and timing within a stated bound;
   no publisher or TRON reads FALCON to decide, validate, dedupe or authorise; the durable record of a
   trigger is the publisher outbox and TRON inbox and journal, with FALCON a best-effort copy and a gap
   after outage backfilled from those journals, never the reverse; emission happens after the local
   durable commit; FALCON failure never changes a terminal outcome.
7. `./tools/secret-scan` passes on the falcon evidence branch and falcon CI is green on the evidence PR (structure, manifest,
   link check, gitleaks, validator suite); `./tools/goal-validate` and `./tools/secret-scan` pass on the later GOAL index-entry PR.
8. A negative check: `git diff --stat` of the evidence PR shows docs only; zero lines in `registry/`,
   `schemas/`, `deploy/`, `tests/`.
9. Audit log lists every runtime command run; none is outside the allowed list in Safety boundaries.

## Stop conditions

- Any check would need a stored credential, an event sent to FALCON, or a configuration change: stop,
  record UNVERIFIED, continue the rest.
- Evidence suggests FALCON is already read by a HELIOS or TRON decision path: stop and escalate to PO.
- A secret, IP address or account identifier appears in any draft evidence: stop, redact, re-run
  `./tools/secret-scan`.
- falcon main moves from `8f218ec` during the audit: re-base findings or pin the audited SHA and say so.
- GOAL-TRIGGER-001 changes the trigger id or evidence-event names after the hook is recorded: stop EP-8 and
  re-read.

## Open decisions

| ID | Decision | Owner | Blocks |
|----|----------|-------|--------|
| D-1 | Amend FALCON-T1 or new item (this PID recommends new) | PO | approval |
| D-2 | Confirm FALCON is evidence-only and never gates entries (reverses Decision 16 coupling; RECON-F B2) | PO (CA) | approval |
| D-3 | Retired: CA's numbered evidence list has been supplied and applied (see Deliverables); no decision remains | none | none |
| D-4 | Authenticated Graylog read access for the audit (read-only account, or HELM-run read-only export) to close the UNVERIFIED rows | Matt (credentials) / HELM | later (audit may close with UNVERIFIED) |
| D-5 | Durable backfill after FALCON outage: accepted loss (PID-06 precedent) or gap-fill from publisher and TRON journals | PO | later (FALCON-T2/T3) |
| D-6 | Where trigger evidence emission lives (publisher component versus HELIOS) | PO | later (HELIOS-T3 PID; GOAL-TRIGGER-001 D-10) |
| D-7 | Add FALCON-T2 and FALCON-T3 to the backlog (RECON-F proposals), with this audit's work list as their input | PO | later |
| D-8 | Retire or rename `tron.discovery_service` component and its input (PID-01 amendment authority) | PO / falcon architect | later |
| D-9 | Retired by programme-controller rulings 1 to 3: evidence PR is primary in falcon, `docs/evidence/GOLD-AUD-E/` | none | none |

## Evidence

- GOAL base `1739e74`: `backlog/backlog.yaml` (FALCON-T1), `backlog/SCHEMA.md`, `pids/GOAL-DCP-001.md`.
- GOAL reconciliation branch `wo/GOAL-RECON-PR` `e2671ff` (FALCON-T1 re-pointed; trigger and `tron.*` excluded).
- `wo/GOAL-CONTRACT-TRIGGER` `64c843b`: `pids/GOAL-TRIGGER-001.md`.
- RECON-F (`GOAL-RECON-F-falcon`, `audits/2026-10-14/reconciliation/RECON-F.md`) and RECON-H2.
- falcon main `8f218ec`: registry, schemas, `deploy/docker-compose.yml`, `deploy/content-packs/`, PID-04 runbook,
  PID-06 runtime evidence, PID07 Stage 1 discovery, contracts, governance, CI file.
- Runtime reads 2026-10-15: `docker ps`, `docker inspect` (state, restart policy, health, labels),
  `systemctl list-units`. No logs, exec, API or secret access.
- Not read: Graylog API, FALCON secrets, HELIOS and TRON source in full, CA-private material.

## Evidence PR checklist

- [ ] Branch `wo/GOLD-AUD-E-evidence` in falcon (`wo/GOAL-GOLD-AUD-E` is the PID draft branch, not evidence), base audited SHA stated in the PR body
- [ ] `docs/evidence/GOLD-AUD-E/` contains EP-1 to EP-10 and the regeneration script; CA evidence items 1 to 10 present in CA numbering (table in Deliverables)
- [ ] `DOCUMENTATION-MANIFEST.json` updated; internal links resolve
- [ ] UNVERIFIED table present with reasons; no credential value anywhere
- [ ] No IPs, accounts, credentials or key material (secret-scan and manual read)
- [ ] `git diff --stat` shows docs only
- [ ] falcon CI green; `./tools/secret-scan` green on the falcon branch
- [ ] After acceptance: one GOAL PR adding E's entry (PR link, audited SHAs) to `EVIDENCE-INDEX.md`, owned by GOLD-MVP-001; `./tools/goal-validate` and `./tools/secret-scan` green there
- [ ] No approval recorded by the author; PO/CA review requested

## Approval

PENDING. No approval has been recorded for this PID candidate. Approval is recorded here by Central Architecture/PO only.

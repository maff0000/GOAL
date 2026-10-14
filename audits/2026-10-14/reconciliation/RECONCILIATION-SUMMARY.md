# Reconciliation summary 2026-10-14 — programme backlog reconciliation

**Work order:** `GOAL-RECON-PR`. **Baseline:** `main` at `1739e74`. **Date:** 2026-10-14.
**Authority:** Central Architecture adjudication of the programme reconciliation, relayed by the delivery train controller.
**Nature:** a forward-only governed change to `backlog/backlog.yaml` plus audit records. No PID is created or edited, no `pid_path` is set, nothing is moved to `DELIVERY_READY`, and no tool is changed.

## 1. Evidence relied on

All evidence is read-only analyst output on branches of this repository; it is cited, not copied.

| record | branch | head |
|---|---|---|
| RECON-F (FALCON, trigger path) | `wo/GOAL-RECON-F-falcon` | `7609761` |
| RECON-G (NEO, CER, SKEPTIC) | `wo/GOAL-RECON-G-neo` | `9bd67f3` |
| RECON-H1 (data chain, contract, research) | `wo/GOAL-RECON-H1-datachain` | `142cc55` |
| RECON-H2 (trade chain) | `wo/GOAL-RECON-H2-tradechain` | `2780076` |
| PID wave 1 group A (ops safety) | `wo/GOAL-PID-WAVE1-A-ops-safety` | `572b3e3` |
| PID wave 1 group B (research) | `wo/GOAL-PID-WAVE1-B-research` | `6990181` |
| PID wave 1 group C (execution) | `wo/GOAL-PID-WAVE1-C-execution` | `3f14c5e` |
| PID wave 1 group D (risk events) | `wo/GOAL-PID-WAVE1-D-risk-events` | `27b07d9` |
| PID wave 1 group E (HELIOS) | `wo/GOAL-PID-WAVE1-E-helios` | `1e7f033` |

Every analyst proposal was marked PO-decision-required. Only the changes in section 2 were adjudicated for application; everything else is listed in section 6 and was not applied.

## 2. Patch list applied

Class: **factual** corrects a statement that was wrong; **prerequisite** changes a genuine engineering dependency; **sequencing** changes an edge or state that expressed architecture preparation or ordering rather than an engineering need; **new** adds an item.

| # | item | field | from | to | class | reason (evidence) |
|---|---|---|---|---|---|---|
| 1 | ARES-CUR-001, ARES-RISK-001, ARES-PIT-001 | target_repository | `maff0000/ARES` | `maff0000/trading-ares` | factual | RECON-H1 F-4; `maff0000/ARES` does not resolve. |
| 2 | NEO-R1 | target_repository | `maff0000/NEO` | `maff0000/neo` | factual | RECON-G F3. |
| 3 | NEO-R1 | depends_on | CER-R1 | GOAL-DCP-001 | sequencing | RECON-G 4.1: CER v1.0.0 is delivered; neither CER-R1 nor DARWIN-R2 is needed to author the PID or for a first increment. |
| 4 | CER-R1 | depends_on | DARWIN-R2 | GOAL-DCP-001 | sequencing | RECON-G 4.2: CER does not need DARWIN; the DARWIN-to-CER mapping is a separate deferred candidate. |
| 5 | CER-R1 | title | Research evidence + EdgeProfileVersion | EdgeProfileVersion and contract v1.1 on delivered CER v1.0.0 | factual | RECON-G F4: research evidence classes already exist in CER v1. |
| 6 | FALCON-T1 | depends_on | HELIOS-T3 | GOAL-DCP-001 | sequencing | RECON-F X1: inputs are the merged HELIOS v1 and FALCON's own stage-1 discovery. |
| 7 | FALCON-T1 | title | Reconcile event registry | Reconcile FALCON event registry with delivered HERMES/ARES/HELIOS reality (excludes strategy_trigger and tron.* families) | factual | RECON-F P2: records that FALCON is delivered and what is excluded. |
| 8 | GOAL-TRIGGER-001 | (new item) | n/a | added, ARCHITECTURE_REQUIRED | new | RECON-F H1 and RECON-H2 F-1; see section 4. |
| 9 | HELIOS-T3 | depends_on | HELIOS-T2 | HELIOS-T2, GOAL-TRIGGER-001 | prerequisite | single owner of the trigger contract. |
| 10 | TRON-T4 | depends_on | TRON-T1, HELIOS-T3 | TRON-T1, GOAL-TRIGGER-001 | sequencing | RECON-F X2, RECON-H2 P5: the inbox needs the frozen contract and signed fixtures, not a running HELIOS signer. HELIOS-T3 stays required at PAPER-E2E-001. |
| 11 | HELIOS-T1 | state | ARCHITECTURE_REQUIRED | PID_DRAFT | sequencing | group E report: architecture settled by evidence; the engineering dependency GOAL-CORE-001 is retained. pid_path stays null. |
| 12 | HELIOS-T2 | depends_on | HELIOS-T1, HERMES-FACT-001, ARES-RISK-001 | HELIOS-T1, HERMES-FACT-001 | prerequisite | RECON-H2 F-2: HELIOS is execution-blind and its PID forbids absorbing ARES news/risk; event risk enters through TRON. |
| 13 | HELIOS-T2 | title | Live HERMES/ARES adapters | Live HERMES adapter | factual | follows from 12. |
| 14 | TRON-D1-RATIFY | (new item) | n/a | added, PID_DRAFT, matt_gate true | new | RECON-H2 F-4; see section 4. |
| 15 | TRON-T1 | depends_on | GOAL-DCP-001 | GOAL-DCP-001, TRON-D1-RATIFY | prerequisite | explicit pre-implementation ratification gate. |
| 16 | TRON-T1 | title | Core ledger/reconciliation + Trading Postgres | Core execution journal/reconciliation + Trading Postgres | factual | terminology: the broker is the system of record, TRON keeps an execution journal (RECON-H2 F-4, RECON-G F9). |
| 17 | TRON-T2 | depends_on | TRON-T1, MT5-GW-003, MT5-GW-004 | TRON-T1, MT5-GW-004 | factual | RECON-H2 P1: MT5-GW-003 is already required transitively via MT5-GW-004; prerequisite unchanged. |
| 18 | GOAL-REF-001 | depends_on | GOAL-CORE-001 | GOAL-CONTRACT-001 | sequencing | RECON-H1 2.4: an independent reference derived from the code it checks shares its bugs. |
| 19 | HSA-C1 | (new item) | n/a | added, ARCHITECTURE_REQUIRED | new | RECON-H1 2.7; see section 4. |
| 20 | PAPER-E2E-001 | title | Full paper lane end-to-end proof | Full paper lane end-to-end proof on Vantage DEMO (not satisfiable by simulation) | factual | RECON-H2 F-5 and ADR-MT5-001 "Required proof before PAPER". |
| 21 | SKEPTIC-T1, LEAN-P1 | state | ARCHITECTURE_REQUIRED | ARCHITECTURE_REQUIRED (confirmed, note added) | factual | neither is defined anywhere (RECON-G 1.3, RECON-H1 section 1); no definition is invented. |
| 22 | (annotated only) | YAML comment and architecture_refs | n/a | delivered-status notes on ARES-CUR-001, NEO-R1, CER-R1, FALCON-T1, DARWIN-R2, DARWIN-R3, HELIOS-T1..T3, TRON-T1..T5, PAPER-E2E-001 | factual | the schema has no notes field; see section 7. |

`architecture_refs` of every touched item gains this record; `PAPER-E2E-001` also gains `ADR-MT5-001`, and `ARES-CUR-001` and `NEO-R1` also gain the correction record.

## 3. Ownership and terminology (settled by this change)

- **HELIOS is execution-blind.** It evaluates strategy state deterministically from facts. It carries no sizing, risk, order or broker vocabulary. Whether a separate publisher or HELIOS itself signs a trigger is a decision owned by `GOAL-TRIGGER-001`; if the signer lives inside HELIOS it must not import sizing or execution concepts.
- **TRON owns sizing, hard risk, kill and execution.** TRON verifies signature, validity window and freshness itself, dedupes durably, and records a terminal outcome.
- **ARES event risk enters through TRON** (`TRON-T3`), as a later additive increment. There is deliberately no `ARES-RISK-001` edge into HELIOS or at P0 into `TRON-T3`.
- **FALCON is an evidence mirror**, never the trigger transport and never an execution gate. A FALCON outage must not block an entry.
- **NEO never makes discretionary live trade, sizing or risk actions.** Legacy practice-account execution exists in NEO code and needs an explicit disposition (a PO ruling), not extension.
- **Terminology:** TRON keeps an *execution journal*; it is not a ledger.

## 4. New-item test and the items added

An item may be added only if it has a distinct owner, a distinct deliverable, distinct acceptance, and justified dependencies.

| item | owner | deliverable | acceptance | dependencies and why |
|---|---|---|---|---|
| GOAL-TRIGGER-001 | PO/CA, repository `maff0000/GOAL` | the contract of record: trigger identity, signed canonical form, validity window, dedupe key, terminal outcomes, delivery semantics | the contract is frozen and conformance fixtures exist for both HELIOS-T3 and TRON-T4 to build against | `GOAL-DCP-001` only, so HELIOS-T3 and TRON-T4 PIDs can be authored in parallel against a declared interface. Identity fields will reuse `goal.strategy/v1` vocabulary by reference; RECON-H2 would add `GOAL-CONTRACT-001`, which is a deferred ordering choice. Owns no implementation. |
| TRON-D1-RATIFY | TRON repository, Matt-gated | independent audit and merge of the existing D1 design baseline; disposition of open decisions (runtime language, trigger transport, quantity ownership, journal versus Postgres) | audit green, merged to the default branch, decisions closed or explicitly deferred | `GOAL-DCP-001`. It is itself the prerequisite of `TRON-T1`. |
| HSA-C1 | HSA repository | HSA emits `goal.strategy/v1` and names facts from the `goal.market-fact/v1` catalogue | HSA output passes the contract conformance fixtures | `GOAL-CONTRACT-001` (the schema it adopts) and `HERMES-FACT-001` (the catalogue it names). Does not include the HSA-DARWIN-CER authoring loop. |

## 5. Revised dependency graph: engineering prerequisite versus architecture preparation

The schema has one `depends_on` list. After this change it is used for **genuine engineering prerequisites** wherever the evidence allowed. Architecture preparation (authoring a PID against a declared interface) is expressed by the item's state (`PID_DRAFT`), never by an extra field. `E` = genuine engineering prerequisite. `E*` = genuine for dispatch and build, but the PID may be authored earlier against a declared interface. `R` = retained conservatively; the analysts judged it artificial or doubtful but the change needs a PO ruling.

| item | depends_on after change | classification |
|---|---|---|
| GOAL-DCP-002/003/004 | DCP-001 / DCP-002 / DCP-002 | E; not on the PAPER path |
| OPS-SAFE-001..003, OPS-LEGACY-001, OPS-CRED-001 | GOAL-DCP-001 | E; gate LIVE only |
| HERMES-CUR-001 | GOAL-DCP-001 | E |
| HERMES-FACT-001 | HERMES-CUR-001 | E* (R for authoring; optional relaxation deferred) |
| HERMES-GR-001 | HERMES-FACT-001 | E (fact-level replay) |
| ARES-CUR-001 | GOAL-DCP-001 | E |
| ARES-RISK-001 | ARES-CUR-001 | E* |
| ARES-PIT-001 | ARES-RISK-001 | R (analysts: interface-only link) |
| GOAL-CONTRACT-001 | GOAL-DCP-001 | E |
| GOAL-CORE-001 | GOAL-CONTRACT-001 | E* (frozen draft is enough for build) |
| GOAL-REF-001 | GOAL-CONTRACT-001 | E (changed: independence) |
| DARWIN-R1 | GOAL-DCP-001 | E |
| DARWIN-R2 | GOAL-CONTRACT-001, DARWIN-R1 | E for CONTRACT; R for R1 (deploy-time only) |
| DARWIN-R3 | GOAL-CORE-001, DARWIN-R1 | R (scope stale) |
| LEAN-P1 | DARWIN-R2, GOAL-CORE-001 | R (item undefined) |
| HSA-C1 | GOAL-CONTRACT-001, HERMES-FACT-001 | E |
| CER-R1 | GOAL-DCP-001 | E (changed) |
| NEO-R1 | GOAL-DCP-001 | E (changed); disposition rulings gate its PID_DRAFT |
| GOAL-TRIGGER-001 | GOAL-DCP-001 | E |
| HELIOS-T1 | GOAL-CORE-001 | E* (PID_DRAFT: architecture prepared against a declared interface) |
| HELIOS-T2 | HELIOS-T1, HERMES-FACT-001 | E (ARES edge dropped) |
| HELIOS-T3 | HELIOS-T2, GOAL-TRIGGER-001 | E for the contract; HELIOS-T2 is R (analyst: signing needs only HELIOS output) |
| FALCON-T1 | GOAL-DCP-001 | E (changed) |
| MT5-GW-001 | GOAL-DCP-001 | E |
| MT5-GW-002 | MT5-GW-001 | E* |
| MT5-GW-003 | MT5-GW-001, MT5-GW-002 | R for authoring; E for image integration (split deferred) |
| MT5-GW-004 | MT5-GW-003 | E |
| TRON-D1-RATIFY | GOAL-DCP-001 | E |
| TRON-T1 | GOAL-DCP-001, TRON-D1-RATIFY | E (gate) |
| TRON-T2 | TRON-T1, MT5-GW-004 | E (Vantage adapter needs the DEMO proof) |
| TRON-T3 | TRON-T1 | E |
| TRON-T4 | TRON-T1, GOAL-TRIGGER-001 | E (changed) |
| TRON-T5 | TRON-T3, CER-R1 | E for edge-profile binding; fixed-size split deferred |
| SKEPTIC-T1 | TRON-T1 | R (item undefined) |
| PAPER-E2E-001 | HELIOS-T3, TRON-T2, TRON-T3, TRON-T4 | E |
| LIVE-GATE-001 | PAPER-E2E-001 and the five OPS items | E |

Independent of the whole PAPER critical path: GOAL-DCP-002/003/004, HERMES-GR-001, ARES-PIT-001, DARWIN-R1..R3, LEAN-P1, CER-R1, NEO-R1, SKEPTIC-T1, HSA-C1, TRON-T5, GOAL-REF-001 (as a predecessor), and all OPS items (which gate LIVE only).

## 6. Deferred candidates (not added) and edge changes not applied

No `pid_depends_on` field was added; CA forbade it.

| candidate | reason not added |
|---|---|
| PAPER-SIM-001 | Fails the justified-dependencies test. Its deliverable needs a simulated execution adapter and a fixed-size sizing policy that no item owns; providing them means splitting TRON-T2 and TRON-T5, outside the adjudicated scope. Whether a simulated lane may exist at all rests on open decisions. State `PAPER` is protected without it (section 8). |
| TRON-T2A, TRON-T5A, MT5-GW-003A, PAPER-DEPLOY-001, TRIGGER-PUBLISHER-001, MT5-GW-005 | Splits or additions that restate the scope of existing items and depend on open PO decisions (typed-service transport, quantity ownership, journal versus Postgres, who signs). |
| NEO-R0 | Its deliverable depends on the unresolved ruling on NEO's legacy executor and needs host operations authority and sizing before it can be defined. |
| NEO-R2, CER-R1a, CER-R1b, CER-R2, CER-R0 | Premature or dependent on EdgeProfileVersion, which is undefined; NEO-R2 builds on an unapproved NEO-R1 PID. |
| TRON-OBS-001 | Depends on TRON runtime events that do not exist yet. |
| HSA-C2 | The HSA-DARWIN-CER authoring loop overlaps the DARWIN workshop and specification work, and that overlap is unresolved. |
| GOAL-STRAT-ADR-001 | A decision record, not a work item; the strategy-representation ruling is a PO decision. |
| GOAL-CONF-001 | Duplicates scope of GOAL-REF-001 and HELIOS-T1 golden comparison; mechanism choice is a PO decision. |
| GOAL-DIKE-001 | DIKE ownership and meaning are unresolved between DARWIN research and TRON enforcement. |
| HERMES-VENUE-001 | Whether a work item or an accepted tolerance is unresolved. |
| DARWIN-RM-001 | Whether GOAL tracks DARWIN-internal PIDs is unresolved. |
| PLATFORM-RT-001 | Overlaps other groups; flagged only. |
| FALCON-T2..T6 | A PO-chosen subset was required; FALCON-T3 and T4 need frozen contracts that do not exist; T5 and T6 are off the PAPER path. |

Edge and state changes proposed by analysts and **not** applied (each needs a PO ruling): HERMES-FACT-001, GOAL-CORE-001 and ARES-RISK-001 to `PID_DRAFT`; FALCON-T1 and NEO-R1 to `PID_DRAFT`; HERMES-FACT-001 to depend on `GOAL-DCP-001`; ARES-PIT-001 to depend on `ARES-CUR-001`; DARWIN-R2 and DARWIN-R3 to drop DARWIN-R1 and DARWIN-R2 to be retitled; HELIOS-T3 to drop HELIOS-T2; SKEPTIC-T1 re-pointed; LIVE-GATE-001 to add TRON-T5; TRON-T3 renamed; an `ARES-PIT-001` Matt gate if a paid provider is chosen.

## 7. What the schema could not express

- No notes field: delivered-status and ownership notes are YAML comments (not machine-readable, not rendered in `MASTER-BACKLOG.md`) and `architecture_refs` pointers to this record.
- No authoring-versus-dispatch dependency: `./tools/goal-ready --pid-wave` lists a `PID_DRAFT` item only when every dependency is already in an accepted terminal state. `HELIOS-T1` (open dependency `GOAL-CORE-001`) and `TRON-T1` (open dependency `TRON-D1-RATIFY`) are in `PID_DRAFT` but are therefore absent from the advisory wave list; this follows from the CA instructions and was not worked around.
- No way to forbid mechanically that a simulated proof moves `PAPER-E2E-001` to `PAPER`; protection is by title, notes and the `ADR-MT5-001` reference only.
- No draft-freeze versus final-freeze for `GOAL-CONTRACT-001`.

## 8. Simulation versus Vantage DEMO acceptance

The state `PAPER` is reserved for the Vantage DEMO lane. `ADR-MT5-001` lists the proof required before `PAPER` (reproducible image, account identity, reads, market and pending orders, cancel, SL/TP, full and partial close, reconnect and reconciliation, idempotent execution identity, broker-side protection). A simulated execution adapter can prove pipeline logic (intake, idempotency, sizing, checks, journal, kill, reconciliation) but cannot satisfy that list. `PAPER-E2E-001` therefore keeps its dependence on `TRON-T2` (the Vantage adapter, which needs `MT5-GW-004`), carries the `ADR-MT5-001` reference and an explicit title. Any future simulation milestone is an internal milestone that never carries `PAPER`.

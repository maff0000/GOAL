# TRON-T1 — Execution journal, reconciliation and the minimum protected-order/risk integration boundary (engineering package 3)

**Lane:** trading  
**Target repository:** `maff0000/tron`  
**Priority:** P0  
**Risk:** High  
**Matt gate:** No (parameter values and any DEMO order activity are separately Matt-gated; see Open decisions)  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  

**Header notes:** DRAFT CANDIDATE, engineering package 3, prepared under the Central Architecture drafting-only authority of 17 October 2026. `TRON-T1` already exists in `backlog/backlog.yaml` (state `PID_DRAFT`, `pid_path: null`, depends on `GOAL-DCP-001` and `TRON-D1-RATIFY`). This file is NOT linked to that item: the backlog is not amended here, no `pid_path` is set, the item count does not change and nothing is registered or approved. Any backlog change (setting `pid_path`, state, dependencies) is a separate governed change after approval. No implementation, no contract freeze, no broker access and no numeric policy value is authorised or decided by this draft. The registered backlog title of `TRON-T1` is "Core execution journal/reconciliation + Trading Postgres"; this draft narrows and defers that title because the durable-store choice is an owner decision of D1 ratification and is not made here. A title change would be a separate governed change.

## Status

DRAFT CANDIDATE. Approval PENDING (see Approval). Not `DELIVERY_READY`; cannot become so while `TRON-D1-RATIFY` is open.

## Purpose

Define one bounded, credential-free package that gives TRON a durable execution journal, an idempotent execution identity, claim and disposition facts, a reconciliation engine against broker truth, an event outbox, and a broker-neutral adapter interface with a deterministic simulated adapter. In the same package, fix the integration boundaries between this journal and the approved `TRON-T3A` risk baseline, so that the minimum protected-order path has exactly one admission path before any submit: journal first, gates second, one kill state read, fail closed.

This package exists so the later items (`TRON-T3A`, `TRON-T3`, `TRON-T2`, `TRON-T4`, `PAPER-E2E-001`, `GOLD-MVP-001`) are built on one agreed foundation rather than each inventing its own state.

## Current state (evidence-derived)

Source: the `GOLD-AUD-D` evidence published in the GOAL lane D directory (the lane itself remains in `PO_ACCEPTANCE`, not `MERGED`; see the GOAL #30 amendment, which keeps acceptance criterion 7 and criterion 12 as amended open). Class vocabulary as in that lane: PROVEN, PARTIAL, UNVERIFIED, MISSING.

- TRON has no runtime code. Its contract baseline (D1) is design and schema only; its tests check document consistency, not behaviour (gap rows G-07, G-33, G-34 MISSING).
- Journal-before-submit, idempotent intent identity, claim and disposition facts, an in-memory journal port, a durable store, a reconciliation engine, restart reconcile-before-write, a broker-neutral adapter interface, a simulated adapter and a conformance suite are all MISSING or PARTIAL (G-07 to G-11, G-20 to G-22, G-33 to G-35).
- The D1 check set lacks risk gates in the minimum set; the stage-0 design carries more than one candidate stop mechanism (finding F-D-14), which `TRON-T3A` resolves by owning one kill state.
- The durable-store choice is an owner decision of D1 ratification, not decided here.

## Boundaries between the items

| Item | Owns | Does not own | Relation to this package |
|---|---|---|---|
| `TRON-T1` (this package) | Execution journal port and implementations; execution identity; claim/disposition facts; reconciliation engine and integrity states; event outbox; broker-neutral adapter interface; simulated adapter with fault injection; adapter conformance suite; the single pre-submit admission sequence (the hook, not the gates' content) | Sizing, limits, the kill state record and its setter, protective-level policy | Foundation |
| `TRON-T3A` (scope approved 17 Oct 2026) | Minimum fixed DEMO sizing; one-position and open-position limits; daily loss and trade-count guards; ONE kill state with its single setter and clearer; protected-order policy and the fail-closed protection gate | Journal, reconciliation, adapter, broker connectivity | Depends on this package; plugs its gates into the admission hook; reads counters derived from the journal |
| `TRON-T3` | Extension of the T3A baseline: exposure, drawdown, consecutive-loss, risk-lock automation, further promoted checks | A second kill state or second gate path | Extends T3A; must pass the same one-writer test |
| `TRON-T5` | Sizing policy and frozen edge-profile binding | Anything on the minimum path | Later; unchanged |
| `TRON-T2` | Vantage adapter implementing the interface, first against the gateway's fake backend, then DEMO reads | The interface itself | Consumes this package's interface and conformance suite |
| `TRON-T4` | Inbox intake against signed fixtures, protection derivation owner for trigger-borne levels | Journal internals | Writes claims through this package's journal port; trigger contract authority stays with `GOAL-TRIGGER-001` (not restated here) |

## Risk-admission architecture (the integration boundary)

There is one admission path for any request that would increase risk. In order, all before any adapter call:

1. **Identity.** A deterministic execution identity is derived from the source reference, broker context, intent kind and leg. The client order id sent to a gateway is derived from it and fixed before the journal write.
2. **Claim.** A claim fact is recorded when TRON takes a trigger; replay of the same source reference yields no second intent; each claim ends in exactly one immutable terminal disposition.
3. **Admission gates.** The `TRON-T3A` hard gates run: configured sizing present, one position per instrument, open-position limit, daily loss and trade-count guards, the protection gate, and the single kill-state read. Counters (trades today, realised result, open positions) are derived from the journal and from adapter reads with a configured UTC day boundary. Reconciliation integrity (current, stale, discrepant) is an input to these gates as "no new risk"; it is not a second switch.
4. **Journal commit.** The intent and the admission decision are durably committed. If the commit fails, no adapter call is made.
5. **Submit.** Only then may an adapter submit be attempted. An uncertain outcome is recorded UNKNOWN, never resubmitted, and resolved by lookup of the client order id.

Rules: any error, missing configuration or unknown state refuses the request (fail closed); every refusal records a reason code and a zero-submit count; every block reason maps either to the one kill state or to a gate result that is not a switch; the gateway's own refusal state and caps are a separate layer that TRON reads and never substitutes for its own kill state. This package supplies the sequence and the journal; `TRON-T3A` supplies the gates, the kill state record and the protection policy. Neither defines a numeric value.

## What is credential-free and what is separately authorised

| Class | Content | Needs |
|---|---|---|
| Credential-free (class a) | Journal port, in-memory and throwaway durable implementations; identity and claim logic; reconciliation engine against simulated broker truth; outbox; adapter interface, simulated adapter and conformance suite with fault injection (duplicate delivery, lost acknowledgement, restart between submit and acknowledgement, orphan creation, missing protection, clock skew); the admission sequence with the T3A gates against the simulated adapter; simulated restart | No session of any kind; D1 ratification for the durable store |
| DEMO read-only (class b) | Adapter reads of a real DEMO session and a reconcile snapshot against it | Separate owner approvals and the approved typed gateway; not part of this package |
| Write-approval (class c) | Order lifecycle, broker-side protection placement and read-back, restart with a live position | Separate DEMO write approval and the `PAPER-E2E-001` Matt gate; not part of this package |

Broker-side protection placement and read-back remain in the later, separately authorised DEMO integration proof, exactly as the approved `TRON-T3A` scope records. The existing unrestricted bridge is never connected to TRON by any adapter, test or harness.

## Scope

In scope (design and credential-free engineering once approved and ready):

1. A journal port with an in-memory implementation and a durable implementation, exercised by one identical test suite.
2. Deterministic execution identity and store-enforced uniqueness.
3. Claim and disposition facts: one immutable terminal disposition per claim.
4. A reconciliation engine: diff of the journal against broker truth presented by an adapter; discrepancy classes; integrity states current, stale and discrepant; restart recovery that reconciles before any write and never resubmits.
5. An event outbox written in the same transaction as the journal write.
6. A broker-neutral adapter interface, a deterministic simulated adapter with fault injection, and an adapter conformance suite importable by the later Vantage adapter. (The lane D evidence leaves open whether this is part of `TRON-T1` or a separate candidate item; see Open decisions.)
7. The single admission sequence and its integration hook for `TRON-T3A` gates, with a test proving the order: gates, then journal commit, then submit.

## Non-goals

No implementation is authorised by this draft. No broker connection, credential, order or DEMO activity. No numeric limit, size or policy value. No kill-state record or setter (that is `TRON-T3A`). No Vantage adapter and no gateway work. No trigger contract text or intake semantics (owned by the trigger contract authority). No edge-profile, event-risk or sizing-policy binding. No Postgres or other store decision (owner decision of D1 ratification). No claim that a simulated rehearsal is PAPER.

## Dependency graph (proposed; backlog not amended)

```text
GOAL-DCP-001 (closed) ─┐
TRON-D1-RATIFY ────────┴─► TRON-T1 (this package)
                              ├─► TRON-T3A ──► TRON-T3 ──► TRON-T5 (also CER-R1)
                              │       └──────────────────► GOLD-MVP-001 (direct)
                              ├─► TRON-T2 (also MT5-GW-004)
                              └─► TRON-T4 (also the trigger contract authority)
TRON-T3 ──► PAPER-E2E-001 (retains TRON-T3)
```

No new edge is proposed by this package. Existing edges are unchanged. If the PO assigns the adapter interface to a separate candidate item, that item would depend on the journal port and be depended on by `TRON-T2`; that is a PO decision, not made here.

## Technical acceptance proofs (credential-free, mechanical)

1. The identical journal test suite passes against the in-memory and the durable implementation.
2. Replaying one source reference yields exactly one intent; every claim ends in exactly one terminal disposition.
3. A test with a failing journal write proves zero adapter calls; a test records the order gates, journal commit, submit.
4. Under the simulated adapter with injected faults (listed in the table above) the conformance suite passes; an uncertain outcome is resolved by lookup and never by resubmit.
5. After a simulated restart between submit and acknowledgement, reconcile runs before any write; no duplicate order and no orphan exist; the reconcile diff is empty.
6. The reconciliation integrity state changes the admission result to "no new risk" without creating a second kill mechanism; a repository test asserts the one-writer property of the kill state defined by `TRON-T3A` still holds.
7. Counters used by the gates are derived from the journal with a configured UTC day boundary and reproduce the same values after restart.
8. A test that opens a socket to a non-local address fails the suite; a test asserts the absence of any raw remote-execution dependency.
9. Evidence events are enqueued in the same transaction as the journal write.
10. The suite runs in the TRON gate with no network and no credential.

## Open decisions

Owner decisions (Matt) already recorded in lane D and not decided here: ratification of the D1 baseline and its amendments; the durable store choice; whether a simulated end-to-end rehearsal may ever carry the state PAPER (default: it does not). Matt-gated and not decided here: all numeric sizing and limit values; the first DEMO order activity.

PO decisions: whether the adapter interface, simulated adapter and conformance suite stay in `TRON-T1` or become a separate candidate item; whether an in-memory journal port is included in the first delivery; who owns trigger-borne protection derivation (`TRON-T4` or the trigger contract authority) — this package only requires that a request without valid protection is refused before submit. Settled by CA, not open: `GOLD-MVP-001` depends on `TRON-T3A` only (among its other direct dependencies), and `PAPER-E2E-001` retains `TRON-T3`.

## Effort and risks

Planning estimate, author's, to be validated at PID approval (not from the lane D evidence, not a commitment): journal port, identity, claims and outbox roughly 12 to 18 engineer-days; reconciliation engine and restart recovery roughly 8 to 12; adapter interface, simulated adapter and conformance suite roughly 8 to 12; admission sequence and hook roughly 3 to 5; independent audits and rework roughly 5 to 8. Total roughly 36 to 55 engineer-days.

Risks: building against an unratified D1 baseline repeats stale intake and wording; a durable-store choice made late forces a port rewrite (mitigated by the port and the shared suite); the second-kill-switch trap if gates elsewhere add their own stop state (mitigated by the one-writer test); a simulated pass being mistaken for broker truth (mitigated by labelling and by keeping classes b and c out of this package); scope creep into the adapter for a real broker (excluded).

## Stop conditions

Stop and return to Central Architecture if the design needs a broker credential, any broker or gateway connection, a second kill mechanism, a live account balance, a numeric policy value, a trigger-contract decision, or any order submission to be demonstrated.

## Evidence

Inputs: the `GOLD-AUD-D` evidence in the GOAL lane D directory (lane state `PO_ACCEPTANCE`; GOAL #30 amendment applies), `pids/TRON-T3A.md`, `backlog/backlog.yaml`, `architecture/DELIVERY-CONTROL-PLANE.md`. Delivery evidence will be the delivery PR in `maff0000/tron` with an index entry in GOAL.

## Approval

PENDING. This draft records no approval. Approval is recorded by Central Architecture/PO only.

# GOAL-DCP-005 — Delivery Identity and Independent Audit Sequencing

**Lane:** shared  
**Target repository:** `maff0000/GOAL`  
**Component:** GOAL  
**Priority:** P0  
**Risk:** Medium  
**PO gate:** Yes  
**Matt gate:** No  
**Parent dependency:** `GOAL-DCP-001` (CLOSED; not reopened)  

**Header notes:** Planning PID only. This file is an architecture-authority candidate registered in `backlog/backlog.yaml` at state `ARCHITECTURE_REQUIRED` with `pid_path: pids/GOAL-DCP-005.md`. It is not `DELIVERY_READY`, no Work Order exists for it, and nothing in it authorises implementation. `GOAL-DCP-002` (the ROGUE dispatcher), `GOAL-DCP-003` and `GOAL-DCP-004` are unchanged; the earlier Central Architecture allocation of `GOAL-DCP-002` to this correction was superseded by the Architect decision of 20 October 2026.

## Purpose

Remove an ambiguity in the delivery chain exposed by the first governed implementation (GOAL pull request #47, Work Order `WO-GOAL-D-ORDERING-002`): the dispatch gate P3 asked for the actual identities of the implementer and of both independent auditors before implementer dispatch, although independent auditors can only be instantiated once an exact candidate head exists. The result was a recorded one-time procedural deviation. This PID clarifies P3 into two stages so that future dispatches can satisfy it literally, while keeping auditor independence verifiable.

## Scope

The scope is a prospective, bounded clarification of two governance documents, to be delivered later through a separate Work Order. The normative model approved by Central Architecture on 20 October 2026 is:

1. **P3a, before implementer dispatch.**
   - Record the actual implementer instance and session identity.
   - Designate independent technical and independent public-safety auditor roles.
   - Record the requirements that neither auditor is the drafter or the implementer and that the two auditors are independent of each other.
   - Record the exact approved Work Order and the governing target baseline.
   - A missing implementer identity or a missing auditor designation blocks dispatch. Auditor sessions need not be instantiated at this stage.
2. **P3b, before each independent audit.**
   - Record the actual auditor instance or session identity.
   - Confirm independence from the drafter, the implementer and the other auditor.
   - Verify the exact candidate head being audited.
   - Use an independent checkout or an equivalent isolated, verifiable source view; read-only source inspection is required, and authorised writing of audit findings is permitted.
   - Do not give the auditor the controller's conclusions as a substitute for independent assessment.
   - Record the audit provenance in the implementation pull request, with private identity details retained in the restricted audit record where necessary.
   - An auditor verdict without its P3b evidence is insufficient for implementation merge acceptance.
3. **Merge conditions.** A governed implementation pull request must not merge unless P3a was satisfied at dispatch, P3b was satisfied for each required independent audit, technical and public-safety findings are attributable to the exact final head, exact-head CI succeeds, Architect acceptance is separately recorded, and the merge targets the accepted head. The existing delivery chain and stop conditions are preserved.

Targets of the later implementation: `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and `templates/WORK-ORDER.md`, with bounded policy-regression tests and, only if required, a generated `MANIFEST.md` entry. The same Work Order is also expected to correct the stale pull request #42 effectiveness labels in those two files using its actual merge commit `3f2f100ea27f515689d1fa05fa815956a396f730`.

## Non-goals

- No change to any previously accepted Work Order and no retroactive change to the pull request #47 deviation, which remains a recorded one-time exception and is not relabelled as compliance.
- No backlog or lane-state change during implementation, and no change to any other governance doctrine.
- No change to the `GOAL-DCP-002`, `GOAL-DCP-003` or `GOAL-DCP-004` records.
- No change to trading, execution or risk authority; no production mutation, broker action, gateway activation, DEMO/LIVE trading or strategy promotion.
- This PID does not itself contain governance-code, template or test implementation.

## Dependencies and interfaces

Depends on `GOAL-DCP-001` only. It relies on the effective governance in `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and the conditional-authority Work Order model in `templates/WORK-ORDER.md`. Its implementation Work Order will be named `WO-GOAL-DCP-P3-001`, with this PID as its parent, and may be prepared only after this PID is independently reviewed, accepted by the Architect at its exact head and merged.

## Safety boundaries

Documentation and policy-regression tests in a single repository only. No credentials, no production systems, no brokers. Transitional rule: until the governance changes are implemented, accepted and merged, the existing P3 rule remains effective. The change is prospective and does not amend any already accepted Work Order. For any Work Order not yet dispatched, the controller must satisfy that Work Order's actual P3 requirements or stop and return for a separate Architect decision. The governance implementation itself must satisfy the currently effective rule and cannot rely on P3a or P3b before they are lawfully activated.

## Deliverables

1. This PID and its canonical backlog registration (this registration pull request).
2. Later, separately governed: Work Order `WO-GOAL-DCP-P3-001` using the conditional-authority model, the twelve mandatory fields, independent assurance, exact-head acceptance and merge gates.
3. Later, under that Work Order: the P3a and P3b wording consistently in both governance files, the pre-dispatch, pre-audit and pre-merge ordering, positive and negative regression tests, and the stale label correction described in Scope.

## Acceptance

1. The two-stage model is stated consistently in both governance files and distinguishes what is required before dispatch from what is required before each audit.
2. Positive and negative regression tests show that missing implementer identity or missing auditor designation blocks dispatch, and that an audit verdict without P3b evidence cannot support merge acceptance.
3. The stale pull request #42 effectiveness labels are corrected using the actual merge commit.
4. No previously accepted Work Order, backlog item or lane state is modified by the implementation.
5. Independent technical and independent public-safety audits satisfy the new two-stage rule as applied to that implementation, or, if it is not yet effective, the existing P3 rule.
6. Exact-head Architect acceptance is recorded before each merge. Passing CI is not Architect acceptance.

## Stop conditions

Stop and return to Central Architecture on any architectural ambiguity, any need to alter an accepted Work Order or the pull request #47 deviation record, any need to change doctrine beyond P3, or any missing authority. Stop on any identifier collision in the backlog.

## Evidence

Inputs: GOAL pull request #47 and its deviation record, Work Order `WO-GOAL-D-ORDERING-002`, the Architect decisions of 20 October 2026 recorded as controller transcriptions where applicable, and `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md`. Evidence of delivery will be the later Work Order pull request with exact-head audits and acceptance.

## Approval

No approval is recorded in this file. Central Architecture approved the architecture for governed registration of this PID on 20 October 2026 (including the identifier correction to `GOAL-DCP-005`); that decision is a chat-delivered directive transcribed by the Delivery Controller and is not itself durable approval of this PID text. This PID's scope is approved only if both an attributable exact-head Architect acceptance record exists in its registration pull request and that exact head is merged into GOAL main. The PO gate remains to be satisfied. This file confers no authority to dispatch or implement.

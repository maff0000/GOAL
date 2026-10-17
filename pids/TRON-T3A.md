# TRON-T3A — Minimum fixed DEMO sizing and risk baseline with one kill state

**Lane:** trading  
**Target repository:** `maff0000/tron`  
**Priority:** P0  
**Risk:** High  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  

**Header notes:** Planning PID only. `TRON-T3A` is registered in `backlog/backlog.yaml` with state `ARCHITECTURE_REQUIRED` and `pid_path: pids/TRON-T3A.md`. It is not `DELIVERY_READY`, and no engineering is dispatched. Header values match the registered backlog item. Priority and risk follow the CA/PO adjudication 2026-10-15 (DR-36) and the CA directives of 16 October 2026.

## Status

PID SCOPE APPROVED (Central Architecture/PO, 17 October 2026; see Approval). Earlier: approved in principle by DR-36 (CA/PO adjudication 2026-10-15), and the planning PR was approved in principle on 17 October 2026 subject only to the protective-level correction recorded in Scope item 5, which is merged.

Backlog state remains `ARCHITECTURE_REQUIRED`. Approval of this PID's scope is not delivery readiness: `TRON-T1` is not accepted-terminal, and promotion to `DELIVERY_READY` is a separate act by the programme controller once `TRON-T1` and the normal control-plane readiness conditions are satisfied. Nothing in this PID authorises engineering, deployment, broker order, contract freeze or live-capital action.

## Purpose

Give TRON the smallest deterministic, credential-free risk and sizing baseline that must exist before any DEMO order can be considered: fixed sizing, position and loss limits, trade-count limits, one enforceable kill state and a protected-order policy. `TRON-T3` later extends this baseline with the fuller hard-risk design. This item exists so `GOLD-MVP-001` depends on a small, bounded foundation rather than on the full extended design.

## Scope

In scope (design and credential-free engineering once approved):

1. Fixed DEMO base sizing taken from configuration, never from a live account balance.
2. A one-position-per-instrument rule and a maximum number of open positions.
3. A maximum daily loss limit and a maximum daily trade-count limit.
4. ONE enforceable kill state with a setter. Every order path checks it, and it fails closed. There is no second kill switch anywhere in TRON.
5. A protected-order policy: which order types and modifications are permitted, and which are rejected before submission. The policy explicitly requires all of the following:
   1. TRON-owned deterministic derivation, or validation, of protective levels from a versioned risk and protection policy.
   2. Validation of protective level direction, distance, instrument precision and the relevant symbol constraints. The check fails closed: if any requirement is unsatisfied, the order is refused.
   3. The pre-submit protection gate uses the existing risk-admission architecture and the one kill state. It adds no second gate path and no second kill mechanism.
   4. Policy values are not set here. No numeric policy value is decided by this PID.
6. Hard gates evaluated before any submit, deterministic, fail-closed, and testable without a broker connection.

Out of scope: broker connectivity, order submission, credential handling, strategy logic, event-risk inputs and edge-profile binding. Broker-side protection placement and read-back belong to the later, separately authorised DEMO integration proof, not to this item.

## Non-goals

No broker order, no DEMO activity, no live capital, no credential handling and no broker connection. No dependency on `CER-R1`. No edge-profile or event-risk coupling, which remain in `TRON-T3` and `TRON-T5`. No final parameter values: actual limits and the first DEMO order activity are separately Matt-gated and are not decided here.

## Dependencies and interfaces

Depends on `TRON-T1` only. `TRON-T3` depends on `TRON-T3A` and extends it, reusing its single kill state rather than creating another. `GOLD-MVP-001` depends directly on `TRON-T3A`. `PAPER-E2E-001` retains `TRON-T3`. Lane D (`GOLD-AUD-D`) validates this scope and the dependency arrangement before any engineering dispatch. The interfaces to the DEMO adapter (`TRON-T2`) and trigger inbox (`TRON-T4`) are defined by their own items and by the Lane D findings.

## Safety boundaries

Credential-free. No broker connection. No production mutation, deployment, contract freeze or live-capital action. One kill state only. Fail closed on any missing configuration, unknown state or evaluation error. Parameter values and any DEMO order activity need separate Matt approval.

## Deliverables

1. Design record for the six elements in Scope, including the single kill state and the protected-order policy.
2. A list of the hard gates that run before submit, each with a credential-free proof, including credential-free tests showing that no OPEN is submitted when valid required protection cannot be established.
3. Reconciliation with the `TRON-T3` design so that it extends rather than duplicates this baseline.
4. Engineering and test plan for a later, separately authorised delivery.

## Acceptance

1. The six scope elements are specified and each has a credential-free test approach.
2. Exactly one kill state exists, and every order path checks it before submission.
3. No element requires a broker credential or a `CER-R1` dependency.
4. Lane D has validated the scope, and `TRON-T3` is shown to extend this baseline without conflict.
5. Parameter values and DEMO order activity remain recorded as Matt-gated.
6. Credential-free tests prove that no OPEN is submitted if valid required protection cannot be established, and that the protection gate sits inside the existing risk-admission path with the one kill state preserved.

## Stop conditions

Stop and return to Central Architecture if the design needs a broker credential, a second kill mechanism, a live account balance, a `CER-R1` dependency, or any order submission to be demonstrated. Stop on any conflict with the Lane D findings.

## Open decisions

Final fixed size, position, daily loss and trade-count values (Matt). The protected-order policy detail. The timing of the first DEMO order activity (Matt). Whether `TRON-T5` should also depend on this item (PO).

## Evidence

Design record and test approach in the delivery PR in `maff0000/tron`, with an index entry in GOAL. Inputs: `GOLD-AUD-D` findings, `GOLD-MVP-001`, and `architecture/DELIVERY-CONTROL-PLANE.md`.

## Approval

APPROVED (PID scope only). Recorded 2026-10-17 by ROGUE on the written authority of Central Architecture/PO.

1. Central Architecture/PO adjudication of GOAL PRs #16 to #19, 17 October 2026: PID approved in principle subject to one bounded correction (TRON-owned protective-level derivation or validation, fail-closed validation, credential-free no-OPEN tests, one kill state, broker-side placement and read-back deferred to the separately authorised DEMO integration proof). The correction merged in GOAL PR #16.
2. Central Architecture/PO post-audit closure directive, 17 October 2026: the merged protective-order corrections satisfy CA's scope requirement and the PID scope is approved.

Limits: this approves the PID scope only. `TRON-T3A` must remain in a pre-delivery state until `TRON-T1` and the required governance conditions are satisfied. No engineering dispatch is authorised, no numeric DEMO policy values are approved, and no broker operation, deployment, contract freeze or live-capital action is authorised. Actual DEMO order activity and final parameters remain separately Matt-gated.

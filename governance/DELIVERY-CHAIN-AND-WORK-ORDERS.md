# Delivery Chain and Work Orders

**Status:** PROPOSED, NOT EFFECTIVE until Architect acceptance and merge.
**Authority:** Central Architecture ruling of 18 October 2026 (governance reset). This document records that ruling; it introduces no new architecture. It is Architect-owned and is drafted here for Architect review only.
**Definition:** Architect means Central Architecture acting as Product Owner for this programme. This is the one term used throughout this document.
**Relationship to other governance:** this document complements `governance/DELIVERY-STATE-MACHINE.md` (the state vocabulary and transition rules) and `architecture/DELIVERY-CONTROL-PLANE.md`. It does not change either of them or any backlog state. How Architect acceptance and independent audit map onto existing state-machine states (PO_ACCEPTANCE, FORGE_AUDIT) is not changed by this document and is an open question for the Architect; FORGE_AUDIT performed by the implementer does not satisfy the independent-audit rule.

## 1. The delivery chain

```text
Architecture decision → PID/Amendment → Git-tracked Work Order → Delivery Controller → Implementer → Independent Audit → PR → Architect Acceptance → Merge → Closure
```

## 2. Invariants

- NO PID → NO WORK ORDER
- NO WORK ORDER → NO IMPLEMENTATION
- NO INDEPENDENT AUDIT + ARCHITECT ACCEPTANCE → NO MERGE (drafter's reading, for Architect confirmation: both an independent audit and Architect acceptance are required)
- NO GIT RECORD → NOT DURABLE PROJECT AUTHORITY

## 3. Rules

1. Every implementation and every correction requires an approved, Git-tracked Work Order before FORGE begins.
2. Every Work Order identifies: the parent approved PID, the applicable amendments, the exact base SHA, the allowed paths, the scope, the exclusions, the required tests, the acceptance criteria and the independent auditor.
3. Architectural ambiguity stops the implementing lane and returns to the Architect.
4. Passing CI is not Architect acceptance.
5. ROGUE may prepare and coordinate pull requests but cannot merge implementation or correction pull requests before explicit Architect acceptance.
6. Historical deliveries are assessed against the authority in force when they were performed. Missing evidence is recorded as missing; it is never backdated or fabricated.
7. The independent auditor cannot be the implementer of the work being audited.
8. ROGUE controls dispatch and delivery coordination. ROGUE does not control architecture, scope or final technical acceptance.

## 4. Required sequence (Central Architecture text, verbatim)

This is the governing sequence.

1. Record and independently review the updated delivery doctrine and applicable PID amendments.
2. Obtain Architect acceptance and merge the governance records.
3. Create the bounded Work Orders with correct parent authority, exact bases and acceptance tests.
4. Independently review and obtain Architect acceptance of the Work Orders.
5. Merge the Work Orders into Git, then have ROGUE dispatch FORGE against those identifiers.
6. Receive implementation results, independent technical and public-safety audits, and PRs.
7. Return the completed PR evidence to Central Architecture for explicit acceptance.
8. Only after acceptance, merge and verify post-merge main CI.
9. Prepare lane-specific PO acceptance/state-change PRs, with separate independent assurance and Architect acceptance.
10. Do not close the overarching PID before its original complete acceptance checklist is satisfied.

## 5. Stop conditions

Any lane stops and returns the precise missing item or finding to the Architect on:

- architectural ambiguity;
- a change of risk authority;
- uncontrolled production access;
- credential exposure;
- an incompatible contract assumption;
- implementation that would fall outside the Work Order scope.

Absence of any required authority is also a stop: return the precise missing item and do not improvise.

## 6. PROJECT DELIVERY CONTRACT (mandatory preamble)

Every ROGUE and every FORGE dispatch prompt must begin with the following text, verbatim:

> PROJECT DELIVERY CONTRACT
>
> You operate under this mandatory chain: Architecture decision → PID/Amendment → Git-tracked Work Order → Delivery Controller → Implementer → Independent Audit → PR → Architect Acceptance → Merge → Closure. Before any action, identify and verify the approved parent PID, applicable amendments, approved Git-tracked Work Order, exact base SHA and allowed paths. ROGUE may dispatch only against that Work Order. FORGE must implement only that Work Order. Neither agent may invent architecture, broaden scope, self-certify independent audit, treat CI success as Architect acceptance, or merge without recorded Architect acceptance. If any required authority is absent, STOP and return the precise missing item. If an architectural ambiguity arises, STOP and return it to the Architect. Do not improvise. Any correction or follow-up requires the same governed Work Order process. Git/GitHub is durable authority. Chat messages and local scratch files are not substitutes.
>
> NO PID → NO WORK ORDER. NO WORK ORDER → NO IMPLEMENTATION. NO INDEPENDENT AUDIT + ARCHITECT ACCEPTANCE → NO MERGE. NO GIT RECORD → NOT DURABLE PROJECT AUTHORITY.

## 7. Work Orders

The nine mandatory Work Order fields are those in rule 2 of section 3: parent approved PID, applicable amendments, exact base SHA, allowed paths, scope, exclusions, required tests, acceptance criteria, and independent auditor (named, and not the implementer of the work being audited). Rule 1 of section 3 requires the Work Order to be approved and Git-tracked.

**Proposed convention for Architect ratification (not in the Central Architecture text).** The following details are drafter proposals only:

- Location: a Work Order is the file `workorders/<WO-ID>.md` in the `maff0000/GOAL` repository, where `<WO-ID>` is the Work Order identifier (for example `GOAL-GOLD-AUD-D-CRIT7-TEST`). The blank template is `templates/WORK-ORDER.md`. No earlier Work Order file convention exists in this repository, so no existing file is displaced.
- Approval is by pull request, like any other governed GOAL change.
- Any empty field means the Work Order is not approved and cannot be dispatched.
- The approver is the Architect.
- Template additions beyond the nine mandatory fields: Implementer, Delivery Controller, Stop conditions, Approval record. These are proposed additions.

## 8. Supersession of earlier broad language

From effectiveness, this document supersedes the following earlier language, only to the extent of conflict:

- `pids/GOLD-AUDIT-CLOSEOUT-001.md` section 2 (Approval of the seven unchanged-scope pull request merges), to the extent it permits merging without an approved Git-tracked Work Order, independent audit and recorded Architect acceptance;
- `pids/GOLD-AUDIT-CLOSEOUT-001.md` section 5 (Continuous operation and escalation policy), the pre-authorisation paragraph for ROGUE and the run loop, only to the extent of conflict;
- the sentence in `pids/GOLD-AUDIT-CLOSEOUT-001.md` section 8 that ROGUE should drive the work continuously, only to the extent of conflict;
- `operations/ROGUE-DISPATCH-GOLD-AUDIT-CLOSEOUT-001.md` (the dispatch note), only to the extent of conflict.

Those originals are not edited. Where they conflict with this document, this document governs. Of the seven section 2 pull requests, GOAL #29 to #32, CER #2 and HSA #2 are merged; DARWIN #27 and any future merge fall under the new chain.

## 9. Provenance

Earlier merges were performed under the authority then in force. This document does not re-judge them (rule 6). Any missing records found when assessing them are reported as gaps in a separate record; they are neither backdated nor reconstructed here.

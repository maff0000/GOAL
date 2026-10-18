# Delivery Chain and Work Orders

**Status:** PROPOSED. It is NOT EFFECTIVE until GOAL PR #42 is accepted by the Architect and merged. It becomes EFFECTIVE only from the merge commit of that PR.
**Effective from merge commit:** `<UNFILLED: to be completed by the Architect-authorised merge record; not yet effective>`
**Authority:** Central Architecture ruling of 18 October 2026 (governance reset, including the ruling of that date that required changes to the first draft of this document). This document records that ruling; it introduces no other architecture. It is Architect-owned.
**Definition:** Architect means Central Architecture acting as Product Owner for this programme. This is the one term used throughout this document.
**Governance bootstrap:** GOAL PR #42 is the narrowly bounded constitutive governance amendment that establishes the Work Order regime. Its drafting and review do not authorise any new engineering implementation. No retrospective Work Order is created or fabricated for it.
**Relationship to other governance:** this document complements `governance/DELIVERY-STATE-MACHINE.md` (the state vocabulary and transition rules) and `architecture/DELIVERY-CONTROL-PLANE.md`. It does not change either of them, any state, or any backlog state. The mapping of the existing states onto this regime is in section 7.4.

## 1. The delivery chain

```text
Architecture decision → PID/Amendment → Git-tracked Work Order → Delivery Controller → Implementer → Independent Audit → PR → Architect Acceptance → Merge → Closure
```

## 2. Invariants

- NO PID → NO WORK ORDER
- NO WORK ORDER → NO IMPLEMENTATION
- NO INDEPENDENT AUDIT + ARCHITECT ACCEPTANCE → NO MERGE (independent audit and Architect acceptance are cumulative, not alternatives; see section 7.3)
- NO GIT RECORD → NOT DURABLE PROJECT AUTHORITY

## 3. Rules

1. Every implementation and every correction requires an approved, Git-tracked Work Order before FORGE begins.
2. Every Work Order carries the twelve mandatory fields listed in section 7.3.
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

### 7.1 Canonical location

The canonical location of every Work Order is `maff0000/GOAL/workorders/<WO-ID>.md`, including Work Orders for component repositories. A Work Order identifies its target repository and the exact target base SHA in that repository. The blank template is `templates/WORK-ORDER.md`.

### 7.2 When a Work Order is executable authority

A Work Order becomes executable authority only after (a) independent review, (b) explicit Architect acceptance and (c) merge into the authoritative GOAL branch. An open pull request, a local file, a conversation approval or a candidate branch is insufficient.

### 7.3 Mandatory fields, audit and acceptance

Every Work Order contains all of the following fields:

1. approved parent PID and applicable amendments;
2. exact target repository and base SHA;
3. permitted paths;
4. scope;
5. exclusions;
6. required tests, including negative tests;
7. acceptance criteria;
8. assigned implementer;
9. independent auditor;
10. Delivery Controller;
11. stop conditions;
12. expected GitHub evidence, pull request and approval record.

A field that is genuinely inapplicable is marked as such with a stated reason. An unresolved placeholder prohibits approval.

Independent audit and Architect acceptance are cumulative, not alternatives. The independent auditor must not be the implementer. The final candidate head must be independently reviewed. A material modification after audit requires renewed independent assurance.

### 7.4 State machine

The existing state machine is unchanged; no state is added or replaced.

- FORGE_AUDIT means independent audit. An audit performed by the implementer does not satisfy it.
- PO_ACCEPTANCE means awaiting explicit Architect acceptance. It does not satisfy downstream dependencies.
- MERGED requires an actually authorised merger and the prescribed post-merge verification.

### 7.5 Approval provenance

Historical actions used a shared GitHub identity, so a GitHub record alone does not prove independent Architect acceptance. An approval is recorded with its exact candidate SHA and an attributable decision source. A transcription of an approval by the Delivery Controller must be labelled as a controller transcription and must not be represented as an independently authenticated Architect action. Separate GitHub identities and branch protection are a separately governed improvement and are not made by this document.

## 8. Supersession of earlier broad language

From effectiveness, this document supersedes the following earlier language, only to the extent of conflict:

- `pids/GOLD-AUDIT-CLOSEOUT-001.md` section 2 (Approval of the seven unchanged-scope pull request merges), to the extent it permits merging without an approved Git-tracked Work Order, independent audit and recorded Architect acceptance;
- `pids/GOLD-AUDIT-CLOSEOUT-001.md` section 5 (Continuous operation and escalation policy), the pre-authorisation paragraph for ROGUE and the run loop, only to the extent of conflict;
- the sentence in `pids/GOLD-AUDIT-CLOSEOUT-001.md` section 8 that ROGUE should drive the work continuously, only to the extent of conflict;
- `operations/ROGUE-DISPATCH-GOLD-AUDIT-CLOSEOUT-001.md` (the dispatch note), only to the extent of conflict.

Those originals are not edited. Where they conflict with this document, this document governs. Of the seven section 2 pull requests, GOAL #29 to #32, CER #2 and HSA #2 are merged; DARWIN #27 and any future merge fall under the new chain.

## 9. Provenance

Earlier merges were performed under the authority then in force. This document does not re-judge them (rule 6). Any missing records found when assessing them are reported as gaps in a separate record; they are neither backdated nor reconstructed here.

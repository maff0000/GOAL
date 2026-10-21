# Work Order WO-GOAL-DCP-P3-001

**Conditional authority.** This file is candidate text and confers no authority by itself. It becomes executable authority solely by (a) an attributable, exact-head Architect acceptance record in GOAL pull request #49 that names the candidate head commit SHA, followed by (b) merge of that exact head into GOAL main (governance sections 7.2 and 7.5). Until both have occurred nothing in this file is approved, and dispatch is barred. This file does not and cannot contain an approval of itself or its own commit SHA: the approval record is external (field 12) and the merge commit on GOAL main is the activation evidence. The gates in "Authority gates" at the end of this file must each be actually satisfied; none is satisfied by assertion.

Governing document: `maff0000/GOAL` `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and template `templates/WORK-ORDER.md`, at GOAL main commit `3f2f100ea27f515689d1fa05fa815956a396f730` (merge of GOAL pull request #42). The authoritative record of this Work Order is this file in `maff0000/GOAL` at `workorders/WO-GOAL-DCP-P3-001.md`. The mandatory dispatch preamble (governance section 6) is not copied here.

**Work Order ID:** WO-GOAL-DCP-P3-001

Current-rule note (Architect decision of 20 October 2026, section 6): this Work Order and its implementation are governed by the CURRENTLY EFFECTIVE gate P3 below, not by P3a or P3b. The change it makes is prospective and takes effect only when it has been implemented, accepted and merged.

## 1. Approved parent PID and applicable amendments

- Parent PID: `GOAL-DCP-005` (`pids/GOAL-DCP-005.md`, Delivery Identity and Independent Audit Sequencing; registered by GOAL pull request #48, merge commit `b7cf9d9c77238777c7d0c36da2388b33b24754fb`, accepted by the Architect on 20 October 2026). Dependency `GOAL-DCP-001` is CLOSED and is not reopened.
- Applicable amendments: none.
- Governance: `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and `templates/WORK-ORDER.md` at GOAL main commit `3f2f100ea27f515689d1fa05fa815956a396f730`; both files are byte-unchanged on main since that commit (re-verified at gate P2).
- Architect decisions of 20 October 2026 (P3 governance correction; PID registration acceptance), recorded as controller transcriptions in GOAL pull request #48.

## 2. Target repository and exact base SHA

Target repository: `maff0000/GOAL`  
Exact base SHA: `b7cf9d9c77238777c7d0c36da2388b33b24754fb` (GOAL `main` after the merge of pull request #48, verified against GitHub when this version was drafted). Registering this Work Order adds only this file and one `MANIFEST.md` line to main; the three target paths below are unchanged by that registration and are re-verified at merge (gate G3) and at dispatch (gate P2).

## 3. Permitted paths

- `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md`
- `templates/WORK-ORDER.md`
- `tests/test_governance_p3.py` (new file; it does not exist at the base)
- `MANIFEST.md`: the generated entry for the new test file only, produced by `./tools/goal-docs --write`, if and only if `./tools/goal-docs --check` reports that the entry is required. No hand edit.

No other path. In particular no backlog file, no `workorders/` file, no `pids/` file, no tool and no workflow.

## 4. Scope

Governance-text and policy-regression-test change only, limited to the following five items.

1. **P3a before implementer dispatch.** Introduce, in the new governance section `7.6` (which holds the P3a and P3b definitions as well as the gate sequence; no P3 text exists in the governance document today, so these are new definitions), the requirement that before any implementer dispatch the Delivery Controller records: the actual implementer instance and session identity; the designated independent technical auditor role and independent public-safety auditor role; the requirements that neither auditor is the drafter or the implementer and that the two auditors are independent of each other; and the exact approved Work Order and the governing target baseline. A missing implementer identity or a missing auditor designation blocks dispatch. Auditor sessions need not be instantiated at this stage.
2. **P3b before each independent audit.** Introduce, likewise inside section `7.6`, the requirement that before each independent audit the Delivery Controller records: the actual auditor instance or session identity; confirmation of independence from the drafter, the implementer and the other auditor; verification of the exact candidate head being audited; use of an independent checkout or an equivalent isolated, verifiable source view; that the auditor is not given the controller's conclusions as a substitute for independent assessment; that source inspection is read-only (authorised writing of audit findings is permitted); and the audit provenance, recorded in the implementation pull request with private identity details retained in the restricted audit record where necessary. An auditor verdict without its P3b evidence is insufficient for implementation merge acceptance.
3. **Sequencing and merge gates.** Make the governance document state the enforced ordering as one numbered list in section `7.6`, headed "Gate sequence" (no existing section is renumbered). It contains exactly six items in this order, each list item beginning with the exact bold label shown, and it is the only numbered list within section `7.6`: (1) `**P3a**`; (2) `**Dispatch**`; (3) `**P3b**`; (4) `**Audit**` (independent audit of the exact final head); (5) `**Acceptance**` (separately recorded Architect acceptance); (6) `**Merge**` (merge of the accepted head). Each label appears exactly once in the list. All detailed requirements and merge conditions are separate unordered bullets (never numbered items). Both independent audits are preserved, the technical audit and the public-safety audit, and P3b applies before each audit separately. Unique anchors: every individually tested P3a requirement, every individually tested P3b requirement and every individually tested merge condition has exactly one stable bold anchor within section `7.6`. The two blocking statements of field 6 mutations 7 and 8 are likewise each uniquely identifiable within section `7.6`, each as one sentence carrying a fixed anchor phrase ("blocks dispatch" and "insufficient for merge acceptance" respectively), each occurring exactly once in section `7.6`. The implementer chooses descriptive anchor names, declares the complete list of anchor identifiers in the implementation pull request, and uses the same identifiers consistently in the tests. Alongside the gate sequence, state the merge conditions (one unordered bullet each): a governed implementation pull request must not merge unless P3a was satisfied at dispatch, P3b was satisfied for each required independent audit, technical and public-safety findings are attributable to the exact final head, exact-head CI succeeds, Architect acceptance is separately recorded, and the merge targets the accepted head. The existing delivery chain, invariants, rules and stop conditions are preserved. Section `7.6` states that it is prospective, applies to Work Orders dispatched after it is effective, does not amend any already accepted Work Order, and does not relabel the one-time procedural deviation recorded on GOAL pull request #47.
4. **Template.** Make `templates/WORK-ORDER.md` carry the same two-stage requirement: field 8 prompts for the P3a implementer record, field 9 for the P3a auditor designation and the P3b before-each-audit record, and field 12 for the P3b provenance location and the merge conditions, each by reference to section `7.6`. Each prompt carries a stable identifying marker inside its own field: field 8 "P3a implementer identity"; field 9 "P3a auditor designation" and "P3b auditor identity"; field 12 "P3b audit provenance" and "merge acceptance conditions". A marker must occur within its required field; occurring elsewhere in the template is insufficient. The implementer authors the surrounding explanatory wording within the approved P3 doctrine. No existing field is renumbered or removed; the twelve mandatory fields stay. The template's header cross-reference to governance "sections 7.1 to 7.5" is updated to "sections 7.1 to 7.6" (one line; this is the only other permitted deletion).
5. **Stale effectiveness labels.** Correct the stale GOAL pull request #42 labels in the two files using the actual merge commit `3f2f100ea27f515689d1fa05fa815956a396f730`: in the governance document, the "Status" line and the "Effective from merge commit" line (replacing the `<UNFILLED …>` placeholder); in the template, the "PROPOSED TEMPLATE …" first line. The corrected wording states that the document is effective from that merge commit, without adding any claim beyond that fact.

Tests (`tests/test_governance_p3.py`) must detect absent or reversed gates, not merely the presence of the words P3a and P3b somewhere in the documents (Architect decision of 20 October 2026, section 4). See field 6.

## 5. Exclusions

- No change to any accepted Work Order, and no retroactive change to the pull request #47 deviation record.
- No backlog, lane-state or state-machine change within this implementation, and no change to `GOAL-DCP-002`, `GOAL-DCP-003` or `GOAL-DCP-004`.
- No change to unrelated delivery doctrine: sections 1 to 6, 7.1 to 7.5, 8 and 9 of the governance document are not edited except for the label lines named in field 4 item 5. Governance line 7 ("Governance bootstrap: GOAL PR #42") is not a stale label and is not edited. The template cross-reference named in field 4 item 4 is the only other permitted edit to existing text.
- No change to the mandatory dispatch preamble text.
- No trading, risk, execution, gateway, broker or production change.
- Tests never write files and never modify the real documents; mutations are built in memory.

## 6. Required tests (including negative tests)

`tests/test_governance_p3.py` extracts section `7.6` from the real governance document and its gate sequence as an ordered list, and checks it with functions that take the document text as an argument, so the real-file tests and the mutation tests exercise the same code. The tests reject a missing required anchor and a duplicated required anchor within section `7.6`, reject a second numbered list within section `7.6`, and parse the existing numbered field boundaries of the template (the twelve fields) and reject a missing, duplicated or misplaced prompt marker. A duplicate anchor must never allow a deletion mutation to pass.

Positive controls: the real governance document and the real template pass every check.

Negative mutations, each built in memory from the real text and each required to FAIL the corresponding check:
1. Remove the P3a item from the gate sequence.
2. Remove the P3b item from the gate sequence.
3. Reverse P3a and implementer dispatch (P3a after dispatch); each label still appears exactly once, so only the order is wrong.
4. Reverse P3b and the independent audit (P3b after audit); each label still appears exactly once, so only the order is wrong.
5. Move Architect acceptance before the independent audit.
6. Move the merge before Architect acceptance.
7. Delete the statement that a missing implementer identity or auditor designation blocks dispatch.
8. Delete the statement that an auditor verdict without P3b evidence is insufficient for merge acceptance.
9. Move the P3a and P3b requirement text outside section `7.6` while leaving the words elsewhere in the document (a bare mention elsewhere must not satisfy the check).
10. Template: remove the P3a prompt from field 8, the P3a/P3b prompts from field 9, and the P3b provenance prompt from field 12 (three separate mutations).
11. Labels: restore the stale "PROPOSED" or "NOT EFFECTIVE until" wording in either file; restore the `<UNFILLED` placeholder; replace the merge SHA with a different 40-hex value (separate mutations).
12. One mutation per individual requirement, each removing that single bullet or statement from section `7.6` and each required to FAIL: every P3a record item (implementer identity; auditor role designation; neither auditor is drafter or implementer; auditors independent of each other; exact approved Work Order and governing baseline); every P3b record item (actual auditor identity; independence from drafter, implementer and other auditor; exact candidate head verified; independent checkout or equivalent isolated view; controller conclusions not provided as a substitute; read-only inspection; provenance recorded in the implementation pull request); and every merge condition (P3a at dispatch; P3b for each audit; findings attributable to the exact final head; exact-head CI success; Architect acceptance separately recorded; merge targets the accepted head).
13. Regression guard: the twelve mandatory fields remain present and in order in both documents.
14. Anchor uniqueness: duplicate a required anchor (for each anchor class: P3a, P3b, merge condition and the two blocking statements) so that it occurs twice in section `7.6`, with its bullet otherwise intact; the anchor check must FAIL. Also duplicate an anchor and delete one copy's bullet text: the check must still FAIL.
15. Gate-sequence uniqueness: add a second numbered list inside section `7.6`; remove or rename the "Gate sequence" heading; repeat or omit a label; each must FAIL.
16. Template field boundaries: move each of the five template markers (field 8; field 9 two markers; field 12 two markers) into a different field, or duplicate it into a second field, while keeping it somewhere in the template; each must FAIL.
17. Content-weakening mutations, each preserving the unique anchor but weakening the obligation, each required to FAIL the policy test: (a) change the mandatory implementer-identity requirement into an optional one; (b) change the mandatory auditor-independence requirement into an optional one; (c) change the missing-identity dispatch blocker into permission to dispatch; (d) change the absence-of-P3b-evidence merge blocker into permission to accept the audit verdict; (e) weaken the rule requiring technical and public-safety audit findings against the exact final head. These are additional to, not substitutes for, the deletion mutations of item 12. The tests therefore check the obligation wording of each tested bullet (mandatory modal wording, not only the anchor).

Control-plane CI steps (`./tools/goal-validate`, `./tools/goal-docs --check`, `./tools/secret-scan`, `python3 -m pytest tests/ -q`) pass at the final head. The diff against the base is shown with `git diff --stat` and `git diff --numstat`: the governance document and template show deletions only on the stale-label lines named in field 4 item 5 and the single template cross-reference line named in field 4 item 4, and no deleted line elsewhere.

## 7. Acceptance criteria

1. Section `7.6` exists with P3a, P3b, the six-step gate sequence and the merge conditions exactly as specified in field 4, and states its prospective nature and the #47 non-relabelling.
2. The template carries the two-stage prompts in fields 8, 9 and 12 without renumbering any field.
3. The stale #42 labels are corrected using `3f2f100ea27f515689d1fa05fa815956a396f730` and no `PROPOSED`, `NOT EFFECTIVE until` or `<UNFILLED` text remains in either file.
4. Every mutation in field 6 (items 1 to 12 and 14 to 17) fails its check, and the positive controls pass; tests detect absent, duplicated, reversed and weakened gates.
5. Only the permitted paths change; the `git diff --numstat` deletion constraint in field 6 holds; no accepted Work Order, backlog item or lane state is modified.
6. Independent technical audit and independent public-safety audit both pass at the exact final head, by auditors who are not the implementer, with the audit provenance recorded in the implementation pull request. A material modification after audit requires renewed independent assurance.
7. Architect acceptance of the exact final head is recorded before merge. Passing CI is not Architect acceptance. Merge is pinned to the accepted head, with post-merge main CI verified.

## 8. Assigned implementer

Assigned by the Delivery Controller (controller assignment of 20 October 2026, under the Architect decision of that date): implementer role label `FORGE-IMPL-WO-GOAL-DCP-P3-001-A`, a FORGE implementer instance. It is launched only after this Work Order is merged into GOAL main and the dispatch gates are met, against this Work Order alone. The actual instance and session identity is recorded in the dispatch pull request (gate P3).

## 9. Independent auditor (not the implementer)

Assigned by the Delivery Controller (controller assignment of 20 October 2026): independent technical auditor role label `FORGE-AUD-TECH-WO-GOAL-DCP-P3-001-B`; independent public-safety auditor role label `FORGE-AUD-SAFE-WO-GOAL-DCP-P3-001-C`. Both are separate instances from the implementer and from each other, and neither may be the drafter or implementer of this Work Order. To satisfy the current gate P3 literally, the Delivery Controller will create the two auditor instances in an idle, no-task standby state, with no knowledge of the implementation, before implementer dispatch, and record their actual instance identities in the dispatch pull request; each is later assigned its audit only once the final candidate head exists. This is the controller's operational method under the current rule; if the Architect objects to it, dispatch stops for adjudication. Public attribution uses the stable role labels; private details stay in the restricted audit record kept by the Delivery Controller.

## 10. Delivery Controller

ROGUE (confirmed by the Architect, 19 October 2026; governance rule 8).

## 11. Stop conditions

Architectural ambiguity (including any need to define a gate not named in field 4, to alter an accepted Work Order or the #47 deviation record, or to change doctrine beyond P3); change of risk authority; uncontrolled production access; credential exposure; incompatible contract assumption; implementation that would fall outside this Work Order's scope; absence of any required authority, including the parent PID's canonical readiness (gate P1). On any of these, stop and return the precise missing item or finding to the Architect (governance section 5).

## 12. Expected GitHub evidence, pull request and approval record

Expected evidence and pull request: one pull request into `maff0000/GOAL` from a branch named for this Work Order, whose diff touches only the permitted paths; the PR body shows `git diff --stat` and `git diff --numstat`; CI results at the exact head; the dispatch record (gate P3 identities, preamble, base re-verification); the independent technical audit and the independent public-safety audit, each recorded against the exact head with its audit provenance; post-merge main CI verification after Architect-accepted merge.  
External approval record (conditional authority model). Approval of this Work Order exists only if both of the following exist, and not otherwise:

1. An attributable Architect acceptance record in GOAL pull request #49 (a review or comment by the Architect) that names the exact candidate head commit SHA accepted and its decision source. A controller transcription of an acceptance is not an Architect action and must be labelled as a transcription (governance section 7.5).
2. Merge of that exact head into GOAL main. The resulting merge commit is the activation evidence.

This file contains no approval fields to fill, no "approved" statement and no SHA of its own commit. If no such record exists, this Work Order is not approved, whatever any other message, local file or CI result says. The pull request body points to the current candidate head and to the acceptance record once it exists. The registration pull request for this Work Order (this one) includes the generated `MANIFEST.md` line for the Work Order file; the future implementation pull request touches `MANIFEST.md` only as stated in field 3.

## Authority gates

Every gate must be actually satisfied, with the evidence named, before the step it guards. A gate that is unsatisfied, unverifiable or satisfied only by assertion blocks that step. Satisfaction is recorded in GOAL pull request #49 (merge gates) or in the dispatch pull request (dispatch gates), not in this file.

Pre-merge gates (all required before this Work Order is merged into GOAL main):

- G1. Independent technical audit and independent public-safety audit of the exact final head, by auditors who are not the drafter or the implementer. A material change after audit requires renewed audit. Evidence: audit records against the exact head SHA.
- G2. Exact-head CI success and a clean secret scan on the same head. CI success is not Architect acceptance.
- G3. Base verified: GOAL main equals the base in field 2 at merge time. If main has moved, reconcile against the new main, independently review any material base or manifest change, and obtain fresh Architect acceptance of the new exact head.
- G4. Explicit Architect acceptance of the exact head, recorded in GOAL pull request #49 as described in field 12, before merge. The merge is pinned to that head.

Pre-dispatch gates (all required before any implementer is dispatched):

- P1. This Work Order is merged into GOAL main and main CI on the merge commit is verified. In addition, the canonical readiness authority applicable to the parent PID is satisfied: `GOAL-DCP-005` is registered at state `ARCHITECTURE_REQUIRED`, and dispatch is barred until its state has advanced through the delivery state machine and its PO gate by separately governed, independently evidenced transitions. This Work Order does not change that state.
- P2. GOAL main is re-verified at dispatch; the three target paths are unchanged from the base used by this Work Order, or the change has been independently reviewed and accepted. On any mismatch, stop and return to the Architect.
- P3. (Currently effective rule; P3a and P3b are not relied on.) Actual instance and session identities of the implementer and both auditors are recorded in the dispatch pull request, and their separation is verified. The role labels in fields 8 and 9 are prospective assignments only. Field 9 states the method.
- P4. The mandatory dispatch preamble of governance section 6 is included in the dispatch prompt.
- P5. Permitted paths (field 3) and exclusions (field 5) are enforced. Any stop condition in field 11 stops work and is returned to the Architect.

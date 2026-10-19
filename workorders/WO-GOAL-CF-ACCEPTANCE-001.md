# Work Order WO-GOAL-CF-ACCEPTANCE-001

**Conditional authority.** This file is candidate text and confers no authority by itself. It becomes executable authority solely by (a) an attributable, exact-head Architect acceptance record in GOAL pull request #45 that names the candidate head commit SHA, followed by (b) merge of that exact head into GOAL main (governance sections 7.2 and 7.5). Until both have occurred nothing in this file is approved, and dispatch is barred. This file does not and cannot contain an approval of itself or its own commit SHA: the approval record is external (field 12) and the merge commit on GOAL main is the activation evidence. The amendment wording in field 4 is not operative, and may be implemented verbatim only after that acceptance and merge. The gates in "Authority gates" at the end of this file must each be actually satisfied; none is satisfied by assertion.

Governing document: `maff0000/GOAL` `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and template `templates/WORK-ORDER.md`, at GOAL main commit `3f2f100ea27f515689d1fa05fa815956a396f730` (merge of GOAL pull request #42). The authoritative record of this Work Order is this file in `maff0000/GOAL` at `workorders/WO-GOAL-CF-ACCEPTANCE-001.md`. The mandatory dispatch preamble (governance section 6) is not copied here.

**Work Order ID:** WO-GOAL-CF-ACCEPTANCE-001

## Status of the amendment wording

The earlier draft of this Work Order was marked "BLOCKED: wording not in Git". That section is replaced. The wording is now PROPOSED inside this Work Order (field 4), written as exact text for the Architect to accept. It becomes operative only if the Architect accepts this Work Order and the Work Order is merged; the PID amendments are then appended by the implementer verbatim from the accepted text. The implementer authors no wording.

## 1. Approved parent PID and applicable amendments

- Parent PIDs: GOLD-AUDIT-CLOSEOUT-001 (`pids/GOLD-AUDIT-CLOSEOUT-001.md`), GOLD-AUD-C (`pids/GOLD-AUD-C.md`) and GOLD-AUD-F (`pids/GOLD-AUD-F.md`).
- Applicable amendments, which remain in force except as expressly stated in field 4:
  - GOLD-AUD-C amendment of 17 October 2026 (GOAL pull request #29, merge commit `028870fcc7213043fb6eb144b1f5d6b93b4f5faa`); item 3 is superseded as to A-9 only, by the wording proposed in field 4.
  - GOLD-AUD-F amendment of 17 October 2026 (GOAL pull request #32, merge commit `a33f954f6c00076ae044b2b5fe552aefb8699266`); no item of it is superseded.
  - GOLD-AUD-D amendment of 17 October 2026 (GOAL pull request #30, merge commit `2caad714247cbe098412832e1cbbf5286c13b82f`), item 2 (criterion 12 as amended). This is the normative GREEN-WITH-NOTICE acceptance rule and the structural model for the proposed wording. It is not edited by this Work Order.
- Governance: `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` at GOAL main `3f2f100ea27f515689d1fa05fa815956a396f730`.

Authority ordering (Architect ruling of 18 October 2026): the normative GREEN-WITH-NOTICE acceptance rule is the dated 17 October 2026 amendment to GOLD-AUD-D criterion 12 (GOAL #30 item 2). The wording of the close-out PID (Phase 3 and checklist) is procedural, not a competing standard. Earlier drafts of this Work Order, which tabulated three differing formulations, are non-authoritative wherever they are inconsistent with this version.

## 2. Target repository and exact base SHA

Target repository: `maff0000/GOAL`  
Exact base SHA: `d7bffec206bf58057e4742edc1611f6ecced5d19` (GOAL `main` after the merge of pull request #43, which changed only a Work Order file and `MANIFEST.md`; the two target PID files are unchanged from `3f2f100ea27f515689d1fa05fa815956a396f730`). The base is re-verified at merge (gate G3) and at dispatch (gate P2).

## 3. Permitted paths

- `pids/GOLD-AUD-C.md` and `pids/GOLD-AUD-F.md`, append-only (new dated amendment sections at the end of each file; existing text is not edited).
- `MANIFEST.md` is not a permitted path of the future PID amendment implementation pull request: no new file is added, so no manifest change is expected. If a file is added after all, or `./tools/goal-docs --check` reports a manifest change, stop and return to the Architect, who adds `MANIFEST.md` to this list before approval.

## 4. Scope

The amendment date is 19 October 2026, the date of the Architect decision that accepts this framework (Architect directive of 19 October 2026, section 4). No earlier historical date is altered. Append to the two PID files the following two separate, explicit, dated amendments, recorded verbatim from the accepted Work Order. They are two independent amendments. The GREEN-WITH-NOTICE rule of Lane D criterion 12 is NOT applied to Lane C A-9 or to Lane F criterion 9 automatically, by reference or by implication; each lane receives only the express wording below, and only on the Architect's acceptance of this Work Order. Each is modelled on the structure of the Lane D criterion 12 amendment (GOAL #30 item 2, read in `pids/GOLD-AUD-D.md` on GOAL main), whose normative text is: "Fresh independent FORGE Auditor verdict recorded against the exact evidence SHA, being GREEN or an independently verified GREEN-WITH-NOTICE, provided that each notice has a named owner, the confidential evidence provenance is recorded, and PO acceptance of the verdict and its notices is recorded."

One acceptance formulation is used in both the Lane C A-9 wording (4.1 item 1) and the Lane F criterion 9 wording (4.2 item 1). It mirrors the structure and words of D criterion 12, including "the confidential evidence provenance is recorded" and "acceptance of the verdict and its notices is recorded". Governance defines the Architect as Central Architecture acting as Product Owner, so acceptance is stated ONCE, as Architect acceptance (which is the PO acceptance of D criterion 12); the wording does not require both a separate PO acceptance and an Architect acceptance. The two wordings differ only in the place where acceptance is recorded, and that difference is not new: it is the location wording already present in each original criterion (Lane C A-9: "PO acceptance recorded per the state machine"; Lane F criterion 9: "PO acceptance recorded in GitHub"). The original criteria also require an evidence PR list with exact SHAs, which is retained. The added "confidential evidence provenance is recorded" replaces the earlier draft's mixed provenance wording, and for Lane F it carries no extra parenthetical.

### 4.1 Proposed wording for `pids/GOLD-AUD-C.md` — proposed wording — becomes operative only if the Architect accepts this Work Order

> ## Amendment (19 October 2026, Central Architecture decision): acceptance A-9
>
> Dated 19 October 2026. This section records a Central Architecture decision of 19 October 2026. It changes only what is stated below. No lane state changes.
>
> 1. **A-9 as amended.** Acceptance A-9 is amended to read: "Fresh independent FORGE Auditor verdict recorded against the exact evidence SHA, being GREEN or an independently verified GREEN-WITH-NOTICE, provided that each notice has a named owner, the confidential evidence provenance is recorded, and Architect acceptance of the verdict and its notices is recorded per the state machine; evidence PR list with exact SHAs." The independent auditor is not the implementer.
> 2. **Supersession, A-9 only.** This amendment expressly amends and supersedes, as to A-9 only, the statement in item 3 of the amendment of 17 October 2026 (GOAL #29) that "A-9 (independent auditor and PO acceptance) is unchanged". The remainder of item 3 and of that amendment stays in force exactly as written: A-1, A-2, A-3, A-4, A-5, A-7 and A-8 apply to CP-1 only with their CP-2 parts deferred, not met; A-6 is unchanged; the `goal-validate` and `secret-scan` checks in A-8 are unchanged.
> 3. **No automatic application.** This amendment applies to Lane C A-9 only. It is not extended to any other lane or criterion by reference.
> 4. **Notices are retained.** A notice is not discharged by this amendment. A recorded GREEN-WITH-NOTICE remains GREEN-WITH-NOTICE; no historic verdict is relabelled GREEN.
> 5. **Boundaries unchanged.** The CP-2 reference-only boundary established by the amendment of 17 October 2026 (GOAL #29) is unchanged. CP-1 stays `PROPOSED`, not frozen. No contract freeze and no compatibility acceptance results from this amendment.
> 6. **No state change here.** This amendment moves nothing to `MERGED`. The lane stays in `PO_ACCEPTANCE` until it is judged against its acceptance criteria as amended, through the governed state transition.

### 4.2 Proposed wording for `pids/GOLD-AUD-F.md` — proposed wording — becomes operative only if the Architect accepts this Work Order

> ## Amendment (19 October 2026, Central Architecture decision): acceptance criterion 9
>
> Dated 19 October 2026. This section records a Central Architecture decision of 19 October 2026. It changes only what is stated below. No lane state changes.
>
> 1. **Criterion 9 as amended.** Acceptance criterion 9 is amended to read: "Fresh independent FORGE Auditor verdict recorded against the exact evidence SHA, being GREEN or an independently verified GREEN-WITH-NOTICE, provided that each notice has a named owner, the confidential evidence provenance is recorded, and Architect acceptance of the verdict and its notices is recorded in GitHub; evidence PR list with exact SHAs." The independent auditor is not the implementer.
> 2. **No other criterion changed.** Acceptance criteria 1 to 8 are unchanged. No item of the amendment of 17 October 2026 (GOAL #32) is superseded.
> 3. **No automatic application.** This amendment applies to Lane F criterion 9 only. It is not extended to any other lane or criterion by reference.
> 4. **Notices are retained.** A notice is not discharged by this amendment. A recorded GREEN-WITH-NOTICE remains GREEN-WITH-NOTICE; no historic verdict is relabelled GREEN.
> 5. **Safety finding unchanged.** The NEO safety finding and the SEC-B investigation are unchanged, and nothing here implies that the NEO observer is approved for read-only consumption.
> 6. **No state change here.** This amendment moves nothing to `MERGED`. The lane stays in `PO_ACCEPTANCE`. Advancement remains governed by item 3 of the amendment of 17 October 2026 (GOAL #32) and the governed state transition.

## 5. Exclusions

- No retroactive relabelling of any recorded verdict. A recorded GREEN-WITH-NOTICE remains GREEN-WITH-NOTICE.
- No unearned MERGED states. This Work Order moves no lane state.
- No application of the Lane D criterion 12 rule to Lane C or Lane F other than the express wording in field 4.
- No strategy freeze and no contract freeze. CP-1 stays PROPOSED.
- The CP-2 reference-only boundary established by the lane C amendment (GOAL #29) is not changed.
- No edit to the backlog, to other PIDs, to existing text of either PID, to evidence files, or to the NEO safety finding; nothing here implies that the NEO observer is approved.
- No wording of the rule is authored by the implementer; only the text in field 4, as accepted by the Architect, is recorded. Any change the Architect makes to field 4 before acceptance is the recorded text.

## 6. Required tests (including negative tests)

- PID-to-backlog consistency (`./tools/goal-validate`).
- No regression of the CP-2 reference-only boundary (the existing contract-package tests continue to pass).
- `./tools/goal-docs --check`.
- `./tools/secret-scan`.
- Control-plane CI steps, including `python3 -m pytest tests/ -q`, pass at the final head.
- Negative checks: (a) the diff of each PID file shows additions only: `git diff --numstat <base-sha>..HEAD -- <pid-file>` reports ZERO deleted lines for each of `pids/GOLD-AUD-C.md` and `pids/GOLD-AUD-F.md` (automated, run per PID file; any non-zero deleted count fails). This check runs alongside, and does not replace, the byte-prefix and verbatim-text checks below; (b) AUDITOR-READ CHECK (not automated): neither PID file, after the change, contains a statement that applies the rule of the other lane or of Lane D automatically; (c) the Lane C addition expressly supersedes the A-9 statement of item 3 of GOAL #29 and no other statement of it; (d) the additions grant no MERGED state (the word MERGED may appear in the additions only in negative statements that grant nothing, such as "moves nothing to `MERGED`").
- Byte-for-byte verification step, combining the byte-prefix (append-only) and verbatim-text checks (automated; run by the implementer, and re-run independently by the auditor, with the output recorded in the pull request and in the audit). A small script, run with `python3 -I` from a scratch directory against a checkout of the branch, extracts and diffs the two texts for each PID file. (1) Extraction of the quoted wording: read `workorders/WO-GOAL-CF-ACCEPTANCE-001.md`; for field 4.1 (resp. 4.2) collect the lines of the blockquote that follows the heading beginning `### 4.1` (resp. `### 4.2`) up to the next line beginning `#`, strip the leading `> ` from each (a bare `>` becomes an empty line), and join with `\n`. (2) Extraction of the appended text: obtain the PID file at the base SHA and at HEAD with `git show <sha>:<path>`; assert the HEAD bytes start with the base bytes (append-only); take the remainder. (3) Compare: after removing leading and trailing blank lines from both, the two strings must be identical; on any difference, print a unified diff and exit non-zero. The step fails if any byte differs, including whitespace and punctuation.
- Auditor check (not an automated test; no automated mechanism exists to trace acceptance criteria to amendments). The independent auditor confirms by reading and records in the audit that: each amended criterion is traceable to the criterion it amends (Lane C A-9, Lane F criterion 9) and to the dated Architect decision that approves it; and the text of the Lane D criterion 12 amendment (GOAL #30 item 2) is unchanged. The byte-for-byte match is established by the script above, not by reading.

## 7. Acceptance criteria

1. The wording in field 4 has been accepted by the Architect and this Work Order is merged into GOAL main before dispatch.
2. Each amendment records the field 4 text verbatim, appended and dated; existing PID text is not edited. The byte-for-byte verification script in field 6 passes for both PID files.
3. The Lane C amendment expressly amends and supersedes item 3 of GOAL #29 as to A-9 only.
4. Each of the two amendments stands alone; neither is derived from Lane D criterion 12 automatically.
5. All unresolved notices are retained in the record, not discharged by the amendments.
6. Only the permitted paths are changed (`git diff --stat` shown in the pull request).
7. Independent technical audit and independent public-safety audit both pass at the exact final head, by an auditor who is not the implementer. A material modification after audit requires renewed independent assurance.
8. Architect acceptance is recorded before merge. Passing CI is not Architect acceptance. Independent audit and Architect acceptance are cumulative, not alternatives.

## 8. Assigned implementer

Assigned by the Delivery Controller (controller assignment of 19 October 2026, recorded under the Architect directive of that date): implementer instance identifier `FORGE-IMPL-WO-GOAL-CF-ACCEPTANCE-001-A`, a FORGE implementer instance. It is launched only after this Work Order is merged into GOAL main, against this Work Order alone. The identifier is a role label; the launch record (session and model identity) will be added to the pull request evidence at dispatch.

## 9. Independent auditor (not the implementer)

Assigned by the Delivery Controller (controller assignment of 19 October 2026). Independent technical auditor identifier `FORGE-AUD-TECH-WO-GOAL-CF-ACCEPTANCE-001-B`; independent public-safety auditor identifier `FORGE-AUD-SAFE-WO-GOAL-CF-ACCEPTANCE-001-C`. Both are separate instances from the implementer and from each other, and neither may be the drafter or implementer of this Work Order. Public attribution uses these stable role identifiers; the actual session identities are traceable in a restricted audit record kept by the Delivery Controller and recorded when each audit is performed.

## 10. Delivery Controller

ROGUE (confirmed by the Architect, 19 October 2026, directive section 6; governance rule 8).

## 11. Stop conditions

Architectural ambiguity (including any doubt about the text in field 4); change of risk authority; uncontrolled production access; credential exposure; incompatible contract assumption; implementation that would fall outside this Work Order's scope, including any edit of existing PID text; absence of any required authority. On any of these, stop and return the precise missing item or finding to the Architect (governance section 5).

## 12. Expected GitHub evidence, pull request and approval record

Expected evidence and pull request: one pull request into `maff0000/GOAL` from a branch named for this Work Order, whose diff is append-only on the two permitted paths; the PR body shows `git diff --stat`; CI results at the exact head; the independent technical audit (including the auditor check in field 6) and the independent public-safety audit, each recorded against the exact head; post-merge main CI verification after Architect-accepted merge. Lane state changes, if any, belong to separate PO acceptance pull requests.  
External approval record (conditional authority model). Approval of this Work Order exists only if both of the following exist, and not otherwise:

1. An attributable Architect acceptance record in GOAL pull request #45 (a review or comment by the Architect) that names the exact candidate head commit SHA accepted and its decision source. A controller transcription of an acceptance is not an Architect action and must be labelled as a transcription (governance section 7.5).
2. Merge of that exact head into GOAL main. The resulting merge commit is the activation evidence.

This file contains no approval fields to fill, no "approved" statement and no SHA of its own commit. If no such record exists, this Work Order is not approved, whatever any other message, local file or CI result says. The pull request body points to the current candidate head and to the acceptance record once it exists. The registration pull request for this Work Order (this one) includes the generated `MANIFEST.md` line for the Work Order file; that is distinct from the future PID amendment implementation pull request, from which `MANIFEST.md` stays excluded.

## Authority gates

Every gate must be actually satisfied, with the evidence named, before the step it guards. A gate that is unsatisfied, unverifiable or satisfied only by assertion blocks that step. Satisfaction is recorded in GOAL pull request #45 (merge gates) or in the dispatch pull request (dispatch gates), not in this file.

Pre-merge gates (all required before this Work Order is merged into GOAL main):

- G1. Independent technical audit and independent public-safety audit of the exact final head, by auditors who are not the drafter or the implementer. A material change after audit requires renewed audit. Evidence: audit records against the exact head SHA.
- G2. Exact-head CI success and a clean secret scan on the same head. CI success is not Architect acceptance.
- G3. Base verified: GOAL main equals the base in field 2 at merge time. If main has moved, reconcile against the new main, independently review any material base or manifest change, and obtain fresh Architect acceptance of the new exact head.
- G4. Explicit Architect acceptance of the exact head, recorded in GOAL pull request #45 as described in field 12, before merge. The merge is pinned to that head.

Pre-dispatch gates (all required before any implementer is dispatched):

- P1. This Work Order is merged into GOAL main and main CI on the merge commit is verified.
- P2. GOAL main is re-verified at dispatch; the two target PID files are unchanged from the base used by this Work Order, or the change has been independently reviewed and accepted. On any mismatch, stop and return to the Architect.
- P3. Actual instance and session identities of the implementer and both auditors are recorded in the dispatch pull request, and their separation is verified. The role identifiers in fields 8 and 9 are prospective assignments only.
- P4. The mandatory dispatch preamble of governance section 6 is included in the dispatch prompt.
- P5. Permitted paths (field 3) and exclusions (field 5) are enforced, including that the amendment text is recorded verbatim from field 4 and that no lane state changes. Any stop condition in field 11 stops work and is returned to the Architect.

# Work Order WO-GOAL-F-ATTESTATION-001

**DRAFT — not approved, not dispatched; Architect acceptance and merge into GOAL main required before it is executable authority.** This file authorises no work. An open pull request, a local file, a conversation approval or a candidate branch is insufficient (governance section 7.2). Dispatch is barred until the Approval record in field 12 is complete, the "Unresolved before approval" list is empty, and this Work Order is merged into GOAL main.

Governing document: `maff0000/GOAL` `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and template `templates/WORK-ORDER.md`, at GOAL main commit `3f2f100ea27f515689d1fa05fa815956a396f730` (merge of GOAL pull request #42). The authoritative record of this Work Order is this file in `maff0000/GOAL` at `workorders/WO-GOAL-F-ATTESTATION-001.md`. The mandatory dispatch preamble (governance section 6) is not copied here.

**Work Order ID:** WO-GOAL-F-ATTESTATION-001

## 1. Approved parent PID and applicable amendments

- Parent PIDs: GOLD-AUD-F (`pids/GOLD-AUD-F.md`) and GOLD-AUDIT-CLOSEOUT-001 (`pids/GOLD-AUDIT-CLOSEOUT-001.md`).
- Applicable amendment: GOLD-AUD-F dated PID amendment of 17 October 2026 (GOAL pull request #32, merge commit `a33f954f6c00076ae044b2b5fe552aefb8699266`), which defers the private mirror note and leaves the NEO safety finding unchanged.
- Governance: `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` at GOAL main `3f2f100ea27f515689d1fa05fa815956a396f730`.

## 2. Target repository and exact base SHA

Target repository: `maff0000/GOAL`  
Exact base SHA: `3f2f100ea27f515689d1fa05fa815956a396f730` (GOAL `main`; verified against GitHub when this version was drafted)

## 3. Permitted paths

- Exactly one new file, `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/ATTESTATION.md` (the sanitised public attestation).
- `MANIFEST.md` (generated; it changes because a file is added, via `./tools/goal-docs --write`).
- `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md` is NOT a permitted path: any index or state change belongs to the separate PO acceptance pull request.
- Private evidence is not stored in the repository.

## 4. Scope

Independently verify GOLD-AUD-F acceptance criteria 1, 2, 4 and 7 (`pids/GOLD-AUD-F.md`). Criterion 1 is in scope because the Architect's dictation for this Work Order lists criteria 1, 2, 4 and 7; no other criterion is added. The verification includes:

- confidential inventory coverage (criterion 2: the coverage reconciliation of the external register, including the private inventory counts); and
- before and after inspection identities (criterion 4: identity unchanged for each inspected system). The baseline record is `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/IDENTITY-SNAPSHOTS.md` (public rows) together with the confidential record for the checkouts it states are held there.

Rules for criteria 2 and 4 (Architect ruling of 18 October 2026):

- A private attestation may satisfy criterion 2 or 4 only if it is independently verifiable. An unsupported private statement, or an Architect ruling alone, is insufficient.
- The independent auditor must verify the private inventory counts and the before and after identities against the actual retained evidence. Verification is performed by the auditor against the retained private evidence, not by reading a summary of it.
- If the auditor cannot reproduce the private checks, the affected criteria stay NOT MET, lane F remains in `PO_ACCEPTANCE`, and the attestation does not paper over this.

Criterion 7: acceptable once the independent auditor's actual verification of it has been performed against the committed evidence, the resulting verification record is committed, and that record has been reviewed. A verdict not backed by the auditor's actual verification does not satisfy criterion 7.

Where the criterion 7 verification record lives: the public-safe record of the independent auditor's actual verification (safe pass or fail outcomes only: one pass or fail per sub-check and an overall pass or fail; no search patterns, no paths, no matches, no counts and no private content) is committed in the same `ATTESTATION.md`, under a clearly labelled section (heading "Criterion 7 verification record"). A verdict alone, without this record, does not satisfy criterion 7.

Public attestation. A public, sanitised attestation is recorded in `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/ATTESTATION.md`. It may contain only: a non-sensitive digest, the criteria tested, the verdict, the auditor identity, and the public-safe criterion 7 verification record described above (safe pass or fail outcomes only, with no search patterns, paths, matches or counts; the permitted content is widened to this extent and no further). It publishes NO counts (no inventory counts, no coverage numbers, no list lengths), no private repository identities, no paths, no addresses and no sensitive source information.

Digest definition (Architect decision, 19 October 2026: a public digest of the canonical public attestation wording ONLY is permitted): the digest is the SHA-256 of a canonical, sanitised statement of the criteria tested and the verdict, and of nothing else. The canonical statement is the exact text published in the attestation for those two items (UTF-8, LF line endings, no trailing whitespace), and the attestation states that form so a reader can recompute the digest. The digest is NOT the hash of any private file, list or register, because such a hash could confirm or leak private content. Limit of this design, stated for the Architect: the digest provides integrity of the published wording only (a reader can detect a change to the published criteria-tested and verdict text); it is not a cryptographic binding to the private evidence, so it does not by itself prove that the private checks were performed. The attestation must state in plain words that the digest is NOT proof of the private evidence and NOT a hash of any private material. The binding to the private evidence rests on the independent auditor's actual verification (criteria 2, 4 and 7) and the audit record, not on the digest.

Auditor identity in the public attestation uses a stable pseudonym or role identifier (Architect decision, 19 October 2026), provided the actual identity is traceable in the restricted audit record. No individual name, account or address is published.

Confidential-evidence access (Architect decision, 19 October 2026): HELM's designated security custodian is the access grantor, subject to existing authority and any required explicit owner authorisation. Access must be scoped, read-only, auditable, and limited to the independent auditor who needs it. Private evidence access is NOT granted automatically to the implementer. Until the custodian's grant, and any required owner authorisation, is recorded, the private checks cannot be dispatched. If access cannot be obtained or the private evidence cannot be reproduced, each affected criterion remains NOT MET and nothing is inferred as complete. Private criteria (2 and 4) are MET only following actual independent reproduction.

## 5. Exclusions

- No publication of private repository identities, paths, operational addresses or sensitive source information, and no counts.
- No NEO runtime mutation and no observer activation. The NEO safety finding and the SEC-B investigation are unchanged, and nothing here implies the NEO observer is approved.
- No change to any other criterion, to any lane state, to the backlog, to `EVIDENCE-INDEX.md`, or to any PID.
- No acceptance of criterion 2 or 4 on an unsupported private statement or on an Architect ruling alone.
- No GREEN-WITH-NOTICE rule is introduced or applied here; that is the subject of the separate WO-GOAL-CF-ACCEPTANCE-001.

## 6. Required tests (including negative tests)

- Reproducible private evidence checks, performed by the independent auditor against the actual retained confidential record.
- Public redaction inspection of the attestation file (no private identity, path, address, count or sensitive source information; a grep for IPv4 addresses, ports and key-like strings returns nothing).
- Digest check: the auditor recomputes the SHA-256 of the canonical statement and it equals the published digest.
- Coverage reconciliation for criterion 2, including the private inventory counts, performed by the auditor against retained evidence and reported only as a verdict in the public file.
- No-change identity verification for criterion 4: before and after identities (baseline `IDENTITY-SNAPSHOTS.md` and the confidential record) compared by the auditor against the retained evidence and found equal, or recorded as not equal.
- Criterion 7: the auditor's actual verification is committed in `ATTESTATION.md` as the labelled "Criterion 7 verification record" section (safe pass or fail outcomes only: no search patterns, paths, matches, counts or private content), in addition to the verdict, and is reviewed.
- Negative tests: (a) an attestation that contains any count, private identity, path or address fails the redaction inspection; (b) an attestation whose digest does not match the recomputed canonical statement fails; (c) an attestation that asserts criterion 2 or 4 met without the auditor's reproduction of the retained evidence fails the audit; (d) where the auditor cannot reproduce, the attestation must record the criterion as NOT MET and the lane as remaining in `PO_ACCEPTANCE`.
- `./tools/goal-validate`, `./tools/goal-docs --check`, `./tools/secret-scan`, and `python3 -m pytest tests/ -q` pass at the final head.

## 7. Acceptance criteria

1. Each of criteria 1, 2, 4 and 7 has an independently reproducible verdict from the auditor's actual verification, or remains NOT MET. Criteria 2 and 4 are met only if independently verified against the retained private evidence.
2. The public attestation (`ATTESTATION.md`) contains only the permitted elements (non-sensitive digest of the canonical statement, criteria tested, verdict, role-level or pseudonymous auditor identity, and the labelled public-safe criterion 7 verification record) and no counts and no private identities, paths or addresses.
3. Only the permitted paths are changed (`git diff --stat` shown in the pull request): the new attestation file and `MANIFEST.md`.
4. Independent technical audit and independent public-safety audit both pass at the exact final head, by an auditor who is not the implementer. A material modification after audit requires renewed independent assurance.
5. Architect acceptance is recorded before merge. Passing CI is not Architect acceptance. Independent audit and Architect acceptance are cumulative, not alternatives.

## 8. Assigned implementer

Assigned by the Delivery Controller (controller assignment of 19 October 2026, recorded under the Architect directive of that date): implementer instance identifier `FORGE-IMPL-WO-GOAL-F-ATTESTATION-001-A`, a FORGE implementer instance. It is launched only after this Work Order is merged into GOAL main, against this Work Order alone. It receives NO access to the confidential record. The identifier is a role label; the launch record will be added to the pull request evidence at dispatch.

## 9. Independent auditor (not the implementer)

Assigned by the Delivery Controller (controller assignment of 19 October 2026). Independent technical auditor identifier `FORGE-AUD-TECH-WO-GOAL-F-ATTESTATION-001-B`, who performs the private-evidence reproduction and is the only party for whom confidential access may be requested; independent public-safety auditor identifier `FORGE-AUD-SAFE-WO-GOAL-F-ATTESTATION-001-C`, who works on public material only. All are separate instances from the implementer and from each other. Public attribution uses these stable role identifiers; the actual session identities are traceable in a restricted audit record kept by the Delivery Controller. Reproduction depends on the access grant described in field 4.

## 10. Delivery Controller

ROGUE (confirmed by the Architect, 19 October 2026, directive section 6; governance rule 8).

## 11. Stop conditions

Architectural ambiguity; change of risk authority; uncontrolled production access; credential exposure (including any exposure of the confidential record); incompatible contract assumption; implementation that would fall outside this Work Order's scope; the auditor cannot obtain or cannot reproduce the private evidence; absence of any required authority. On any of these, stop and return the precise missing item or finding to the Architect (governance section 5).

## 12. Expected GitHub evidence, pull request and approval record

Expected evidence and pull request: one pull request into `maff0000/GOAL` from a branch named for this Work Order, whose diff touches only the permitted paths; the PR body shows `git diff --stat`; CI results at the exact head; the independent technical audit and the independent public-safety audit, each recorded against the exact head, with no private particulars; post-merge main CI verification after Architect-accepted merge. Lane state changes belong to the separate PO acceptance pull request.  
External durable location of final acceptance: the exact-head Architect acceptance of this Work Order is recorded on GOAL pull request #46 (this pull request), not inside this file, so that this file need not embed its own SHA. Merge of this pull request on the accepted head is the activation evidence. The fields below are intentionally left unfilled in the candidate and are not to be filled by the controller.
Approval record (exact candidate SHA; attributable decision source; label any controller transcription as such):

- Approved by (Architect): NOT APPROVED
- Candidate SHA: 
- Decision source: 
- Date: 
- Git reference (commit/PR): 

## Unresolved before approval

Each item below must be resolved before this Work Order is merged or dispatched. An unresolved placeholder prohibits approval.

1. Independent review of the final head by an auditor who is not the implementer or drafter, with exact-head CI and secret scan results.
2. Re-verify the GOAL base SHA immediately before merge and dispatch; if main has moved, reconcile and re-audit any material change.
3. Explicit Architect acceptance of the exact final head, recorded on GOAL pull request #46.
4. Confidential access arrangement: HELM's designated security custodian grant (scoped, read-only, auditable, limited to the independent technical auditor), and any explicit owner authorisation required by existing authority. No such grant exists or is claimed. This item may remain pending while the other Work Orders proceed; it blocks dispatch of the private checks.

Resolved by the Architect directive of 19 October 2026 (recorded on PR #46): access grantor is HELM's designated security custodian; public digest of canonical public wording only, with the not-proof disclaimer; pseudonym or role-identifier attribution with traceable restricted record; criterion 7 records are safe pass or fail outcomes only; the ambiguous grep-outcome wording is replaced; Delivery Controller is ROGUE; implementer and auditor identifiers assigned as above.

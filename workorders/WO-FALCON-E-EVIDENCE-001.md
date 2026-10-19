# Work Order WO-FALCON-E-EVIDENCE-001

**Conditional authority.** This file is candidate text and confers no authority by itself. It becomes executable authority solely by (a) an attributable, exact-head Architect acceptance record in GOAL pull request #44 that names the candidate head commit SHA, followed by (b) merge of that exact head into GOAL main (governance sections 7.2 and 7.5). Until both have occurred nothing in this file is approved, and dispatch is barred. This file does not and cannot contain an approval of itself or its own commit SHA: the approval record is external (field 12) and the merge commit on GOAL main is the activation evidence. The gates in "Authority gates" at the end of this file must each be actually satisfied; none is satisfied by assertion.

Governing document: `maff0000/GOAL` `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and template `templates/WORK-ORDER.md`, at GOAL main commit `3f2f100ea27f515689d1fa05fa815956a396f730` (merge of GOAL pull request #42). The authoritative record of this Work Order is this file in `maff0000/GOAL` at `workorders/WO-FALCON-E-EVIDENCE-001.md`; the work itself targets `maff0000/falcon`. The mandatory dispatch preamble (governance section 6) is not copied here.

**Work Order ID:** WO-FALCON-E-EVIDENCE-001

## 1. Approved parent PID and applicable amendments

- Parent PIDs: GOLD-AUD-E (`pids/GOLD-AUD-E.md`) and GOLD-AUDIT-CLOSEOUT-001 (`pids/GOLD-AUDIT-CLOSEOUT-001.md`).
- Applicable amendment: GOLD-AUD-E dated PID amendment of 17 October 2026 (GOAL pull request #31, merge commit `b5752fd6adb6ef0fa6d64bf26af05c556bdc04f1`). The amendment reassigns the FALCON outage rehearsal to `GOLD-MVP-001` AC-12 and states that running ingestion remains UNVERIFIED wherever it was not observed.
- Governance: `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` at GOAL main `3f2f100ea27f515689d1fa05fa815956a396f730`.
- Acceptance criteria 1 and 3 of `pids/GOLD-AUD-E.md` are NOT waived by this Work Order. Both must be met as written.

## 2. Target repository and exact base SHA

Target repository: `maff0000/falcon`  
Exact base SHA: `7734856596085200967b94a79ff4faa697633878` (the merge commit of falcon pull request #21). Re-verified against GitHub when this version was drafted: it is still the head of falcon `main` and is the merge commit of that pull request.

This Work Order file is recorded in `maff0000/GOAL`, whose base when this version was drafted is `d7bffec206bf58057e4742edc1611f6ecced5d19` (GOAL main after the merge of pull request #43, which itself sits on `3f2f100ea27f515689d1fa05fa815956a396f730`). Both bases were re-verified against GitHub on 19 October 2026 (falcon `main` is `7734856596085200967b94a79ff4faa697633878`; GOAL `main` is `d7bffec206bf58057e4742edc1611f6ecced5d19`). The falcon base must be verified again immediately before approval and again before dispatch (Architect directive of 19 October 2026, section 3).

## 3. Permitted paths

In `maff0000/falcon`, these named files only, all under `docs/evidence/GOLD-AUD-E/`:

- `EP-09-outside-the-path.md`
- `EP-02-running-ingestion-record.md`
- `AUDIT-LOG.md` (a new command class must be logged; see field 4)
- `README.md` and `UNVERIFIED.md`, only if needed to stay consistent with the two corrections
- `DOCUMENTATION-MANIFEST.json` (repository root), only if a file is added or removed; no file is expected to be added or removed

## 4. Scope

Documentation-only. Correct two evidence defects in the GOLD-AUD-E evidence set, using independently reproducible historical source reads. The exact missing items are:

1. **Acceptance criterion 1 of `pids/GOLD-AUD-E.md` (EP-09, and EP-02 for its evidence-column SHA).** `EP-09-outside-the-path.md` cites repository paths and line numbers (for example the HELIOS publisher lines, the TRON design documents, `docs/contracts/TRON-FALCON-CONTRACT.md`) but names no repository and no commit SHA at the citation. Each citation must carry `repository@full-SHA`. Full 40-hex SHAs only; no abbreviation. The mapping, verified against the falcon `docs/evidence/GOLD-AUD-E/README.md` revision table, `AUDIT-LOG.md` rows 2 and 3 and local clones when first drafted, and re-checked against GitHub when this version was drafted (each SHA resolves in its repository), is:
   - falcon documents, registry, schemas, CI: `maff0000/falcon@8f218ec1b85b932285b042a7b1ae64dbd11eebee`;
   - HELIOS source (publication surface, failure semantics): `maff0000/HELIOS@7f7193d55475e40583892b94dd461b1b64d6f1ef`;
   - TRON design documents `docs/03-ARCHITECTURE.md`, `docs/06-CHECKS-CATALOGUE.md`, `docs/09-EVENTS-AND-GRAYLOG.md`: these exist only at the BRANCH commit `maff0000/tron@37d5f009a080d25930eea37cf8c627bb0f3a1ff4` (branch `wo/WO-TRON-D1`). It is a branch commit, not main. At this drafting the three paths resolve at that commit and return not-found on tron `main`. The citation must say so;
   - TRON `PID.md`: `maff0000/tron@5577039b5db05e70effef72c7e59df14db408419`. This was tron `main` when the evidence was produced; tron `main` has since moved (it is now `765ad7a3c2719ea157ce47b4d09cbf1191bea76d`) and the cited commit is an ancestor of it. The citation names the commit, not "main".

   Completeness (Architect decision, 19 October 2026): the check is not limited to added or changed lines. The implementer reviews EVERY factual citation in the whole of `EP-02-running-ingestion-record.md` and `EP-09-outside-the-path.md` (each repository path, line number, document reference, commit or file claim) and confirms that each carries `repository@full-SHA`, resolves at that SHA, and exists at the cited path and line. The result is a complete citation table (file, citation, repository, full SHA, resolves yes/no) in the pull request. Branch-only TRON design documents must cite their verified exact commit and must never be represented as files on `main`. Historical source records must remain distinct from actual current runtime observations; nothing in either file may blur the two.

   The implementer re-verifies each SHA and each cited path at that SHA before writing it. A citation whose full SHA cannot be verified from the README, the AUDIT-LOG or the repository itself is not given a SHA by guesswork; it is recorded in `UNVERIFIED.md`. No previously present citation is removed.
   Audit basis for the scope of criterion 1 (scan performed by the drafting worker, read-only, on a clone of `maff0000/falcon` checked out at `7734856596085200967b94a79ff4faa697633878`, over all files `docs/evidence/GOLD-AUD-E/EP-*.md`; pattern: any 40-character lowercase hexadecimal string, then each hit read in context to confirm it is qualified by a repository name):
   - EP-01, EP-03 (`EP-03-registry-matrix.md`), EP-04, EP-05, EP-06, EP-07, EP-08 and EP-10 each carry at least one repository-qualified full 40-hex SHA (falcon `8f218ec1b85b932285b042a7b1ae64dbd11eebee`; in addition HELIOS `7f7193d55475e40583892b94dd461b1b64d6f1ef` in EP-04 and EP-07; TRON `5577039b5db05e70effef72c7e59df14db408419` and branch `wo/WO-TRON-D1` `37d5f009a080d25930eea37cf8c627bb0f3a1ff4` in EP-05; GOAL branch `wo/GOAL-CONTRACT-TRIGGER` `64c843b901d435a17efa56e3b2a1f925ad58c30b` in EP-08). Abbreviated forms also appear in EP-01, EP-04, EP-05 and EP-08 alongside the full ones; they are not changed by this Work Order.
   - EP-09 carries NO 40-hex SHA of any kind (zero hits). This is the defect named by criterion 1.
   - EP-02 carries NO 40-hex SHA (zero hits); its only SHA reference is the abbreviated `8f218ec` in the table header "Evidence (path, SHA `8f218ec`)". It therefore also lacks a repository-qualified full SHA and is ADDED to the scope of criterion 1 by this version. This EP-02 scope addition rests on the full-SHA standard adopted by this Work Order, not on the literal wording of PID criterion 1 (`pids/GOLD-AUD-E.md` line 248: "each with at least one cited repository path and commit SHA"), and was CONFIRMED by the Architect on 19 October 2026. The change is limited to the repository-qualified full SHA `maff0000/falcon@8f218ec1b85b932285b042a7b1ae64dbd11eebee` at the table header (and wherever the abbreviated form is used for a citation in that file); `EP-02-running-ingestion-record.md` is already a permitted path. The abbreviated `8f218ec` is the falcon pull request #20 merge commit as recorded in `EP-01-delivered-inventory.md`; the implementer re-verifies that it expands to the stated full SHA before writing it.
   - Outstanding provenance finding (outside the permitted paths; not repaired by this Work Order): the GOAL branch commit `64c843b901d435a17efa56e3b2a1f925ad58c30b` (branch `wo/GOAL-CONTRACT-TRIGGER`) cited in `EP-05` and `EP-08` does not resolve on GitHub in GOAL, falcon or tron at the time of the independent review of 19 October 2026. EP-05 and EP-08 are not permitted paths. The implementer must NOT invent or substitute a replacement SHA, and must not expand the repair. The finding is carried forward to the Architect for separately governed disposition.
   - `EP-03-registry-matrix.table.md` (the generated table companion of EP-03) carries no SHA; the EP-03 file itself carries the falcon full SHA in its header and the README revision table lists the two files as one evidence item (EP-3). It is not made a permitted path here. Architect decision, 19 October 2026: it stays outside scope and is left unchanged.
   - Net result: of EP-01 to EP-10, the files lacking a repository-qualified full SHA are EP-02 and EP-09; the other eight carry one.

2. **Acceptance criterion 3 of `pids/GOLD-AUD-E.md` (EP-02).** In `EP-02-running-ingestion-record.md`, each claim row of the table "What source and committed evidence do establish" (and the "Legacy-stack exclusion" row, which is a source claim) lacks a read-only command and a captured output excerpt. Each such row needs: the exact command, run read-only against a historical clone at `maff0000/falcon@8f218ec1b85b932285b042a7b1ae64dbd11eebee` (git, and python or jq parsing only), and an output excerpt without secrets, hostnames or addresses. The commands are NEVER run against a running FALCON, Graylog, container or host service. Named caution for the EP-02 rows that cite earlier runtime acceptance records and the identity-spoof report (the rows citing `docs/operations/FALCON-PID06-RUNTIME-ACCEPTANCE-EVIDENCE.md` s3 to s5 and s7, and the row citing `tests/fte/last_run_report_pid04.json`): for these rows the command must be a read of the committed record at the historical SHA only (for example `git show maff0000/falcon@8f218ec1b85b932285b042a7b1ae64dbd11eebee:<path>` or parsing the committed file), and the output excerpt must be presented as an excerpt of the committed historical record. An excerpt must not read as an observation of a live system, as a current-state statement, or as a statement that the recorded runtime event was re-observed; the wording must keep the existing labels "PROVEN as a record; not re-observed" and "says nothing about today's runtime".

   Rows already in the UNVERIFIED table (container names, status and labels; systemd; steady-state publishing; message counts and live configuration, i.e. U1 to U4) need no command and stay UNVERIFIED.
3. **Audit log.** `AUDIT-LOG.md` must record every added command (new rows, dated, stating that these are correction-run commands against the historical clone at the stated SHA, with the read-only class). A new command class must be logged; none may be run unlogged.

Each correction must be reproducible by an independent reader from historical source reads at stated SHAs. Any observation that cannot be reproduced stays recorded as UNVERIFIED. A README reference must not be substituted for the required command and output excerpts. Nothing added may state or suggest that any runtime, live-service or host inspection took place.

## 5. Exclusions

- No FALCON runtime access, and no command against any running service.
- No ingestion changes.
- No producer changes.
- No outage rehearsal.
- No change outside the permitted paths (no edits to `registry/`, `schemas/`, `deploy/`, `tests/`, CI files or any other evidence file).
- No waiver of acceptance criterion 1 or 3 of `pids/GOLD-AUD-E.md`.
- Unsupported observations remain UNVERIFIED; none is promoted to a verified statement by this Work Order.
- `docs/evidence/GOLD-AUD-E/VERDICT.md` is OUT OF SCOPE (Architect decision, 19 October 2026). Its stale "pending" status is recorded here as an OUTSTANDING ACCEPTANCE BLOCKER for the GOLD-AUD-E evidence set, to be reconciled under a separately governed Work Order. This Work Order does not resolve it, and its completion does not make the lane E evidence set acceptable while that blocker stands.

## 6. Required tests (including negative tests)

- Exact source-SHA checks: every cited SHA is a full 40-hex SHA, resolves in the stated repository, and the cited path exists at that SHA (for the TRON design documents, at the branch commit named above).
- Negative tests: (a) in EVERY factual citation in EP-09 and EP-02 (the whole files, not only added or changed lines), an abbreviated SHA, a SHA that does not resolve, or a citation that names a branch or "main" instead of a commit, or that presents a branch-only TRON document as a file on `main`, fails the check; an untouched citation with no repository and full SHA also fails; (b) a claim row with no command or no output excerpt, and not in the UNVERIFIED table, fails the check; (c) a grep over added text for IPv4 addresses, ports, hostnames, account identifiers and key-like strings returns nothing; (d) a grep over added text for wording that states or implies runtime, live-service or host inspection returns nothing.
- Evidence reproducibility: each added command, run read-only against the historical clone at the cited SHA by an independent party, reproduces the quoted output excerpt.
- The falcon CI jobs that actually exist in `.github/workflows/ci.yml` at the base SHA pass at the exact head:
  - job `repository-foundation`: required top-level structure check, `DOCUMENTATION-MANIFEST.json` cross-check against the working tree, internal Markdown link check, and the gitleaks secret scan;
  - job `contract-registry-foundation`: the FALCON validator test suite (`python3 -m unittest discover -s tests -p "test_*.py"`) and the validator CLI report (`python3 -m tests.validator.cli`).

  There is no lint job in falcon CI; none is required here. (Re-verified from `.github/workflows/ci.yml` at `7734856596085200967b94a79ff4faa697633878`.)
- Secret scan, run on the falcon branch (the gitleaks step above, and a local run before the pull request).

## 7. Acceptance criteria

1. Acceptance criterion 1 of `pids/GOLD-AUD-E.md` is independently reproducible for EP-09 and for the EP-02 evidence-column SHA (the two files found by the audit basis in field 4 to lack a repository-qualified full SHA): EVERY factual citation in the whole of both files (not only changed lines) carries `repository@full-SHA`, resolves, and is shown in the complete citation table; branch-only TRON documents cite their verified exact commit and are never represented as on `main`; no previously present citation is removed.
2. Acceptance criterion 3 of `pids/GOLD-AUD-E.md` is independently reproducible for EP-02: every claim row carries a read-only command and a secret-free output excerpt, or sits in the UNVERIFIED table with the reason; `AUDIT-LOG.md` records the commands.
3. Only the permitted paths are changed (`git diff --stat` shown in the pull request); `VERDICT.md` is unchanged and its stale status is carried forward as an outstanding acceptance blocker.
4. No secret, address or account identifier appears in any added text, and no added text states or implies that runtime inspection took place.
5. Independent technical audit and independent public-safety audit both pass at the exact final head, by an auditor who is not the implementer. A material modification after audit requires renewed independent assurance.
6. Architect acceptance is recorded before merge. Passing CI is not Architect acceptance. Independent audit and Architect acceptance are cumulative, not alternatives.

## 8. Assigned implementer

Assigned by the Delivery Controller (controller assignment of 19 October 2026, recorded under the Architect directive of that date): implementer instance identifier `FORGE-IMPL-WO-FALCON-E-EVIDENCE-001-A`, a FORGE implementer instance. It is launched only after this Work Order is merged into GOAL main, against this Work Order alone. The identifier is a role label; the launch record (session and model identity) will be added to the pull request evidence at dispatch.

## 9. Independent auditor (not the implementer)

Assigned by the Delivery Controller (controller assignment of 19 October 2026). Independent technical auditor identifier `FORGE-AUD-TECH-WO-FALCON-E-EVIDENCE-001-B`; independent public-safety auditor identifier `FORGE-AUD-SAFE-WO-FALCON-E-EVIDENCE-001-C`. Both are separate instances from the implementer and from each other, and neither may be the drafter or implementer of this Work Order. Public attribution uses these stable role identifiers; the actual session identities are traceable in a restricted audit record kept by the Delivery Controller and recorded when each audit is performed.

## 10. Delivery Controller

ROGUE (confirmed by the Architect, 19 October 2026, directive section 6; governance rule 8).

## 11. Stop conditions

Architectural ambiguity; change of risk authority; uncontrolled production access (including any need to run a command against a running service); credential exposure; incompatible contract assumption; implementation that would fall outside this Work Order's scope; falcon `main` no longer matching the base SHA at dispatch; a citation SHA that cannot be verified; absence of any required authority. On any of these, stop and return the precise missing item or finding to the Architect (governance section 5).

## 12. Expected GitHub evidence, pull request and approval record

Expected evidence and pull request: one pull request into `maff0000/falcon` from a branch named for this Work Order, whose diff touches only the permitted paths; the PR body shows `git diff --stat` and the SHA verification results; falcon CI results (both jobs) at the exact head; the independent technical audit and the independent public-safety audit, each recorded against the exact head; post-merge main CI verification after Architect-accepted merge.  
External approval record (conditional authority model). Approval of this Work Order exists only if both of the following exist, and not otherwise:

1. An attributable Architect acceptance record in GOAL pull request #44 (a review or comment by the Architect) that names the exact candidate head commit SHA accepted and its decision source. A controller transcription of an acceptance is not an Architect action and must be labelled as a transcription (governance section 7.5).
2. Merge of that exact head into GOAL main. The resulting merge commit is the activation evidence.

This file contains no approval fields to fill, no "approved" statement and no SHA of its own commit. If no such record exists, this Work Order is not approved, whatever any other message, local file or CI result says. The pull request body points to the current candidate head and to the acceptance record once it exists.

## Authority gates

Every gate must be actually satisfied, with the evidence named, before the step it guards. A gate that is unsatisfied, unverifiable or satisfied only by assertion blocks that step. Satisfaction is recorded in GOAL pull request #44 (merge gates) or in the dispatch pull request (dispatch gates), not in this file.

Pre-merge gates (all required before this Work Order is merged into GOAL main):

- G1. Independent technical audit and independent public-safety audit of the exact final head, by auditors who are not the drafter or the implementer. A material change after audit requires renewed audit. Evidence: audit records against the exact head SHA.
- G2. Exact-head CI success and a clean secret scan on the same head. CI success is not Architect acceptance.
- G3. Base verified: GOAL main equals the base recorded for the candidate at merge time. If main has moved, reconcile against the new main, independently review any material base or manifest change, and obtain fresh Architect acceptance of the new exact head.
- G4. Explicit Architect acceptance of the exact head, recorded in GOAL pull request #44 as described in field 12, before merge. The merge is pinned to that head.

Pre-dispatch gates (all required before any implementer is dispatched):

- P1. This Work Order is merged into GOAL main and main CI on the merge commit is verified.
- P2. GOAL main is re-verified at dispatch, and falcon `main` is re-verified against the falcon base SHA in field 2 (`7734856596085200967b94a79ff4faa697633878`) immediately before dispatch. On any mismatch, stop and return to the Architect.
- P3. Actual instance and session identities of the implementer and both auditors are recorded in the dispatch pull request, and their separation is verified. The role identifiers in fields 8 and 9 are prospective assignments only.
- P4. The mandatory dispatch preamble of governance section 6 is included in the dispatch prompt.
- P5. Permitted paths (field 3) and exclusions (field 5) are enforced. Any stop condition in field 11 stops work and is returned to the Architect. The `VERDICT.md` stale status remains an outstanding acceptance blocker for separately governed reconciliation, and the provenance finding in field 4 remains outstanding.

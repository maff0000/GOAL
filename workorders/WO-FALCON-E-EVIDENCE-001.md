# Work Order WO-FALCON-E-EVIDENCE-001

**DRAFT — not approved, not dispatched; Architect acceptance and merge into GOAL main required before it is executable authority.** This file authorises no work. An open pull request, a local file, a conversation approval or a candidate branch is insufficient (governance section 7.2). Dispatch is barred until the Approval record in field 12 is complete, the "Unresolved before approval" list is empty, and this Work Order is merged into GOAL main.

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

This Work Order file is recorded in `maff0000/GOAL`, whose base when this version was drafted is `3f2f100ea27f515689d1fa05fa815956a396f730`.

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

   The implementer re-verifies each SHA and each cited path at that SHA before writing it. A citation whose full SHA cannot be verified from the README, the AUDIT-LOG or the repository itself is not given a SHA by guesswork; it is recorded in `UNVERIFIED.md`. No previously present citation is removed.
   Audit basis for the scope of criterion 1 (scan performed by the drafting worker, read-only, on a clone of `maff0000/falcon` checked out at `7734856596085200967b94a79ff4faa697633878`, over all files `docs/evidence/GOLD-AUD-E/EP-*.md`; pattern: any 40-character lowercase hexadecimal string, then each hit read in context to confirm it is qualified by a repository name):
   - EP-01, EP-03 (`EP-03-registry-matrix.md`), EP-04, EP-05, EP-06, EP-07, EP-08 and EP-10 each carry at least one repository-qualified full 40-hex SHA (falcon `8f218ec1b85b932285b042a7b1ae64dbd11eebee`; in addition HELIOS `7f7193d55475e40583892b94dd461b1b64d6f1ef` in EP-04 and EP-07; TRON `5577039b5db05e70effef72c7e59df14db408419` and branch `wo/WO-TRON-D1` `37d5f009a080d25930eea37cf8c627bb0f3a1ff4` in EP-05; GOAL branch `wo/GOAL-CONTRACT-TRIGGER` `64c843b901d435a17efa56e3b2a1f925ad58c30b` in EP-08). Abbreviated forms also appear in EP-01, EP-04, EP-05 and EP-08 alongside the full ones; they are not changed by this Work Order.
   - EP-09 carries NO 40-hex SHA of any kind (zero hits). This is the defect named by criterion 1.
   - EP-02 carries NO 40-hex SHA (zero hits); its only SHA reference is the abbreviated `8f218ec` in the table header "Evidence (path, SHA `8f218ec`)". It therefore also lacks a repository-qualified full SHA and is ADDED to the scope of criterion 1 by this version. This EP-02 scope addition rests on the full-SHA standard adopted by this Work Order, not on the literal wording of PID criterion 1 (`pids/GOLD-AUD-E.md` line 248: "each with at least one cited repository path and commit SHA"), and needs Architect confirmation. The change is limited to the repository-qualified full SHA `maff0000/falcon@8f218ec1b85b932285b042a7b1ae64dbd11eebee` at the table header (and wherever the abbreviated form is used for a citation in that file); `EP-02-running-ingestion-record.md` is already a permitted path. The abbreviated `8f218ec` is the falcon pull request #20 merge commit as recorded in `EP-01-delivered-inventory.md`; the implementer re-verifies that it expands to the stated full SHA before writing it.
   - `EP-03-registry-matrix.table.md` (the generated table companion of EP-03) carries no SHA; the EP-03 file itself carries the falcon full SHA in its header and the README revision table lists the two files as one evidence item (EP-3). It is not made a permitted path here. Proposed resolution for Architect confirmation: leave it unchanged.
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
- `docs/evidence/GOLD-AUD-E/VERDICT.md` is OUT OF SCOPE. Its stale "pending" wording is an Architect decision: it is included only if the Architect adds it to this Work Order before approval.

## 6. Required tests (including negative tests)

- Exact source-SHA checks: every cited SHA is a full 40-hex SHA, resolves in the stated repository, and the cited path exists at that SHA (for the TRON design documents, at the branch commit named above).
- Negative tests: (a) in the citations added or changed by this Work Order in EP-09 and EP-02, an abbreviated SHA, a SHA that does not resolve, or a citation that names a branch or "main" instead of a commit fails the check; (b) a claim row with no command or no output excerpt, and not in the UNVERIFIED table, fails the check; (c) a grep over added text for IPv4 addresses, ports, hostnames, account identifiers and key-like strings returns nothing; (d) a grep over added text for wording that states or implies runtime, live-service or host inspection returns nothing.
- Evidence reproducibility: each added command, run read-only against the historical clone at the cited SHA by an independent party, reproduces the quoted output excerpt.
- The falcon CI jobs that actually exist in `.github/workflows/ci.yml` at the base SHA pass at the exact head:
  - job `repository-foundation`: required top-level structure check, `DOCUMENTATION-MANIFEST.json` cross-check against the working tree, internal Markdown link check, and the gitleaks secret scan;
  - job `contract-registry-foundation`: the FALCON validator test suite (`python3 -m unittest discover -s tests -p "test_*.py"`) and the validator CLI report (`python3 -m tests.validator.cli`).

  There is no lint job in falcon CI; none is required here. (Re-verified from `.github/workflows/ci.yml` at `7734856596085200967b94a79ff4faa697633878`.)
- Secret scan, run on the falcon branch (the gitleaks step above, and a local run before the pull request).

## 7. Acceptance criteria

1. Acceptance criterion 1 of `pids/GOLD-AUD-E.md` is independently reproducible for EP-09 and for the EP-02 evidence-column SHA (the two files found by the audit basis in field 4 to lack a repository-qualified full SHA): every citation carries `repository@full-SHA`, and no previously present citation is removed.
2. Acceptance criterion 3 of `pids/GOLD-AUD-E.md` is independently reproducible for EP-02: every claim row carries a read-only command and a secret-free output excerpt, or sits in the UNVERIFIED table with the reason; `AUDIT-LOG.md` records the commands.
3. Only the permitted paths are changed (`git diff --stat` shown in the pull request); `VERDICT.md` is unchanged unless the Architect added it before approval.
4. No secret, address or account identifier appears in any added text, and no added text states or implies that runtime inspection took place.
5. Independent technical audit and independent public-safety audit both pass at the exact final head, by an auditor who is not the implementer. A material modification after audit requires renewed independent assurance.
6. Architect acceptance is recorded before merge. Passing CI is not Architect acceptance. Independent audit and Architect acceptance are cumulative, not alternatives.

## 8. Assigned implementer

Not yet named. The implementer is a FORGE instance to be assigned by the Delivery Controller. A named implementer is required before approval and is listed under "Unresolved before approval". It is not a permitted placeholder at approval.

## 9. Independent auditor (not the implementer)

Not yet named. Required: an independent FORGE Auditor who is not the implementer, for the technical audit, and a separate independent public-safety audit. Each named identity is recorded in the Approval record before approval. Listed under "Unresolved before approval"; no name is invented in this draft.

## 10. Delivery Controller

ROGUE (Proposed resolution for Architect confirmation: governance rule 8 gives ROGUE control of dispatch and delivery coordination; the Architect confirms the identity in the Approval record).

## 11. Stop conditions

Architectural ambiguity; change of risk authority; uncontrolled production access (including any need to run a command against a running service); credential exposure; incompatible contract assumption; implementation that would fall outside this Work Order's scope; falcon `main` no longer matching the base SHA at dispatch; a citation SHA that cannot be verified; absence of any required authority. On any of these, stop and return the precise missing item or finding to the Architect (governance section 5).

## 12. Expected GitHub evidence, pull request and approval record

Expected evidence and pull request: one pull request into `maff0000/falcon` from a branch named for this Work Order, whose diff touches only the permitted paths; the PR body shows `git diff --stat` and the SHA verification results; falcon CI results (both jobs) at the exact head; the independent technical audit and the independent public-safety audit, each recorded against the exact head; post-merge main CI verification after Architect-accepted merge.  
Approval record (exact candidate SHA; attributable decision source; label any controller transcription as such):

- Approved by (Architect): NOT APPROVED
- Candidate SHA: 
- Decision source: 
- Date: 
- Git reference (commit/PR): 

## Unresolved before approval

Each item below must be resolved and recorded before this Work Order can be approved. An unresolved placeholder prohibits approval.

1. Implementer: not named (to be assigned by the Delivery Controller).
2. Named independent technical auditor identity (not the implementer).
3. Named independent public-safety auditor identity.
4. Delivery Controller identity: confirmation of ROGUE.
5. Architect decision on whether `VERDICT.md` is added to the permitted paths (field 3 and field 5). Also for Architect confirmation: the EP-02 scope addition in field 4 item 1 rests on the full-SHA standard adopted by this Work Order, not on the literal wording of PID criterion 1 (`pids/GOLD-AUD-E.md` line 248: "each with at least one cited repository path and commit SHA").
6. Re-verify the GOAL base SHA and the falcon base SHA at approval (falcon `7734856596085200967b94a79ff4faa697633878`, GOAL `3f2f100ea27f515689d1fa05fa815956a396f730`).
7. Independent review of this Work Order, and explicit Architect acceptance.

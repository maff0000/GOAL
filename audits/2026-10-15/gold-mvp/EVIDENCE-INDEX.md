# GOLD MVP cross-component evidence index

Owned by `GOLD-MVP-001`. Single writer: the `GOLD-MVP-001` programme lead. One lane is contributed per audited GOAL pull request, merged serially (`pids/GOLD-MVP-001.md`, contribution rule for deliverables 2 and 3). The companion file is `COMPATIBILITY-MATRIX.md`; there is no second matrix.

## What this file is and is not

* It records, per lane: exact merged references, the independent verdicts and the heads they were given against, provenance, findings, the acceptance criteria that are not satisfied, and the owner who closes each.
* It is **not** an acceptance, closure or approval record. Lane acceptance is a Central Architecture / PO decision recorded in the backlog state; a lane in `PO_ACCEPTANCE` is not accepted-terminal and satisfies no dependency.
* It does **not** equate a research report with an implemented component: every UNPROVEN, UNVERIFIED or MISSING finding stays open here even where its source audit is accepted.
* Statements that Central Architecture accepted something are by reference to the dated directives of 16 and 17 October 2026, which are not held in this repository.
* Confidential findings are held in the private record and appear here at class level only, if at all. Confirmed absence in this file is not confirmation of absence elsewhere.

## Vocabulary

* Criterion result: `MET` (cross-reference given), `NOT MET`, `NEEDS CA RULING`, or `NOT RE-VERIFIED HERE` (the lane's own record or an auditor's report is relied on and this entry did not repeat the check).
* Verdicts: technical `GREEN` / `GREEN-WITH-NOTICE` / `RED`; public-safety `SAFE` / `SAFE-WITH-REDACTIONS` / `UNSAFE`. The audit reports themselves are held outside the repository by the programme controller; the verdicts are recorded in the pull request bodies.
* Finding ids are each lane's own. Severity, class and label are as the lane assigned them.
* Verdict source: each verdict row says whether it is stated in a public pull request body or is a **controller record** (held by the programme controller, not in the public pull request). A split of verdicts across successive heads is derived from controller records unless the row says otherwise. Results marked "independent verification" were returned by the independent audit of this contribution stack.

## Pointers for the historical-document hygiene review (DR-38)

Already-merged lane C and lane D files cite an unpublished local commit and, at class level, touch elements of a candidate contract that is not published. This index does not repeat those elements. The pointer is for the DR-38 review to assess; it is not a finding that anything is unsafe.

## Lane D: GOLD-AUD-D (TRON and MT5 minimum DEMO execution path)

Backlog item `GOLD-AUD-D`, state at contribution `PO_ACCEPTANCE`. Closing owner for the lane's open findings: see the last column of the findings table. Acceptance decision: none recorded in this file.

### References

| Repository | PR | Audited head | Merge commit |
|---|---|---|---|
| `maff0000/GOAL` (primary evidence) | #14 | `2227de266e90c2acfbbc8a77be95d794d0e2a6b6`, then `b9674fed0c12343bbcb917830c11b52d8d2ec7b9` (wording corrections) | `fbfc83cfffe1431f6c482fdaaec4a7204557fe28` |
| `maff0000/tron` (mirror note) | #2 | `3f31b3b87728100f822e32a861ae889d4bbeaefe`, then `dc6448edbcfa10d425ec012ec989a1680f8a37b4` | `765ad7a3c2719ea157ce47b4d09cbf1191bea76d` |
| `maff0000/mt5-gateway` (mirror note) | #11 | `2c5b5fb1feeb5357e1d7df5c467496f1aaad9eed`, then `b65cc8e9f3fc1804bf00c89e4ddea2615a796102` | `5fb591af850b64b9d04304589671ea2b7f3710c9` |

Lane files: `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/` (`BASELINE`, `GAP-MATRIX`, `CANDIDATES`, `TRIGGER-ASSUMPTIONS`, `INCREMENTS`, `PROOF-CLASSES`, `ORDERING`, `FINDINGS`, `DISPOSITION`, `EVIDENCE-HASHES.txt`, `README`). Mirror notes: `docs/evidence/GOLD-AUD-D/TRON-FACTS.md` and `MT5-FACTS.md`. Main CI after each merge: GOAL success, mt5-gateway success, tron has no CI configured.

### Independent verdicts

| Subject | Head | Technical | Public-safety | Source |
|---|---|---|---|---|
| GOAL #14, mt5-gateway #11, tron #2 ("final heads") | not named in the PR body | GOAL `GREEN-WITH-NOTICE`, mt5-gateway `GREEN`, tron `GREEN-WITH-NOTICE` | `SAFE` on all three | PR #14 body |
| GOAL #14 pre-publication | `2227de26` | `GREEN-WITH-NOTICE` | `SAFE` | controller record |
| GOAL #14 corrections (delta) | `b9674fed` | `GREEN-WITH-NOTICE` | `SAFE` | controller record |
| mt5-gateway #11 corrections (delta) | `b65cc8e9` | `GREEN` | `SAFE` | controller record |
| tron #2 corrections (delta) | `dc6448ed` | `GREEN-WITH-NOTICE` (the PR #14 body value; the controller delta report gave `GREEN`) | `SAFE` | PR #14 body; controller record |

The split of the GOAL #14 verdict across the two heads is derived from controller reports, not from the PR body, which names "final heads" only.

Recorded notices: class-level references to one withheld item remain in the public set (accepted by Central Architecture as class-level audit evidence, subject to the renewed safety review under DR-38); earlier published commits keep their original wording.

### Provenance

Read-only audit by the GOLD-AUD-D forge worker on 15 to 16 October 2026. The signed statement in `FINDINGS.md` section 1 records no broker contact, no bridge connection, no legacy-executor interaction and no credential read. Evidence hashes: `EVIDENCE-HASHES.txt` (all in-repository entries verify with `sha256sum -c`; checked again for this entry). Sources were read at the revisions recorded in `BASELINE.md`.

### Findings (by id; full text in `FINDINGS.md`)

| Id | Severity | Class | Summary | Status at this contribution | Closing owner |
|---|---|---|---|---|---|
| F-D-01 | MAJOR | PROVEN | `TRON-T3A` / `TRON-T3` extension not expressed in the backlog | addressed by GOAL #16 (merge `2c90eb3f`); recorded, not closed by this lane | CA / ROGUE |
| F-D-02 | MINOR | PROVEN | `TRON-T3A` scope carries the six required elements, needs no credential | informational | none |
| F-D-03 | MAJOR | PROVEN | TRON D1 unmerged, no recorded auditor verdict or owner acceptance | open | `TRON-D1-RATIFY` (Matt gate) |
| F-D-04 | MAJOR | PROVEN | D1 check set has no exposure, position-count, size, loss or drawdown gate | open | `TRON-T3A` / `TRON-T3` |
| F-D-05 | MAJOR | PROVEN | check-promotion list not self-sufficient; no one-position gate | open | `TRON-T3A` |
| F-D-06 | MINOR | PROVEN | trade-count limit key has no configuration home | open | `TRON-T3A` |
| F-D-07 | MAJOR | PROVEN (absence) | no stop or take-profit distance policy owner | scope now stated in the approved `TRON-T3A` PID; implementation open | `TRON-T3A` |
| F-D-08 | MINOR | INFERRED | negotiation (symbol and quantity mapping) has no named backlog item | open | CA / PO |
| F-D-09 | MINOR | PROVEN | gateway backlog states drifted from merged content | open | ROGUE (backlog) |
| F-D-10 | MAJOR | PROVEN | no in-container DEMO latch in the gateway | open | mt5-gateway items |
| F-D-11 | BLOCKER (any TRON integration) | PROVEN | no typed gateway; only the unrestricted control surface exists | open | mt5-gateway items |
| F-D-12 | MAJOR | PROVEN | D1 has no signature or key-trust concept | open | `GOAL-TRIGGER-001` / TRON intake |
| F-D-13 | MINOR | PROVEN | D1 secret-scan commit counts unexplained | open | TRON |
| F-D-14 | MAJOR | INFERRED | several stop-like states; single-kill-state rule needs enforcement | scope stated in `TRON-T3A` PID; implementation open | `TRON-T3A` |
| F-D-15 | MAJOR (stop condition) | PROVEN | one finding withheld; handled in the private record, no particulars here | open, private | private-record handling; owner per Central Architecture |
| F-D-16 | MINOR | PROVEN | one legacy tool assessed as lessons only | informational | none |
| F-D-17 | MAJOR | UNPROVEN | `HELIOS-T3` has no PID; signing assumptions not stated by the holder | open | HELIOS architect |
| F-D-18 | MINOR | PROVEN | stale statements in cited documents | informational | none |
| F-D-19 | MINOR | PROVEN | example sizing is for a different instrument | open | `TRON-T3A` (Matt-gated values) |
| F-D-20 | MINOR | UNPROVEN | one legacy executor source not located | open | PO / operations |
| F-D-21 | MINOR | PROVEN | seven cited documents exist only on local branches | open | PO |
| F-D-22 | MINOR | UNPROVEN | exposure statements in gateway limitations not re-verified | open | PO-authorised probe |

### Original acceptance criteria (`pids/GOLD-AUD-D.md`, Acceptance 1 to 12)

| # | Result | Cross-reference for an independent verifier |
|---|---|---|
Results are those of the independent verification of this contribution.

| # | Result | Cross-reference for an independent verifier |
|---|---|---|
| 1 | MET | `goal-validate` and `secret-scan` clean at GOAL #14 head `b9674fed` and on main `fbfc83cf`; CI success on the merge |
| 2 | MET | deliverables 1 to 9 exist in the lane directory, all non-empty |
| 3 | MET | `GAP-MATRIX.md` has 35 rows over hops H1 to H6 (at least 24 required; 18 `missing`, 17 `partial`, 0 `exists`); no blank cell |
| 4 | MET | no uncited `partial` row |
| 5 | MET | all 17 increments (INC-01 to INC-17) have a mapping and a done-test and appear in `PROOF-CLASSES.md` |
| 6 | MET | each increment is in exactly one proof class; `GAP-TRON-FIXED-SIZE-DEMO-RISK` (INC-05) carries all six elements and is classed credential-free |
| 7 | NOT MET | `ORDERING.md` states both obligations (typed gateway before TRON integration or PAPER proof) but no repository test asserts them; a test from a forge lead, or a Central Architecture waiver, is needed |
| 8 | MET | baselines reproduce: the TRON D1 gate reports 148 passed; the gateway reports 105 passed and 3 xfailed with CI success; no typed gateway and no DEMO latch exist; the dependency graph at `e80fcda` is acyclic |
| 9 | MET | the PR #14 diff was 12 files (11 under the lane directory plus the generated `MANIFEST.md`); `backlog/backlog.yaml` and other PIDs byte-identical to base |
| 10 | MET | every finding carries a class |
| 11 | MET | a scripted scan of the lane files and both mirror notes found no addresses, account numbers or tokens |
| 12 | NEEDS CA RULING | recorded verdicts are `GREEN-WITH-NOTICE` (GOAL, tron) and `GREEN` (mt5-gateway) per the PR #14 body, which names "final heads" and not exact SHAs; the audit reports are held outside the repository; PO acceptance is not recorded in GitHub |

### Unsatisfied or open obligations of the lane

* Criterion 7 (no repository test asserts the ordering obligations): owner `GOLD-AUD-D` forge lead to supply the test, or Central Architecture to waive. Nothing is implied by this entry.
* Criterion 12 (exact-head verdict record and PO acceptance record in GitHub): Central Architecture ruling.
* The transition from `PO_ACCEPTANCE` to `MERGED` is Central Architecture's, after the two items above; this entry does not make it.
* All `open` findings above remain open whatever the lane's state.

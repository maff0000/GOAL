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

## Lane B: GOLD-AUD-B (HERMES to HELIOS integration search and reconciliation)

Backlog item `GOLD-AUD-B`, state at contribution `PO_ACCEPTANCE`; Central Architecture directed (17 October 2026) that it **retains `PO_ACCEPTANCE`** until this entry and its production-dependent comparison obligations are satisfied or formally transferred through a CA-approved scope amendment. Acceptance decision: none recorded in this file.

### References

| Repository | PR | Audited head | Merge commit |
|---|---|---|---|
| `maff0000/HELIOS` | #3 | published head `691558afba89f2258d2ea7c92f7a112dd96b05df` (earlier pre-publication heads exist only in local history) | `fd181215c35d760c279c27f1b7831f2d8121dd07` |

Evidence: `docs/evidence/GOLD-AUD-B/` in `maff0000/HELIOS` (`README`, `INVENTORY`, `CONTRACT-MAPPING`, `TESTS-AND-REPRODUCTION`, `GAPS`, `CANDIDATE-REQUIREMENTS`, `ADAPTATION-PLAN`, `SAFETY`, `SEARCH-LOG`, `DISPOSITION`, `STRATEGY-MODEL`). HELIOS has no CI, so no automated scan covers the merge; this was recorded when Central Architecture accepted it.

### Independent verdicts

| Subject | Head | Technical | Public-safety | Source |
|---|---|---|---|---|
| HELIOS #3 ("this head") | published head `691558af` | `GREEN-WITH-NOTICE` (re-audit) | `SAFE` | PR body |
| two post-audit wording edits | `691558af` | `GREEN-WITH-NOTICE` | `SAFE` | controller record; **unverifiable from the public record**: the audited pre-edit head is not preserved on GitHub, so the delta cannot be re-derived there |

The PR body also records that the first audit of an earlier head was `RED` for a mis-copied disposition file, since resolved.

### Provenance

Read-only audit, 15 to 16 October 2026, against HELIOS `7f7193d`, hermes `ca19017`, HSA `279ec18`, falcon `8f218ec`, cerberus `ffe85e6`, GOAL `ceaf029`; private repositories were summarised only. A throwaway no-network container reproduced the probe accept and refuse results; HELIOS's own suite ran unchanged: 1000 passed and 5 skipped (1005 collected, equal to the baseline count). Disclosed deviation (PR body, rated a low notice by the independent auditor): three throwaway no-network containers reproduced the validator probe and loaded the HSA packages, one process list was read, and the five Docker runtime tests were skipped.

### Findings (`GAPS.md`, `README.md`)

| Id | Summary | Status at this contribution | Closing owner |
|---|---|---|---|
| headline 1 | no completed HERMES Redis to new-HELIOS integration found in the searched locations (absence elsewhere UNVERIFIED) | open | `HELIOS-T2` |
| headline 4 | live HERMES output does not pass HELIOS validators untranslated (5 of 6 raw probes refused; accepted only after translation) | open | `HELIOS-T2`, `HERMES-FACT-001` |
| G-01 to G-04 | schema identity, float versus exact decimal, `is_closed` versus `complete`, extra indicators and session case | open | `GOAL-CONTRACT-001` / CP-1 decision; HELIOS adapter |
| G-05, G-06 | DEV and PROD facts indistinguishable in the frame; publisher status, gap and derivation accounting not carried | open | HERMES, HELIOS adapter |
| G-07, G-08 | H4 `ema_200` depth arithmetic (UNVERIFIED); RSI and ATR method not Wilder | open | HERMES, `HERMES-FACT-001` |
| G-09, G-10 | `XAUUSD` versus `XAU_USD` identity; timeframe spelling | open | `GOAL-CONTRACT-001` |
| G-11, G-14 | ingest clock determinism; no live-source seam | open | `HELIOS-T2` |
| G-12 | characterisation of the deployed stack's input | reported privately | per the private record |
| G-13 | `regime` fact absent from HERMES | open | ARES / `HELIOS-T1` |
| G-15, G-16, G-22 | no HSA-to-HELIOS emitter; atom needs mismatched; no published `goal.strategy/v1` text | open | `GOAL-CONTRACT-001`, HSA, HELIOS |
| G-17 | HELIOS H4 fixtures use a different grid from HERMES | open | HELIOS |
| G-18 | HERMES production facts unavailable (Lane A pending): completeness, freshness and key presence UNVERIFIED | open, **production-dependent** | `GOLD-AUD-A` / HELM |
| G-19 | no `tools/` in HELIOS for the PID's scan | open | ROGUE |
| G-20 | indicator history production activation recorded as pending | open, **production-dependent** | HERMES / `GOLD-AUD-A` |
| G-21 | probe provenance and citation permission unconfirmed | open | PO / ROGUE |

Strategy-model finding: the 4-stage H4/H1/M15/M5 sequence skeleton is expressible in HELIOS v1; the proposed `GOLD-TREND-PO3-001` content is only partly expressible with the six shipped atoms (design candidate only, not selected); neither HSA candidate package loads in HELIOS as authored (`STRATEGY-MODEL.md`, `TESTS-AND-REPRODUCTION.md` section 3).

### Original acceptance criteria (`pids/GOLD-AUD-B.md`, Acceptance 1 to 10)

| # | Result | Cross-reference |
|---|---|---|
| 1 | NOT MET | the PID names the GOAL scan tool on the HELIOS branch; HELIOS has no `tools/` (G-19); public-safety was checked by independent audit instead |
| 2 | MET | the HELIOS PR changed only `docs/evidence/GOLD-AUD-B/`; this lane's GOAL commit in this stack changes only the two index files |
| 3 | NOT MET as written | the PID asks for the same pass count as the 1005 baseline; the actual result is 1000 passed and 5 skipped (1005 collected) because the five Docker runtime tests were skipped (`TESTS-AND-REPRODUCTION.md` section 1) |
| 4 | NOT RE-VERIFIED HERE | candidate-inventory marks in `INVENTORY.md`; not re-checked row by row for this entry |
| 5 | NOT RE-VERIFIED HERE | sanitisation grep; relied on three independent safety audits (`SAFE`) |
| 6 | NOT MET (production-dependent part) | each GOLD-capable package has a requirements row (`CANDIDATE-REQUIREMENTS.md`, 7 rows covering the two HSA candidates and the HELIOS reference packages, unranked), but the check against the audit A facts could not be made (G-18) |
| 7 | MET | every gap in `GAPS.md` names an owner repository and a closing proof |
| 8 | NOT MET (disclosed deviation) | the PID forbids `docker exec` and any service start; the PR body discloses three throwaway no-network containers and one process-list read (rated a low notice); `SAFETY.md` records no write or unit-state change; not repeated here |
| 9 | MET | the checklist is `README.md` (CA items 1 to 10); item 10 is the verdict row above |
| 10 | MET | `DISPOSITION.md` present (31 lines); the newer engine has rows distinct from legacy generations |

### Unsatisfied or open obligations of the lane

* **Production-dependent comparison obligations** (criterion 6, G-07, G-18, G-20): the field-level comparison of the adapter mapping against Lane A's production facts, and the HERMES production completeness and freshness statements. They cannot be satisfied before the HELM production read and independent acceptance of Lane A; they may instead be transferred by a CA-approved scope amendment, which is **not** proposed or assumed here.
* Criterion 1 (scan tool on the HELIOS branch) and the independent-verdict file for CA item 10 (the verdicts above are recorded in the PR body, the reports are held outside the repository).
* `PO_ACCEPTANCE` is retained; no transition is requested.
* Closing owners: production-dependent items, HELM and `GOLD-AUD-A`; the others as in the findings table.

## Lane C: GOLD-AUD-C (shared contract reconciliation, CP-1 and reference-only CP-2)

Backlog item `GOLD-AUD-C`, state at contribution `PO_ACCEPTANCE`. A bounded dated amendment to the lane's PID has been prepared and submitted to Central Architecture for approval; it is **not effective**, and **the original CP-2 criteria stand unchanged** until Central Architecture approves it. The lane is not marked `MERGED` before an approved amendment (if any) and the acceptance gates pass. Acceptance decision: none recorded in this file.

### References

| Repository | PR | Audited head | Merge commit |
|---|---|---|---|
| `maff0000/GOAL` (clean replacement) | #19 | `618520a3547964fcb3a39af43c8a4d6361cd88c5`, then main-reconcile merge `554802f8c010d0cb216666ef641156e79f72ac9e` | `0f0dc45c9765568a823c3e5fed5befcf9e4361f2` |
| `maff0000/GOAL` (superseded) | #15 | `44d62793c3b0a63c12347913127691a89b850ce2`, closed unmerged | not merged |

Lane files: `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-C/` (`RECONCILIATION`, `DISPOSITION`, `AUDIT-VERDICT`, `SOURCES.tsv`, `verify-sources.sh`, `negative-searches.sh`); packages: `contracts/packages/cp-1-hermes-helios-input/` and the one-file reference-only `contracts/packages/cp-2-trigger-outbox-inbox/PACKAGE.md`; tests `tests/test_cp1_conformance.py`, `tests/test_cp_packages_common.py`, `tests/cp_support/`. Main CI after the merge: success. Cached references of the superseded PR #15 and its original content remain accessible on GitHub; they are tracked under DR-38.

### Independent verdicts

| Subject | Head | Technical | Public-safety | Source |
|---|---|---|---|---|
| first clean replacement attempt (local, never published) | `46e0c812` | `RED` (a test listed unpublished-contract vocabulary; MANIFEST drift) | `SAFE-WITH-REDACTIONS` | controller record, not public PR content |
| GOAL #19 | `618520a3` | `GREEN-WITH-NOTICE` | `SAFE` | PR #19 body |
| main reconcile merge (delta) | `554802f8` | `GREEN` | `SAFE` | controller record, not in the PR body |

Recorded notices: the reference-only guard in the tests is a structural tripwire, not a content guarantee (plain prose restatement, or text added to other documents, would not be caught; the guarantee depends on audit review); the withheld finding-id range shows how many findings were withheld; `SOURCES.tsv` records digests of three unpublished texts.

### Provenance

Read-only reconciliation, 15 to 17 October 2026. The unpublished trigger and contract texts were read from a local commit that is not on GitHub; their substance is not republished (the withdrawn draft is held in the private record). `verify-sources.sh` re-reads every cited source at its recorded revision: `verified=84 mismatched=0 skipped=3` on the delivery host (the three skipped are the unpublished texts); an independent run against stale local clones saw one mismatch that disappears with fresh clones.

### Findings (`RECONCILIATION.md` section 4 and section 8)

| Ids | Summary | Status at this contribution | Closing owner |
|---|---|---|---|
| AC-1 to AC-15 | HERMES surface versus HELIOS input: no manifest entry, version-string inconsistency, number and instant forms, no supplier for `regime` / `session`, extra indicators, indicator method, H4 and D1 grid and depth, future-dated refusal omitted from the published rules, ingest-clock rule, no external adapter or Redis reader | open | `HERMES-FACT-001`, `HELIOS-T2`, `GOAL-CONTRACT-001` / CP-1 |
| AC-16 to AC-18, AC-26 | published-component facts about the trigger path (HELIOS has no trigger or outbox code; FALCON's registered payload and TRON D1 intake have different shapes; the normative sources are unpublished) | open | `GOAL-TRIGGER-001` |
| AC-19 to AC-25, AC-27, AC-28 | withheld; ids reserved; held in the private record | open, private | CA / `GOAL-TRIGGER-001` |
| AC-29 to AC-38 | strategy definition: no shared fingerprint or canonical form across HSA, HELIOS and DARWIN; no importer or emitter; three condition semantics; timeframe grammars differ; no reproducibility vectors | open | `GOAL-CONTRACT-001`, `HELIOS-STRATEGY-STANDARD-001` (documentation) |

### Original acceptance criteria (`pids/GOLD-AUD-C.md`, A-1 to A-9), unchanged, against the delivered reference-only scope

| # | Result | Cross-reference |
|---|---|---|
| A-1 | MET for CP-1; NOT MET for CP-2 (CP-2 delivered reference-only) | `tests/test_cp1_conformance.py` and `tests/test_cp_packages_common.py`: 136 passed; full suite 493 passed |
| A-2 | MET for CP-1 with a CI limit | schema validator plus two hand-written checkers; with `jsonschema` or `cryptography` absent the checker-A tests skip (80 passed, 56 skipped), reported not hidden |
| A-3 | MET for CP-1 (rejection matrix covered by the conformance tests); NOT MET for CP-2 | `PACKAGE.md` section 6; fixtures `<code>__<case>.json` |
| A-4 | MET for the CP-1 scenarios (10 scenario fixtures); NOT MET for CP-2 scenarios | `fixtures/scenarios/` |
| A-5 | MET | `verify-sources.sh`: 84 verified, 0 mismatched, 3 skipped (unpublished texts) with fresh clones |
| A-6 | MET | forbidden-content test in the suite; sanitisation tests pass |
| A-7 | NOT MET for CP-2 (no CP-2 rows by design); MET for CP-1 | 7 CP-1 rows exist; none `COMPATIBLE`; no package marked `FROZEN`; no CP-2 rows by design |
| A-8 | PARTLY MET | `goal-validate` OK, `secret-scan` clean, no existing test fails; the `C-1` to `C-14` re-test is delivered (section 5); the `T-1` to `T-11` re-test is not delivered |
| A-9 | MET in substance; record not in repository | verdicts above are recorded in PR bodies, reports held outside the repository; PO acceptance is by Central Architecture directive, not recorded in GitHub |

### Proposed amendment (not effective)

A proposed amendment to `pids/GOLD-AUD-C.md` has been submitted to Central Architecture for approval. It is not part of this repository change and is not effective; until Central Architecture approves it, the original CP-2 criteria above stand unchanged.

### Unsatisfied or open obligations of the lane

* The original CP-2 criteria (A-1, A-3, A-4, A-7 and A-8, their CP-2 parts) are not met by the reference-only delivery and stand unchanged unless and until Central Architecture approves a proposed amendment.
* Normative CP-2 conformance tests, scenarios and matrix rows, and the `T-1` to `T-11` re-test, depend on the unpublished trigger authority (`GOAL-TRIGGER-001`) and are not delivered.
* CP-1 freeze is blocked while `C-12` of `GOAL-CONTRACT-001` is open (CP-1 stays `PROPOSED`).
* Findings AC-1 to AC-18, AC-26 and AC-29 to AC-38 stay open with the owners above; the withheld findings stay in the private record.
* Closing owner: Central Architecture / PO for the amendment decision, acceptance and the `MERGED` transition.

## Lane E: GOLD-AUD-E (FALCON registry and ingestion evidence; minimum HELIOS and TRON publication work)

Backlog item `GOLD-AUD-E`, state at contribution `PO_ACCEPTANCE`. Acceptance decision: none recorded in this file.

### References

| Repository | PR | Audited head | Merge commit |
|---|---|---|---|
| `maff0000/falcon` | #21 | pre-publication head (inferred from local history), published head `f5c9300cb9c48990eab794f225f9d115c4b1e78d` | `7734856596085200967b94a79ff4faa697633878` |

Evidence: `docs/evidence/GOLD-AUD-E/` in `maff0000/falcon` (`README`, `EP-01` to `EP-10`, `MINIMUM-WORK-LIST`, `DISPOSITION`, `UNVERIFIED`, `AUDIT-LOG`, `VERDICT`, and three stdlib scripts `regenerate_ep3.py`, `verify_stale_lines.py`, `ep09_reference_model.py`), plus an entry count change in `DOCUMENTATION-MANIFEST.json`. Falcon CI on the PR: 2 of 2 success; main CI after the merge: success.

### Independent verdicts

| Subject | Head | Technical | Public-safety | Source |
|---|---|---|---|---|
| falcon #21 (delta re-audit of the amended head) | amended head, not named in the PR body | `GREEN` | `SAFE` | PR body |
| post-audit one-line substitution (accepted by Central Architecture as equivalent to the requested deletion) | `f5c9300c` | `GREEN-WITH-NOTICE` | `SAFE` | controller record |

Recorded notice, **unverifiable from the public record**: the PR body describes the post-audit edit as "deletion-only"; the controller's delta check found a one-line rewrite (one insertion, one deletion) that removed location pointers and added only a connective phrase, no new facts. The falcon pull request is merged and the pre-edit head is not preserved on GitHub, so a reader of the public record cannot check which description is accurate. At the published head the three scripts pass (`regenerate_ep3.py --check` 28 rows, `verify_stale_lines.py` 31 rows, `ep09_reference_model.py` 8 tests).

### Provenance

Read-only audit, 15 to 16 October 2026, falcon `8f218ec`, HELIOS `7f7193d`, TRON `5577039` (main) and `37d5f00` (design branch), GOAL `ceaf029`. No running service was inspected; the lane's own record states that the running-ingestion facts of the PID are agent assertions, not established facts.

### Findings (headline; full text in the evidence files)

| Ref | Summary | Status at this contribution | Closing owner |
|---|---|---|---|
| EP-4 s2 | HELIOS publication is synchronous and fatal: a sink error ends the evaluation loop (P-H1) | open | `HELIOS-T2` / HELIOS architect |
| EP-4 s3 | HELIOS cannot supply the registered strategy families (8 of 13 required fields not published; no `evaluation_id`) | open | `FALCON-T1`, HELIOS |
| EP-5 | TRON has no runtime or publisher code; three differing pictures of its evidence and intake; lifecycle families missing for claim disposition and reconcile | open | `TRON-T1`, `TRON-T4`, FALCON |
| EP-8 | registered FALCON trigger payload is not aligned with the unpublished trigger authority; re-read needed when that is published | open | `GOAL-TRIGGER-001`; FALCON trigger-evidence item (proposed in lane E decision D-7, not in the backlog) |
| EP-10 | stale discovery-model language: 31 rows in 22 files | open | FALCON amendment route |
| U1 to U6 | running FALCON ingestion, Graylog configuration and volume, HERMES publication state: not established | open, **runtime-dependent** | operations owner read-only export (decision D-4) |
| U11 | the isolated-FALCON outage rehearsal was not run | open, **runtime-dependent** | follow-on items and `GOLD-MVP-001` |
| U7 to U10, U12, U13 | producer code, HELIOS deployment configuration, TRON runtime, legacy stack, real volumes, trigger content after approval | open | as listed in `UNVERIFIED.md` |

### Original acceptance criteria (`pids/GOLD-AUD-E.md`, Acceptance 1 to 10)

| # | Result | Cross-reference |
|---|---|---|
| 1 | NOT RE-VERIFIED HERE | EP-1 to EP-10 files exist; the per-EP path-and-SHA citation was not re-checked row by row |
| 2 | MET | `regenerate_ep3.py --check` reproduces the 28-row matrix (delta auditor) |
| 3 | PARTLY MET | `UNVERIFIED.md` has 13 rows with reasons; the per-claim command excerpts in EP-2 were not re-checked |
| 4 | MET | `verify_stale_lines.py` passes 31 rows (at least the 9 required) |
| 5 | MET | `MINIMUM-WORK-LIST.md` has owner, delta, fixture, acceptance test, sequencing and a "FALCON absent means" column per row |
| 6 | MET as a statement; **rehearsal NOT performed** | `EP-09-outside-the-path.md` states the requirements and a test for each, with a reference model (8 tests pass); the outage rehearsal on an isolated FALCON (EP-9 R-5, U11) has not been run; the proposed timing bound in the PID is not approved and is not asserted here |
| 7 | MET (CI); scan tool NOT RE-VERIFIED HERE | falcon CI 2 of 2 success on the PR; the GOAL scan tool was not run against the falcon branch for this entry |
| 8 | MET | the delta auditor found only `docs/evidence/GOLD-AUD-E/` and `DOCUMENTATION-MANIFEST.json` changed; no lines in `registry/`, `schemas/`, `deploy/`, `tests/` |
| 9 | NOT RE-VERIFIED HERE | `AUDIT-LOG.md` exists; each command was not re-checked against the allowed list |
| 10 | MET | `DISPOSITION.md` present |

### Unsatisfied or open obligations of the lane

* **Operational outage rehearsal** (EP-9 R-5, U11): not run. It needs an isolated development or test FALCON and a real component under test.
* **Running-ingestion facts** (U1 to U6): not established; they need the operations owner's read-only export (D-4).
* Criteria 1, 3, 7 (scan tool) and 9 were not re-verified for this entry; the independent verdict file for CA item 10 is held outside the repository.
* **Proposed amendment (text only; the PID is not edited here):** transfer the integration execution proofs (the isolated-FALCON outage rehearsal, and the running-ingestion verification through the D-4 export) from `GOLD-AUD-E` to `GOLD-MVP-001` and the follow-on items P-H1 and P-T1, stating that the research audit did not perform them and that no result of them is claimed. The research deliverables (EP-1 to EP-10, the work list, the disposition table) stay as delivered.
* Closing owner: Central Architecture / PO for acceptance or amendment; the operations owner for the export; HELIOS and TRON owners for the follow-on proofs.

## Lane F: GOLD-AUD-F (qualification-to-review path)

Backlog item `GOLD-AUD-F`, state at contribution `PO_ACCEPTANCE`. Acceptance decision: none recorded in this file. The observer safety blocker (below) is retained.

### References

| Repository | PR | Audited head | Merge commit |
|---|---|---|---|
| `maff0000/GOAL` (clean replacement, primary evidence) | #18 | `e2a2c525e72041d632abfc8069a005a1ed74a2a0`, then main-reconcile merge `186f3af1f4daa28391c03694923b9e38fc417f89` | `ddf6a7ad9349187dee54d6172ddfd584ab8690f3` |
| `maff0000/GOAL` (superseded) | #13 | `4f424dcfb69ee08487fb652bee4f0f55000969ab`, closed unmerged | not merged |
| component mirror notes (`maff0000/DARWIN`, `maff0000/CER`, `maff0000/HSA`) | none opened | n/a | **not published** (see obligations) |
| component mirror note for a private repository | none opened | n/a | **withheld** pending owner decision D10 |

Lane files: `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/` (`AUDIT-F`, `DISPOSITION`, `EXTERNAL-REGISTER`, `IDENTITY-SNAPSHOTS`, `AMENDMENT-PROPOSALS`, `APOLLO-ATHENA-EXTENSION`). Main CI after the merge: success. Cached references of the superseded PR #13 and its original content remain accessible on GitHub; they are tracked under DR-38. Private source detail stays in the private record.

### Independent verdicts

| Subject | Head | Technical | Public-safety | Source |
|---|---|---|---|---|
| first clean replacement (local, never published) | `6a82e39c` | `GREEN-WITH-NOTICE` | `SAFE-WITH-REDACTIONS` (private repository names and component kinds to reduce) | controller record, not public PR content |
| GOAL #18 after redactions | `e2a2c525` | `GREEN-WITH-NOTICE` | `SAFE` | PR #18 body |
| main reconcile merge (delta) | `186f3af1` | `GREEN` | `SAFE` | controller record, not in the PR body |

Recorded notice: the redactions condensed more of the disposition rows than strictly required (criteria detail and retained-value lists). The verdict-bearing component rows are as in the published `DISPOSITION.md`; counts are not restated here.

### Provenance

Read-only audit, 15 to 16 October 2026, over the public component repositories at the revisions recorded in `AUDIT-F.md` section 2 and over private sources described at class level only. No broker contact, no outbound call to any evaluated service, no installation of evaluated code. Before and after identity snapshots for the public checkouts are in `IDENTITY-SNAPSHOTS.md`; those for private sources were removed from the public set by the sanitisation and replaced by a one-line unchanged statement.

### Findings (`AUDIT-F.md` section 6)

| Id | Severity | Summary | Status at this contribution | Closing owner |
|---|---|---|---|---|
| F-01 | BLOCKER | no translator from the HSA package to the HELIOS runtime package; HELIOS refuses both candidates as authored | open | `HSA-C1` (partial); emission of the runtime package: no home |
| F-02, F-03 | MAJOR, MINOR | no shared fingerprint across HSA / HELIOS / DARWIN / CER; no HSA-to-DARWIN importer; CER version record has no package-hash field | open | `GOAL-CONTRACT-001`, `DARWIN-R2` (undefined), `CER-R1` |
| F-04, F-05, F-15 | BLOCKER, MAJOR, MAJOR | APOLLO 006B cannot test either candidate; no `APOLLO_PROOF` producer; no engine yields backtest evidence for either candidate | open | `DARWIN-R3` (scope stale) or DARWIN-internal; no GOAL home |
| F-06, F-07, F-09 | MAJOR | no writer of any evidence class into CER; promotion authority free text and evidence per state undefined; CER strategies, versions and runs unreadable | open | `CER-R1` and candidates; PO / CA rule |
| F-08 | MAJOR | HELIOS performs no promotion check | open | no home (candidate row proposed) |
| F-10 | BLOCKER for a "read-only" claim | **the NEO observer is not approved as a read-only GOLD MVP consumer**: it has no CER client and its review capability is not mechanically read-only | open; **blocker retained** | `NEO-R1` and a PO disposition ruling |
| F-11, F-12, F-13 | MAJOR / UNVERIFIED | NEO test hermeticity and CI; NEO observer runtime state unknown; deployed DARWIN / CER / HELIOS builds versus main unknown | open | `NEO-R0` (deferred candidate); HELM-operated reads; `DARWIN-R1` |
| F-14 | MINOR | no hypothesis intake | open (deferred beyond MVP) | `NEO-R2`, `HSA-C2` (deferred candidates) |
| F-16, F-17, F-18 | BLOCKER (outside lane), MAJOR, MAJOR | trigger path to TRON not built; HELIOS has no live HERMES transport; the two candidates have never run through HELIOS | open | `TRON-D1-RATIFY`, `TRON-T1`, `GOAL-TRIGGER-001`; `HELIOS-T2`; follows F-01 |

### Original acceptance criteria (`pids/GOLD-AUD-F.md`, Acceptance 1 to 9)

| # | Result | Cross-reference |
|---|---|---|
| 1 | NOT RE-VERIFIED HERE | 10-hop path matrix, `AUDIT-F.md` section 3.1; citation re-runs were not repeated for this entry |
| 2 | PARTLY MET | 10 hops and CA items 1 to 10 present; the count of memory-fabric review records in the external register depends on private identifiers that the clean replacement removed from the public set; that count is held in the private record |
| 3 | MET | `goal-validate` and `secret-scan` clean at the merge; independent public-safety audits found no address or key-like string |
| 4 | PARTLY MET | identity snapshots equal for the public checkouts; private-source snapshots are not in the public set |
| 5 | MET (lane statement) | no external code installed, no outbound call to an evaluated service; not re-verified here |
| 6 | MET | no backlog, `pid_path` or state change in the lane PR (the later reconciliation PR, not this lane, changes the state) |
| 7 | NOT RE-VERIFIED HERE | each missing mark names an owner or "no home"; external register is information only; no strategy ranked; audits found no contradiction |
| 8 | MET | `DISPOSITION.md` present with verdict-bearing component rows per the published file (counts not restated here); each row carries a cost cell; NEO parts are kept apart as roles |
| 9 | MET in substance; record not in repository | verdicts above are in PR bodies, reports held outside the repository; PO acceptance is by Central Architecture directive, not recorded in GitHub |

### Unsatisfied or open obligations of the lane

* **Mandatory public component mirrors not published.** PID checklist items for `maff0000/DARWIN`, `maff0000/CER` and `maff0000/HSA` (documents only) remain unpublished. Local drafts exist but are stale: they point at the old unpublished primary branch and list non-public repositories among the audited set, so each needs revision against the sanitised primary record and an independent public-safety audit before any publication. They are to be raised as separate one-repository pull requests; that is a follow-on action, not done here.
* **Private-repository mirror note withheld** pending owner decision D10 and the owner's ruling on the observer blocker.
* **Proposed limited PID amendment (text only; the PID is not edited here):** the checklist item for the private-repository mirror is made conditional on D10 and that ruling; if no safe public mirror can be produced, the mirror is held in the private record and the primary record's class-level statement and the retained observer blocker are the only public statement. No other mirror is proposed for amendment: the three public mirrors can be produced safely once revised.
* The observer blocker F-10 stays: the NEO observer is not approved as a read-only GOLD MVP consumer.
* Amendment text proposals for `CER-R1`, `NEO-R1`, `HSA-C1` and `DARWIN-R2` are delivered as proposals (`AMENDMENT-PROPOSALS.md`), not applied.
* Closing owner: Central Architecture / PO for acceptance; the `GOLD-AUD-F` forge lead for the three public mirrors; Central Architecture for the items that depend on the observer ruling.

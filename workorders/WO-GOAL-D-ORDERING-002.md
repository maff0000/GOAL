# Work Order WO-GOAL-D-ORDERING-002

**Conditional authority.** This file is candidate text and confers no authority by itself. It becomes executable authority solely by (a) an attributable, exact-head Architect acceptance record in GOAL pull request #43 that names the candidate head commit SHA, followed by (b) merge of that exact head into GOAL main (governance sections 7.2 and 7.5). Until both have occurred nothing in this file is approved, and dispatch is barred. This file does not and cannot contain an approval of itself or its own commit SHA: the approval record is external (field 12) and the merge commit on GOAL main is the activation evidence. The gates in "Authority gates" at the end of this file must each be actually satisfied; none is satisfied by assertion.

Governing document: `maff0000/GOAL` `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` and template `templates/WORK-ORDER.md`, at GOAL main commit `3f2f100ea27f515689d1fa05fa815956a396f730` (merge of GOAL pull request #42). The authoritative record of this Work Order is this file in `maff0000/GOAL` at `workorders/WO-GOAL-D-ORDERING-002.md`. The mandatory dispatch preamble (governance section 6) is not copied here.

**Work Order ID:** WO-GOAL-D-ORDERING-002

Numbering note: `-001` does not exist; the number `-002` follows the already merged Lane D criterion 7 test (GOAL pull request #41, branch `wo/GOAL-GOLD-AUD-D-CRIT7-TEST`).

## 1. Approved parent PID and applicable amendments

- Parent PID: GOLD-AUDIT-CLOSEOUT-001 (`pids/GOLD-AUDIT-CLOSEOUT-001.md`, Phase 3: fulfil Lane D acceptance criterion 7) and GOLD-AUD-D (`pids/GOLD-AUD-D.md`, acceptance criterion 7).
- Applicable amendment: GOLD-AUD-D dated PID amendment of 17 October 2026 (GOAL pull request #30, merge commit `2caad714247cbe098412832e1cbbf5286c13b82f`), item 1 (criterion 7 is not waived). This Work Order is a correction to the criterion 7 policy test delivered under the closeout PID.
- Governance: `governance/DELIVERY-CHAIN-AND-WORK-ORDERS.md` at GOAL main `3f2f100ea27f515689d1fa05fa815956a396f730`.

## 2. Target repository and exact base SHA

Target repository: `maff0000/GOAL`  
Exact base SHA: `3f2f100ea27f515689d1fa05fa815956a396f730` (GOAL `main`; verified against GitHub when this version was drafted)

## 3. Permitted paths

- `tests/test_gold_aud_d_ordering_policy.py` only.
- `MANIFEST.md` is not a permitted path: the test file already exists and is already listed, so no manifest change is expected. If `./tools/goal-docs --check` reports that a manifest change is needed, stop and return to the Architect.
- No separate integrity-reference file is permitted: the integrity reference is a SHA-256 constant held inside the test file (Architect decision, 19 October 2026, PR #43 directive section 2).

## 4. Scope

Correct the criterion 7 policy test `tests/test_gold_aud_d_ordering_policy.py` so that the ENTIRE lane D ordering document, `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/ORDERING.md`, is integrity-guarded by whole-file content pinning. Central Architecture approved whole-file content pinning as the interim control. It is added alongside the existing graph tests and the existing text checks, which remain.

Required behaviour: an altered `ORDERING.md` is rejected by the test until its integrity reference is updated through an independently reviewed Work Order. Any legitimate edit to `ORDERING.md` therefore requires a new Work Order, which updates the integrity reference in the same governed change.

Digest guard design (the in-test SHA-256 constant and byte-exact whole-document integrity are Architect decisions of 19 October 2026; function naming and message layout are left to the implementer within these rules):

- The digest is the SHA-256 of the RAW BYTES of the lane D `ORDERING.md`, read with `open(path, 'rb')`. No decoding, no newline normalisation, no whitespace normalisation, no BOM handling. A CRLF variant of the document must therefore fail.
- The expected digest is held as a hex constant in the test file. Recomputed from GOAL main `3f2f100ea27f515689d1fa05fa815956a396f730` when this version was drafted: the file is 5111 bytes and its SHA-256 is `6571e2a6bf52c4c7e6a0002175578865dee02f18eed959eb138becdf3b29f93a`. The implementer recomputes this at the base SHA and states it in the pull request; the value here is a drafting aid, not a substitute for that check.
- The guard is a function that takes bytes (or text, encoded as UTF-8 by the function) as an argument, so that the real-file test and the mutation tests exercise the same code.
- On failure the message prints both the expected digest and the actual digest.

Half-check independence (required, added in this version): the whole-file digest guard is added alongside the existing independent half-checks `check_tron_half` and `check_paper_half`, and must not replace, subsume or weaken either. After the change, each half-check must remain independently failing: the existing named mutation tests `test_m6_text_drop_paper_proof_fails_paper_half_only` (removes the PAPER half alone) and `test_m7_text_drop_accepted_tron_integration_fails_tron_half_only` (removes the TRON half alone) must remain unchanged, must pass, and must continue to show that removing one half alone fails only that half's check and leaves the other half's check passing. The digest guard must not be called from inside either half-check, so that a half-check failure is never masked or merged into a digest failure.

The test file is changed; `ORDERING.md` itself is not changed. The existing exact-item test, the independent half-checks (TRON half, PAPER half), the Gate A and readings checks, the weakening-word guard and the graph tests are unchanged: not weakened, not deleted, and they still pass.

## 5. Exclusions

- No gateway implementation.
- No trading code.
- No broker access.
- No operational change.
- No edit to `ORDERING.md`, to the backlog, to `MANIFEST.md`, or to any PID.
- No change to, weakening of, or deletion of any existing test in the file.
- Mutation tests never write files: they call the guard function on in-memory bytes or text arguments only.
- This Work Order does not prove that the typed gateway is operationally approved. It guards the wording of the ordering document only.

## 6. Required tests (including negative tests)

Negative mutations, each built in memory and passed to the relevant check as an argument. Failure routing (Architect decision, 19 October 2026): M-a through M-f, M-i and the byte-level variants (item 8) must FAIL the digest guard, with the expected and actual digests printed; M-g and M-h are graph-level mutations and must FAIL the graph inversion check (`check_no_inversion`), not the digest guard. Items 1 to 8 below are digest-guard mutations built from the bytes of the real document (item 7 is the PAPER-side text inversion; the graph-level PAPER-side mutations are M-g and M-h):

1. Whole-document mutation: a change to any part of the document, including a single character outside section 1.
2. A cancelling statement added in obligation item 2.
3. A new item 3 added to the obligations list.
4. A cancelling statement placed outside section 1.
5. Gate A moved (relocated within the document).
6. A qualified gateway statement (M-i), and a qualified gate-table row (M-f).
7. An independent PAPER-side inversion (the PAPER half reversed while the TRON half is left intact).
8. Byte-level variants: CRLF line endings (every `\n` replaced by `\r\n`), a trailing newline added or removed, and a leading byte-order mark.

Required mutations, stated concretely (M-a to M-f and M-i are built in memory from the bytes of the real document and must fail the digest guard, and where a lettered half-check or text check also applies it must still fail independently as described; M-g and M-h are built on the in-memory dependency graph and must fail the graph inversion check):

- M-a: mutate the item 1 sentence in `## 1. The two binding obligations` (the sentence "The typed gateway must exist and be approved before accepted TRON integration or PAPER proof."), by removing " or PAPER proof" alone, and separately by removing "accepted TRON integration or " alone. The first must also fail `check_paper_half` and not `check_tron_half`; the second must also fail `check_tron_half` and not `check_paper_half`.
- M-b: append a cancelling sentence to obligation item 2 ("Diagnostic bridge use is permitted only for isolated proof that is not TRON integration."), for example a sentence stating that the first obligation does not apply while the diagnostic bridge is in use.
- M-c: add a new item 3 to the obligations list in section 1 (a line beginning "3. ") that qualifies or cancels item 1.
- M-d: add a cancelling statement outside section 1, for example a new sentence in `## 4. Orderings that look necessary but are not (evidence)` stating that the typed gateway ordering is advisory.
- M-e: move the Gate A line ("GATE A  typed gateway exists AND is approved ...") in the `## 2. Order` diagram so that it sits below the INC-14 line and below the INC-17 line (two separate variants).
- M-f: append "(not required for PAPER)" to the gate-table row beginning "Typed gateway exists and is approved (Gate A)" in `## 3. Where each gate applies`.
- M-i: qualify the gateway obligation: replace the item 1 sentence in `## 1. The two binding obligations` with the same sentence extended by a qualifier, for example "The typed gateway must exist and be approved before accepted TRON integration or PAPER proof, except where the diagnostic bridge is in use." Built in memory from the bytes of the real document; it must fail the digest guard. It is a separate mutation from M-a, M-b and M-f.
- M-g: reverse the PAPER-side dependency: a graph-level mutation in which the typed gateway (`MT5-GW-003`) depends on `PAPER-E2E-001`. `check_no_inversion` rejects this through the transitive `TRON-T2` ancestor (message "TRON-T2 is an ancestor of MT5-GW-003"), because `PAPER-E2E-001` depends on `TRON-T2`. M-g therefore does not independently isolate PAPER proof. The existing `test_m5_reversed_edge_fails_anti_inversion` covers the direct TRON-side form; M-g is an addition.
- M-h (PAPER consumer isolated): the same reversal with the `TRON-T2` consumer path cut, so that only the PAPER consumer can trigger the rejection. Build: `g = real_graph()`; `g["MT5-GW-003"] = g["MT5-GW-003"] + ("PAPER-E2E-001",)`; compute `cut = [(s, "TRON-T2") for s, deps in g.items() if "TRON-T2" in deps]` (at drafting time `PAPER-E2E-001` and `GOLD-MVP-001`); `g = without_edges(g, *cut)`. `check_no_inversion(g)` must then fail with the message "PAPER-E2E-001 is an ancestor of MT5-GW-003", and `TRON-T2` must not be an ancestor of `MT5-GW-003` in `g`. It uses only the existing helpers `real_graph`, `without_edges`, `ancestors` and `check_no_inversion`; feasibility was checked in memory at drafting time against the base SHA graph and the implementer re-verifies it. M-h is a required mutation.

Positive control: the unmodified document, read with `open(path, 'rb')`, passes.

Regression: the existing exact-item, half-check, Gate A, readings and graph tests in the file are unchanged and continue to pass, and the control-plane CI steps (`./tools/goal-validate`, `./tools/goal-docs --check`, `./tools/secret-scan`, `python3 -m pytest tests/ -q`) pass at the final head.

## 7. Acceptance criteria

1. Every digest-guard mutation (field 6 items 1 to 8 and M-a to M-f and M-i, including the byte-level variants) fails the digest guard, and its failure message prints the expected and actual digest. M-g and M-h fail the graph inversion check (`check_no_inversion`) with the messages stated in field 6; no digest output is required of them. The PAPER-isolated M-h result ("PAPER-E2E-001 is an ancestor of MT5-GW-003", with `TRON-T2` not an ancestor) is preserved.
2. The original, unmodified `ORDERING.md` passes, and the digest is of its raw bytes as defined above.
3. The existing exact-item, half-check and graph tests are unchanged (diff shows no removed or weakened assertion) and pass. In particular, the existing independent half-checks remain independently failing: `test_m6_text_drop_paper_proof_fails_paper_half_only` and `test_m7_text_drop_accepted_tron_integration_fails_tron_half_only` still pass unchanged, and each M-a variant fails the digest guard AND only its corresponding independent half-check: the variant removing " or PAPER proof" fails `check_paper_half` and not `check_tron_half`; the variant removing "accepted TRON integration or " fails `check_tron_half` and not `check_paper_half`.
4. Only the permitted path is changed (`git diff --stat` shown in the pull request); `ORDERING.md` and `MANIFEST.md` are unchanged.
5. Every required mutation M-a to M-i in field 6 is implemented as named and fails as stated.
6. Independent technical audit and independent public-safety audit both pass at the exact final head, by an auditor who is not the implementer. A material modification after audit requires renewed independent assurance.
7. Architect acceptance is recorded before merge. Passing CI is not Architect acceptance. Independent audit and Architect acceptance are cumulative, not alternatives.

## 8. Assigned implementer

Assigned by the Delivery Controller (controller assignment of 19 October 2026, recorded under the Architect directive of that date): implementer instance identifier `FORGE-IMPL-WO-GOAL-D-ORDERING-002-A`, a FORGE implementer instance. It is launched only after this Work Order is merged into GOAL main, against this Work Order alone. The identifier is a role label; the launch record (session and model identity) will be added to the pull request evidence at dispatch.

## 9. Independent auditor (not the implementer)

Assigned by the Delivery Controller (controller assignment of 19 October 2026). Independent technical auditor identifier `FORGE-AUD-TECH-WO-GOAL-D-ORDERING-002-B`; independent public-safety auditor identifier `FORGE-AUD-SAFE-WO-GOAL-D-ORDERING-002-C`. Both are separate instances from the implementer and from each other, and neither may be the drafter or implementer of this Work Order. Public attribution uses these stable role identifiers; the actual session identities are traceable in a restricted audit record kept by the Delivery Controller and recorded when each audit is performed. Audit separation from implementation is a condition of acceptance.

## 10. Delivery Controller

ROGUE (confirmed by the Architect, 19 October 2026, directive section 6; governance rule 8).

## 11. Stop conditions

Architectural ambiguity (including any need to change the digest definition or the ordering document); change of risk authority; uncontrolled production access; credential exposure; incompatible contract assumption; implementation that would fall outside this Work Order's scope; absence of any required authority. On any of these, stop and return the precise missing item or finding to the Architect (governance section 5).

## 12. Expected GitHub evidence, pull request and approval record

Expected evidence and pull request: one pull request into `maff0000/GOAL` from a branch named for this Work Order, whose diff touches only the permitted path; the PR body states the recomputed size and digest of `ORDERING.md` at the base SHA and shows `git diff --stat`; CI results at the exact head; the independent technical audit and the independent public-safety audit, each recorded against the exact head; post-merge main CI verification after Architect-accepted merge.  
External approval record (conditional authority model). Approval of this Work Order exists only if both of the following exist, and not otherwise:

1. An attributable Architect acceptance record in GOAL pull request #43 (a review or comment by the Architect) that names the exact candidate head commit SHA accepted and its decision source. A controller transcription of an acceptance is not an Architect action and must be labelled as a transcription (governance section 7.5).
2. Merge of that exact head into GOAL main. The resulting merge commit is the activation evidence.

This file contains no approval fields to fill, no "approved" statement and no SHA of its own commit, so that it can be accepted without being modified to embed its own approval. If no such record exists, this Work Order is not approved, whatever any other message, local file or CI result says. The pull request body points to the current candidate head and to the acceptance record once it exists.

## Authority gates

Every gate must be actually satisfied, with the evidence named, before the step it guards. A gate that is unsatisfied, unverifiable or satisfied only by assertion blocks that step. Satisfaction is recorded in GOAL pull request #43 (merge gates) or in the dispatch pull request (dispatch gates), not in this file.

Pre-merge gates (all required before this Work Order is merged into GOAL main):

- G1. Independent technical audit and independent public-safety audit of the exact final head, by auditors who are not the drafter or the implementer. A material change after audit requires renewed audit. Evidence: audit records against the exact head SHA.
- G2. Exact-head CI success and a clean secret scan on the same head. Evidence: GitHub Actions result and secret-scan output for that SHA. CI success is not Architect acceptance.
- G3. Base verified: GOAL main equals the base SHA in field 2 at merge time. If main has moved, reconcile against the new main, independently review any material base or manifest change, and obtain fresh Architect acceptance of the new exact head.
- G4. Explicit Architect acceptance of the exact head, recorded in GOAL pull request #43 as described in field 12, before merge. The merge is pinned to that head.

Pre-dispatch gates (all required before any implementer is dispatched):

- P1. This Work Order is merged into GOAL main and main CI on the merge commit is verified.
- P2. GOAL main is re-verified at dispatch; the Work Order text on main is the text accepted. Target base for the test file is re-verified against field 2. On any mismatch, stop and return to the Architect.
- P3. Actual instance and session identities of the implementer and both auditors are recorded in the dispatch pull request, and their separation is verified (neither auditor is the implementer or drafter). The role identifiers in fields 8 and 9 are prospective assignments only.
- P4. The mandatory dispatch preamble of governance section 6 is included in the dispatch prompt.
- P5. Permitted paths (field 3) and exclusions (field 5) are enforced; any stop condition in field 11 stops work and is returned to the Architect.

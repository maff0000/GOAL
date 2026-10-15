# GOLD-AUD-D — GOLD MVP Lane D: TRON / MT5 minimum DEMO execution path gap analysis

**Lane:** Research (read-only)  
**Target repository:** `maff0000/GOAL` (evidence PRs also into `maff0000/tron` and, for MT5 facts, `maff0000/mt5-gateway`)  
**Priority:** P0  
**Risk:** Medium (read-only audit; the path it analyses is capital-adjacent)  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  
**Audit id:** GOLD-AUD-D (child audit of GOLD-MVP-001)  
**Depends on:** `GOAL-DCP-001` only  
**Status:** DRAFT CANDIDATE

## Purpose

Produce one bounded, read-only answer to a single question: what is the smallest set of missing capabilities that lets ONE order travel the whole DEMO path

```text
HELIOS trigger in -> TRON claim / risk / size -> MT5 gateway place on DEMO -> reconcile -> evidence
```

Central Architecture directive for Lane D (verbatim): "Audit TRON D1 and its existing implementation candidates, risk rules, journal and trigger-intake assumptions. Coordinate with the ongoing MT5-GW-001 GitHub consolidation. Identify the smallest missing capabilities for one DEMO execution path. Do not duplicate existing MT5 work or disturb operating broker instances."

### Amend or new: decision and justification

The lane is a **thin new item** (option ii), not an amendment increment of TRON-D1-RATIFY (option i).

1. TRON-D1-RATIFY is a Matt-facing decision package about one artefact (the unmerged D1 baseline). Its authority, recipient and decision block (R-1..R-10) are TRON-only. Adding an MT5 gap statement and a cross-hop matrix would turn a decision brief into a programme audit and blur which decisions are Matt's.
2. Lane D's unique value is the composition: the hop-by-hop matrix, the credential-free / read-only-session / write-approval separation, and the ordering against the typed-gateway requirement. None of that exists in any single prior document.
3. Roughly 80 percent of the TRON-side facts already exist and are re-confirmed, not re-derived. This PID therefore forbids re-auditing them (see Scope, "Reuse rules") and limits TRON-side new work to the questions the ratification package did not ask.
4. If the PO prefers option (i), the fallback is explicit: the same deliverables become one appendix to the ratification package plus a stub item. The matrix and increment list are written to be transplantable, so the choice costs little.

The PID is a composition and gap-closing audit. It creates no code and no runtime capability.

## Current state

All facts below were read read-only on 2026-10-15 against GOAL `main` @ `1739e742154c77e9e2a96927dc40d4978b9cd798`. Items marked UNVERIFIED must be re-read by the audit before being relied on.

### TRON

- `maff0000/tron` `main` @ `5577039` holds documentation and tooling only: `PID.md` (Product Constitution, HR-01..HR-16), gitleaks rules, a pre-commit hook. There is **no runtime code** on `main` (source: TRON-D1-RATIFY section 2.1).
- `wo/WO-TRON-D1` @ `37d5f00` is 20 commits ahead of `main`, 60 files: 12 design documents, 5 contract schemas, 7 config schemas, 25 schema examples, one test module (`tests/test_docs_baseline.py`). The only Python file in the branch is that test. Nine `wi-a..wi-i` branches are all ancestors of D1. No pull request exists for D1 (TRON-D1-RATIFY 2.2, 2.3; the file-type count was independently re-checked by this PID's author).
- D1's gate (148 tests) proves the document, schema and example set is internally consistent; it proves nothing about execution (D1 PID section 29).
- The D1 MVP check set contains no exposure, position-count, order-size, daily-loss, drawdown, consecutive-loss or risk-lock check; CHK-074 (kill switch engaged) is MVP while its setter (BL-OPS-01) is backlog (TRON-D1-RATIFY N-5).
- D1 assumes three things the CA rulings of 2026-10-14 changed: a Redis board as intake, "ledger" for TRON's own store, and FALCON as the upstream (TRON-D1-RATIFY section 5, stale-content register).
- TRON-T1 candidate (branch `wo/GOAL-PID-WAVE1-C-execution`) uses the superseded "ledger" wording; TRON-D1-RATIFY section 11 holds the reconciling amendment note.
- Backlog: TRON-T1 is `PID_DRAFT`; TRON-T2..T5, HELIOS-T3, MT5-GW-002..004 are `ARCHITECTURE_REQUIRED`; PAPER-E2E-001 carries a Matt gate (`backlog/backlog.yaml` at the base SHA).
- No `GOAL-TRIGGER-001` item exists in the backlog and branch `wo/GOAL-CONTRACT-TRIGGER` holds no commits beyond `main` at the time of reading (TRON-D1-RATIFY N-3). UNVERIFIED for later changes.

### MT5 gateway

- `maff0000/mt5-gateway` `main` = `46308bad7b896f1e4f816d9e264d88dd23a9bd57`. MT5-GW-001 reconciliation is merged; PRs #1..#8 are MERGED; PR #9 (`MT5GW-TEMPLATE-001`: instance config contract, validation suite, documentation) is OPEN (verified read-only via the GitHub API on 2026-10-15).
- The typed gateway does **not** exist. The only control surface is a raw RPyC `SlaveService` bridge: unauthenticated, arbitrary code execution inside the container, order-capable; protection is network isolation only (MT5 readiness assessment, headline 5 and section B; DEMO verification finding 14).
- No automated tests, no DEMO environment guard in code, health check tests process presence only, restart policy is `no` (same sources).
- Template contract (design only, branch `wo/GOAL-MT5-TEMPLATE`): broker-neutral operation set `describe`, `health`, quotes/bars/symbol spec/account/positions/orders/deals, `place_order`, `modify`, `cancel_order`, `close_position`, `reconcile`; mandatory `client_order_id` idempotency; error taxonomy including `TIMEOUT_UNKNOWN_OUTCOME`; mandatory-now safeguards M1..M12; increments 0..6.
- DEMO verification (branch `wo/GOAL-MT5-DEMO-VERIFY`, PROPOSED not approved): the existing paper instance is PROVEN DEMO by local records; trading-password nature is INFERRED; ownership/authorisation of the account is UNPROVEN (owner decision); one read-only broker session and one bounded lifecycle test are proposed and unapproved.
- Legacy MT5 containers and live-flagged executors are out of bounds (ADR-MT5-002).

### Other execution candidates (assess for reuse only)

- NEO's practice bridge (`neo_ftmo_executor`, `neo_dispatcher`, `neo_account_lifecycle_canary` in the NEO scripts) places orders through the raw bridge with its own account gate. It is an existing execution path with a different authority model (NEO is observer-only per the authority chain). It is a candidate to assess for lessons (request construction, return-code handling), not to reuse as code, and never to run.
- Legacy executors elsewhere on the estate: same rule. Name them in the assessment by role only.

### Prior audits this PID must not duplicate

TRON-D1-RATIFY (baseline, 148 tests, risk-gate gap, A1..A12, R-1..R-10); RECON-H2 trade-chain reconciliation (three intake models, TRON-T2/T3 findings); MT5 readiness, template contract and DEMO verification (branches above); TRON-T1 candidate; GOAL-TRIGGER-001 (not yet authored).

## Target outcome

At closure, a reviewer can read one document set and answer, for each of six hops (H1 trigger intake, H2 claim/disposition and journal, H3 risk and sizing, H4 adapter and gateway call, H5 broker execution and protection, H6 reconcile and evidence):

1. what exists, is partial, or is missing (with citation);
2. the smallest increment that closes each gap, its owner and its target repository;
3. whether that increment is provable credential-free, needs a DEMO read-only session, or needs the write-test approval;
4. the order in which the increments must land relative to the typed gateway requirement.

The output is a gap analysis and an increment list. It is not a build, not an approval, and not a backlog edit.

## Scope

All work is read-only analysis of existing branches, documents and repositories, plus authoring of evidence documents in the audit worktree.

### Reuse rules (no duplication)

- Cite, do not restate, TRON-D1-RATIFY, RECON-H2, the MT5 readiness assessment, the template contract and the DEMO verification. Re-confirm only the facts that decide a gap-matrix cell; record the re-confirmation command.
- Decisions R-1..R-10 are referenced by id. Their content is not restated.
- Any claim that contradicts a cited document is a stop-and-report finding, not a silent correction.

### Audit areas

1. **TRON D1 and candidates.** Verify the D1 baseline facts that the matrix depends on (tip, branch ancestry, file inventory, absence of runtime code, absence of PR). Inventory every TRON asset beyond documents (code, schemas, test fixtures) and every `wi-*` branch via git only. Confirm nothing exists on any TRON ref that executes, signs, or calls a broker.
2. **Risk rules and hard gates.** Map HR-01..HR-16 and the D1 check catalogue to the DEMO path. Identify the minimum set of gates that must exist and run before one DEMO order (building on TRON-D1-RATIFY N-5; do not re-derive the list, test it against the path). State which gates are deterministic and credential-free.
3. **Execution journal.** State the minimum journal behaviour the path needs for journal-before-submit (HR-08), idempotency (HR-13) and reconcile (HR-06, HR-14), against the CA rulings R1..R5 as recorded in TRON-D1-RATIFY. Identify the smallest viable store for the first path (in-memory port versus Postgres), without deciding R-4.
4. **Trigger-intake assumptions versus GOAL-TRIGGER-001.** List every assumption TRON D1, TRON-T1/T4 and HELIOS-T3 make about the trigger (envelope, identity, signing, validity, level vocabulary, claim/disposition, SL/TP derivation). Mark each as covered, contradicted, or unspecified relative to the GOAL-TRIGGER-001 contract once it exists. If that contract does not yet exist, record the assumption list as the input it needs and do not invent a contract.
5. **MT5 gateway.** Using MT5-GW-001 outcomes (merged main, PR #9 state), state the current capability against the template contract operations and ADR-MT5-001. Separate what is in the merged repository, in PR #9, and in design documents only.
6. **Other execution candidates.** Assess NEO's practice bridge and legacy executors strictly from source as reuse candidates (what to learn, what must not be reused, authority and gate differences). No execution, no import, no call.
7. **One-path composition.** Build the capability gap matrix per hop and the minimal increment list (see Deliverables). Classify every increment as credential-free, DEMO read-only session, or write-test approval.
8. **Ordering.** State the dependency order and the point at which each of these gates applies: typed gateway mandatory before any accepted TRON integration or PAPER proof; diagnostic bridge use permitted only for isolated proof that is not TRON integration.

### Coordination with MT5-GW-001

The audit reads the merged `mt5-gateway` main and PR #9 as the current truth and records the SHA read. It proposes no change to either. Where the gap list overlaps template increments 1..6 or backlog items MT5-GW-002..004, the matrix references those ids and adds nothing new.

## Non-goals

- No implementation, schema change, test code, compose file or gateway code.
- No broker call, no DEMO session, no instance start, stop, restart or alteration; no use of the diagnostic bridge.
- No contact with, inspection of, or change to the legacy MT5 containers or live-flagged executors.
- No ratification of D1 and no decision on R-1..R-10; no acceptance of any "Proposed" value.
- No authoring of GOAL-TRIGGER-001, no HELIOS or FALCON repository change.
- No backlog edit, no `pid_path`, no `DELIVERY_READY`, no approval, no running of `goal-docs --write`.
- No merge, no force push, no PR merge on any repository.
- No claim that a simulated lane satisfies ADR-MT5-001 or the state `PAPER` (R-9 is Matt's).

## Dependencies and interfaces

| Item | Relation | Interface |
|------|----------|-----------|
| `GOAL-DCP-001` | Hard dependency (CLOSED) | Control plane the PID and its evidence live in. |
| TRON-D1-RATIFY | Input, not duplicated | Baseline facts, amendment schedule A1..A12, decisions R-1..R-10. This audit is complementary and must not alter them. |
| MT5-GW-001 and PR #9 | Input | Merged main and the template contract are the MT5 truth; coordination only. |
| MT5-GW-002..004, TRON-T1..T5, HELIOS-T3, PAPER-E2E-001 | Referenced | Backlog items the increment list maps to; none is edited. |
| GOAL-TRIGGER-001 | Soft input (not yet authored) | Supplies the trigger contract; audit area 4 compares against it if present, otherwise produces its input list. |
| RECON-H2 | Input | Intake-model and ownership findings; cite by finding id. |
| Lane C outputs (HELIOS trigger) | Soft input | The trigger shape and level vocabulary the TRON side must accept. If absent at audit time, record the assumption and flag UNVERIFIED. |
| GOLD-MVP-001 | Parent | Receives the matrix and increment list; the cross-index in GOAL points here. |

## Safety boundaries

- **Read-only.** Only git reads, document reads and local test runs from scratch copies outside every repository.
- **No broker session of any kind**, no network call to a broker, no RPyC connection to any instance.
- **No legacy executor interaction.** Source of NEO and legacy executors may be read as text. They are never executed, imported, or pointed at.
- **Public repository hygiene.** `maff0000/GOAL`, `maff0000/tron` and `maff0000/mt5-gateway` are public. Evidence contains no IP addresses, hostnames of operating systems beyond role names, account or login identifiers, server strings, credentials or tokens; `./tools/secret-scan` must pass on every evidence commit.
- **No disturbance of operating instances.** Container state is read from existing recorded evidence, not from new probes, unless the PO separately authorises a probe.
- Findings that would require any of the above are recorded as "needs approval X" and left unperformed.

## Deliverables

All deliverables are committed under `audits/<date>/gold-aud-d/` in a GOAL evidence PR; TRON-facing and MT5-facing evidence is mirrored into the named repository by separate PRs (see the checklist).

1. **Source inventory and baseline re-confirmation** (`BASELINE.md`): refs and SHAs read, commands used, and for each re-confirmed fact the result and the citing document.
2. **Capability gap matrix** (`GAP-MATRIX.md`): one row per capability per hop, with the status "exists", "partial" or "missing", a citation, the owner and the classification (credential-free, DEMO read-only, write-test approval).

   | Hop | Minimum capability to assess |
   |-----|------------------------------|
   | H1 Intake | Trigger envelope, identity, signature and validity check; TradingTriggerInbox claim; duplicate rejection |
   | H2 Journal | Journal-before-submit; claim and disposition facts; idempotent intent identity; in-memory and durable port |
   | H3 Risk and size | Fixed minimum size policy; hard gates (exposure, position count, order size, daily loss, drawdown, risk lock, kill switch); fail-closed on uncertainty |
   | H4 Adapter | Broker-neutral adapter interface; simulated adapter; conformance suite; SL/TP derivation from semantic levels |
   | H5 Gateway and broker | Typed allow-list gateway; DEMO assertion; place with broker-side protection; error taxonomy; `TIMEOUT_UNKNOWN_OUTCOME` handling |
   | H6 Reconcile and evidence | Read positions/orders/deals; diff against journal; restart reconcile-before-write; evidence record |

3. **Candidate assessment** (`CANDIDATES.md`): D1 branches and the other execution candidates (including NEO's practice bridge and legacy executors, source-read only), each with reuse verdict (learn / adapt design / reject) and reason, including authority-model differences.
4. **Trigger-assumption register** (`TRIGGER-ASSUMPTIONS.md`): assumption, source, status against GOAL-TRIGGER-001.
5. **Minimum increment list** (`INCREMENTS.md`): the smallest ordered increments to one DEMO path, each with id, owner (persona or component), target repository, backlog item mapped, dependencies, classification, and a mechanical done-test. Increments are mapped to existing backlog items and template increments; a new increment id is allowed only where nothing existing covers the gap, and is justified.
6. **Proof-class separation** (`PROOF-CLASSES.md`): for the whole path, what can be proven (a) credential-free (simulated adapter, fake-broker conformance suite, deterministic risk, in-memory journal, schema and lint checks), (b) with a DEMO read-only session (account identity and `trade_allowed`, symbols, ticks, positions, orders, deals), (c) only with the write-test approval (order lifecycle, restart reconcile with a live position). Each (b) and (c) item names the approval or owner decision it needs, by reference to the DEMO verification owner decisions.
7. **Ordering statement** (`ORDERING.md`): the dependency order, with the rule that the typed gateway must exist and be approved before accepted TRON integration or PAPER proof, and that diagnostic bridge use is limited to isolated proof with no TRON connection.
8. **Findings and contradictions** (`FINDINGS.md`): contradictions between cited documents and current repositories, each classed PROVEN / INFERRED / UNPROVEN.
9. **Evidence hashes** (`EVIDENCE-HASHES.txt`) and the Evidence PR checklist below.

### CA evidence items mapping

The CA's ten evidence items are carried by GOLD-MVP-001. Until the parent PID is merged this PID uses the placeholders E1..E10 below; the parent author replaces them with the CA's numbering.

| Id | Evidence | Deliverable |
|----|----------|-------------|
| E1 | Baseline SHAs and refs read (GOAL, TRON, mt5-gateway) | 1 |
| E2 | TRON D1 and implementation-candidate inventory | 1, 3 |
| E3 | Risk rules and hard-gate coverage against the path | 2 (H3), 6 |
| E4 | Execution journal assumptions and minimum viable journal | 2 (H2) |
| E5 | Trigger-intake assumptions versus GOAL-TRIGGER-001 | 4 |
| E6 | MT5 gateway state after MT5-GW-001 | 2 (H4, H5), 8 |
| E7 | Other execution candidates assessed for reuse | 3 |
| E8 | Gap matrix exists / partial / missing | 2 |
| E9 | Minimal increment list with owner and classification | 5, 6 |
| E10 | Ordering against the typed-gateway requirement | 7 |

## Acceptance

Mechanical, checkable by a fresh auditor:

1. `./tools/goal-validate` exits 0 and `./tools/secret-scan` exits 0 on the evidence branch head.
2. Deliverables 1..9 exist at the paths named above and are non-empty.
3. `GAP-MATRIX.md` has one row per capability listed in the hop table (at least 24 rows) and every row has status in {exists, partial, missing}, a citation, an owner and a classification in {credential-free, DEMO-read-only, write-approval}; a script check finds no blank cell.
4. Every `exists` and `partial` cell cites a file path with a commit SHA or a PR number; a grep check finds no uncited cell.
5. `INCREMENTS.md` increments each map to a backlog id or template increment, or carry a stated justification for a new id; each has a done-test that is a command or an observable artefact.
6. `PROOF-CLASSES.md` places every increment in exactly one class; no increment classed credential-free references a broker, gateway instance, account or secret.
7. `ORDERING.md` contains the sentence structure: typed gateway before TRON integration or PAPER proof; a test asserts both obligations appear.
8. Reproducibility: the baseline commands in `BASELINE.md` re-run to the recorded SHAs and counts on the audit's recorded base.
9. A diff review shows no change outside `audits/` and the evidence mirrors; `backlog/backlog.yaml` and all `pids/` files other than this PID are byte-identical to base.
10. No finding is stated without a class of PROVEN, INFERRED or UNPROVEN; UNPROVEN items name the observation or decision needed.
11. Public-repo scan over all evidence for IPv4 patterns, account-id-like numerics next to the words login/account/server, and token-like strings returns nothing.
12. Fresh independent FORGE Auditor GREEN recorded against the exact evidence SHA.

## Stop conditions

Return to PO if:

- any contradiction against TRON-D1-RATIFY or the MT5 documents changes a binding ruling, an ADR or an HR;
- reading would require a broker session, bridge connection, container probe or legacy executor interaction;
- GOAL-TRIGGER-001 is authored in parallel with content that contradicts the assumption register;
- MT5-GW-001 or PR #9 changes state during the audit so that the recorded SHA no longer represents main;
- a secret, account identifier or address is found in any source being read (stop, report location only, do not copy);
- the increment list would need a decision that is Matt's by the PID or the ratification package.

Do not invent around a stop condition.

## Open decisions

| # | Decision | Owner | Note |
|---|----------|-------|------|
| 1 | Amend TRON-D1-RATIFY (option i) or accept this thin new item (option ii) | PO | Recommended: option ii (see Purpose). |
| 2 | Is the first path allowed to use an in-memory journal port for the credential-free proof ahead of the Postgres decision | PO | Depends on R-4; this audit may not decide R-4. |
| 3 | Treatment of the simulated-adapter lane in relation to the state `PAPER` | Matt | Reference R-9. |
| 4 | Whether the audit may read-only inspect NEO and legacy executor source | PO | Source read only; no execution. Recommended: yes, text only. |
| 5 | Whether audit area 4 waits for GOAL-TRIGGER-001 or proceeds with the assumption register only | PO | Recommended: proceed; refresh when the contract exists. |
| 6 | Which of the DEMO owner decisions (account entitlement, existing versus fresh instance, one read-only session) are answered before this audit closes | Matt | Reference DEMO verification section 5; needed only to classify, not to execute. |
| 7 | The TRON-side decisions the path depends on: R-1, R-2, R-4, R-5, R-6, R-7, R-8 | Matt | Referenced by id from TRON-D1-RATIFY; not restated. |

## Evidence

Required evidence package (PR into GOAL under `audits/`, mirrors into the component repositories):

- Deliverables 1..9 above with SHAs of every ref read.
- Command transcripts for re-confirmation, redacted to the public-repo rule.
- Hash list of the evidence folder.
- Independent Auditor verdict reference.

### Evidence PR checklist

- [ ] GOAL evidence PR opened from `wo/GOAL-GOLD-AUD-D`, base `main`, one commit per deliverable group, trailer per CLAUDE.md
- [ ] `./tools/goal-validate` and `./tools/secret-scan` pass on the PR head
- [ ] `maff0000/tron` evidence PR: TRON facts (inventory, gate coverage, journal, trigger assumptions) under `audits/`, no change to `main` content outside `audits/`
- [ ] `maff0000/mt5-gateway` evidence PR: MT5 facts (state after MT5-GW-001, gap rows) under `docs/evidence/`, no change to source, compose or template files
- [ ] Cross-index entry in GOAL pointing to both mirror PRs and to GOLD-MVP-001
- [ ] E1..E10 mapped to the CA's numbering in the parent PID
- [ ] Public-repo scan clean (acceptance 11)
- [ ] No change to `backlog/backlog.yaml` or other PIDs (acceptance 9)
- [ ] No broker call, bridge connection or legacy executor interaction occurred (statement signed in `FINDINGS.md`)
- [ ] Independent Auditor GREEN recorded on the evidence SHA
- [ ] Merge authorised separately by the PO; none implied by this checklist

## Approval

PENDING. No approval has been recorded for this PID candidate. Approval is recorded here by Central Architecture/PO only.

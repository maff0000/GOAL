# GOLD-AUD-D — GOLD MVP Lane D: TRON / MT5 minimum DEMO execution path gap analysis

**Lane:** research  
**Target repository:** `maff0000/GOAL`  
**Evidence:** primary PR in `maff0000/GOAL`, branch `wo/GOLD-AUD-D-evidence`, path `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/`; mirror notes on branch `wo/GOLD-AUD-D-evidence` in each of `tron` and `mt5-gateway`, path `docs/evidence/GOLD-AUD-D/`  
**Priority:** P0  
**Risk:** Medium  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  
**Complements:** `TRON-D1-RATIFY`, `MT5-GW-001`  

**Header notes:** GOAL is the primary repository for the TRON and MT5 facts, with mirror notes in `maff0000/tron` and `maff0000/mt5-gateway`. Risk Medium: this is a read-only audit and the path it analyses is capital-adjacent. `TRON-D1-RATIFY` is consumed, not redone; amendment fallback in Purpose. Evidence location follows programme-controller rulings 1 to 3 (`PORTFOLIO.md` appendix).

Header values match the registered backlog item (`backlog/backlog.yaml`, `pid_path: pids/GOLD-AUD-D.md`). Lane vocabulary is the backlog set {shared, research, trading, ops}; `research` is used for all
six audits (CA frame). Priority, lane and risk follow the CA/PO adjudication 2026-10-15 (recorded in `PORTFOLIO.md`, not in this PID); approval is recorded in the Approval section below.

**Audit id:** GOLD-AUD-D (child audit of GOLD-MVP-001)  
**Depends on:** `GOAL-DCP-001` only  
**Status:** APPROVED (Central Architecture, 16 October 2026; see Approval). Registered in the backlog as DELIVERY_READY by the governed amendment.

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

All facts below were read read-only on 2026-10-15 against GOAL `main` @ `1739e742154c77e9e2a96927dc40d4978b9cd798`; baseline now `90323b3`. Items marked UNVERIFIED must be re-read by the audit before being relied on.

### TRON

- `maff0000/tron` `main` @ `5577039` holds documentation and tooling only: `PID.md` (Product Constitution, HR-01..HR-16), gitleaks rules, a pre-commit hook. There is **no runtime code** on `main` (source: TRON-D1-RATIFY section 2.1).
- `wo/WO-TRON-D1` @ `37d5f00` is 20 commits ahead of `main`, 60 files: 12 design documents, 5 contract schemas, 7 config schemas, 25 schema examples, one test module (`tests/test_docs_baseline.py`). The only Python file in the branch is that test. Nine `wi-a..wi-i` branches are all ancestors of D1. No pull request exists for D1 (TRON-D1-RATIFY 2.2, 2.3; the file-type count was independently re-checked by this PID's author).
- D1's gate (148 tests) proves the document, schema and example set is internally consistent; it proves nothing about execution (D1 PID section 29).
- The D1 MVP check set contains no exposure, position-count, order-size, daily-loss, drawdown, consecutive-loss or risk-lock check; CHK-074 (kill switch engaged) is MVP while its setter (BL-OPS-01) is backlog (TRON-D1-RATIFY N-5).
- **GAP-TRON-FIXED-SIZE-DEMO-RISK (named gap, recorded explicitly by the consolidation per CA guidance 2026-10-15, item 5).** No backlog item owns a minimum fixed-size DEMO risk and sizing policy. `TRON-T5` pulls in `CER-R1` (it is not a minimum policy); `TRON-T5A` is only a deferred candidate (RECON-H2 F-6); and D1's MVP checks contain no exposure, size, loss or drawdown gate (D1 ratification package; see the preceding bullet). TRON cannot place a DEMO order without a quantity and without gates that run before submit. Required content, owner, candidate item and acceptance linkage are in `PORTFOLIO.md` section 3b; this audit sizes the gap against hops H3 to H5 and confirms or corrects that shape (Deliverables 2 and 5), and does not close it.
- D1 assumes three things the CA rulings of 2026-10-14 changed: a Redis board as intake, "ledger" for TRON's own store, and FALCON as the upstream (TRON-D1-RATIFY section 5, stale-content register).
- TRON-T1 candidate (branch `wo/GOAL-PID-WAVE1-C-execution`) uses the superseded "ledger" wording; TRON-D1-RATIFY section 11 holds the reconciling amendment note.
- Backlog: TRON-T1 is `PID_DRAFT`; TRON-T2..T5, HELIOS-T3, MT5-GW-002..004 are `ARCHITECTURE_REQUIRED`; PAPER-E2E-001 carries a Matt gate (`backlog/backlog.yaml` at the base SHA).
- Trigger authority (CA guidance 2026-10-15, item 2): `GOAL-TRIGGER-001` alone owns signed-trigger, outbox and inbox semantics. TRON's intake is a consumer of that contract; D1's `falcon.trade_action.v1` / `action_id` intake and the three inbound models recorded by RECON-H2 are competing assumptions to reconcile to it, not alternatives to specify.
- `GOAL-TRIGGER-001` status (programme-controller ruling 7): the drafted PID candidate is on branch `wo/GOAL-CONTRACT-TRIGGER` (commit `64c843b`) and its backlog item is on `main` since GOAL PR #5 merged (`90323b3`, 2026-10-15); the PID candidate is not on `main` and no `pid_path` is set. (TRON-D1-RATIFY N-3 recorded the branch as empty at an earlier reading; that statement is superseded.) The candidate is a proposal pending its own decisions, not an authority.

### MT5 gateway

- Canonical `maff0000/mt5-gateway` `main` = `6263d61f4cb0d4d5b16337e67c30f409bc9c5051` (CA/PO adjudication 2026-10-15; this replaces the earlier head `46308bad…` and the earlier 'PR #9 open' state, which are stale). MT5-GW-001 reconciliation is merged; PR #9 (`MT5GW-TEMPLATE-001`: instance config contract, validation suite, documentation) is MERGED and Gate A is CLOSED GREEN WITH NOTICES. Template-hardening notices are tracked in maff0000/mt5-gateway issue #10, to be resolved before the template is used. No TRON connection to the existing unrestricted bridge (see ADR-MT5-001). The functional Vantage DEMO proof remains a separate gated workstream. The GitHub PRIVATE visibility change is eligible for Matt's authorisation (DR-32); the audit's recorded SHA is whatever `main` is at audit start.
- The typed gateway does **not** exist. The only existing control surface is the existing unrestricted bridge (see ADR-MT5-001), which is out of bounds for TRON (MT5 readiness assessment; DEMO verification). Those documents pre-date Gate A closure, so their statements of the repository topology (open stacked PRs, no CI) are superseded by the paragraph above; the audit re-confirms the current capability against the merged `main`.
- The current gateway capability against the template contract is recorded in the MT5 readiness assessment and is re-confirmed, not restated, by this audit.
- Template contract (design only, branch `wo/GOAL-MT5-TEMPLATE`): broker-neutral operation set `describe`, `health`, quotes/bars/symbol spec/account/positions/orders/deals, `place_order`, `modify`, `cancel_order`, `close_position`, `reconcile`; mandatory `client_order_id` idempotency; error taxonomy including `TIMEOUT_UNKNOWN_OUTCOME`; mandatory-now safeguards M1..M12; increments 0..6.
- DEMO verification (branch `wo/GOAL-MT5-DEMO-VERIFY`, PROPOSED not approved): records the DEMO-status evidence and the owner decisions still needed; one read-only broker session and one bounded lifecycle test are proposed and unapproved.
- Legacy MT5 services and legacy trading executors are out of bounds for running or modification (ADR-MT5-002); legacy trading executors: source text only may be read; no running, no execution, no modification, no connection.

### Other execution candidates (assess for reuse only)

- Legacy practice-account tooling (identified by source inspection in the audit) is an existing execution path with a different authority model (NEO is observer-only per the authority chain). It is a candidate to assess for lessons, not to reuse as code, and never to run.
- Other legacy executors: same rule. Name them in the assessment by role only.

### Prior audits this PID must not duplicate

TRON-D1-RATIFY (baseline, 148 tests, risk-gate gap, A1..A12, R-1..R-10); RECON-H2 trade-chain reconciliation (three intake models, TRON-T2/T3 findings); MT5 readiness, template contract and DEMO verification (branches above); TRON-T1 candidate; GOAL-TRIGGER-001 (PID candidate on `wo/GOAL-CONTRACT-TRIGGER`, not on `main`; its backlog item is on `main` since GOAL PR #5 merged).

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
2. **Risk rules and hard gates.** Map HR-01..HR-16 and the D1 check catalogue to the DEMO path. Identify the minimum set of gates that must exist and run before one DEMO order (building on TRON-D1-RATIFY N-5; do not re-derive the list, test it against the path). State which gates are deterministic and credential-free. Confirm or correct the required content of `GAP-TRON-FIXED-SIZE-DEMO-RISK` (fixed DEMO base quantity from configuration; one-position-per-instrument rule; maximum open positions; maximum daily loss and trade-count guard; kill switch with a setter; hard gates before submit, fail-closed) and state the smallest credential-free proof for each element. **Validate the scope of the approved `TRON-T3A`** (CA/PO adjudication 2026-10-15: approved as a proposed P0 / high-risk, credential-free minimum DEMO sizing and risk item, subject to this validation): confirm that its content matches the six elements, that it needs no broker credential, and that it reuses or extends the `TRON-T3` hard-risk / kill-switch design. A single kill switch exists: there are no competing TRON kill switches, and `TRON-T3A` must not create a second one; report any scope that would.
3. **Execution journal.** State the minimum journal behaviour the path needs for journal-before-submit (HR-08), idempotency (HR-13) and reconcile (HR-06, HR-14), against the CA rulings R1..R5 as recorded in TRON-D1-RATIFY. Identify the smallest viable store for the first path (in-memory port versus Postgres), without deciding R-4.
4. **Trigger-intake assumptions versus GOAL-TRIGGER-001.** List every assumption TRON D1, TRON-T1/T4 and HELIOS-T3 make about the trigger (envelope, identity, signing, validity, level vocabulary, claim/disposition, SL/TP derivation). Mark each as covered, contradicted, or unspecified relative to the GOAL-TRIGGER-001 contract once it exists. If that contract does not yet exist, record the assumption list as the input it needs and do not invent a contract.
5. **MT5 gateway.** Using MT5-GW-001 outcomes (merged `main`, merged PR #9, issue #10), state the current capability against the template contract operations and ADR-MT5-001. Separate what is in the merged repository (including PR #9) and what is in design documents only.
6. **Other execution candidates.** Assess legacy practice-account tooling and other legacy trading executors strictly from source as reuse candidates (what to learn, what must not be reused, authority and gate differences). Source text only may be read; no running, no execution, no modification, no connection (CA/PO adjudication 2026-10-15). No import, no call.
7. **One-path composition.** Build the capability gap matrix per hop and the minimal increment list (see Deliverables). Classify every increment as credential-free, DEMO read-only session, or write-test approval.
8. **Ordering.** State the dependency order and the point at which each of these gates applies: typed gateway mandatory before any accepted TRON integration or PAPER proof; diagnostic bridge use permitted only for isolated proof that is not TRON integration.

### Coordination with MT5-GW-001

The audit reads the merged `mt5-gateway` main (including PR #9) as the current truth, records the SHA read, and notes issue #10's open hardening notices. It proposes no change to either. Where the gap list overlaps template increments 1..6 or backlog items MT5-GW-002..004, the matrix references those ids and adds nothing new.

## Non-goals

- No implementation, schema change, test code, compose file or gateway code.
- No broker call, no DEMO session, no instance start, stop, restart or alteration; no use of the existing unrestricted bridge.
- No contact with, or runtime inspection of, the legacy MT5 services. Legacy trading executors: source text only may be read; no running, no execution, no modification, no connection.
- No ratification of D1 and no decision on R-1..R-10; no acceptance of any "Proposed" value.
- No authoring of GOAL-TRIGGER-001, no HELIOS or FALCON repository change, and no competing trigger, outbox or inbox contract (CA guidance 2026-10-15, item 2): the trigger-assumption register records TRON's assumptions against `GOAL-TRIGGER-001`, it does not define an alternative.
- No backlog edit for `GAP-TRON-FIXED-SIZE-DEMO-RISK`: `TRON-T3A` is APPROVED as proposed subject to this audit's scope validation (DR-36 resolved), listed in `PORTFOLIO.md` section 11.4; its backlog entry is a later serial governed change and is not applied.
- No backlog edit, no `pid_path`, no `DELIVERY_READY`, no approval, no running of `goal-docs --write`.
- No merge, no force push, no PR merge on any repository.
- No claim that a simulated lane satisfies ADR-MT5-001 or the state `PAPER` (R-9 is Matt's).

## Dependencies and interfaces

| Item | Relation | Interface |
|------|----------|-----------|
| `GOAL-DCP-001` | Hard dependency (CLOSED) | Control plane the PID and its evidence live in. |
| TRON-D1-RATIFY | Input, not duplicated | Baseline facts, amendment schedule A1..A12, decisions R-1..R-10. This audit is complementary and must not alter them. |
| MT5-GW-001, merged PR #9 and issue #10 | Input | Merged main and the template contract are the MT5 truth; coordination only. |
| MT5-GW-002..004, TRON-T1..T5, HELIOS-T3, PAPER-E2E-001 | Referenced | Backlog items the increment list maps to; none is edited. |
| GOAL-TRIGGER-001 | Soft input (candidate on `wo/GOAL-CONTRACT-TRIGGER` @ `64c843b`; backlog item on `main` since PR #5 merged; the PID candidate is not on `main`) | Supplies the trigger contract; audit area 4 uses an assumption register and compares against the candidate where it exists. |
| RECON-H2 | Input | Intake-model and ownership findings; cite by finding id. |
| `GOLD-AUD-C` | No dependency (ruling 5) | D does not depend on C. D uses its assumption register for trigger intake until `GOAL-TRIGGER-001` exists; C reads D's intake facts as a soft input. |
| GOLD-MVP-001 | Parent | Receives the matrix and increment list. After D's evidence PR is accepted, one GOAL PR contributes D's entry to `audits/2026-10-15/gold-mvp/EVIDENCE-INDEX.md` (owned by `GOLD-MVP-001`; one lane per PR). |

## Safety boundaries

- **Read-only.** Only git reads, document reads and local test runs from scratch copies outside every repository.
- **No broker session of any kind**, no network call to a broker, no bridge connection to any instance.
- **No legacy executor interaction.** Source of legacy practice-account tooling and legacy trading executors may be read as text only; no running, no execution, no modification, no connection, no import.
- **Public repository hygiene.** `maff0000/GOAL`, `maff0000/tron` and `maff0000/mt5-gateway` are public. Evidence contains no IP addresses, hostnames, account or login identifiers, server strings, credentials or tokens; `./tools/secret-scan` must pass on every evidence commit.
- **No disturbance of operating instances.** Container state is read from existing recorded evidence, not from new probes, unless the PO separately authorises a probe.
- Findings that would require any of the above are recorded as "needs approval X" and left unperformed.

## Deliverables

All deliverables are committed under `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/` in the one primary GOAL evidence PR (branch `wo/GOLD-AUD-D-evidence`); TRON-facing and MT5-facing mirror notes go into the named repository under `docs/evidence/GOLD-AUD-D/` by separate PRs on the same branch name (see the checklist).

1. **Source inventory and baseline re-confirmation** (`BASELINE.md`): refs and SHAs read, commands used, and for each re-confirmed fact the result and the citing document.
2. **Capability gap matrix** (`GAP-MATRIX.md`): one row per capability per hop, with the status "exists", "partial" or "missing", a citation, the owner and the classification (credential-free, DEMO read-only, write-test approval).

   | Hop | Minimum capability to assess |
   |-----|------------------------------|
   | H1 Intake | Trigger envelope, identity, signature and validity check; TradingTriggerInbox claim; duplicate rejection |
   | H2 Journal | Journal-before-submit; claim and disposition facts; idempotent intent identity; in-memory and durable port |
   | H3 Risk and size | Fixed minimum size policy (`GAP-TRON-FIXED-SIZE-DEMO-RISK`: fixed DEMO base quantity from configuration, one position per instrument, maximum open positions, daily loss and trade-count guard, kill switch with setter); hard gates (exposure, position count, order size, daily loss, drawdown, risk lock, kill switch) before submit; fail-closed on uncertainty |
   | H4 Adapter | Broker-neutral adapter interface; simulated adapter; conformance suite; SL/TP derivation from semantic levels |
   | H5 Gateway and broker | Typed allow-list gateway; DEMO assertion; place with broker-side protection; error taxonomy; `TIMEOUT_UNKNOWN_OUTCOME` handling |
   | H6 Reconcile and evidence | Read positions/orders/deals; diff against journal; restart reconcile-before-write; evidence record |

3. **Candidate assessment** (`CANDIDATES.md`): D1 branches and the other execution candidates (including legacy practice-account tooling and legacy executors, source-read only), each with reuse verdict (learn / adapt design / reject) and reason, including authority-model differences.
4. **Trigger-assumption register** (`TRIGGER-ASSUMPTIONS.md`): assumption, source, status against GOAL-TRIGGER-001.
5. **Minimum increment list** (`INCREMENTS.md`): the smallest ordered increments to one DEMO path, each with id, owner (persona or component), target repository, backlog item mapped, dependencies, classification, and a mechanical done-test. Increments are mapped to existing backlog items and template increments; a new increment id is allowed only where nothing existing covers the gap, and is justified. `GAP-TRON-FIXED-SIZE-DEMO-RISK` appears as its own row with its required content, TRON as owner, `credential-free` classification, and the shape of the candidate backlog item (marked proposed, for PO decision).
6. **Proof-class separation** (`PROOF-CLASSES.md`): for the whole path, what can be proven (a) credential-free (simulated adapter, fake-broker conformance suite, deterministic risk, in-memory journal, schema and lint checks), (b) with a DEMO read-only session (account identity and `trade_allowed`, symbols, ticks, positions, orders, deals), (c) only with the write-test approval (order lifecycle, restart reconcile with a live position). Each (b) and (c) item names the approval or owner decision it needs, by reference to the DEMO verification owner decisions.
7. **Ordering statement** (`ORDERING.md`): the dependency order, with the rule that the typed gateway must exist and be approved before accepted TRON integration or PAPER proof, and that diagnostic bridge use is limited to isolated proof with no TRON connection.
8. **Findings and contradictions** (`FINDINGS.md`): contradictions between cited documents and current repositories, each classed PROVEN / INFERRED / UNPROVEN.
9. **Evidence hashes** (`EVIDENCE-HASHES.txt`) and the Evidence PR checklist below.

### Evidence items (CA numbering)

The ten evidence items below are CA's, in CA's numbering. The deliverable numbers refer to the Deliverables list above.

CA's ten mandatory evidence items, in CA's numbering (the numbering is CA's and is not to be changed by a lane): (1) PID/WO identifier and exact audited scope; (2) source repositories, revisions and relevant documentation references; (3) existing implementation: proven, partially proven, unverified or missing; (4) actual versus expected contract comparison; (5) tests, fixtures and evidence references; (6) specific defects and compatibility gaps; (7) reusable code and documentation; (8) minimum recommended implementation changes; (9) safety and deployment constraints; (10) independent audit verdict and any unresolved findings.

| CA # | CA evidence item | This audit puts it in | Proof method |
|---|---|---|---|
| 1 | PID/WO identifier and exact audited scope | Evidence PR header (quote of the single question and the CA directive); deliverable 1 | Quote equals approved PID |
| 2 | Source repositories, revisions and documentation references | `BASELINE.md` (deliverable 1): refs and SHAs of GOAL, TRON (main and the D1 branch) and mt5-gateway (main, with PR #9 merged), documents read | Baseline commands re-run to the recorded SHAs and counts |
| 3 | Existing implementation: proven, partially proven, unverified or missing | `GAP-MATRIX.md` (deliverable 2, at least 24 rows over hops H1..H6) and `CANDIDATES.md` (deliverable 3): each capability exists / partial / missing, mapped to proven / partially proven / unverified / missing, with citation | Every exists / partial cell cites a path with SHA or a PR number |
| 4 | Actual versus expected contract comparison | `TRIGGER-ASSUMPTIONS.md` (deliverable 4): intake assumptions of TRON D1, TRON-T1/T4 and HELIOS-T3 versus `GOAL-TRIGGER-001`; MT5 gateway state versus the template contract (GAP-MATRIX H4, H5) | Each assumption classed covered / contradicted / unspecified |
| 5 | Tests, fixtures and evidence references | `EVIDENCE-HASHES.txt` (deliverable 9) and the recorded re-confirmation command transcripts; reference to the D1 gate (148 tests) | Hash list verifies; commands reproduce |
| 6 | Specific defects and compatibility gaps | `FINDINGS.md` (deliverable 8): contradictions and defects, each PROVEN / INFERRED / UNPROVEN, plus the gap matrix rows with status missing | No finding without a class; UNPROVEN items name the needed observation |
| 7 | Reusable code and documentation | `CANDIDATES.md`: reuse verdict (learn / adapt design / reject) per candidate, including legacy practice-account tooling and legacy executors (source read only) | Verdict and reason per candidate |
| 8 | Minimum recommended implementation changes | `INCREMENTS.md` (deliverable 5) and `ORDERING.md` (deliverable 7): smallest ordered increments with owner, repository, backlog id, done-test; typed gateway before TRON integration or PAPER proof | Each increment maps to a backlog id or template increment, or a justified new id |
| 9 | Safety and deployment constraints | `PROOF-CLASSES.md` (deliverable 6) credential-free / DEMO read-only / write-approval; no broker call, bridge connection or legacy executor interaction (signed statement in `FINDINGS.md`); public-repo scan | No credential-free increment references a broker, instance, account or secret; scan empty |
| 10 | Independent audit verdict and unresolved findings | Independent auditor (AUD-3) verdict file with unresolved findings | Fresh auditor GREEN with exact SHA; merge authorised separately by the PO |

## Acceptance

Mechanical, checkable by a fresh auditor:

1. `./tools/goal-validate` exits 0 and `./tools/secret-scan` exits 0 on the evidence branch head.
2. Deliverables 1..9 exist at the paths named above and are non-empty.
3. `GAP-MATRIX.md` has one row per capability listed in the hop table (at least 24 rows) and every row has status in {exists, partial, missing}, a citation, an owner and a classification in {credential-free, DEMO-read-only, write-approval}; a script check finds no blank cell.
4. Every `exists` and `partial` cell cites a file path with a commit SHA or a PR number; a grep check finds no uncited cell.
5. `INCREMENTS.md` increments each map to a backlog id or template increment, or carry a stated justification for a new id; each has a done-test that is a command or an observable artefact.
6. `PROOF-CLASSES.md` places every increment in exactly one class; no increment classed credential-free references a broker, gateway instance, account or secret. `INCREMENTS.md` contains a row named `GAP-TRON-FIXED-SIZE-DEMO-RISK` covering all six required elements, classed credential-free (script check for the name and the six elements).
7. `ORDERING.md` contains the sentence structure: typed gateway before TRON integration or PAPER proof; a test asserts both obligations appear.
8. Reproducibility: the baseline commands in `BASELINE.md` re-run to the recorded SHAs and counts on the audit's recorded base.
9. A diff review shows no change outside `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/` and the `docs/evidence/GOLD-AUD-D/` mirror notes; `backlog/backlog.yaml` and all `pids/` files other than this PID are byte-identical to base.
10. No finding is stated without a class of PROVEN, INFERRED or UNPROVEN; UNPROVEN items name the observation or decision needed.
11. Public-repo scan over all evidence for IPv4 patterns, account-id-like numerics next to the words login/account/server, and token-like strings returns nothing.
12. Fresh independent FORGE Auditor GREEN recorded against the exact evidence SHA.

### Disposition table

**Disposition table (REQUIRED; CA/PO legacy application doctrine 2026-10-15).** The evidence PR contains `DISPOSITION.md` (format: `PORTFOLIO.md` section 7.4): one row per reusable component in scope — TRON D1 and its `wi-*` branches, TRON-T1 candidate, the MT5 gateway as merged (including the template), the existing unrestricted bridge (see ADR-MT5-001), legacy practice-account tooling and the legacy trading executors (the last two by source inspection only) — each with generation (legacy / newer canonical / currently deployed), the criteria assessed (architecture fit, code quality, determinism, test evidence, maintainability, contracts, operational dependencies, integration cost), a verdict REUSE | REFACTOR | REPLACE | RETIRE, evidence, and the approximate comparative engineering cost of reuse versus refactor versus a clean build. A verdict is a recommendation only: nothing is retired, shut down or mutated, and the lane cannot be accepted without this table (it is part of CA evidence items 7 and 8).

## Stop conditions

Return to PO if:

- any contradiction against TRON-D1-RATIFY or the MT5 documents changes a binding ruling, an ADR or an HR;
- reading would require a broker session, bridge connection, container probe or legacy executor interaction;
- GOAL-TRIGGER-001 is authored in parallel with content that contradicts the assumption register;
- `maff0000/mt5-gateway` `main` moves during the audit so that the recorded SHA no longer represents main;
- a secret, account identifier or address is found in any source being read (stop, report location only, do not copy);
- the increment list would need a decision that is Matt's by the PID or the ratification package.

Do not invent around a stop condition.

## Open decisions

| # | Decision | Owner | Note |
|---|----------|-------|------|
| 1 | Amend TRON-D1-RATIFY (option i) or accept this thin new item (option ii) | PO | Recommended: option ii (see Purpose). |
| 2 | Is the first path allowed to use an in-memory journal port for the credential-free proof ahead of the Postgres decision | PO | Depends on R-4; this audit may not decide R-4. |
| 3 | Treatment of the simulated-adapter lane in relation to the state `PAPER` | Matt | Reference R-9. |
| 4 | RESOLVED by CA/PO adjudication 2026-10-15: for legacy practice-account tooling and the legacy trading executors source text only may be read; no running, no execution, no modification, no connection. | PO | none |
| 5 | Retired by programme-controller ruling 5: audit area 4 proceeds with the assumption register until `GOAL-TRIGGER-001` exists and is refreshed when it does | none | none |
| 6 | Which of the DEMO owner decisions (account entitlement, existing versus fresh instance, one read-only session) are answered before this audit closes | Matt | Reference DEMO verification section 5; needed only to classify, not to execute. |
| 7 | The TRON-side decisions the path depends on: R-1, R-2, R-4, R-5, R-6, R-7, R-8 | Matt | Referenced by id from TRON-D1-RATIFY; not restated. |
| 8 | RESOLVED with a condition by CA/PO adjudication 2026-10-15 (DR-36): `TRON-T3A` approved as proposed (P0, high risk, credential-free); condition: this audit validates its scope and the single-kill-switch rule. Backlog application is a later governed change. | PO | blocks `PAPER-E2E-001` and `GOLD-MVP-001` acceptance until closed |

## Evidence

Required evidence package (primary PR into GOAL under `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/`, mirror notes in the component repositories):

- Deliverables 1..9 above with SHAs of every ref read.
- Command transcripts for re-confirmation, redacted to the public-repo rule.
- Hash list of the evidence folder.
- Independent Auditor verdict reference.

### Evidence PR checklist

- [ ] GOAL primary evidence PR opened from `wo/GOLD-AUD-D-evidence` (not the PID draft branch `wo/GOAL-GOLD-AUD-D`), base `main`, one commit per deliverable group, trailer per CLAUDE.md
- [ ] `./tools/goal-validate` and `./tools/secret-scan` pass on the PR head
- [ ] `maff0000/tron` mirror-note PR (branch `wo/GOLD-AUD-D-evidence`): TRON facts (inventory, gate coverage, journal, trigger assumptions) under `docs/evidence/GOLD-AUD-D/`, no change outside that path
- [ ] `maff0000/mt5-gateway` mirror-note PR (branch `wo/GOLD-AUD-D-evidence`): MT5 facts (state after MT5-GW-001, gap rows) under `docs/evidence/GOLD-AUD-D/`, no change to source, compose or template files
- [ ] After acceptance: one GOAL PR contributing D's entry (pointing to the primary PR and both mirror PRs) to `EVIDENCE-INDEX.md`, owned by GOLD-MVP-001
- [ ] CA evidence items 1 to 10 present in CA numbering (table in Deliverables)
- [ ] Public-repo scan clean (acceptance 11)
- [ ] No change to `backlog/backlog.yaml` or other PIDs (acceptance 9)
- [ ] No broker call, bridge connection or legacy executor interaction occurred (statement signed in `FINDINGS.md`)
- [ ] Independent Auditor GREEN recorded on the evidence SHA
- [ ] Merge authorised separately by the PO; none implied by this checklist

## Approval

APPROVED. Recorded 2026-10-16 by ROGUE on the written authority of Central Architecture/PO.

1. Central Architecture adjudication of the GOLD MVP Portfolio, 15 October 2026 (APPROVED WITH CORRECTIONS AND GOVERNED MERGE CONDITIONS; approves the architecture and scope of this audit PID).
2. Central Architecture formal approval, 16 October 2026, Decision: OPTION 1. The previous adjudication is confirmed as the formal approval of record for the seven GOLD PIDs, including this one. No further approval of this PID scope is required unless a substantive change is proposed.

Scope of this approval: the read-only audit scope in this PID. It authorises no deployment, production mutation, broker order, contract freeze or live-capital action.

TRON-T3A remains subject to this audit's design and dependency validation before its own separate backlog amendment.

# GOLD-AUD-F audit record: CER / HSA / DARWIN / NEO qualification-to-review path

**Audit id:** `GOLD-AUD-F` (lane research, read-only, P1). **PID:** `pids/GOLD-AUD-F.md` (APPROVED 2026-10-16). **Date of audit:** 2026-10-16.
**Branch:** `wo/GOLD-AUD-F-evidence`. **Status of this record:** DRAFT evidence. The independent verdict (CA item 10) is **pending independent audit by ROGUE**. This record is not self-certified. Replacement record: it supersedes the earlier lane F publication and carries private-source particulars at a generic level only (see section 9).
**Companions in this directory:** `DISPOSITION.md` (REUSE / REFACTOR / REPLACE / RETIRE table, required), `EXTERNAL-REGISTER.md` (information only), `AMENDMENT-PROPOSALS.md` (text only, not applied), `IDENTITY-SNAPSHOTS.md` (before / after), `APOLLO-ATHENA-EXTENSION.md` (minimum APOLLO / ATHENA extension, added by CA directive 16 Oct 2026).

Labels used for every finding: **PROVEN** (read in source or reproduced by a command recorded here), **PARTIAL**, **UNVERIFIED** (not checkable from source / GitHub within the read-only limits), **MISSING** (searched for, not present; the search is stated). A claim about absence is bounded by the searches listed in section 2 and is not a claim about anywhere else.

No GOLD strategy is selected, ranked, preferred or implied by this audit. Two HSA candidates are under review (`gold_context_breakout` 1.0.0, `wick_rejection_sequence` 0.1.0, as listed by lane B); both are treated identically and neutrally. Selection waits for audits A and B to be accepted and reconciled (DR-23).

---

## 1. CA item 1: PID / WO identifier and exact audited scope

Quoted from the approved PID (Purpose): *"Establish, from evidence, how **one** GOLD (XAUUSD) strategy can be qualified, registered, executed and reviewed using functions that are already delivered, and exactly which hops are missing, so the MVP builds only the gaps and rebuilds nothing."*

In scope: versioning, evidence, causal-testing, promotion and NEO-review audits; the 10-hop path matrix; the MVP minimum; the external evaluation register (information only); the disposition table; amendment text proposals. Out of scope (PID non-goals): any strategy selection, new engine or SaaS, backlog edit, deployment, migration, restart, broker contact, running of legacy order tooling.

The audit was done by reading source on GitHub-origin clones and by running **only** each repository's own offline test suites on `git archive` copies placed outside every clone, inside an isolated network namespace (so nothing could reach a live service). Nothing was installed from an evaluated external project.

## 2. CA item 2: source repositories, revisions, documentation references

| Repository | Visibility | Audited revision (full SHA) | Branch note |
|---|---|---|---|
| `maff0000/GOAL` | public | `ceaf0291a43d029b1a47b1c192a62ff147f05ac0` | `main`; PID base read `1739e74`, baseline `90323b3` are historical |
| `maff0000/CER` | public | `60eae45305a25f8b1ad03769e5bf4264b4d294e2` | `main`, v1.0.0 merge |
| `maff0000/HSA` | public | `279ec181b5cd78df953671e087e01b7c1190ff96` | `main` |
| `maff0000/DARWIN` | public | `bf1142b5be9f6988ec36b60ba3db9022c76a47af` | `main` (PID-006B closed) |
| NEO source repository | not a public source | identity held in the private record | `main`; referenced here at class level only; no content copied |
| `maff0000/HELIOS` | public | `7f7193d55475e40583892b94dd461b1b64d6f1ef` | `main`, v1 PRODUCT_GREEN merge |
| runtime-composition repository | not a public source | identity held in the private record | `main`; cited at class level only; no content copied |
| `maff0000/tron` | public | `5577039b5db05e70effef72c7e59df14db408419` | `main`; design PID only |

Later movement of a source: GOAL `main` advanced during the audit (a merge at `7520833f5b6b2c0b3d7f4e432b138a7b941cb302` registering `GOLD-MVP-001`). The audited base remains `ceaf0291a43d029b1a47b1c192a62ff147f05ac0` as instructed; the later change was not reviewed.

Documentation read: GOAL `pids/GOLD-AUD-F.md`; `audits/2026-10-15/gold-mvp/PORTFOLIO.md` (sections 7.1-7.4, appendices A-D); `audits/2026-10-15/gold-mvp/DECISION-REGISTER.md`; `audits/2026-10-14/reconciliation/RECONCILIATION-SUMMARY.md`; `backlog/backlog.yaml` entries CER-R1, NEO-R1, HSA-C1, DARWIN-R2, DARWIN-R3, LEAN-P1 (read only). CER `PID.md`, `docs/KNOWN-LIMITATIONS.md`, `docs/adr/ADR-001-cross-producer-evidence-reference-resolution.md`. HSA `docs/VERSIONING.md`, `strategies/README.md`. DARWIN `docs/archaeology/*` (5 files), `MEMORY.md` sections 13-17. HELIOS `docs/CONTRACTS.md` sections 4-5. the runtime-composition repository's architecture and component-delta documents (not a public source; class-level use only).

**Inputs the PID cites that could not be retrieved:** RECON-G and RECON-H1 (analysis records, 2026-10-14). The branches the reconciliation summary names for them no longer exist on the GitHub remote (remote refs listed: `main`, the DCP, backup-plan, portfolio, register and recon-PR branches, and pull heads 2, 4-10), and the commit ids quoted for them do not resolve. Their findings and decisions are therefore taken only as they are re-stated in GOAL `main`; nothing in them could be independently confirmed or contradicted from the records themselves. Where this audit checked the same fact in source (NEO exists and is not approved as a read-only GOLD MVP consumer; CER v1 is built; `EdgeProfileVersion` and `ResearchEngineAdapter` are defined nowhere; HSA-C1 emits nothing yet) it **agrees** with the restatement. No contradiction was found. Status: **UNVERIFIED as records, consistent as facts**.

Searches behind the absence claims (all `git grep` on the revisions above): `EdgeProfileVersion` and `ResearchEngineAdapter` occur only in GOAL planning documents and the backlog; no occurrence in CER, HSA, DARWIN, the NEO sources, HELIOS, the runtime-composition repository or tron. Network-client imports in HSA `hsa/` : none. CER-client usage in the NEO sources: none. CER or NEO references in DARWIN `darwin/`: documentation mentions of HSA only, no code import of HSA or CER.

## 3. CA item 3: existing implementation (path matrix and the five sub-audits)

### 3.1 Path matrix (10 hops)

| # | Hop | Mark | Finding (all strategy-neutral) | Evidence |
|---|---|---|---|---|
| 1 | Author candidate | **exists (PROVEN)** | HSA holds two `CANDIDATE` XAUUSD packages, each with a source text and an evidence index (`evidence.json`, status `NOT_LIVE`). HSA validates both structurally and semantically. 871 HSA tests pass offline. | `HSA@279ec18` `strategies/gold_context_breakout/1.0.0/package.json:869`, `strategies/wick_rejection_sequence/0.1.0/package.json:1369`; command C-2 |
| 2 | Canonical identity (`StrategyVersion` fingerprint) | **partial (PROVEN)** | The identity pair `strategy_id` + `strategy_version` is carried unchanged and is valid under every consumer's pattern (CER, HELIOS). **No fingerprint survives a hop**: HSA package has none; DARWIN's `semantic_fingerprint` exists but no importer builds it from an HSA package and DARWIN's identity is a separate opaque `strategy_version_id`; HELIOS computes its own `definition_fingerprint` (excludes the version); CER stores a git repository and commit, not a fingerprint or package hash. Three unrelated identity / fingerprint regimes, none shared. | `CER@60eae45` `src/cer/contract/models.py:107-135`, `identity.py:45,215-221`; `DARWIN@bf1142b` `darwin/specification/domain.py:146-225`, `fingerprint.py`; `HELIOS@7f7193d` `helios/integration/cer_boundary.py:120-145`; HSA package top-level keys (no fingerprint / hash key); command C-4 |
| 3 | Causal test | **partial (PROVEN)** | APOLLO core is delivered and tested, but fails closed outside a narrow envelope: ATOMIC composition only, LONG only, one timeframe, a single comparison of an OHLCV field against a literal / parameter, one instrument. **Each of the two candidates is outside that envelope** (chained composition; two timeframes; both directions; indicator-derived inputs). | `DARWIN@bf1142b` `darwin/apollo/plan_adapter.py:197-231,264-275`, `darwin/apollo/capability.py`; tests `tests/unit/test_apollo_plan_adapter.py:48,57`; table 4.2 |
| 4 | Qualification verdict (proof-grade) | **missing (PROVEN)** | The qualification and ATHENA packages are 4-line placeholders. Every APOLLO run is persisted as `APOLLO_RESULT`; nothing produces `APOLLO_PROOF`. | `DARWIN@bf1142b` `darwin/qualification/__init__.py`, `darwin/athena/__init__.py`, `darwin/apollo/persistence.py:111-112,149,186`, `darwin/core/evidence.py:10-26` |
| 5 | Deployed qualification runtime | **UNVERIFIED** | Not inspected (running systems are out of bounds). GitHub-side records say the research-contracts migration was "source accepted only, not applied to any deployed runtime" at PID-006A closure and describe a live container re-verified at PID-006B closure; whether the deployed build contains APOLLO is not stated in any source read. | `DARWIN@bf1142b` `MEMORY.md` sections 13, 17 |
| 6 | Register in CER (strategy, version, evidence) | **partial (PROVEN)** | CER write endpoints exist and are tested (440 pass, 1 skip). **No writer exists** in any audited repository: HSA has no network code; DARWIN has no CER code; the NEO sources have none; HELIOS's CER boundary is a pure identity check that "stores nothing". CER cannot read strategies, versions, experiments or runs back (write-only by documented design). | `CER@60eae45` `src/cer/api/routes.py:255-340,346-410`, `docs/KNOWN-LIMITATIONS.md` section 1; `HELIOS@7f7193d` `helios/integration/cer_boundary.py:1-30`; searches in section 2 |
| 7 | Promotion transition and authority | **partial (PROVEN)** | CER records `PromotionTransition` (strategy, version, from / to state, time, `authority` free text, `producer`, at least one evidence id, reason). It does not validate transition legality, authority, evidence class, or that cited evidence exists (accepted, never trusted: ADR-001; resolution index deferred). HSA separately enforces immutable-once-promoted and its own lifecycle (4 statuses) over package files. The two state vocabularies are unrelated and nothing links them. | `CER@60eae45` `src/cer/contract/models.py:546-593`, `src/cer/api/routes.py:701-737`, `src/cer/metadata/sqlite_store.py:1107-1150`, `docs/KNOWN-LIMITATIONS.md` section 2, ADR-001; `HSA@279ec18` `docs/VERSIONING.md` sections 1-2 |
| 8 | Execute approved version | **partial (PROVEN)** | HELIOS loads and resolves a handoff of its own package format and refuses unresolved components and nearest-version binding. It has **no promotion check** (the CER boundary is identity / fingerprint only; no lifecycle field is read) and it **refuses both HSA candidates as authored** (command C-5). HELIOS has no live HERMES transport (runtime component delta CD-1). The TRON repository holds only a design PID (4 files), so the trigger path is not built. | `HELIOS@7f7193d` `helios/integration/hsa_boundary.py:99-215`, `helios/spec/model.py:45`, `docs/CONTRACTS.md:302-400`; `tron@5577039` (4 files); runtime component delta CD-1 (not a public source; class-level); command C-5 |
| 9 | Review (NEO) | **partial (PROVEN)** | NEO review components exist at legacy and newer generations. **No CER read path and no contract usage.** The observer is **not approved as a read-only GOLD MVP consumer**: order-capable code is reachable from it (section 3.6). Its runtime state is UNVERIFIED. | confidential record (section 9); searches in section 2 |
| 10 | Feedback to research (hypothesis intake) | **missing (PROVEN)** | The CER class `NEO_HYPOTHESIS` exists; no producer (NEO) and no consumer (DARWIN, HSA) exists in the audited code. HSA's doctrine describes the rule (NEO may supply evidence; HSA governs any redesign) but implements no intake of it. | `CER@60eae45` `src/cer/contract/enums.py:17-60`; `HSA@279ec18` `docs/VERSIONING.md` section 7; searches in section 2 |

Count check: 10 hops, 10 marks, each with at least one citation or command.

### 3.2 Versioning audit (scope item 1)

For each candidate under review: HSA identity pair and package hash (SHA-256 of the committed file, an audit-local snapshot only, **not** a programme fingerprint):

| Candidate | `strategy_id` @ `strategy_version` | Lifecycle | Package file SHA-256 (audit-local) | Pattern-valid in CER / HELIOS |
|---|---|---|---|---|
| A | `gold_context_breakout` @ `1.0.0` | `CANDIDATE`, `immutable_once_promoted: true` | `1b60e9721e18e33ab2aa02f7ceb824476a57583bfda92cb2196648411d8cf5c0` | yes / yes (command C-4) |
| B | `wick_rejection_sequence` @ `0.1.0` | `CANDIDATE`, `immutable_once_promoted: true` | `5ce9fdc275d10a5f1fdfb68d52ec30b27eca982c5100f178996f1c9cb89ea957` | yes / yes (command C-4) |

Three live representations with no shared contract: HSA `strategy_package` (authoring), HELIOS `helios.strategy_package/1.0.0` (runtime), DARWIN A-007 canonical JSON to immutable `StrategyVersion` with `semantic_fingerprint` (research). The CER record is a fourth shape (id, version, git repo, git commit). The HELIOS test fixtures include a hand-authored handoff in HELIOS format that is labelled as HSA-authored, but it names different strategies from the two candidates, so no continuity between the real HSA candidates and HELIOS has been demonstrated (searched: neither candidate id appears anywhere in the HELIOS repository). Representation-authority is open decision DR-30 / lane D3 (RECON-H1 D-1); this audit supplies the facts only.

### 3.3 Evidence audit (scope item 2): CER classes, states and writers

CER defines 20 controlled evidence classes and 10 promotion states and 5 health states (`enums.py:17-140`). No document and no code states which classes a given promotion state needs (PID section "Promotion lifecycle records" says only that CER records and does not decide). So "required at each state" is **not defined anywhere** and is a PO / CA decision (F-07). What can be said from code is which classes have any producer:

| Class group | CER class(es) | Producer in audited code | Mark |
|---|---|---|---|
| Research | `SOURCE_ANALYSIS`, `STRATEGY_HYPOTHESIS` | HSA emits CER-reference documents (fixtures, `NOT_LIVE`); no writer | MISSING (writer) |
| Historical | `BACKTEST` and five others | APOLLO result exists in DARWIN's own tables only; no CER writer | MISSING (writer) |
| Forward | `SHADOW`, `PAPER`, `MT5_DEMO`, `PLUTUS` | none in audited code (TRON not built) | MISSING |
| Live | `TINY_LIVE`, `PERSONAL_LIVE`, `FUNDED_LIVE` | none | MISSING (out of MVP) |
| Learning | `NEO_OBSERVATION`, `NEO_HYPOTHESIS`, `REGIME_ANALYSIS`, `DRIFT_ALERT`, `STRATEGY_HEALTH` | none in NEO; health envelopes are consumed by NEO from another source, not written to CER | MISSING |

Scope of this "no writer" mark: the eight repositories in section 2 only. Other producers (for example the strategy-health producer) were not audited and are UNVERIFIED.

### 3.4 Causal-testing audit (scope item 3)

What `APOLLO_RESULT` can claim: a deterministic next-bar-open replay, stop-first on same-bar ambiguity, wick-based touches, MAE / MFE, mark-to-market equity, preflight identity checks, for one instrument, one timeframe, LONG only, one position, fixed research quantity, all stamped non-proof (`persistence.py:111-112,149`). What it cannot claim: qualification, proof-grade evidence, multi-timeframe or composed entries, indicators, shorts, session rules (each is a typed capability block in `errors.py` / `plan_adapter.py`).

APOLLO envelope versus the candidates (source-level; **not** run through the engine, because building an equivalent plan would be strategy design):

| Requirement of the engine (`plan_adapter.py`) | Candidate A | Candidate B |
|---|---|---|
| composition is a single `AtomicCondition` (L199) | chain of 2 atomics (context + trigger) | chain of 3 atomics (sequence) |
| direction LONG only (L207) | emits LONG and SHORT | emits LONG and SHORT |
| single `Comparison`, left side an OHLCV field, same timeframe (L218-275) | context on 4H, trigger on 5M; moving-average fields | locations on 15M, trigger on 5M; ATR and candle-shape fields |
| declared parameters exactly those the engine consumes | declares window parameter | declares two window parameters |
| **Outcome** | outside envelope (PROVEN by code read) | outside envelope (PROVEN by code read) |

The tests that pin these blocks exist (`test_non_atomic_composition_is_capability_blocked`, `test_short_direction_is_capability_blocked`). 301 DARWIN engine / specification tests pass offline; the persistence-dependent tests could not run here (a database driver is not installed, not a defect). Consequence (F-04, F-15): **no engine in the audited code can produce a `BACKTEST` evidence record for either candidate**. Whether a legacy engine outside the audited repositories could is UNVERIFIED.

### 3.5 Promotion audit (scope item 4)

| Question | Answer | Mark |
|---|---|---|
| Who authorises a transition? | `authority` is a non-empty free-text string; nobody and nothing checks it | PROVEN (models.py:561, :575-593) |
| What evidence must a transition cite? | at least one well-formed evidence id; existence not checked; ADR-001: unresolved reference is not verified support, resolution index deferred to a future contract version | PROVEN |
| Are illegal transitions refused (for example DRAFT to APPROVED)? | no, no legality table; the store records any `from_state` / `to_state` pair | PROVEN (sqlite_store.py:1107-1150, routes.py:701-720) |
| Does CER check that the strategy / version exists? | no for promotions and health records; yes for several other references (`KNOWN-LIMITATIONS` section 2 table) | PROVEN |
| HSA immutability versus CER state | independent: HSA freezes the package file when its own lifecycle says PROMOTED; CER's `PROMOTED`-like states (`APPROVED`, `LIVE_CANDIDATE`, `TINY_LIVE`) do not read or set it | PROVEN |
| Does HELIOS refuse an unpromoted version? | **no**: it loads any resolvable package; no lifecycle or CER lookup exists | PROVEN (hsa_boundary.py:99-215; cer_boundary.py) |
| Two sources of truth for "promoted" | HSA `lifecycle.status` (file) and CER promotion history (database); no reconciliation rule | PROVEN as absent |

### 3.6 NEO review audit (scope item 5)

Detail is held in a confidential record and is deliberately not reproduced here. Public-safe, class-level findings, all from source:

1. **SAFETY BLOCKER: the NEO observer is not approved as a read-only GOLD MVP consumer.** Order-capable code is reachable from it. This is a stop-condition candidate (section 9) and is the subject of a separate confidential investigation. Nothing in this record describes the routes.
2. **Coupling to live infrastructure.** Part of the NEO test suite cannot be collected or passed without live infrastructure, so it was not given network access and is UNVERIFIED.
3. **Pure and tested parts exist.** Some scoring and strategy-health consumption logic is declared pure and passes its own tests offline. Per-component test counts are held in the confidential record.
4. **No CER read path, no contract usage** (searched). Inputs are not obtained through governed contracts.
5. **Not reproducible from the repository.** Configuration and deployment path sit outside the repository; there is no dependency manifest and no CI.
6. **Some stages are LLM-driven** and nondeterministic by construction.
7. **Strategy-health authority split (RECON-G D4):** in code NEO is advisory only toward R2D2 health envelopes (cannot block or hide). Who holds authority over health in the GOLD path is undecided (DR-30); the NEO code does not claim it.
8. **Runtime state / failure class: UNVERIFIED.** The dispatch brief limits this audit to source and GitHub and forbids touching running systems, so no log was read.

## 4. CA item 4: actual versus expected contract comparison

### 4.1 Identity and fingerprint across hops (candidate A and B alike)

| Hop boundary | Identity pair | Package fingerprint / hash | Result |
|---|---|---|---|
| HSA package -> CER `StrategyVersion` | pair accepted (pattern-valid) | CER has no hash field; `git_repo` + `git_commit` only | identity survives, fingerprint cannot (F-03) |
| HSA package -> HELIOS package | pair identical in name; **package refused as authored** (wrong schema shape, command C-5) | HELIOS fingerprint is its own (excludes version) | no automated path (F-01) |
| HSA package -> DARWIN `StrategyVersion` | no importer; DARWIN identity is an opaque id plus version label | DARWIN `semantic_fingerprint` (title / thesis / provenance excluded) | no path (F-02) |
| HELIOS fingerprint vs DARWIN fingerprint | different canonicalisation and field sets | n/a | not comparable |

"Same identity and fingerprint tested hop to hop": **identity survives by naming convention only; fingerprint does not survive and is not shared by any two components**. Snapshots before and after are in `IDENTITY-SNAPSHOTS.md`.

### 4.2 Expected versus actual by interface

| Interface | Expected (PID / architecture) | Actual | Mark |
|---|---|---|---|
| CER evidence classes | 20 controlled classes | 20 present, strict parse (unknown class rejected) | PROVEN |
| CER promotion record | strategy, version, states, time, authority, producer, evidence refs, reason | all present; authority and refs unvalidated | PROVEN |
| CER read-back | query evidence, artifacts, promotions, health | present; strategies / versions / runs write-only | PROVEN |
| HSA to HELIOS handoff | HSA authored packages loadable by HELIOS | refused | PROVEN (F-01) |
| HELIOS refuses unpromoted | refuse unpromoted version | not implemented | PROVEN (F-08) |
| `APOLLO_PROOF` | produced by qualification | no producer | PROVEN |
| NEO read-only evidence access | read CER, no order path | no CER client; execution-capable code present | PROVEN |

## 5. CA item 5: tests, fixtures, evidence references

All commands run on `git archive` copies of the revisions in section 2, extracted outside any clone, with `PYTHONDONTWRITEBYTECODE=1` and `unshare -n` (no network). Results are counts printed by the test runner on 2026-10-16.

| Id | Command (relative to the extracted copy) | Result |
|---|---|---|
| C-1 | CER: `python3 -m pytest -p no:cacheprovider -q tests` | 440 passed, 1 skipped |
| C-2 | HSA: same; plus `python3 -m hsa.cli validate strategies/<id>/<ver>/package.json` for both candidates | 871 passed; both candidates: valid structurally and semantically |
| C-3 | HELIOS: same | 1005 passed |
| C-3b | runtime-composition repository (loopback enabled inside the namespace): same | passes (counts in the confidential record) |
| C-3c | DARWIN: `tests/unit tests/architecture tests/contract --continue-on-collection-errors` | 559 passed, 9 failed, 7 collection errors; the failures are a missing database-driver module and no-network scout-adapter tests (environmental, not defects); APOLLO + specification subset: 301 passed, 1 failed (driver import) |
| C-3d | NEO sources: per test file, same method | pure parts pass offline; observer-dependent tests not collectable offline (section 3.6); counts in the confidential record |
| C-4 | validate candidate ids against CER `validate_strategy_id` / `validate_strategy_version` and the HELIOS id pattern | all four checks accept both candidates |
| C-5 | load each candidate `package.json` through HELIOS `load_handoff` | both refused: `StrategySpecError` malformed strategy package (a required evaluation field is missing; an HSA-only evaluation-timeframe field is not permitted) |
| C-6 | `git grep` searches listed in section 2 and in `EXTERNAL-REGISTER.md` | as stated |

Fixtures cited: HSA `contracts/fixtures/cer/*` (8 CER-reference fixtures), HELIOS `fixtures/hsa/handoff/*` (hand-authored handoff). Nothing in this record is fabricated; items not run are labelled UNVERIFIED.

## 6. CA item 6: specific defects and compatibility gaps

Severity: BLOCKER (the one-strategy path cannot run) / MAJOR / MINOR. Owner is an existing backlog id or "no home".

| Id | Gap | Hop | Severity | Mark | Owner |
|---|---|---|---|---|---|
| F-01 | No translator from the HSA package to the HELIOS runtime package; HELIOS refuses both candidates as authored | 8 | BLOCKER | PROVEN | partial: HSA-C1 (adopts `goal.strategy/v1`); emission of the HELIOS runtime package is named in no row -> **no home** (candidate row proposed) |
| F-02 | No shared fingerprint across HSA / HELIOS / DARWIN / CER; no HSA-to-DARWIN importer | 2 | MAJOR | PROVEN | DR-30 / representation authority (RECON-H1 D-1); DARWIN-R2 is undefined; **no home** for the importer |
| F-03 | CER `StrategyVersion` has no package-hash field | 2, 6 | MINOR (workaround: record the hash as `config_hash` on evidence) | PROVEN | CER-R1 |
| F-04 | APOLLO 006B cannot test either candidate | 3 | BLOCKER for hop 3 (per candidate) | PROVEN | DARWIN-R3 (scope stale) or DARWIN-internal PID-006C onward; no GOAL row defines the extension |
| F-05 | No `APOLLO_PROOF` producer; qualification and ATHENA are placeholders | 4 | MAJOR (not needed for a non-proof MVP record) | PROVEN | DARWIN-internal; no GOAL home |
| F-06 | No writer of any evidence class into CER from any audited repository | 6 | MAJOR | PROVEN (bounded) | CER-R1b / NEO-R1 deferred candidates; HSA-to-CER and TRON-to-CER writers: **no home** |
| F-07 | Promotion: authority free text, evidence classes per state undefined, no legality table, citations unresolved | 7 | MAJOR | PROVEN | CER-R1 (partly) and a PO / CA rule (new decision) |
| F-08 | HELIOS performs no promotion check (it has `assert_promotion_immutable`, which detects a changed definition under a promoted identity; that is change detection, not a promotion gate) | 8 | MAJOR | PROVEN | **no home** (candidate row proposed) |
| F-09 | CER strategies / versions / runs unreadable | 9 | MAJOR for NEO review | PROVEN | CER-R1 (read paths) |
| F-10 | NEO has no CER client and order-capable code is reachable from the observer | 9 | BLOCKER for "read-only" claim | PROVEN | NEO-R1 plus a PO disposition ruling (DR-18 / DR-37) |
| F-11 | NEO tests partly non-hermetic; no dependency manifest or CI | 9 | MAJOR if rehabilitation is chosen | PROVEN | NEO-R0 (deferred candidate) |
| F-12 | NEO observer runtime state unknown | 9 | n/a | UNVERIFIED | HELM-operated read, outside this audit |
| F-13 | Deployed DARWIN / CER / HELIOS builds versus `main` unknown | 5 | n/a | UNVERIFIED | DARWIN-R1 PID draft |
| F-14 | No hypothesis intake in DARWIN or HSA; no NEO hypothesis producer | 10 | MINOR (deferred beyond MVP) | PROVEN | NEO-R2 / HSA-C2 deferred candidates |
| F-15 | No existing engine yields `BACKTEST` evidence for either candidate (follows F-04); MVP-minimum item 2 cannot be met with delivered engines | 3 | MAJOR | PROVEN (delivered engines in audited repos) | **no home**; options in section 8 |
| F-16 | Trigger path to TRON not built (design PID only) | 8 | BLOCKER for the MVP, outside this lane | PROVEN | TRON-D1-RATIFY, TRON-T1.. , GOAL-TRIGGER-001 |
| F-17 | HELIOS has no live HERMES transport | 8 | MAJOR, outside this lane | PROVEN (via runtime component delta CD-1) | HELIOS-T2 |
| F-18 | The two real candidates have never been run through HELIOS | 8 | MAJOR | PROVEN (no fixture, C-5) | follows F-01 |

## 7. CA item 7: reusable code and documentation

**No-rebuild register** (delivered functions the MVP must reuse; verdict detail in `DISPOSITION.md`):

| Function | Where | Reuse boundary |
|---|---|---|
| HSA versioning, immutability, lineage, validation, ambiguity refusal | `HSA@279ec18` `hsa/versioning.py`, `hsa/contracts.py`, `hsa/semantics.py`, `hsa/intake/*` | as is |
| DARWIN `StrategyVersion`, specification model, fingerprinting, research contracts, APOLLO core | `DARWIN@bf1142b` `darwin/specification`, `darwin/research_contracts`, `darwin/apollo` | as is, inside APOLLO's stated envelope; not on the MVP critical path until F-04 is resolved |
| CER registry, evidence classes, artifacts, promotion and health records, producer client | `CER@60eae45` | as is; `config_hash` carries a package hash (F-03) |
| HELIOS HSA boundary and identity checks | `HELIOS@7f7193d` `helios/integration` | as is (HELIOS dispositions belong to lane B) |
| Runtime composition (HSA + HELIOS + CER, with status reporting) | not a public source; class-level use | as is |
| NEO strategy-health consumer, judgement scorer, conflict resolver, ledger-writer invariants | NEO sources (confidential record), function level | extract as libraries; see disposition |

**External repository and SaaS evaluations:** `EXTERNAL-REGISTER.md`. Information only. The register contains no recommendation to use any external engine or service for the MVP; none is an MVP option (CA guidance 2026-10-15 item 4).

**Disposition table:** `DISPOSITION.md`, complete for the four NEO parts and for the CER, HSA, DARWIN and runtime components in the path, with the clean-read-only-service versus rehabilitation question answered and costed.

## 8. CA item 8: minimum recommended implementation changes (strategy-neutral)

### 8.1 MVP minimum for the one governed strategy (PID Deliverable 3), sequenced

Sequenced relative to the trigger path (long pole, owned elsewhere). "Before" means before the first live-like trigger; "After" means can follow it.

| # | Item | When | Delivered? | Gap / change | Owner |
|---|---|---|---|---|---|
| M1 | One frozen identity: `strategy_id@version` + package hash recorded in CER (hash as `config_hash` until a field exists) | **Before** | CER and HSA exist | writer (F-06) | HSA-C1 / new row |
| M2 | A package HELIOS can load for that identity (hop 8 handoff) | **Before** | no | translator (F-01) | HSA-C1 / HELIOS-T1 / new row |
| M3 | One clearly non-proof evidence record with artifact hash from an engine that exists | **Before** (it is the evidence the promotion cites) | **no engine for either candidate** (F-15) | see options | PO |
| M4 | One PO-recorded promotion transition citing M3 | **Before** | CER records it | authority / citation rule (F-07) and a procedural gate, because HELIOS does not check (F-08) | PO / CA rule |
| M5 | HELIOS running exactly that version | **Before** | partial | F-01, F-17, F-18 | HELIOS-T1..T3 |
| M6 | Read-only NEO review report: one strategy, CER evidence plus fires, human-readable | After | no | CER read paths (F-09), new service | NEO-R1 |
| M7 | Deferred beyond MVP: ATHENA, DARWIN-to-CER automation, hypothesis intake, `EdgeProfileVersion`, SKEPTIC | After | n/a | `EdgeProfileVersion` is not on the PAPER path (dependency graph, `RECONCILIATION-SUMMARY.md` section 5: PAPER-E2E-001 depends on HELIOS-T3, TRON-T2, T3, T4; TRON-T5 and CER-R1 are not on it) | PO |

**Options for M3, presented without preference and without naming a strategy** (PO decision after audits A and B): (a) extend APOLLO to the needed composition (DARWIN-internal PIDs, large); (b) restate a candidate within the engine's atomic envelope (a strategy change owned by HSA / PO, which this audit does not make); (c) accept forward-only evidence (`SHADOW` / `PAPER` / `MT5_DEMO` classes, which exist in CER) for the demo promotion and defer backtest evidence; (d) use an engine outside the audited repositories, which is UNVERIFIED and subject to the no-new-dependency rule.

### 8.2 Minimum APOLLO / ATHENA extension (added scope)

`APOLLO-ATHENA-EXTENSION.md`: current capability (10 marked rows), a 9-item minimal requirement set (R-1..R-9) for reproducing HELIOS atomic and chain semantics, LONG and SHORT, on the same governed facts and the same identity, the CER evidence / promotion touchpoints, and verdicts with comparative cost (about 40-75 ed extension against about 70-110 ed clean). Requirements only: no design, no authorisation. `GOLD-TREND-PO3-001` is a design candidate, not selected and not found in GOAL `main`.

### 8.3 Amendment text

`AMENDMENT-PROPOSALS.md` holds ready-to-apply text for CER-R1, NEO-R1, HSA-C1 and DARWIN-R2 (not applied; backlog untouched), the candidate rows for gaps with no home, and the list of undefined terms needing a ruling. Each change maps to an existing item or "no home".

## 9. CA item 9: safety and deployment constraints

- Read-only throughout. No broker contact; no live legacy system, service, data store or log aggregator was contacted, run, imported or scheduled. Tests were run only inside a network-isolated namespace on copies outside the clones.
- No credential was read. Secret scans found no leaks in the audited sources beyond placeholders.
- No code from any externally evaluated project was installed or executed; no outbound call was made.
- Particulars of non-public sources (component index, paths, per-file results, identities of the private revisions) are held in a confidential record outside this repository. They are intentionally not enumerated here.
- **Safety blocker (raised, not resolved):** order-capable code is reachable from the NEO observer, which therefore is not approved as a read-only GOLD MVP consumer. Whether this was already recorded in RECON-G cannot be verified (record unavailable). It is returned to ROGUE / PO and to the separate confidential investigation. No finding in this audit depends on the answer.
- Any physical retirement, shutdown, migration or deployment change needs a separate authorised work order (DR-37). Nothing in this audit does any of those.

## 10. CA item 10: independent audit verdict and unresolved findings

**Pending independent audit by ROGUE.** This record carries no self-issued verdict. Unresolved at the time of writing: F-01 .. F-18 (section 6), the UNVERIFIED items below, the safety blocker in section 9, the unavailable RECON-G / RECON-H1 records, and the PO decisions D3, D4, D5, D6, D7, D10 (DR-30, DR-18, DR-37). Evidence PR list: the replacement PR for this lane.

### UNVERIFIED items

1. NEO runtime state and failure class (F-12).
2. Deployed DARWIN / CER / HELIOS builds and applied migrations versus `main` (F-13); "Applied live migrations UNVERIFIED by this item" per PID.
3. Behaviour of the non-collectable NEO tests with live infrastructure.
4. Content of the twelve memory-fabric review records in `EXTERNAL-REGISTER.md` (carried from the PID table; not re-read).
5. RECON-G and RECON-H1 as records.
6. Whether an engine outside the audited repositories could back-test either candidate.
7. Producers of CER evidence in repositories not audited here (for example the strategy-health producer).

### Acceptance cross-check (mechanical items for the auditor)

1. Hops 10, each marked with a citation: section 3.1. 2. Count check: 10 hops; CA items 1-10 present (sections 1-10); register lists 12 review records and 5 archaeology documents (`EXTERNAL-REGISTER.md`). 3. `./tools/goal-validate` and `./tools/secret-scan`: results recorded in the handback; grep for addresses, ports and key-like strings over committed files to be repeated by the auditor. 4. Before / after identity: `IDENTITY-SNAPSHOTS.md`. 5. No external code run. 6. No backlog change. 7. Each missing mark names an owner or "no home"; no strategy ranked. 8. `DISPOSITION.md` present. 9. Independent verdict: pending.

# HELIOS-STRATEGY-STANDARD-001 — HELIOS Strategy Development Standard and Common Strategy Language (documentation and interoperability planning)

**Lane:** shared  
**Target repository:** `maff0000/HELIOS`  
**Deliverable path:** `docs/STRATEGY-DEVELOPMENT-STANDARD.md` (in the target repository; this PID does not create it)  
**Priority:** P1  
**Risk:** low  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE  
**Complements:** `GOLD-AUD-B`, `GOLD-AUD-C`, `GOLD-AUD-F`, `GOAL-CONTRACT-001`, `HELIOS-T2`  

**Header notes:** Header values match the registered backlog item (`backlog/backlog.yaml`, `pid_path: pids/HELIOS-STRATEGY-STANDARD-001.md`). Lane `shared` and priority P1 follow the registration; the backlog item depends on `GOAL-DCP-001` and on audits `GOLD-AUD-B`, `GOLD-AUD-C` and `GOLD-AUD-F` (their evidence is merged, but the audit items have not yet been advanced to an accepted-terminal state). Approval is recorded in the Approval section below.

## Status

APPROVED (Central Architecture / PO, 17 October 2026; see Approval). Registered in the backlog as BLOCKED, not DELIVERY_READY and not dispatched. The audit items it depends on (`GOLD-AUD-B`, `GOLD-AUD-C`, `GOLD-AUD-F`) are not yet in an accepted-terminal state; the move to DELIVERY_READY is a separate governed transition that happens only when every readiness gate passes.

This PID follows the Central Architecture directive of 16 October 2026 (HELIOS Strategy Development Standard and Common Strategy Language) and the authorisation of the same date to draft a bounded documentation and cross-application compatibility PID using the evidence of audits B, C and F as the initial base.

## Purpose

State, in one governed document, how a strategy is authored, described, identified, composed and reproduced across HSA, HELIOS, DARWIN (APOLLO and ATHENA), CER and NEO, without changing any of them.

Architectural standard (from the directive): **one governed strategy meaning; reusable atomic implementations; declarative composition; identical signal semantics across compatible evaluators; separately governed execution and evidence.**

The audits found that the parts exist but share no common language: HELIOS has a working atom, package and chain model; HSA authors packages that HELIOS cannot yet load; DARWIN represents the HELIOS composition vocabulary but can execute only a single-atom LONG shape; and the three bodies compute identity and fingerprints differently. This PID produces the documentation that closes the language gap and plans, but does not perform, the small adapters and decisions that follow from it.

This is documentation and interoperability planning. It is not a HELIOS rebuild.

## Current state

Evidence base (labels: PROVEN read directly; PARTIAL; UNVERIFIED). Source identities are the ones recorded in the audit evidence; the audits and this PID are read-only with respect to every source.

- **Audit B** (merged evidence in the HELIOS repository, pull request #3, merge `fd181215c35d760c279c27f1b7831f2d8121dd07`, `docs/evidence/GOLD-AUD-B/STRATEGY-MODEL.md`, `CANDIDATE-REQUIREMENTS.md`, at HELIOS source `7f7193d`). PROVEN: six shipped atoms (`golden_cross`, `momentum_volatility`, `no_wick_candle`, `range_breakout`, `rejection_wick`, `swing_proximity`); one `AtomRegistry`, no chain registry and no plugin discovery; closed fact set and closed timeframe enum; package schema `helios.strategy_package/1.0.0` (ATOMIC and CHAIN, closed world, exact decimals); four composition primitives (ALL, ANY, SEQUENCE, CONTEXT_TRIGGER); seven states; strict semver and `strategy_id` pattern; chains name exact component versions. An atom implementation is bound by its own name only, so one implementation cannot be reused under a second `strategy_id`. HSA's own package format is not loadable by HELIOS and no emitter exists.
- **Audit C** (strategy-definition reconciliation, findings AC-29 to AC-38 and C-1 to C-4; merged evidence in GOAL under `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-C/`, GOAL pull request #19, merge `0f0dc45c9765568a823c3e5fed5befcf9e4361f2`; the superseded earlier pull request is closed and is not evidence). PROVEN: HSA defines no fingerprint or canonical serialisation (immutability is enforced by a diff); HELIOS fingerprints the canonical package minus metadata and version but **includes** `strategy_id`; DARWIN fingerprints eleven named semantic fields and **excludes** all ids; canonical JSON differs in decimal, datetime, tagging and hex-prefix forms, so the three fingerprints are not comparable; DARWIN accepts any non-empty version string while HELIOS and HSA require strict semver; HSA to HELIOS and DARWIN to HELIOS adapters are missing.
- **Audit F** (merged evidence in GOAL under `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/`, GOAL pull request #18, merge `ddf6a7ad9349187dee54d6172ddfd584ab8690f3`; the superseded earlier pull request is closed and is not evidence). PROVEN: DARWIN represents the HELIOS vocabulary (ATOMIC, ALL, ANY, SEQUENCE with tie rule, CONTEXT_TRIGGER; LONG, SHORT, BOTH; SAME, OPPOSITE, ANY; the same seven state names); APOLLO executes only ATOMIC, LONG, one OHLCV-versus-literal comparison on one timeframe; ATHENA is a placeholder; HELIOS emits states and never trades, so reproduction means state-stream equality before any trade replay; the identity pair `strategy_id@strategy_version` differs from DARWIN's opaque version id. Audit F requirements R-1 to R-9 are the capability checks this standard must name; their cost estimates (40 to 75 engineer-days inside DARWIN) are audit F's and are not restated as commitments here.
- **PO3 capability question** (audit B section 2). Answer: **partly expressible**. The staged skeleton (four timeframes, ordered, bidirectional, per-stage persistence) is expressible without semantic change; the stage contents are not expressible with the six shipped atoms; chain-of-chain, multi-input atoms, per-stage ordering windows and a chain-level latch would each change v1 semantics and are not proposed. `GOLD-TREND-PO3-001` is a **design candidate only**: not selected, implemented, qualified or promoted.

## Target outcome

When this PID closes, Central Architecture can approve and the HELIOS maintainers can build from a single reviewed document and a short list of governed follow-ups:

1. `docs/STRATEGY-DEVELOPMENT-STANDARD.md` exists in the HELIOS repository, reviewed, cross-referencing (not duplicating) the authoritative HELIOS documents (`docs/ATOMS.md`, `docs/COMPOSITION.md`, `docs/CONTRACTS.md` which carries the CER identity rule, `docs/INTEGRATION.md`, `docs/RUNTIME.md` and `docs/schema/strategy_package.schema.json`; there is no separate CER document).
2. The Common Strategy Language is defined as a **vocabulary and a set of rules over the existing artefacts**, not as a new model. Each rule names the existing artefact that carries it.
3. Every gap that blocks interoperability is listed with an owner, an options list and a cost class, and none is silently resolved by the document.
4. A bounded, ordered list of follow-up work orders is returned for separate approval.

## Scope

In scope. The standard document defines the following ten topics (taken from the directive) and nothing else:

1. **Atom authoring, isolation, reusability and independence.** One condition per atom, single semantic input, no cross-atom imports, instrument-neutral and direction-explicit, no execution vocabulary, naming rule so that two uses of the same condition on different timeframes are distinguishable (audit B F4).
2. **Executable Python versus declarative JSON/YAML responsibilities.** What belongs in code (the condition and its parameters schema) and what must be declarative (identity, timeframes, roles, composition, persistence, expiry, direction relationship). Preserve the existing atom implementations, loader, schema, states and chain primitives.
3. **Parameter validation, configuration and version immutability.** Closed-world parameters, exact decimals, strict semver, a promoted version never mutates; chains name exact component versions.
4. **Composition primitives, ordering, state and expiry semantics.** The four primitives, SEQUENCE window and tie rule, CONTEXT_TRIGGER ordering limit, per-component persistence, the seven states and legal transitions, rearm only through DORMANT. Documented as they are in v1.
5. **Semantic identity, fingerprints and implementation provenance.** The identity pair; what a semantic fingerprint covers and excludes; a proposed single canonical-JSON rule and prefix form for decision (not frozen); separation of semantic identity from implementation provenance (code revision, atom hashes).
6. **LONG/SHORT behaviour, causal market-fact consumption and deterministic replay.** Closed-frame causality, no look-ahead across timeframes, the governed fact set, replay determinism, symmetric direction handling.
7. **Requirements for HSA-authored definitions and HELIOS acceptance.** What an HSA package must contain to be accepted, the acceptance checks, and the translation (emitter) gap stated as a requirement, not built.
8. **APOLLO/ATHENA semantic compatibility and capability checks.** Capability-constrained reproduction: audit F requirements R-1 to R-9 as named, fail-closed capability checks; state-stream parity before trade replay; ATHENA reference-only for the MVP.
9. **CER evidence and promotion governance.** Evidence classes, the identity and artefact hashes a run must cite, parity evidence recorded separately from performance, results of extended shapes never reusing the evidence of another shape or package hash.
10. **A worked example using the generic Trend–Pullback–PO3 family.** Presented as a **design candidate**: how far the existing v1 model expresses it, which stages need new single-input atoms, which options change semantics and are therefore not proposed.

Also in scope: a conformance checklist, a glossary of the common vocabulary mapped to the existing artefact names in HSA, HELIOS and DARWIN, an open-decisions register, and the follow-up work-order list.

## Non-goals

- No change to any HELIOS atom, loader, schema, state, chain primitive, package or fixture. No new atom is written.
- No competing strategy model and no new contract. The document describes rules over `helios.strategy_package/1.0.0`, the HSA package contract and DARWIN's specification; any proposal for a unified schema is recorded as an option only.
- No expanded chain engine: no chain-of-chain, multi-input atoms, per-stage ordering windows or chain-level latch.
- No contract freeze, including of `goal.strategy/v1`, the fingerprint rule or `goal-canon/1`. `GOAL-CONTRACT-001` keeps ownership of fact reference grammar.
- No APOLLO or ATHENA implementation or expansion; no DARWIN, HSA, CER or NEO change.
- No live strategy change, no selection, qualification or promotion of any strategy (including `GOLD-TREND-PO3-001`), no deployment, no production mutation, no broker order, no live capital.
- No new market-fact definition (owned by `HERMES-FACT-001` and `GOAL-CONTRACT-001`) and no trigger contract (owned by `GOAL-TRIGGER-001`).
- No runtime or service dependency on any third-party engine or SaaS.

## Dependencies and interfaces

- Evidence: `GOLD-AUD-B`, `GOLD-AUD-C` and `GOLD-AUD-F`. Their evidence records are merged (see Current state) and are accepted by Central Architecture as a body of findings; the corresponding audit items are listed as backlog dependencies and become satisfied when the control-plane reconciliation advances them to an accepted-terminal state. The standard cites the merged records, not the superseded pull requests.
- Authoritative HELIOS documents are cross-referenced, not duplicated.
- Interfaces owned elsewhere: market-fact names (`HERMES-FACT-001`, `GOAL-CONTRACT-001`); trigger contract (`GOAL-TRIGGER-001`); HELIOS adapter (`HELIOS-T2`); CER evidence classes (CER); DARWIN specification doctrine (DARWIN). The document names these interfaces and does not alter them.
- Unlocks: a later, separately approved fingerprint and canonical-JSON decision, the HSA-to-HELIOS emitter decision, and any new-atom work order for a selected strategy.

## Safety boundaries

Documentation only, in a public repository. No secrets, credentials, broker account identifiers, internal hostnames or addresses, or live configuration. Examples use generic instrument-neutral parameter names. No statement may describe a strategy as validated, qualified or approved for any account. The worked example must carry the text "design candidate only". The document is audited for public safety before any push.

## Deliverables

1. `docs/STRATEGY-DEVELOPMENT-STANDARD.md` in `maff0000/HELIOS`, one pull request, documentation only, passing the repository's existing checks.
2. A short evidence note (in the same pull request or in GOAL) mapping each of the ten topics to its source evidence and to the existing artefact that carries the rule.
3. An open-decisions register and follow-up work-order list returned to Central Architecture.
4. Independent technical and public-safety audits of the exact pull-request head.

## Acceptance

1. All ten topics present, each citing existing HELIOS documents or code by path and each stating a mark (PROVEN, PARTIAL, UNVERIFIED, or PROPOSED for new rules).
2. Every rule is attributed to an existing artefact; no new field, state, primitive or schema is introduced.
3. The PO3 section states "design candidate only" and reproduces audit B's answer (partly expressible), including the failure table and the five listed options, and recommends none.
4. The fingerprint and canonical-JSON content lists the differences found by audit C and is marked PROPOSED for decision, not frozen.
5. The APOLLO/ATHENA section names audit F requirements R-1 to R-9 as capability checks and states the fail-closed behaviour.
6. Diff of the pull request is limited to documentation files; no code, schema, fixture or test file is changed; existing test suite and any CI unchanged and green.
7. Independent technical audit GREEN or GREEN-WITH-NOTICE and public-safety audit SAFE at the exact head, before the pull request is published.
8. Open decisions and follow-ups are listed; none is presented as decided.

## Stop conditions

Stop and return to Central Architecture if: drafting would require changing a HELIOS atom, schema, state or primitive; a contract would need to be frozen to complete a section; a source cited by the audits proves different from the evidence; any secret, account identifier or internal address would appear in the document; or the replacement evidence for audits C or F contradicts this PID.

## Open decisions

For Central Architecture, not decided here:

- **D-1** Which artefact is authoritative for the strategy fingerprint (HELIOS `definition_fingerprint`, DARWIN `semantic_fingerprint`, or a new shared rule) and whether `strategy_id` is inside it.
- **D-2** Whether the canonical-JSON rule is HELIOS's, DARWIN's, or a new `goal-canon` form, and the hex prefix form.
- **D-3** Who owns the HSA-to-HELIOS emitter and the DARWIN-to-HELIOS comparison adapter.
- **D-4** Whether DARWIN `strategy_version_id` is constrained to strict semver or mapped.
- **D-5** Whether additive single-input atoms (audit B option 1) are the preferred route for any future PO3 work; this PID makes no selection.
- **D-6** Naming of parity evidence in CER (audit F C-2).
- **D-7** Whether the standard becomes a normative HELIOS document immediately or after the follow-up decisions above.

## Implementation plan

Planning estimate only, in engineer-days (ed), made by this PID from the size of the evidence and the ten-topic outline; it is not measured and not a commitment.

| Phase | Work | Estimate |
|---|---|---|
| 1 | Outline and cross-reference map against existing HELIOS documents; confirm sources at their recorded revisions | 1 ed |
| 2 | Draft topics 1 to 4 (atoms, python versus declarative, parameters and immutability, composition and state) from audit B and existing documents | 2 to 3 ed |
| 3 | Draft topics 5 to 6 (identity, fingerprints, causality and replay) from audits B and C | 1.5 to 2 ed |
| 4 | Draft topics 7 to 9 (HSA acceptance, APOLLO/ATHENA capability checks, CER governance) from audits B, C, F | 2 to 3 ed |
| 5 | Worked example (topic 10), glossary, conformance checklist, decisions register, follow-up list | 1.5 to 2 ed |
| 6 | Independent technical and public-safety audits, fixes, publication | 2 ed |
| Total | | roughly 10 to 13 ed |

Sequence: phases 1 to 5 by one FORGE worker in a HELIOS worktree on a work-order branch; no code touched; audits by independent auditors before any push; merge only on explicit authorisation by exact head.

## Risks

| Id | Risk | Mitigation |
|---|---|---|
| R-1 | The standard hardens into a de facto contract freeze | Every new rule marked PROPOSED; D-1 to D-7 stay open; no schema or field added |
| R-2 | A competing strategy model emerges by drafting | Rules must name an existing artefact; reviewed against Non-goals |
| R-3 | Audit C and F replacement evidence changes findings | Closure depends on replacements; cite finding ids; re-check before audit |
| R-4 | The worked example reads as selection or approval of a strategy | Mandatory "design candidate only" text; audited |
| R-5 | Public disclosure of internal detail in a public repository | Generic names only; public-safety audit before push |
| R-6 | Documentation diverges from code | Cross-reference rather than duplicate; mark each statement with its source revision |

## Evidence

- Audit B evidence (merged): `docs/evidence/GOLD-AUD-B/` in the HELIOS repository, notably `STRATEGY-MODEL.md`, `CANDIDATE-REQUIREMENTS.md`, `GAPS.md`.
- Audit C evidence (merged): `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-C/` in GOAL (pull request #19). Audit F evidence (merged): `audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-F/` in GOAL (pull request #18).
- Directive: Central Architecture, 16 October 2026 (HELIOS Strategy Development Standard and Common Strategy Language), the drafting authorisation of the same date, and the formal approval of 17 October 2026.

## Approval

APPROVED. Central Architecture / PO formally approved this PID on 17 October 2026 (`HELIOS-STRATEGY-STANDARD-001`), recorded here by ROGUE on that written authority. The approved scope is documentation and interoperability planning: the deliverable `docs/STRATEGY-DEVELOPMENT-STANDARD.md` in `maff0000/HELIOS`, covering reusable atoms, chain composition and cross-application strategy semantics.

Authorised after approval: a separately audited GOAL change registering the item (this change), and, only after an independently audited readiness transition in which every readiness gate passes, dispatch of documentation-only implementation under this PID.

Not authorised by this approval: runtime code, schema change, contract freeze, selection or promotion of any trading strategy (including `GOLD-TREND-PO3-001`, which remains a design candidate only), deployment, production mutation, broker order, or live-capital action. The open decisions D-1 to D-7 remain open and are not decided by this approval.

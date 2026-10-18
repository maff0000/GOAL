# PKG-AUTHORITY-DECISIONS-CONTRACT-TRIGGER — authority-decision package for GOAL-CONTRACT-001 and GOAL-TRIGGER-001 (drafting only)

**Lane:** shared  
**Target repository:** `maff0000/GOAL`  
**Priority:** P0  
**Risk:** medium (decision package; the contracts it concerns carry high risk)  
**Matt gate:** Yes for the trigger decisions (as `GOAL-TRIGGER-001` is already gated); No for the package itself  
**PO gate:** Yes  
**Delivery:** not applicable; decision package only  
**Relates to:** `GOAL-CONTRACT-001`, `GOAL-TRIGGER-001`, `GOLD-AUD-C`, `GOLD-AUD-B`, `GOLD-AUD-F`, `HELIOS-STRATEGY-STANDARD-001`, `HELIOS-T2`, `HELIOS-T3`, `TRON-T4`

**Header notes:** This is a DRAFT proposal prepared under the Central Architecture directive of 17 October 2026 (draft four bounded technical packages; package 2 of 4). It is not registered in `backlog/backlog.yaml`, has no `pid_path`, and does not amend `GOAL-CONTRACT-001` or `GOAL-TRIGGER-001`, which remain as registered (`PID_DRAFT` and `ARCHITECTURE_REQUIRED`, no `pid_path`). Any backlog change is a separate governed change after approval.

## Status

DRAFT. Approval PENDING. No implementation, no contract freeze and no broker access is authorised by drafting this package.

## Publication boundary

The candidate text of `GOAL-TRIGGER-001` is unpublished on GitHub main; main holds only its backlog title and digests recorded by `GOLD-AUD-C`. This package is an authority-decision package only. It does not restate, summarise, encode or exercise the trigger candidate, and it contains none of its vocabulary. Anything that cannot be said without restating it is held in the private record (see "Private record") and referenced generically. Publishing the trigger text is a decision for its owner, through its own governed change.

## Purpose

Two contracts are on the critical path of the GOLD MVP and neither has an approved normative text:

* `GOAL-CONTRACT-001`, titled `goal.strategy/v1` in the backlog: the shared strategy identity and canonical-form contract.
* `GOAL-TRIGGER-001`: the cross-system trigger contract between the strategy engine and the execution side.

They are separate artefacts with separate normative owners, but one depends on the other (the backlog already records `GOAL-TRIGGER-001` depends on `GOAL-CONTRACT-001`). Audits B, C and F found that the components disagree on identity, fingerprint and canonical form, and that no published text decides between them. This package frames who may decide, which options exist and what must be proved, so that each contract can be taken to its own approval without either absorbing the other.

## Separate normative ownership

| Aspect | `GOAL-CONTRACT-001` | `GOAL-TRIGGER-001` |
|---|---|---|
| Normative scope | What a strategy's identity, semantic fingerprint and canonical form are, shared by every system that names a strategy | The contract for the path from the strategy engine to the execution-side inbox |
| Owner of the normative text | GOAL contract owner (proposed: a named GOAL architect under CA/PO) | The trigger authority owner (proposed: named separately from the contract owner; a Matt-gated decision because the backlog already gates it) |
| Consumers | HELIOS, HSA, DARWIN (APOLLO and ATHENA), CER, FALCON, TRON, private consumers | HELIOS-T3, TRON-T4, future FALCON trigger-path work (not yet registered; only FALCON-T1 is in the backlog), GOLD-MVP-001 |
| May define for the other | Nothing about the trigger path | Nothing about strategy identity or canonical form; it must reference `GOAL-CONTRACT-001` |
| Conformance packages | CP-1 is a separate, input-side package (`PROPOSED`, not frozen) | CP-2 is reference-only; a conformance package may be rebuilt only after the owning PID is published and approved (see `contracts/packages/cp-2-trigger-outbox-inbox/PACKAGE.md`) |
| Change control | Own PID, own approval, own freeze decision | Own PID, own approval, own freeze decision |

Rule proposed for approval: no clause of either contract may be defined by reference to an implementation in a component. Components conform to the contract, not the reverse.

## Decisions required, with options

Options are listed without adopting any. Each decision names the evidence in the merged audit records. Identifiers D-1 to D-7 continue the open decisions registered in `pids/HELIOS-STRATEGY-STANDARD-001.md`; DC-n identifiers are new to this package.

### A. Decisions for `GOAL-CONTRACT-001`

| Id | Decision | Options | Evidence |
|---|---|---|---|
| D-1 | Which artefact is authoritative for the strategy fingerprint, and whether `strategy_id` is inside it | (a) HELIOS definition fingerprint; (b) DARWIN semantic fingerprint; (c) a new shared rule that each system computes beside its internal one | Lane C AC-29, AC-30, C-1, C-2, SD-10 |
| D-2 | Which canonical-JSON rule applies, and the digest form | (a) HELIOS rule; (b) DARWIN rule; (c) a new shared canonical form; any option needs published reproducibility vectors | Lane C C-1, C-13, SD-11, SD-14 |
| D-4 | Whether DARWIN's version identifier is constrained to strict semver or mapped | (a) constrain; (b) map through an adapter; (c) leave unconstrained and carry both | Lane C C-4 |
| DC-1 | Where lifecycle status lives (inside the package, outside it, or both with a defined mapping) | (a) inside; (b) outside the semantic document; (c) both with rules | Lane C AC-35, C-11 |
| DC-2 | Whether the contract is published before, with, or after the document-convergence decision in lane C section 8.6 | (a) identity and fingerprint first, defer document convergence (option O-C); (b) designate one interchange document first (O-B); (c) versioned adapters only (O-A) | Lane C 8.6 |
| DC-3 | Who owns the shared canonical-form library, if one is chosen | (a) GOAL; (b) one component owner with GOAL conformance vectors | Lane C C-13 |
| DC-4 | How CER evidence binds to a strategy definition when its identity fields are shape-checked only | (a) bind by fingerprint through the shared rule; (b) bind by identity and version with the immutability rule only | Lane C section 8.4 (CER row), referred to there as AC-36 but not listed in its findings tables; lane F |

### B. Decisions for `GOAL-TRIGGER-001`

These are decisions about authority and process. Their substance is the owner's, and is not stated here.

| Id | Decision | Options |
|---|---|---|
| DC-5 | Who is the trigger authority owner, and who approves | (a) a named GOAL architect with Matt as gate holder; (b) a component owner with GOAL review |
| DC-6 | Whether and when the candidate is published | (a) publish the candidate as a PROPOSED text through its own governed change before any package is rebuilt; (b) publish only after the owner's own review round; (c) keep it private until a reviewed redacted form exists. Lane C required (a) or (b) before a conformance package is rebuilt (finding AC-26) |
| DC-7 | Order against `GOAL-CONTRACT-001` | (a) trigger waits for the contract's identity and canonical-form decisions; (b) the two proceed in parallel with the trigger referencing the contract by version; the backlog already records the dependency |
| DC-8 | How the owner's decisions are reconciled with existing component texts (TRON, FALCON, HELIOS) | (a) the contract overrides; (b) a per-component reconciliation list owned by each component architect, as lane C section 9 already proposes |
| DC-9 | Whether any settled TRON item must change to adopt the contract, and who decides | the backlog already records this as a Matt decision; the options belong to the owner |

## Dependency graph

```
GOAL-DCP-001 (CLOSED)
   └── GOAL-CONTRACT-001  (PID_DRAFT, no pid_path)  ── owns identity + canonical form
          └── GOAL-TRIGGER-001  (ARCHITECTURE_REQUIRED, no pid_path, Matt-gated)  ── owns the trigger path
                 ├── HELIOS-T3, TRON-T4, future FALCON trigger-path work (unregistered)  (implementations; unchanged by this package)
                 └── GOLD-MVP-001  (PID approved; backlog state BLOCKED)

CP-1 (PROPOSED, input side)  ← informs GOAL-CONTRACT-001 only where it touches shared identity
CP-2 (reference-only)        ← rebuilt only after GOAL-TRIGGER-001 is published and approved
```

This package adds no item and no edge. Order of approval proposed: the `GOAL-CONTRACT-001` decisions DC-2 and D-1/D-2 first, then the `GOAL-TRIGGER-001` decisions DC-5 to DC-7, then each contract through its own PID.

## Scope of this drafting package

* Frame the decisions, owners and options above.
* Propose the acceptance proofs each contract's eventual PID must carry.
* Propose a bounded effort estimate for the two PIDs' authoring.

## Non-goals

* No restatement of the trigger candidate, and no text that would let a reader reconstruct it.
* No implementation, adapter, schema, fixture, key material or conformance package.
* No contract freeze; every rule remains PROPOSED.
* No change to `backlog/backlog.yaml`, `pids/GOAL-*.md` or the CP-1 and CP-2 packages.
* No selection of a strategy (including `GOLD-TREND-PO3-001`) and no change to HELIOS, HSA, DARWIN or CER.
* No broker, DEMO, LIVE, production, credential or deployment action.

## Technical acceptance proofs (for the two contract PIDs when authored)

Each proof is credential-free and offline.

1. **Independent derivation:** a reference built from the published text alone, by someone other than the author of the contract or a component, agrees byte for byte with the contract's published vectors.
2. **Published reproducibility vectors:** vectors exist, are public, and are reproduced by at least two independently written implementations (closes lane C SD-14).
3. **Cross-component agreement:** each component named in lane C section 8.1 either passes the vectors or has a recorded, owned adapter task; no COMPATIBLE claim without a passing test.
4. **No-leak proof:** a tooling check that the published contract text and fixtures contain no credential, address, account or key material, and that private candidate text is not republished beyond its owner's approved form.
5. **Change-control proof:** a negative test that changing any contract rule without a version change fails; promoted versions are immutable.
6. **Boundary proof:** the trigger contract references identity and canonical form only by `GOAL-CONTRACT-001` version, and `GOAL-CONTRACT-001` contains no trigger-path rule (mechanical grep over both published texts).
7. **Independent audit:** an auditor other than the author, GREEN with a public-safety review, before any freeze request.

## Unresolved owner decisions

All of D-1, D-2, D-4, DC-1, DC-2 to DC-9 above, plus: who authors each PID, whether Matt delegates the `GOAL-TRIGGER-001` gate, and whether CA wants the lane C options O-A, O-B or O-C ruled on before either PID is written.

## Estimate (planning only, not a commitment)

| Work | Engineer-days |
|---|---|
| Decision rounds with CA/PO and Matt | 2 to 3 |
| Authoring the `GOAL-CONTRACT-001` PID with vectors | 4 to 6 |
| Authoring the `GOAL-TRIGGER-001` PID (after publication decision) | 4 to 6 |
| Independent audits and public-safety reviews | 3 to 4 |
| Total | 13 to 19 |

## Private record

Detail that depends on the unpublished trigger text is not held here. A generic pointer list is held in a private file (0600) in the private store. It records which parts of the decisions above depend on the candidate and where the candidate sits, without public reproduction.

## Risks

| Id | Risk | Control |
|---|---|---|
| R-1 | A decision package becomes a de facto contract | Every item is a question or an option; nothing is stated as a rule |
| R-2 | The unpublished candidate leaks through this package | Boundary above; token sweep before any push; private record |
| R-3 | One contract absorbs the other | Separate owners and the no-cross-definition rule |
| R-4 | Components diverge while decisions wait | Lane C section 9 reconciliations remain owned by component architects |

## Approval

PENDING. This package is a draft for Central Architecture. Approval is recorded by CA/PO only, through a separate governed change, and would approve the decision framing, not either contract.

## Evidence

Merged records: GOAL PR #19 (`GOLD-AUD-C`, lane C directory) and its amendment GOAL #29 (CP-2 deferred to `GOAL-TRIGGER-001`; CP-1 cannot freeze while C-12 is open), GOAL PR #18 (`GOLD-AUD-F`), HELIOS PR #3 (`GOLD-AUD-B`), `pids/HELIOS-STRATEGY-STANDARD-001.md` (D-1 to D-7). Backlog entries for `GOAL-CONTRACT-001` and `GOAL-TRIGGER-001` verified at GOAL main `a33f954f`.

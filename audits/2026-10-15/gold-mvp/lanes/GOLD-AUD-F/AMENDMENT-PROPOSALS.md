# GOLD-AUD-F amendment text proposals (TEXT ONLY, NOT APPLIED)

Status: DRAFT, pending independent audit by ROGUE and CA / PO decision. The backlog, `pid_path` values and states are untouched by this audit. Informed by RECON-G S1-S8 and RECON-H1 P-14 only as restated in GOAL `main` (the records themselves were not retrievable; see `AUDIT-F.md` section 2). No strategy is named as selected.

## CER-R1 (current title: EdgeProfileVersion and contract v1.1 on delivered CER v1.0.0)

Proposed replacement scope text: "Contract v1.1 on delivered CER v1.0.0, bounded to what the GOLD MVP and the review path need: (1) an additive package-hash field on the strategy-version record; (2) read endpoints for strategies, strategy versions, experiments and runs; (3) the reference-resolution state and query defined by ADR-001; (4) a promotion rule set to be ruled by CA / PO: permitted transitions, minimum evidence classes per target state, and a structured authority field. `EdgeProfileVersion` is out of scope until it is defined (the term occurs in no repository; it is not on the PAPER-E2E-001 dependency path). Acceptance: existing v1.0.0 records unchanged and still readable; the 440 existing tests pass unmodified; new behaviour is versioned." Findings: F-03, F-07, F-09.

## NEO-R1 (current title: Read-only evidence/MCP architecture)

Proposed scope text: "A clean read-only intelligence service. It reads CER evidence, promotion and health records and fires, and produces a human-readable review of one strategy. It contains no order, terminal-bridge or broker code, enforced by an architecture test that fails if such imports appear. It reuses, as extracted libraries with injected input, the judgement scorer and the strategy-health consumer. It does not run, extend or import the previous runtime. Disposition of the previous runtime and of its practice-account tooling (recommended: replace and retire respectively, per `DISPOSITION.md`) is a separate CA / PO ruling under DR-37 and any physical retirement is a separate authorised work order." Depends on CER read paths (CER-R1 item 2). Findings: F-09, F-10, F-11.

## HSA-C1 (current title: HSA adopts goal.strategy/v1 and the goal.market-fact/v1 fact catalogue)

Proposed addition: "Deliverable (b): an emitter from an HSA strategy package to the HELIOS runtime package format, with conformance fixtures built from the two candidates under review and from the existing HELIOS handoff fixtures; acceptance: HELIOS loads the emitted package, the identity pair is unchanged, and a single package hash is computed once and recorded with the identity. A package hash is defined in one place and used by HSA, CER and NEO; DARWIN and HELIOS fingerprints are mapped to it or declared distinct." Findings: F-01, F-02, F-18.

## DARWIN-R2 (current title: ResearchEngineAdapter; undefined in every repository)

Proposed replacement (PO to re-scope or cancel): "Minimum APOLLO extension to reproduce HELIOS atomic and chain semantics for LONG and SHORT using the governed fact catalogue and the HSA identity pair, as the requirement set R-1..R-9 in `APOLLO-ATHENA-EXTENSION.md`. No ATHENA work. Results remain non-proof. Not authorised by this proposal." The name `ResearchEngineAdapter` should be retired or defined. Findings: F-02, F-04, F-05, F-15.

## Candidate rows for gaps with no home (proposals, not added)

| Proposed id | Title | Gap | Owner suggestion |
|---|---|---|---|
| HELIOS-PROMO-GATE | Refuse to load a strategy version whose CER promotion state is not the approved one | F-08 | HELIOS architect |
| DARWIN-CER-WRITER | Minimal writer of non-proof historical evidence records into CER | F-06 | DARWIN, after R-1 |
| HSA-CER-REGISTER | Register a frozen strategy, version and package hash in CER | F-06, M1 | HSA |
| PROMO-RULES | Ruling document: who authorises a transition, which evidence classes each state needs, trust rule for citations | F-07 | CA / PO |

## Undefined terms needing a ruling

`EdgeProfileVersion` (defined in no repository), `ResearchEngineAdapter`, `LEAN` / `LEAN-P1`, the strategy-health authority (DR-30), the representation authority for HSA / HELIOS / DARWIN (D3), and the meaning of "reproduced" for a HELIOS strategy in APOLLO (state-sequence equality; R-6). `GOLD-TREND-PO3-001` was not found in GOAL `main` and is a design candidate only.

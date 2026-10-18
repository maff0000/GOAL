# HELIOS-T2 (candidate PID) — HERMES to HELIOS external market-fact adapter (technical package, drafting only)

**Lane:** trading  
**Target repository:** `maff0000/HELIOS` (adapter package outside the pure engine)  
**Backlog item addressed:** `HELIOS-T2` (title "Live HERMES adapter"; registered, `ARCHITECTURE_REQUIRED`, no `pid_path`; P0, risk high, PO gate yes, Matt gate no). This draft is **not registered** and changes no backlog item.  
**Priority:** P0  
**Risk:** high  
**Matt gate:** No  
**PO gate:** Yes  
**Delivery:** ROGUE → FORGE (only after registration, approval and the readiness conditions below)  
**Complements:** `GOLD-AUD-A`, `GOLD-AUD-B`, `GOLD-AUD-C` (CP-1), `HERMES-FACT-001`, `GOAL-CONTRACT-001`, `HELIOS-T1`, `HELIOS-T3`, `GOLD-MVP-001`

**Header notes:** Drafted under Central Architecture's 17 October 2026 authorisation to draft four bounded technical packages (drafting only). Header values are proposals and follow the registered `HELIOS-T2` item. Nothing here is implemented, frozen or approved.

## Status

DRAFT CANDIDATE. Approval **PENDING**. Not registered, not dispatched, not `DELIVERY_READY`. It is conditioned on two things that do not yet exist: (1) the **HERMES production observations** of `GOLD-AUD-A`, whose production phase has **not run** (every production-dependent statement below is marked UNVERIFIED or PENDING), and (2) **CP-1 authority**: CP-1 (`contracts/packages/cp-1-hermes-helios-input`, version `cp-1/0.1.0`) is PROPOSED, not frozen, and GOAL has not approved it as the interface.

## Purpose

Specify the smallest governed technical package that lets HELIOS consume HERMES market facts live without weakening HELIOS's pure, deterministic engine: a HELIOS-side **external adapter**, outside the engine, that reads HERMES publication read-only, translates it to HELIOS's canonical market-fact frames under the CP-1 rules, and refuses anything it cannot translate exactly.

Context (from the accepted evidence): HELIOS today has no live HERMES transport; its entire HERMES input is fixture documents (`GOLD-AUD-A` D-A-14; `GOLD-AUD-B` G-14). Raw HERMES output is not accepted by HELIOS untranslated (floats vs exact decimals, schema identity, field names, closed-world indicator set). The Central Architecture guidance of 15 October 2026 places the reader and the translation in a HELIOS-side external adapter, with GOAL approving the interface and HERMES publishing against a `HERMES-FACT-001`-style contract.

## Current state (evidence base; labels: PROVEN read directly from source; PARTIAL; UNVERIFIED; PENDING = awaits the HELM production protocol)

- **Provider side** (`GOLD-AUD-A`, hermes pull request #193, merge `ec68407733faa5bfdbd12b901a655b59bae619b6`; source phase only): governed candle, history and indicator contracts exist at source (PROVEN, source); no repository document registers those key families (D-A-02); most persistent keys carry no expiry or validity window (D-A-03); D1 history keeps 35 bars so `ema_50`/`ema_200` are structurally null on D1 (D-A-07) (per the cited lane evidence or author estimate; not re-verified here); the H4 anchor is documented inconsistently (D-A-08); indicator method conventions (RSI, ATR) are declared only inside payloads (D-A-09); no market-fact schema string exists in HERMES (D-A-11); no candle or indicator golden samples exist in HERMES (disposition row 14). **What is actually deployed and published in production is UNVERIFIED / PENDING HELM PROTOCOL** (D-A-16, P-A-01 to P-A-09).
- **Consumer side** (`GOLD-AUD-B`, HELIOS pull request #3, merge `fd181215c35d760c279c27f1b7831f2d8121dd07`): HELIOS has a closed-world, exact-decimal, ordered-window fact contract and a deterministic fixture-fed feed; the adapter plan estimates **8 to 12 engineer-days** (per the cited lane evidence or author estimate; not re-verified here); gaps G-01 to G-22 are listed with owners (key ones below).
- **Interface** (`GOLD-AUD-C`, GOAL pull request #19, merge `0f0dc45c9765568a823c3e5fed5befcf9e4361f2`): CP-1 supplies field-level mapping tables, an ordered verdict rule list (`W`, `S`, `H`, `J`, `F` codes), fixtures (2 valid wire, 2 valid frame, 26 invalid wire, 26 invalid frame, 10 scenarios), two independent reference checkers and a reference adapter. It is PROPOSED; no field is frozen; the freeze mechanics are with `HERMES-FACT-001` and GOAL (D-C1 resolved by CA/PO 2026-10-15), and the `v1`-to-HELIOS-fact mapping belongs to this adapter (D-C3). Per the GOLD-AUD-C amendment (GOAL #29), CP-1 cannot freeze while C-12 of `GOAL-CONTRACT-001` is open, and the CP-2 half is deferred to `GOAL-TRIGGER-001` (reference-only stub; not used here).
- **Existing backlog:** `HELIOS-T2` depends on `HELIOS-T1` (`PID_DRAFT`, depends on `GOAL-CORE-001`) and `HERMES-FACT-001` (`ARCHITECTURE_REQUIRED`, no PID, depends on `HERMES-CUR-001`). `GOAL-CONTRACT-001` (`PID_DRAFT`) owns the fact-reference grammar only.

## Dependency graph

```
GOLD-AUD-A production phase (HELM, S1-S9)  ──►  accepted PROD observations (PENDING)
                                                     │
GOAL-CONTRACT-001 (fact-ref grammar) ──┐             ▼
HERMES-CUR-001 ──► HERMES-FACT-001 ────┼──► CP-1 approval / freeze decision (GOAL, PO)
   (names, payloads, publication       │             │
    semantics, status/gap carriage)    │             ▼
GOAL-CORE-001 ──► HELIOS-T1 ───────────┴──────► THIS PACKAGE (HELIOS-T2 adapter)
                                                     │
                                                     ├──► HELIOS-T3 (trigger path; also needs GOAL-TRIGGER-001)
                                                     └──► GOLD-MVP-001 integration/acceptance
```

Proposed readiness conditions for dispatch (for CA decision; not applied): `HELIOS-T1` and `HERMES-FACT-001` accepted-terminal (existing edges), **plus** an accepted `GOLD-AUD-A` production phase, **plus** a recorded GOAL decision approving CP-1 (or its successor) as the interface. Adding the last two as explicit dependencies would be a governed backlog change; this draft does not make it.

## Scope (in scope for the later build; none of it authorised now)

1. **Adapter package** in `maff0000/HELIOS`, outside the pure engine and outside any import path the engine can reach (the existing execution-blind import ban stays authoritative). The adapter owns: read-only consumption of HERMES publication, wire validation, translation to canonical frames, refusal, and the environment binding.
2. **Read-only transport boundary.** A narrow reader interface satisfied by a recorded/fake source in tests and by a read-only client in operation. Operation may use only read commands from a fixed allow-list; no write, no subscribe-and-ack, no key enumeration beyond the registered key shapes. Credentials, endpoints and environment selection come from the control plane at deployment time and are never in the repository.
3. **Translation exactly per CP-1** (or its approved successor): closed-world wire validation; exact-decimal parsing from the literal text (no binary float); instant widening; field mapping `MAPPED`/`DERIVED`/`UNSUPPORTED`; the lowest-ordinal-rule verdict; whole-window accept or refuse (no partial acceptance, repair, re-sort or default).
4. **Status-to-action table** for publisher status, freshness and gap accounting (G-06): every non-usable status refuses the bar with a named code; a missing fact is never defaulted.
5. **Environment binding**: each read is bound to the control-plane environment fields; DEV and PROD facts are never relabelled or mixed (G-05).
6. **Ingest clock as an injected input**, so replay is deterministic (G-11): identical facts and recorded ingest instants produce identical frames.
7. **Live-source seam**: a design for supplying new windows each cycle to the engine, which today builds one immutable feed at start (G-14), while keeping replay determinism and the pure engine unchanged. The seam's shape is an owner decision (below), not decided here.
8. **Golden fixtures and conformance tests** derived from CP-1, plus (later, PENDING) fixtures derived from Lane A's production observations.

## Non-goals

- No implementation, code, test, schema or fixture is produced by this drafting step.
- No contract freeze: CP-1, `goal.market-fact/v1`, `goal.strategy/v1`, the fingerprint rule and `goal-canon/1` remain unfrozen; this package does not decide fact names or payload schemas (owned by `HERMES-FACT-001`) or the reference grammar (`GOAL-CONTRACT-001`).
- No change to the pure HELIOS engine, its atoms, loader, schema, states or chain primitives; no Redis or network import in the engine.
- No HERMES change: HERMES publication gaps (G-06, G-07, G-20, the H4 anchor, D1 depth, expiry) are HERMES-owned work items, not part of this package.
- No indicator computation in the adapter; no regime fact (ARES-owned); no regime relabelling.
- No trigger path, no FALCON/TRON interface, no signing (`GOAL-TRIGGER-001`/`HELIOS-T3`).
- No broker access, credential, production access or production read is authorised or needed by this drafting step. The later build is credential-free in test; operation-time read access is a separate authorisation.
- No deployment, service change or retirement of any existing component; the deployed runtime that currently consumes HERMES is not touched (its replacement is a later, separate deployment item).
- No strategy selection or promotion (including `GOLD-TREND-PO3-001`).

## Technical acceptance proofs (for the later build; all credential-free and deterministic unless marked PENDING)

1. **CP-1 conformance.** Every CP-1 fixture yields its recorded verdict: the valid wire and frame fixtures are accepted and byte-identical to the recorded frames; each of the 26 invalid wire and 26 invalid frame fixtures is refused with exactly its recorded code; each of the 10 scenarios yields its recorded window verdict. Two independent reference checkers agree with the adapter on the full fixture set.
2. **No float, no default.** Property tests: for decimal literals with up to 6 fractional digits, the adapter's exact-decimal output equals the literal's normalised text; no code path calls a binary-float conversion on a price; deleting any required fact never produces a frame.
3. **Whole-window verdict.** A window with one refused bar is refused as a whole; the verdict is the lowest-ordinal violated rule; planted violations (mutation tests) are detected.
4. **Replay determinism.** Given the same recorded facts and the same injected ingest instants, outputs are byte-identical across runs and processes; the adapter reads no wall clock in translation.
5. **Read-only enforcement.** A test double records every command the reader issues; any command outside the allow-list fails the test; an attempted write fails closed. A static check proves the adapter package contains no write-capable client call.
6. **Boundary integrity.** The existing execution-blind import guard passes; the engine imports nothing from the adapter, Redis or a network library; the adapter imports nothing that can place an order.
7. **Environment binding.** A fact whose environment does not match the bound environment is refused; DEV facts are never presented as PROD.
8. **Status table.** Every row of the status-to-action table has a test; every non-usable status refuses with its named code.
9. **Independent audit** of the exact pull-request head: technical GREEN or GREEN-WITH-NOTICE, public-safety SAFE, with the CI and secret scan green.
10. **PENDING (production-dependent; cannot be claimed before `GOLD-AUD-A` production phase and independent acceptance):** replay of the recorded production observations through the adapter, reporting accepted and refused counts by code; confirmation that the fact families, key shapes, instrument spellings (including any alias form), H4 anchor, D1/H4 history depth and indicator availability seen in production match the CP-1 assumptions. Any mismatch returns to the owners below; none is resolved by the adapter.

## Unresolved owner decisions

| # | Decision | Owner | Evidence |
|---|---|---|---|
| OD-1 | Approve CP-1 (or successor) as the interface and decide the freeze mechanics | GOAL / PO with `HERMES-FACT-001` | D-C1 (resolved ownership), D-C3 |
| OD-2 | Fact schema identity string and version naming (HERMES `v1` vs HELIOS qualified form) | GOAL / `HERMES-FACT-001` | G-01, D-A-11 |
| OD-3 | Instrument identity and spelling (alias form vs canonical form) | GOAL / HERMES / HELIOS | G-09 |
| OD-4 | Timeframe spelling canon and the legacy daily token | GOAL / HELIOS | G-10 |
| OD-5 | Extra HERMES indicators: adapter drops, or HELIOS contract extends (closed world) | `HERMES-FACT-001` / HELIOS | G-04 |
| OD-6 | Indicator method conventions declared in a contract (RSI, ATR) | `HERMES-FACT-001` | G-08, D-A-09 |
| OD-7 | H4 anchor (session-aligned vs UTC-aligned) and fixture regeneration | HERMES / HELIOS | D-A-08, G-17 |
| OD-8 | History depth for `ema_200` on H4 and D1 | HERMES | G-07, D-A-07 |
| OD-9 | Numeric form on the wire (HERMES number vs decimal text) | PO | D-C5 |
| OD-10 | Environment discriminator and its binding to the control plane | HERMES / HELIOS / control plane | G-05 |
| OD-11 | Live-source seam shape and cadence (pull cycle vs other), and where the adapter runs | HELIOS architect / PO | G-14 |
| OD-12 | Optional `regime` field: keep in HELIOS or remove | ARES / HELIOS-T1 | G-13 |
| OD-13 | Whether the readiness conditions above are added as backlog dependencies | CA / ROGUE | this draft |

## Effort estimate

**8 to 12 engineer-days** for the adapter build, **unchanged from `GOLD-AUD-B`** (ADAPTATION-PLAN steps 5 and 6; reader, translation, environment binding, golden fixtures and tests) (per the cited lane evidence or author estimate; not re-verified here). The CP-1 fixtures and two reference checkers already exist, which lowers fixture authoring, but the live-source seam (G-14), the read-only transport boundary and the status table add work the lane B estimate already counted as the adapter; no reduction is claimed. **Not included:** HERMES-owned publication gaps; `HERMES-FACT-001` and `HELIOS-T1` themselves; independent audits; deployment; and a **contingency of about 2 to 3 engineer-days** (per the cited lane evidence or author estimate; not re-verified here) that applies only if the production observations (PENDING) show spelling, anchor, depth or key-shape divergence that changes the translation tables. The estimate is a planning figure from files, tests and decisions touched, not a measurement or a commitment.

## Risks

1. **Production divergence** (HIGH, UNVERIFIED): the deployed publisher is documented as older than the audited source; fact families, keys, alias forms or depth may differ. Mitigation: no dispatch before the production phase is accepted; fixtures from observation.
2. **CP-1 freeze risk**: CP-1 is PROPOSED; building before approval risks rework. Mitigation: dependency above; version rules in CP-1.
3. **Silent coercion**: float or alias leniency could pass wrong data. Mitigation: closed world, exact decimals, whole-window refusal, mutation tests.
4. **Read path becoming a write path** (capital-adjacent): Mitigation: allow-list, recording test double, static check, separate operation-time authorisation.
5. **Environment confusion** (DEV vs PROD): Mitigation: binding and refusal (proof 7).
6. **Non-determinism from the ingest clock**: Mitigation: injected clock and replay proof (proof 4).
7. **Scope creep** into HERMES fixes, regime, triggers or deployment: Mitigation: non-goals and owner table.
8. **Stale evidence**: the audit source revisions will move. Mitigation: re-verify SHAs at dispatch.

## Safety boundaries

Documentation/drafting only, in a public repository. No secrets, credentials, broker account identifiers, internal hostnames or addresses, or live configuration. No production access, no broker access, no deployment, no contract freeze, no order, no strategy promotion is authorised by this draft.

## Stop conditions

Stop and return to Central Architecture if: the production phase reveals that the published facts cannot satisfy CP-1 without a HERMES change; CP-1 approval is withdrawn or reshaped; any step would require production access, a credential or a write path; or the adapter would need to enter the pure engine.

## Evidence

`GOLD-AUD-A` (hermes #193 merge `ec68407733faa5bfdbd12b901a655b59bae619b6`: `docs/evidence/GOLD-AUD-A/` defects D-A-01 to D-A-20, disposition, consumer mapping); `GOLD-AUD-B` (HELIOS #3 merge `fd181215c35d760c279c27f1b7831f2d8121dd07`: `docs/evidence/GOLD-AUD-B/ADAPTATION-PLAN.md`, `GAPS.md`, `CONTRACT-MAPPING.md`); `GOLD-AUD-C` (GOAL #19 merge `0f0dc45c9765568a823c3e5fed5befcf9e4361f2`: `contracts/packages/cp-1-hermes-helios-input/`, lane C `RECONCILIATION.md`, `DISPOSITION.md`); `GOLD-AUD-F` (GOAL #18 merge `ddf6a7ad9349187dee54d6172ddfd584ab8690f3`). Lane A production observations: **none yet**.

## Approval

PENDING. This is a drafting deliverable. Central Architecture / PO approval, backlog registration and the readiness conditions above are required before any dispatch. Nothing here approves, freezes or authorises implementation.

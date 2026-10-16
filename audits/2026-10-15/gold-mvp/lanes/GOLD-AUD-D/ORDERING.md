# GOLD-AUD-D ORDERING: dependency order and gate points

Deliverable 7. CA evidence item 8 (ordering half). Increment ids are those of `INCREMENTS.md`.

## 1. The two binding obligations

1. The typed gateway must exist and be approved before accepted TRON integration or PAPER proof.
2. Diagnostic bridge use is permitted only for isolated proof that is not TRON integration.

Reading of the first obligation used here: "accepted TRON integration" means any change in which the TRON adapter is accepted as working against a real gateway instance (INC-14 and later); "PAPER proof" means any proof offered toward the state PAPER (INC-15, INC-16, INC-17, `PAPER-E2E-001`). A TRON adapter built and tested against the gateway's fake backend (INC-11) is not an accepted integration, because it touches no instance. A simulated end-to-end rehearsal (INC-12) is not PAPER proof and cannot carry the state PAPER (R-9 is Matt's; ADR-MT5-001 required proofs are Vantage-specific).

Reading of the second obligation used here: the existing unrestricted bridge is never connected to TRON, by any adapter, test, rehearsal or harness. Any diagnostic use by the gateway maintainers is a gateway-side, isolated, owner-approved proof with no TRON process in the loop. This audit made no such use and no connection of any kind.

## 2. Order

```text
Wave 1  credential-free, TRON side           Wave 1' credential-free, gateway side
  INC-01 ratify D1 (Matt)                       INC-08 clear issue #10 notices
  INC-02 freeze trigger contract (Matt gate)    INC-09 digest-pinned image
  INC-03 journal (needs INC-01)                 INC-10 typed service + fake backend (needs INC-09 for image integration)
  INC-04 adapter interface + simulated adapter
  INC-05 GAP-TRON-FIXED-SIZE-DEMO-RISK (TRON-T3A): minimum sizing/risk + the single kill state (needs INC-03)
  INC-06 extended hard risk limits (TRON-T3 extends INC-05; not on the minimum path)
  INC-07 inbox intake (needs INC-03, INC-02)
  INC-11 Vantage adapter vs fake backend (needs INC-04, INC-10)
  INC-12 simulated rehearsal (needs INC-04, INC-05, INC-07)  <- first complete credential-free run; not PAPER

GATE A  typed gateway exists AND is approved (INC-10 merged and approved)
Wave 2  DEMO read-only (approvals of PROOF-CLASSES section 1, INC-13 row)
  INC-13 first DEMO instance, read-only proof (gateway)
  INC-14 adapter reads through the gateway  <- first accepted TRON integration

GATE B  DEMO write-test approval; Matt gate on the capital-risk item
Wave 3  write-approval
  INC-15 order lifecycle proof
  INC-16 restart and recovery with a live position
  INC-17 one order end to end (`PAPER-E2E-001`)  <- PAPER proof
```

## 3. Where each gate applies

| Gate | Applies before | Why |
|---|---|---|
| D1 ratified (R-1..R-10, Matt) | INC-03 onward is built against the amended baseline; INC-01 must land first | A build against an unratified baseline repeats the stale intake and wording (F-D-03, RAT@d5f6d32 section 5) |
| Trigger contract frozen | INC-07 merge (the build may start against the draft and signed fixtures) | One owner for intake semantics (CA guidance 2026-10-15 item 2) |
| INC-05 (`TRON-T3A` kill state) before INC-06 (`TRON-T3` extension) | INC-06 | One kill switch, one owner; `TRON-T3` extends (F-D-01) |
| Journal port before gates and adapter | INC-04..INC-07 | Gates read journal state; HR-08 |
| Typed gateway exists and is approved (Gate A) | INC-14, INC-15, INC-16, INC-17 and any PAPER claim | Obligation 1 |
| Issue #10 notices cleared | first use of the template for any instance (INC-13) | CA direction recorded in issue #10 |
| DEMO read-only approval | INC-13, INC-14 | `DEMO@da2e4ea` section 5 |
| DEMO write-test approval | INC-15, INC-16, INC-17 | Test plan and per-run authorisation |
| Matt gate | INC-17 (`PAPER-E2E-001`, capital-risk item) | State machine: PAPER to LIVE gating is Matt's |
| No LIVE | never in this programme step | The gateway template refuses LIVE; no increment authorises it |

## 4. Orderings that look necessary but are not (evidence)

- INC-11 and INC-12 do not wait for the real gateway or for any DEMO instance (`H2@2780076` F-5, RAT@d5f6d32 N-6).
- INC-07 does not wait for a running HELIOS signer (backlog comment on `TRON-T4`, GOAL@ceaf029).
- OPS items gate LIVE only (`H2@2780076` F-7); none is a precondition of the DEMO path. Scheduling the legacy-estate item before any write test is advisable but is not a declared dependency.

## 5. Interaction with the backlog as it stands (findings only)

Under the CA arrangement of 16 Oct 2026, `TRON-T3A` (`depends_on: [TRON-T1]`) owns the minimum baseline and the single kill state, and `TRON-T3` extends it. The drafted `TRON-T3` still has `depends_on: [TRON-T1]` only, so the backlog graph does not yet force INC-05 before INC-06; adding `TRON-T3A` to `TRON-T3.depends_on` is acyclic on GOAL `main` `e80fcda` (B19). The minimum DEMO path then waits for `TRON-T3A` but not for `TRON-T3` in full nor for `TRON-T5`; `PAPER-E2E-001` and `GOLD-MVP-001` list `TRON-T3` directly today (F-D-01). No backlog edit is made or proposed as applied.

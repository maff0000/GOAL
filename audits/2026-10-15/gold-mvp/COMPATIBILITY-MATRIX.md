# GOLD MVP consolidated contract compatibility matrix

Owned by `GOLD-MVP-001`. Single writer: the `GOLD-MVP-001` programme lead. There is no second matrix. Lanes contribute rows by one GOAL pull request each, after their evidence is accepted for contribution (`pids/GOLD-MVP-001.md`, deliverable 3).

## Reading rules

* Interfaces covered by the PID: market-fact input, strategy contract, signed trigger, inbox, execution journal, FALCON event families. An interface with no row here has not been assessed by any contributed lane; absence is not compatibility.
* Status (PID vocabulary): `COMPATIBLE` (no translation and no change on either side, supported by an executed conformance test), `ADAPTER` (a named owner must build or change something), `INCOMPATIBLE` (the pair cannot work as published; a decision or redesign is needed), `UNVERIFIED` (not established from source or an executed test), `NOT-ASSESSED` (the lane recorded the pair but did not assess compatibility, for example because it is not an input relation).
* **No row is `COMPATIBLE`.** None is supported by an executed conformance test between real components; source-level agreement is recorded as evidence, not as a compatible status.
* Provider and consumer versions are repository revisions (short SHAs of public repositories) or `not built` / `not published`. A row about an unpublished or unbuilt component records that, and nothing about its content.
* `Owner / closing item` is the backlog item or authority that closes the gap; `none assigned` means the lane found no backlog home. A row is evidence of a gap, not an assignment.
* A row does not freeze any contract. `GOLD-MVP-001` acceptance criterion AC-2 (zero `INCOMPATIBLE` or `UNVERIFIED` rows on the critical path) is far from met; this file records that honestly.

## Rows

| Id | Interface | Provider | Provider version | Consumer | Consumer version | Status | Owner / closing item | Evidence |
|---|---|---|---|---|---|---|---|---|
| M-D-01 | signed trigger / inbox | trigger authority (`GOAL-TRIGGER-001`) | not published | TRON intake design (D1 branch) | `37d5f00`, unmerged design | UNVERIFIED | `GOAL-TRIGGER-001`; TRON intake item | lane D F-D-12 (design has no signature or key-trust concept), F-D-17; `TRIGGER-ASSUMPTIONS.md`; the authority is unpublished, so no conformance statement is possible |
| M-D-02 | execution journal | TRON journal (`TRON-T1` candidate) | not built | reconciliation and evidence consumers | not built | ADAPTER | `TRON-T1` | lane D `GAP-MATRIX.md` hops H2 and H6 (rows `missing` / `partial`) |
| M-D-03 | risk and size admission | TRON D1 check set | `37d5f00`, design only | minimum DEMO path (single-position, size, loss and trade-count gates) | not built | ADAPTER | `TRON-T3A` (scope approved 17 Oct 2026), then `TRON-T3` | lane D F-D-04, F-D-05, F-D-06, F-D-14 |
| M-D-04 | protective-order policy | trigger (execution-blind by design) | not published | TRON order path | not built | ADAPTER | `TRON-T3A` (protective-level derivation and fail-closed validation in the approved PID scope) | lane D F-D-07 |
| M-D-05 | typed broker gateway | typed MT5 gateway | does not exist (`6263d61` holds only the unrestricted control surface, a documented hazard) | TRON broker adapter | not built | ADAPTER (build required; blocker for any TRON integration) | mt5-gateway typed-gateway items (named in lane D F-D-09) | lane D F-D-11 |
| M-D-06 | DEMO-only latch | mt5-gateway container | `6263d61` | DEMO acceptance run | not built | ADAPTER | mt5-gateway items | lane D F-D-10 (no in-container runtime assertion found; enforcement is by lint and render tooling) |

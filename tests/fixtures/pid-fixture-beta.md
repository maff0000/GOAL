# BETA-001 — fixture PID for the DELIVERY_READY agreement case

**Lane:** Ops
**Target repository:** `maff0000/GOAL`
**Priority:** P2
**Risk:** Capital
**Matt gate:** Yes
**PO gate:** Yes
**Delivery:** ROGUE → FORGE

This is a test fixture, not a real Product Initiation Document. It exists so
`tests/fixtures/valid.yaml` can hold a `DELIVERY_READY` item that is genuinely
delivery-ready: `DELIVERY_READY` requires a canonical PID, so an item in that
state with `pid_path: null` is `MISSING_PID`, not a valid document.

It deliberately differs from `pid-fixture.md` in every compared label it
shares, and declares a `Risk` label that `pid-fixture.md` omits. Agreement is
therefore being proven against a second, distinct label set — including a
`Risk` comparison and a `Matt gate` of `Yes` — rather than against one set of
values that might happen to match for the wrong reason.

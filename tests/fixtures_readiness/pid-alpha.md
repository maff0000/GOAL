# ALPHA-001 — fixture PID

**Lane:** Shared
**Target repository:** `maff0000/alpha`
**Priority:** P0
**Matt gate:** No
**PO gate:** Yes

A test fixture, not a real Product Initiation Document. It exists so
`multiple_ready.yaml`'s ALPHA-001 can be genuinely dispatch-ready: readiness
requires the item to declare a PID, and this file is the PID it declares.

One fixture PID per item, rather than one shared file, so the payload has to
carry *each item's own* `pid_path` — a payload that reused one value for all
three entries would pass a single-file version of this fixture.

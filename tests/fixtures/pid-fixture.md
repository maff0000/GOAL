# PIDFIX-001 — fixture PID for backlog/PID agreement tests

**Lane:** Shared
**Target repository:** `maff0000/GOAL`
**Priority:** P0
**Matt gate:** No
**PO gate:** Yes
**Delivery:** ROGUE → FORGE

This is a test fixture, not a real Product Initiation Document. It exists to
give `BACKLOG_PID_MISMATCH` something to compare against.

Three properties are deliberate:

1. Labels are spelled and cased as a canonical PID spells them (`Shared`, not
   `shared`), so the comparison must be case-insensitive.
2. `Target repository` is wrapped in backticks, so the value must be stripped
   of them before comparison.
3. There is **no** `Risk` label, and `Delivery` is a label the comparison does
   not know. A label the PID omits is not a mismatch, and a label outside the
   compared set is ignored — a PID is prose, and only the metadata it actually
   declares can disagree with the backlog.

# Delivery State Machine

Canonical states:

```text
DISCOVERED
ARCHITECTURE_REQUIRED
PID_DRAFT
PO_REVIEW
BLOCKED
DELIVERY_READY
ROGUE_DISPATCHED
FORGE_BUILD
FORGE_AUDIT
REPAIR
PO_ACCEPTANCE
MATT_DECISION
CANDIDATE
MERGED
DEPLOYMENT_READY
PAPER
LIVE
CLOSED
CANCELLED
```

Authority:
- PO controls architecture/PID/readiness/acceptance.
- ROGUE controls dispatch state.
- FORGE PL controls build/audit loop state.
- Matt controls only declared `MATT_DECISION` gates.
- PAPER→LIVE always requires Matt/capital authority.

Suggested labels:

```text
state:*
lane:shared
lane:research
lane:trading
lane:ops
gate:po
gate:matt
risk:low
risk:medium
risk:high
risk:capital
```

Exactly one `state:*` label may be present.

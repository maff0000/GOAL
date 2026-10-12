# ADR-MT5-001 — Reuse MT5 Container, Replace Bridge

**Status:** ACCEPTED  
**Date:** 2026-10-12  
**Evidence:** HELM MT5 Connector Provenance & Reuse Audit

## Decision

Vantage MT5 remains the first execution venue, DEMO-first.

Retain the existing `mt5-vantage-paper` Docker/Wine/MetaTrader platform. Replace the unrestricted raw RPyC `SlaveService` broker-control boundary. Build TRON's broker-neutral Vantage adapter outside the MT5 container.

## Preferred boundary

```text
TRON
  ↓
broker-neutral VantageMT5Adapter
  ↓
protected local transport
  ↓
typed in-container MT5 allow-list service
  ↓
MetaTrader5 Python package
  ↓
Wine + MetaTrader 5
  ↓
Vantage DEMO
```

Preferred first transport is a Unix-domain socket shared only with the TRON adapter. If a bounded prototype disproves that approach, use an internal-only authenticated service. Raw unrestricted RPyC must not become the GOAL API.

## Required proof before PAPER

- reproducible image/build provenance;
- account/environment identity;
- reads: account/symbols/ticks/positions/orders/deals;
- market and pending orders;
- cancel;
- SL/TP placement and modification;
- full/partial close;
- reconnect/restart/reconciliation;
- idempotent execution identity;
- broker-side protection.

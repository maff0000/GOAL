# ADR-MT5-002 — Legacy Live-Flagged Executor Is a P0 Operational Risk

**Status:** ACCEPTED  
**Date:** 2026-10-12

HELM found `agent-smith-original` listening on `0.0.0.0:8787`, with `TRADING_ENABLED=true`, and configuration naming a Vantage Live server while the broker account identity remains unconfirmed.

## Decision

Treat it as potentially live until disproven. Do not stop it blindly.

A controlled operations PID must establish:

1. broker account/environment;
2. open positions/orders;
3. current consumers/operators;
4. whether it provides active position protection;
5. safe retirement/quarantine path.

No new GOAL execution architecture may depend on it.

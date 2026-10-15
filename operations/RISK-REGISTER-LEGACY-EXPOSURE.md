# Risk Register - Legacy Executor and Credential Exposure

Source: read-only assessment dated 2026-10-14. **No action has been taken on
any item. All entries are OPEN / UNMITIGATED.** Details that would aid misuse
(addresses, accounts, file-level inventories) are intentionally omitted from
this public document and held privately.

| ID | Finding (sanitised) | Status |
|---|---|---|
| LE-1 | A legacy trade-executor service on the dell host is network-reachable on the LAN with trading enabled and a terminal authorised on a live broker server. No consumer was observed in the retained log window. Current positions were not proven. Treat as live-exposed | OPEN / UNMITIGATED |
| LE-2 | The executor's mutating routes require authentication and a trading-enabled check, but defence in depth is weak: PIN login without lockout or rate limit, plain HTTP, non-secure cookie, in-memory sessions, one global trading switch spanning two live venues, API documentation probably unauthenticated (inferred, not probed) | OPEN / UNMITIGATED |
| LE-3 | The same executor runs on the Trinity host, is in active use (fills and closes on a live account in the retained window), and is reachable from the LAN | OPEN / UNMITIGATED |
| LE-4 | Unauthenticated remote-procedure (RPyC-class) endpoints on the Trinity host are published on all interfaces with no containment; one is reachable from another LAN host. Such endpoints permit arbitrary code execution | OPEN / UNMITIGATED |
| LE-5 | A live broker gateway container on Trinity runs in live mode with read-only API disabled and is unhealthy; remote-desktop endpoints for it and for web terminals are reachable on the LAN | OPEN / UNMITIGATED |
| CE-1 | Environment files carrying live-broker credentials are world-readable on both hosts (modes 644/664), plus further world-readable environment files carrying database, cache and third-party keys, and system unit files embedding database/cache credentials | OPEN / UNMITIGATED |
| CE-2 | Archives and dumps under the backup directories on both hosts are world-readable, some containing credential-bearing paths; one parent directory is world-writable on Trinity | OPEN / UNMITIGATED |
| CE-3 | A hard-coded database administrative credential exists in application source on dell; the database port is published on all interfaces | OPEN / UNMITIGATED |
| CE-4 | One broker-gateway Java process exposes a truststore-password class in its process arguments | OPEN / UNMITIGATED |
| CE-5 | Rotation of any live-broker credential class needs a capital gate and the owner; no rotation has been performed | OPEN, owner decision |

Proposed (not applied) mitigations exist in the private assessment: a
host-firewall containment mirroring an existing containment pattern, interim
file-permission tightening with recorded old modes for rollback, and later a
loopback-only bind. Each needs owner approval; none has been executed.
Related: `operations/BACKUP-AND-RESTORE-PLAN.md` (section 7.5 context and BR-7).

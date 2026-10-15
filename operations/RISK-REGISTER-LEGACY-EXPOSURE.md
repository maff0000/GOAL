# Risk Register - Legacy Exposure (generic categories)

Source: read-only assessment dated 2026-10-14. **No action has been taken on
any item. All entries are OPEN / UNMITIGATED unless stated.** This is a public
document: host names, addresses, ports, mechanisms, file details and inventories
are deliberately omitted. Detail is held in the maintainers' private operations
record. Separate, explicitly authorised, reversible work orders are required for
any intervention. Deferral is **not a completed safety control**: the exposures
below remain in place until such work orders are approved and executed.

| ID | Category (generic) | Status | Action taken |
|---|---|---|---|
| LE-1 | Legacy execution service reachable on the local network, potentially capital-bearing | OPEN / UNMITIGATED | None |
| LE-2 | Weak defence in depth on that legacy service's access controls | OPEN / UNMITIGATED | None |
| LE-3 | A second instance of the legacy service, in active use, reachable on the local network | OPEN / UNMITIGATED | None |
| LE-4 | Network-exposed control interfaces without containment, on a host that handles live activity | OPEN / UNMITIGATED | None |
| LE-5 | Network exposure of broker-adjacent interfaces not independently verified or contained | OPEN / UNMITIGATED | None |
| CE-1 | Credentials stored in files readable by other local users | OPEN / UNMITIGATED | None |
| CE-2 | Backup and archive content readable by other local users, and a permissive parent location | OPEN / UNMITIGATED | None |
| CE-3 | Credential handling in application code and database network exposure not yet remediated | OPEN / UNMITIGATED | None |
| CE-4 | Credential material visible to other local users through process metadata | OPEN / UNMITIGATED | None |
| CE-5 | Credential rotation for live-broker classes requires an owner decision and a capital gate | OPEN, owner decision | None |

Backup and recovery coverage gaps are tracked separately in
`operations/BACKUP-AND-RESTORE-PLAN.md` (section 8).

Detail held in the maintainers' private operations record; separate explicitly
authorised, reversible work orders are required for any intervention.

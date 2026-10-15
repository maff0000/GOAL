# Backup and Restore Plan - dell-debian (local, /data/backups)

Reader: the owner, ROGUE, and whoever later executes this plan. Facts are taken
from read-only investigation notes dated 2026-10-14/15. Every command below is
a **procedure to be reviewed**, not a deployed script.

## 1. Purpose, scope and status

| Item | Value |
|---|---|
| Status | **PLAN ONLY. NOT EXECUTED. OWNER-PAUSED.** |
| Purpose | Define a simple, local backup and restore approach so a recovery point exists and can be proven restorable |
| Destination | `/data/backups/` on the same host (local disk only) |
| In scope | What to back up, how to take consistent copies, how to restore and verify, naming, retention policy, integrity checks |
| Out of scope | Running anything, editing existing config, new timers or automation, off-host replication, credential changes, pruning |

This document is **not a completed safety control**. Nothing here protects any
data until the owner approves and someone executes it (see section 9).

## 2. Components requiring backup (priority tiers)

Sizes are approximate and from the investigation notes. "Covered today" means
by a scheduled job that is currently producing data (see section 7).

### Tier 0 - irreplaceable live state
| Dataset | Type | Approx size | Covered today |
|---|---|---|---|
| Primary dev MariaDB server: `trading*` schemas (Dev, Docs, Dolos, Neo, Proteus, Report, Risk, Scalp, Signals) - holds live trading and market-data records | MariaDB | part of ~237 GB datadir | Designed yes, **failing since 2026-08-11**; last good 2026-08-10 |
| Same server: ARGUS, TRINITY, plutus, CompaniesHouse schemas | MariaDB | part of the above | **No** (script filters `trading%` only) |
| Primary Redis (market-truth store, password-protected) | Redis | ~173 MB | **No** (only a 2026-05-31 manual copy) |

### Tier 1 - important application state
| Dataset | Type | Approx size | Covered today |
|---|---|---|---|
| Argus and ArgCat Postgres instances | PostgreSQL | ArgCat ~72 MB | **No** scheduled job |
| DARWIN Postgres | PostgreSQL | not sized | **No** (ad-hoc pre-migration dumps only, last 2026-09-18) |
| Infosecurs relocation DB and other app Postgres (one further application DB) | PostgreSQL | ~77 MB / not sized | **No** (manual sets only) |
| Companies House MariaDB | MariaDB | ~14 GB | **No** (declared out of scope in config) |
| ARES MariaDB | MariaDB | ~4.6 GB | **No** |
| Falcon MongoDB | MongoDB | ~460 MB | **No** |
| Dev Redis and ARES cache Redis | Redis | ~8 MB | **No** |

### Tier 2 - non-git state under /srv and container volumes
| Dataset | Notes | Covered today |
|---|---|---|
| `/srv-dev` tree (configs, evidence, local-only files) | ~14 GB; `.env`, logs, venvs, node_modules, git packs excluded | Partial: hard-link rsync snapshots (failing intermittently), git bundles only inside the failing daily job |
| Evidence and artifact directories (hermes-evidence, ares-runtime, ares-artifacts, DARWIN runtime) | Non-git state; app repos themselves are on GitHub | **No** |
| Gateway/terminal container volumes with state (MT5 terminal data, broker gateway settings) | Contain broker-related configuration; treat as sensitive | **No** |
| Other service state (LLM gateway, web UI data, Cerberus working data) | Classify per owner | **No** |
| Graylog Mongo, Apollo dev Postgres containers | Owner must classify "needed or disposable" first | **No** |

### Tier 3 - repositories
Repositories with a GitHub remote are protected by the remote; back up only
**unpushed work**. Use `git bundle create <name>.bundle --all` for any
checkout that has branches/commits not on a remote, and `git bundle verify`
after creating.

### Deliberately NOT backed up
Secret files (`.env`, secrets directories, key files). They are excluded by
design (`EXCLUDE_ENV_FILES=1`). A separate, owner-approved secure method is
needed to recover secrets; the claim in existing docs that an environment
recovery document exists is **unverified**. Absence of secrets from backups
means a full restore also needs those secrets from another source.

## 3. Consistent backup procedures (per datastore type)

General rules: run serially, one datastore at a time, at low priority
(`ionice -c3 nice -n 19`), inside the quiet window, writing to a **temporary
name** (`*.partial`) and renaming only after checks pass. Credentials come
from a 0600 file or environment variable, **never on the command line and never
echoed**. A dedicated least-privilege read account is preferred over a
privileged one (see section 7 for the account that already exists).

### 3.1 MariaDB
- Tool: `mariadb-dump` (the version matching the server).
- Flags: `--single-transaction --quick --routines --triggers --events --hex-blob --default-character-set=utf8mb4`, one schema per file.
- Why: `--single-transaction` takes a consistent InnoDB snapshot without table locks, so writers are not blocked. It does **not** give consistency for non-InnoDB (MyISAM/Aria) tables - list engines first with `information_schema.TABLES` and treat any such tables separately (brief lock or accept inconsistency, owner decision).
- Do **not** use `--force` or `|| true` (a mid-dump error must fail the job; the existing script uses both).
- Schema selection: all non-system schemas (exclude `mysql`, `sys`, `performance_schema`, `information_schema`), not a name pattern. Record the schema list in the manifest so a new schema cannot be silently missed.
- Capture alongside each dump: per-table row counts and engines (`information_schema`) into `<schema>.counts.tsv`, and the server version.
- Pre-check: current `Innodb_history_list_length` (see section 7). A very long snapshot transaction on a busy server increases undo history; take dumps per schema and watch it.
- Pipe through `gzip` into the `.partial` file; check the trailer (section 6) before rename.
- Large schema (Companies House, ~14 GB) is its own step with its own time budget.

### 3.2 PostgreSQL
- `pg_dump -Fc --no-owner=false` (custom format; consistent single snapshot by default) per database: `pg_dump -Fc -f <db>.dump <db>`.
- Cluster-wide roles: `pg_dumpall --globals-only > globals.sql` once per instance.
- Run inside the container (`docker exec`) or against its published local port, using a password file / `PGPASSFILE`, not argv.
- Verify with `pg_restore --list <db>.dump` (must exit 0).

### 3.3 MongoDB
- `mongodump --archive=<name>.archive --gzip` (add `--oplog` only on a replica set). For a single standalone instance with small data this is consistent enough; note it is not a point-in-time snapshot across collections unless `--oplog` is available.
- Verify: `mongorestore --archive=<name>.archive --gzip --dryRun`.

### 3.4 Redis
- Preferred: trigger `BGSAVE`, wait until `rdb_bgsave_in_progress:0` and `rdb_last_bgsave_status:ok` (via `INFO persistence`), then copy the resulting `dump.rdb`. If AOF is enabled, also copy the whole AOF directory after `BGREWRITEAOF` completes (`aof_rewrite_in_progress:0`), not a live-growing file.
- Alternative: `redis-cli --rdb <file>` streams an RDB from the server.
- Authentication via an environment variable (`REDISCLI_AUTH`) or ACL file; never `-a <password>` on the command line.
- Verify: `redis-check-rdb <file>` (and `redis-check-aof` for AOF).
- Context: a power cut in 2026-05 corrupted an AOF, which is why a copy that was validated, not merely present, matters.

### 3.5 Container volumes and /srv state
- Stop-free option: `tar --numeric-owner -C <dir> -czf <name>.tar.gz.partial .` for directories that are quiescent or file-oriented.
- For volumes belonging to a running database, do **not** tar the live datadir; use the datastore procedures above.
- Exclude secrets (`.env*`, `secrets/`, key files) explicitly with `--exclude`.
- For the large `/srv-dev` tree, `rsync -a --link-dest=<previous snapshot>` hard-link snapshots are acceptable (existing design); the summary statistics step must not walk all snapshots (see section 7).

### 3.6 Repositories
`git bundle create <repo>.bundle --all`, then `git bundle verify <repo>.bundle`. Only for repos with unpushed refs.

## 4. Restore procedures and isolated verification

**Rule: never restore over a live datastore as a test.** Restore tests happen in
a throwaway container with no network to production, a scratch directory under
`/data/restore-test/`, loopback-only ports, and a random password in a 0600
file. Teardown removes only that container and directory.

### 4.1 MariaDB restore
1. Start a throwaway MariaDB container of the **same major/minor image** as the source, `--network none` (or an isolated network), data in `/data/restore-test/mariadb`.
2. Create the schema, then `zcat <schema>.sql.gz | mariadb <schema>` (credential via env var).
3. Verify (section 6): table count, row counts vs `<schema>.counts.tsv`, `mariadb-check --databases <schema>` or `CHECK TABLE`, a few sample queries.
4. A **real** recovery follows the same steps but targets the new, owner-approved destination datastore, with the application stopped first.

### 4.2 PostgreSQL restore
1. Throwaway Postgres container (same major version), isolated, scratch dir.
2. `pg_restore --list` first, then `createdb` and `pg_restore --no-owner -d <db> <db>.dump`; load `globals.sql` first if roles are needed.
3. Verify: `\dt` table count, row counts of key tables vs the manifest counts, `pg_restore` exit status 0.

### 4.3 MongoDB restore
Throwaway `mongod`, `mongorestore --archive=<name>.archive --gzip`, compare collection counts (`db.<c>.countDocuments()`) with counts captured at backup time.

### 4.4 Redis restore
Copy the RDB (or AOF directory) into a scratch directory, start `redis-server --port <loopback test port> --dir <scratch>` with no replication configured, compare `DBSIZE` to the value captured at backup time, spot-check some keys, then shut down.

### 4.5 Files and bundles
Extract tarballs into a scratch directory (`tar -xzf ... -C /data/restore-test/files`), compare the file list against `tar -tzf`, and spot-check a few files with `sha256sum`. For bundles: `git clone <bundle> <scratch>`.

### 4.6 Cadence
Perform an isolated restore test of every datastore class **at least once after the first backup, then monthly**. A backup that has never been restored is unproven.

## 5. Directory naming, retention and permissions under /data/backups

### 5.1 Proposed layout (new, additive; existing sets are left as they are)
```
/data/backups/
  plan-v1/
    <class>/<YYYYMMDDTHHMMSSZ>/
      <artifact files>
      MANIFEST.sha256        # sha256sum of every artifact in the set
      MANIFEST.meta          # source, tool+version, schema list, row counts file names, start/end UTC, status
      COMPLETE               # created last; a set without it is invalid
```
`<class>` examples: `mariadb`, `postgres`, `mongo`, `redis`, `files`, `git`.
Date-stamped directories are UTC. A set is created under a `.partial` name and
renamed only once complete, so empty or half-written dated directories (the
current state) cannot occur.

### 5.2 Preconditions before any write (fail loudly otherwise)
- **Mountpoint check:** `/data` must be a real mount (`mountpoint -q /data`). The disk is mounted `nofail`; without this check a dropped disk would let backups silently fill the root filesystem.
- Free space on `/data` at least 2x the expected set size.
- Write probe (create and remove a test file inside the target).

### 5.3 Permissions
- Directories `0700`, files `0600`, owner root. Run under `umask 077`.
- Today `/data/backups` is `0775` with `0644` files, readable by any local user although the dumps contain full database content. Tightening applies to **new** sets only; changing existing sets is a separate owner decision.

### 5.4 Retention (POLICY ONLY - nothing is pruned by this plan)
| Class | Proposed keep |
|---|---|
| Daily sets | 7 |
| Weekly sets | 4 |
| Monthly sets | 3 |
| Restore-test evidence records | 12 months |

Rules: creating a backup never prunes. Pruning, if ever approved, is a
separate previewed (dry-run listing first) action that never removes the
newest verified set, never removes a set that lacks a newer verified one, and
requires explicit owner approval. The existing prune setting is off
(`PRUNE_ENABLED=0`) and **stays off**; existing directories (137 daily dates,
most empty) are not touched.

## 6. Integrity and restore verification checks

| Check | How | Pass condition |
|---|---|---|
| SQL dump trailer | last line of the decompressed dump: `-- Dump completed on ...` | present. `gzip -t` alone is NOT enough, because a failed dump piped through gzip is still a valid gzip |
| gzip integrity | `gzip -t <file>` | exit 0 |
| tar integrity | `tar -tzf <file> >/dev/null` | exit 0 |
| Postgres archive | `pg_restore --list` | exit 0 |
| Redis | `redis-check-rdb` / `redis-check-aof` | exit 0 |
| Bundles | `git bundle verify` | exit 0 |
| Checksums | `sha256sum -c MANIFEST.sha256` immediately after writing and again before any restore or copy | all OK |
| Size sanity | compare size with previous set of same class | not below, say, 50 percent of previous unless explained (the Report schema dump was 6 KB against 9.6 MB in an older copy and needs owner confirmation) |
| Row counts | restored row counts vs counts captured at dump time (exact for stable tables; tolerance for tables written during the dump, since the dump is a snapshot) | match |
| Table health | `CHECK TABLE` / `mariadb-check` on restored MariaDB tables | OK |
| Freshness | newest complete set age: databases at most 36 h, Redis at most 48 h, file snapshots at most 36 h | within limit; otherwise alert |

A set counts as **verified** only when its checks pass and it has been through
at least one isolated restore (section 4). The status field in the manifest
distinguishes `written`, `checked`, `restore-tested`.

## 7. Existing state (recorded factually; nothing changed by this plan)

### 7.1 Scheduled units (systemd; no cron entries)
| Unit | Schedule | Latest result (2026-10-14) | Cause |
|---|---|---|---|
| backup-db-daily | daily ~00:00 | FAILED exit 1, every night since 2026-08-11 | database login rejected |
| backup-db-weekly | Sunday 00:30 | FAILED exit 1, same cause | same |
| backup-db-hourly | disabled by design since 2026-02-15 | n/a | n/a |
| backup-rsync-daily | daily 01:00 | FAILED exit 2 (intermittent) | pipeline race, see 7.3 |
| backup-verify | daily 02:00 | FAILED, killed at the 300 s timeout | see 7.4 |
| backup-canary, redis-aof-backup | designed, unit files only in the tool's repo directory | **never installed or enabled** | never deployed |

### 7.2 Root cause of the database failures
The backup login stored in the backup tool's `.env` (key names: `PROD_CONTAINER`, `PROD_USER`, `PROD_PASS`, `DEV_CONTAINER`, `DEV_USER`, `DEV_PASS`, `DISCORD_WEBHOOK`) is **rejected by the database server** (access denied, reproduced with a read-only test query). The script discards the client's error output, so it logs only "failed at line 350, exit 1". The first failed run was 2026-08-11; the database admin secret and audit configuration were changed on 2026-08-10, consistent with a credential rotation that never updated the backup login. The alert path (webhook) was never confirmed to deliver. Result: the newest readable database recovery point is **2026-08-10 (daily) / 2026-08-09 (weekly)**.

### 7.3 Rsync lane
- Intermittent failure: a `find | sort -r | head -1` under `pipefail` makes `sort` fail with a broken pipe, exit 2 before any copy (failed 2026-10-11, -12, -14).
- On 2026-10-13 the copy completed (about 430k files, 12 GB) but the unit was killed by its 1800 s timeout during an end-of-run `du -sh` over 120+ hard-linked snapshots, so no success marker was written (marker dated 2026-09-14). Snapshots exist through 20261013 with gaps.
- Retention is preview-only; nothing has ever been pruned.

### 7.4 Verify job
Times out at 300 s, reports FAIL on missing schemas/code/bundles (it inspects the empty current dated directory), WARNs on the retired PROD tier, then hangs on a broken pipe. All success markers show `verify_status: unverified`.

### 7.5 Stale PROD tier noise
The retired PROD database container has been absent for months (config: `PROD_DB_STATUS=ABSENT`), but the verifier still warns that the weekly PROD set is about 241 days old (last data 2026-02-15). That is stale noise about a dead tier, not a signal about live data.

### 7.6 Coverage gaps
See section 2: schemas filtered out by name pattern, all Postgres, Mongo, Redis, ARES DB, Companies House DB, non-git `/srv` state and container volumes have no working scheduled backup. Empty dated directories are created before the first failure point, which hides failures. Dumps are written with `--force ... || true`, so a partial dump can still look valid.

### 7.7 Already-created items (EXISTING STATE - names and paths only)
Per the stage-2a notes of 2026-10-14, the following were created before the owner pause. **Nothing has been activated.**
- Database account `backup_ro` (host `localhost`) on the primary dev MariaDB server, intended as least-privilege read access.
- Secret file `/srv-dev/tradingBackup/.backup_ro.secret` (mode 0600, content not read for this document).
- Old-state marker copy `/var/tmp/backup-p0/last_success_db_daily.json.pre2a` (saved before any intended re-run).
- Backup copy of the old env file `/srv-dev/tradingBackup/.env.pre-2026-10-14` (mode 0600, holds the OLD rejected values).
- `/srv-dev/tradingBackup/.env` is **unchanged** (modification time 2026-07-11); the success marker for the daily database job is unchanged (2026-08-09 content); no restore-test directory exists; no new timers were installed.
- The account's existence and privileges were not re-queried for this document. Rollback notes are in `/var/tmp/backup-p0/ROLLBACK-2a.md` (drop the user, remove the secret file, restore the env copy).

### 7.8 History-list-length observation
A baseline taken 2026-10-14 10:09 on the primary dev MariaDB server showed `Innodb_history_list_length` of about 6.7 million, with 5 connected and 1 running thread, health "healthy", host load average about 4-5. That is a large InnoDB undo backlog (a sign of a long-open or long-lived read view, or purge lag). It is recorded as an observation, not diagnosed. It matters here because a long `--single-transaction` dump can add to it; the first dump should be run per schema with the value watched before and after, and the owner should know about it independently of backups.

## 8. Known risks register

| ID | Risk | Status |
|---|---|---|
| BR-1 | **No off-host replication.** All backups are on one local disk in the same chassis; a single-disk or host failure loses all backups and the live data together | OPEN, no mitigation in place |
| BR-2 | **This plan is NOT a completed safety control.** It is documentation only; nothing is protected by it until executed and restore-tested | OPEN |
| BR-3 | No database recovery point newer than 2026-08-10 (about 66 days at time of writing) | OPEN |
| BR-4 | Redis, Postgres, Mongo, ARES DB, Companies House DB and several MariaDB schemas have no scheduled backup | OPEN |
| BR-5 | No restore has ever been performed or tested; restorability of existing sets is unproven (readability only: gzip and tar tests passed on the 2026-08-10 set) | OPEN |
| BR-6 | Failure detection is weak: errors hidden, alert delivery unconfirmed, verify job times out, canary lane not installed | OPEN |
| BR-7 | Existing backup directories are world-readable and contain full database content | OPEN |
| BR-8 | `/data` not mount-checked; a dropped disk would silently fill the root filesystem | OPEN |
| BR-9 | Secrets are not backed up by design; a full recovery needs a separate approved route for secrets | OPEN, owner decision |
| BR-10 | Large InnoDB history list on the primary database server; a dump could aggravate it | OPEN, observation |
| BR-11 | Non-InnoDB tables (if any) are not consistent under `--single-transaction` | UNVERIFIED, check engines |
| BR-12 | Report schema dump is suspiciously small (6 KB vs 9.6 MB earlier) | OPEN, owner to confirm intended |
| BR-13 | Stale PROD-tier warnings could mislead dashboards | OPEN, cosmetic |

## 9. Deferred (not part of this plan; each needs an owner decision)

| Deferred item | Decision point for the owner |
|---|---|
| Executing any backup, including a one-off fresh recovery point | Approve a run, its timing outside the quiet window, and the I/O impact on the primary database |
| Choice of database credential: use the existing least-privilege account or an owner-supplied rotated credential; and editing the backup tool's `.env` | Approve which, and approve the edit (with dated copy) |
| New automation: timers, canary, Redis AOF lane, new verify job, alert rewiring | Approve installation and schedule windows |
| Scripts v2 (stderr not swallowed, schema selection widened, trailer and manifest checks, rsync race and `du` fix, mountpoint check, umask) | Approve development and swap procedure |
| Off-host copy | Approve a destination class, who provisions it, and whether encryption at rest is required |
| NAS decision (use an existing network storage target or not; access control; client package install on this host) | Owner decision; no access was attempted |
| Retention enablement and cleanup of existing mostly-empty dated directories | Approve policy in 5.4 and any pruning separately |
| Scope calls: Companies House and ARES databases, Apollo/Graylog containers, `/srv` state classification | Confirm in or out of scope |
| Isolated restore-test environment creation and cadence | Approve scratch directory and test ports |
| Secrets recovery route | Approve a method independent of these backups |

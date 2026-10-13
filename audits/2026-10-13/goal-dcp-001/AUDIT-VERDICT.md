# GOAL-DCP-001 — Repair-Round Independent Auditor Verdict (2026-10-13)

Dispatched as a **fresh** FORGE Auditor with no inherited Engineer or PL
context, and **not** a continuation of the Auditor who reviewed the first round
(`audits/2026-10-12/goal-dcp-001/AUDIT-VERDICT.md`). It did not edit the
repository; all mutation and injected-defect work was done in sandbox copies
outside its worktree.

Presentation target for this increment is `FUNCTIONAL_ONLY`. The Auditor
**verified that determination rather than accepting it**: the tracked tree
contains no `.html/.css/.js/.jsx/.ts/.tsx/.vue/.svelte/.jinja/.j2/...` file,
and `git diff b40c4f13 653ce7c` matches none of
`flask|django|fastapi|render_template|<html|text/html|http.server|uvicorn|<!DOCTYPE`.
No browser-rendering surface exists, so the mandatory real-browser verification
gate does not apply. The substituted rigour: the Auditor ran every command
itself and verified observed output, never accepting a document's or a commit
message's claim about what a command prints.

Host governance note: as a dispatched subagent the Auditor had no access to the
`tradingGovernance` database, so it declined to state a CRITICAL rule count
rather than fabricate one. Governance was not loaded; the audit is read-only
against the repository and was unaffected.

## Verdict block

```text
AUDIT_VERDICT: GREEN
commit_sha: 653ce7cc2271549e82fbd10e5fbc0f6e17231c5f
server_fingerprint_verified: n/a — no server in this increment (FUNCTIONAL_ONLY;
  no HTML-producing route, no listening process). Substituted: independent fresh
  clone pinned to 653ce7c, HEAD re-verified before every run.
real_browser_reproduction_completed: n/a — no browser-rendering surface in the
  tracked tree or the diff (mechanically confirmed).
root_cause_identified: n/a — no RED finding against the diff.
pid_boundary_verified: yes
strict_readiness_verified: yes
pre_pid_wave_verified: yes
dcp_sequencing_verified: yes
regression_verified: yes
acceptance_run_in_fresh_checkout_verified: yes
no_hardcoded_wave_or_readiness_list_verified: yes
wave_proof_non_vacuity_verified: yes
fixture_exemption_cannot_hide_regression_verified: yes
console_errors: n/a — no browser. No stderr on any successful tool invocation;
  exit codes as documented.
findings: 7 — none falsifies a delivered claim. F1/F2 are MEDIUM hardening and
  evidence-trail findings; F3–F7 LOW or nit.
confidence: high
```

Environment: Python 3.11.2, pytest 9.0.2, gitleaks 8.30.1. **No `chmod` was
issued anywhere.** `git ls-files -s tools/` records `100755` for `goal-docs`,
`goal-ready`, `goal-validate` and `secret-scan`; all four were executable
straight out of the clone.

## Replay recipe

```bash
git clone --no-local <repo> fresh && cd fresh
git checkout 653ce7cc2271549e82fbd10e5fbc0f6e17231c5f
python3 -m pytest tests/ -q      # 276 passed in 35.82s
./tools/goal-validate            # "backlog OK: 40 items"        exit 0
./tools/goal-docs --check        # "generated regions in sync"    exit 0
./tools/secret-scan              # working tree CLEAN, history CLEAN, RESULT: CLEAN
./tools/goal-ready               # {"ready":[]}
./tools/goal-ready --pid-wave    # {"pid_authoring_wave":[]}
./tools/goal-ready --pid-wave --assume-closed=GOAL-DCP-001   # exactly the eleven
```

## What was proved

**1. PID boundary.** Eleven mutations of a synthetic `DELIVERY_READY` item,
each caught, with `goal-ready` refusing every time: `pid_path: null` →
`MISSING_PID`; key absent → `MISSING_FIELD`; `int` and `list` →
`INVALID_FIELD_TYPE`; `""`, `"   "`, `/pids/…`, `../pids/…`, a nonexistent
file, and a *directory* → `PID_FILE_NOT_FOUND`; disagreeing metadata → four
`BACKLOG_PID_MISMATCH`. A sweep over all 19 states confirms the boundary is
exactly as claimed: the 13 states `DELIVERY_READY` through `CLOSED` require a
PID; the five pre-delivery states **and** `CANCELLED` correctly do not.

**2. Strict readiness.** Eight attack paths — normal, `--with-pid`,
`--assume-closed` on a dependency, `--assume-closed` on the item itself,
`--pid-wave` key confusion, duplicate-id smuggling (two items sharing an id,
one with a PID and one without), and a typo'd projection id — all contained.
The guarantee holds **by validation first**, which is load-bearing: injecting
`findings = ()` was caught by three tests. The emit-time post-condition is
provably unreachable while validation stands, and is tested directly rather
than through the CLI.

**3. Pre-PID wave, non-vacuous.** Empty before closure; exactly the eleven
under the projection, every one with `pid_path: null`; and `ready` stays `[]`
even post-closure — the honest answer. Set equality plus `len(after) == 11` is
asserted, not containment. Six backlog mutations confirm the answer is
*derived*: a twelfth qualifying item appears; `TRON-T1` demoted by state drops
out; `OPS-SAFE-002` given an unmet dependency drops out; a twelfth with an
unmet dependency or the wrong state stays out; an unknown dependency makes the
validator refuse. `pids/` contains exactly one file — the real 2568-byte
canonical PID with seven label lines. **No placeholder, shim or content-free
PID exists anywhere.** CLI help text and all six documents state plainly that
wave items are **not** FORGE-dispatchable.

**4. DCP sequencing.** The duplication was real and is removed — at
`b40c4f13`, `GOAL-DCP-002` was *"Machine-readable backlog + dependency/
readiness validator"*, precisely DCP-001's deliverable. Chain
`001 → 002 → {003, 004}`, consistent across `backlog.yaml`, the generated
`MASTER-BACKLOG.md` table and the architecture document. Every surviving
mention of auto-merge is an explicit negation; the old "selective auto-merge"
rung 4 is gone.

**5. Regression.** All 18 validator classes caught: cycles, self-dependency,
unknown dependencies, shorthand `DCP-001` via the membership layer, wildcard
`OPS-SAFE-*`, lowercase and comma-list ids via the syntax layer, duplicate
dependencies and ids, all four enums, target-repository presence and shape,
architecture refs, empty fields. `LIVE-GATE-001` declares exactly its six
expected dependencies and **each is independently load-bearing** — withholding
any one keeps it out. Output is byte-stable (one unique result over 20 runs in
each of five modes) and invariant under three random shuffles of backlog source
order. Drift detection has teeth: tampered wave id, deleted table row, removed
marker pair and tampered manifest all exit 1, while prose edited *outside* a
region correctly stays in sync. The secret scan is non-vacuous: four planted
secrets produced three findings in the working tree, and still three after
committing and deleting them from the tree, proving the history scan works.

**6. Mutation probing.** Ten of eleven injected defects caught, including
hard-coding the wave as a literal id list (ten failures). The only reference to
any work-item id under `tools/` is
`PID_AUTHORING_WAVE_PROJECTION = frozenset({"GOAL-DCP-001"})` — the rule's
*input*, not its output. The fixture-integrity exemption is genuinely
self-policing: giving `TARGET-001` a valid PID, or swapping its defect for a
different one, both fail. It cannot hide a real regression. Test-suite vacuity
scan: 210 test functions, none without assertions, none trivially true.

## Findings — none RED

**F1 · MEDIUM · false coverage claim in the evidence trail.** Commit
`653ce7c`'s message states *"Each set is byte-checked against
`tools/goal_dcp/model.py`."* No test reads
`governance/DELIVERY-STATE-MACHINE.md`; the only reference to it in `tests/` is
`test_model.py::test_vocabularies_match_the_delivery_state_machine`, which is
misleadingly named and asserts only the model's internal consistency. Proof:
removing `DELIVERY_READY` from that document's PID-required block → 276 passed;
adding `CANCELLED` to its accepted-terminal block → 276 passed. The document
that `653ce7c` deliberately designated as the *single* authority for the rule
is the one restatement of machine truth with no mechanical guard — exactly the
"two independent truths" failure `docsync.py`'s own docstring says generated
regions exist to prevent. The documents are correct at this commit, so no
delivered claim is falsified; the gap is future drift plus a commit message a
later reader would reasonably take on trust. The Auditor considered PRODUCT RED
and landed on GREEN-with-finding because nothing shipped is wrong, while
putting the false claim in front of the PL because Forge treats the git
evidence trail as durable truth.

> **PL disposition:** confirmed independently — both mutations reproduced at
> 276 passed. The overclaim is corrected forward in
> `REPAIR-EVIDENCE.md` §5 rather than by amending `653ce7c`, which this
> verdict cites by SHA. The underlying guard is logged as an open item (§6.3)
> and deliberately not added in this round, because changing the test suite
> after the audited head would make the audited code no longer the delivered
> code for a gap that falsifies nothing shipped.

**F2 · MEDIUM · a content-free PID satisfies the gate.** `touch pids/X.md`
(zero bytes) with `pid_path: pids/X.md` → `goal-validate` exit 0 →
`goal-ready` emits the item as `ready`. Same for a single space, `TODO\n`,
unrelated prose with no labels, or one agreeing label.
`BACKLOG_PID_MISMATCH` compares only labels the PID *actually declares*, so a
PID declaring none agrees vacuously. `operations/ROGUE-READINESS.md` already
forbids this in prose — *"a stub PID would satisfy the validator while
delivering none of the authority a PID exists to carry"* — so the doctrine
recognises the hole and mitigates it by policy alone. Within the PID's stated
failure modes as written, so not RED; but the PO's semantic hardening is
bypassable by one `touch`.

> **PL disposition:** confirmed directly — a zero-byte PID yields
> `backlog OK: 40 items` and `{"ready":[{"id":"OPS-SAFE-001","pid_path":"pids/EMPTY-PROBE.md",...}]}`.
> Escalated to the PO as the highest-value follow-up (§6.2). What makes a PID
> substantive is a PO decision, so no rule was invented here.

**F3 · LOW · test coverage.** Replacing
`violations = ready_invariant_violations(backlog, payload)` with
`violations = []` in `tools/goal-ready` survived — 276 passed. The function is
thoroughly tested and the CLI path is analytically unreachable while validation
stands; the uncovered thing is the *wiring* in `main()`, so a future silent
removal plus a later weakening of validation would leak. Defence-in-depth,
correctly reasoned, genuinely uncovered.

**F4 · LOW · agrees with the PL's PID adjudication, with a caveat.**
`pids/GOAL-DCP-001.md` lines 61–68 still publish the two-clause rule and the
`MT5-GW-001` example; `MT5-GW-001` is now `PID_DRAFT`, so that example is not
merely shape-stale — it names an item the tool now classifies the opposite way.
The adjudication is right in substance: the third clause is a *restriction*, so
the shipped rule can never emit anything the PID's rule forbids; the PID itself
lists "missing PID" among required failure modes (line 55); and the PO's later
CHANGES REQUIRED supersedes earlier PID prose. **But** "forward-fix later" is
too weak — the PID is the artifact FORGE builds against, and it currently
contradicts the shipped tool. The Auditor would make the PO-authored PID update
**blocking before closure**, not an intention.

**F5 · LOW · the stale evidence line needs a dated superseding note.**
`audits/2026-10-12/goal-dcp-001/DELIVERY-EVIDENCE.md` line 236 reads
*"`DELIVERY_READY` therefore does not require a PID"*. Not rewriting dated
evidence is correct, but the sentence is phrased as standing doctrine rather
than a time-stamped belief, and it was the only contradicting statement left in
the repository. A dated superseding note citing `38768e4`, leaving the original
text intact, would close it — and should be tracked as closure-blocking rather
than intended.

> **PL disposition:** done in this commit, in exactly that form — appended, not
> rewritten, citing `38768e4`, with the original text intact. A matching note
> was appended to the first round's `AUDIT-VERDICT.md`.

**F6 · nit · the ten `DEP-*` fixtures are accepted, but the recorded
justification is inaccurate.** The substance holds — a dependency's `pid_path`
is never read: flipping `DEP-001`'s `pid_path` between `None` and a real file
in `dep_merged.yaml` leaves `ready = ['TARGET-001']` unchanged. But "readiness
fixtures are never validated" is false:
`test_every_delivery_ready_fixture_item_declares_an_agreeing_pid` *does* call
`validate()` on them; it merely scopes the assertion to `DELIVERY_READY` items.
Right answer, wrong reason recorded.

> **PL disposition:** accepted; the reasoning is corrected in
> `REPAIR-EVIDENCE.md` §6.5.

**F7 · nit.** `tests/test_first_wave.py` keeps a stale filename (justified in
its docstring: committed evidence cites it).
`test_vocabularies_match_the_delivery_state_machine` should be renamed or made
to actually read the document (see F1). Three `assert f(x) == f(x)` determinism
tests are low-power but not vacuous — real byte-stability is covered by CLI
tests and the Auditor's 20-run probe.

## PL adjudication

**Accepted: GREEN.** Both PO blockers are delivered and independently proven.
Two findings were spot-checked directly against the artifact rather than
against the Auditor's narrative — F1 (both mutations reproduced at 276 passed)
and F2 (zero-byte PID emitted as `ready`) — and both reproduced exactly as
reported, which is the evidence that this Auditor is independent rather than
merely trusted. No finding was overruled. Nothing was repaired silently: the
two findings the PL could close without touching the audited code (F5, and the
F1 overclaim) are closed in this commit, and the rest are escalated to the PO
in `REPAIR-EVIDENCE.md` §6.

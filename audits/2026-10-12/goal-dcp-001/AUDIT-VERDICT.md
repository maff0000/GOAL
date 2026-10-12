# GOAL-DCP-001 — Independent Auditor Verdict

Dispatched as a fresh-context FORGE Auditor with no inherited Engineer or PL
context, against the delivered head. It did not edit the repository; all
mutation and probe work was done in sandbox clones outside the worktree.

Presentation target for this increment is `FUNCTIONAL_ONLY`: it delivers
repository data, command-line tools, tests and documentation, with no
templates, CSS, client JS, HTML-producing route or server. The Auditor's
real-browser verification gate therefore does not apply, and the equivalent
rigour was substituted — the Auditor ran every command itself and verified
observed results rather than accepting any document's claim about them.

## Verdict block

```text
AUDIT_VERDICT: GREEN
commit_sha: 16e28909c43e8ea07ba27544f66fd830bec794f3
server_fingerprint_verified: n/a (no server in this increment)
real_browser_reproduction_completed: n/a (no browser surface)
root_cause_identified: n/a
pid_compliance_verified: yes
dependency_validation_verified: yes
cycle_detection_verified: yes
alias_wildcard_rejection_verified: yes
state_validation_verified: yes
backlog_pid_consistency_verified: yes
readiness_correctness_verified: yes
hardcoded_readiness_list_found: no
first_wave_non_vacuity_verified: yes
secret_safe_public_repo_verified: yes
unnecessary_infrastructure_found: no
console_errors: n/a
findings: three, none of them RED — (1) committed evidence asserts an audit
  artifact that does not exist at this SHA; (2) the internal-host scrub is
  partial and the evidence describes it as complete in the working tree;
  (3) PID Acceptance still needs a PR — zero pulls exist on the repo.
confidence: high
```

## How the verdict was established

The audit went beyond replaying the shipped suite. Material checks:

- **Mutation testing — 15 injected defects, 15 killed, zero survivors**,
  across the validator, readiness, docsync and the model. Specifically, a
  hard-coded eleven-id readiness list substituted for the rule is killed by
  4 tests in `test_first_wave.py` and 13 in `test_readiness.py`; removing
  either layer of the two-layer identifier check kills the suite; and
  suppressing cycle findings kills the suite.
- **The anti-hardcoding test has its own guard-the-guard**
  (`test_code_only_source_actually_strips_prose`), so a source-stripper
  returning an empty string would not vacuously pass everything.
- **Adversarial cycle probes beyond the shipped fixtures**: a cycle entered
  mid-ring behind a two-node prefix, and a true figure-eight where one node
  belongs to two overlapping cycles with different smallest members. Both
  cycles were enumerated correctly.
- **A 19-state readiness matrix** produced zero mismatches against the
  declared rule, including the two cases most likely to be fudged —
  `CANCELLED` correctly does *not* satisfy a dependency, and
  `PO_ACCEPTANCE`/`MATT_DECISION`/`CANDIDATE` correctly do not.
- **`FIRST_WAVE_PROJECTION` proven to be an input, not a cached answer**: the
  Auditor set `TRON-T1` to `BLOCKED` in the YAML and the rendered wave
  dropped from eleven items to ten.
- **Drift forced in both directions and caught both ways**: editing the human
  table drifted `backlog-table`; changing the YAML alone drifted both
  `backlog-table` and `first-wave`. Deleting a marker pair yields
  `MISSING_GENERATED_REGION`, and `--write` refuses to invent a missing
  region rather than exiting 0 on a partial job.
- **Secret-scan non-vacuity proven in both layers**: planted non-allowlisted
  token material produced findings in the working tree, and — after being
  committed and then deleted — the history layer still produced findings.
  That is the case that actually matters for a public repository.
- **Baseline independently reproduced in a fresh `git clone`**, so no result
  depends on the audited worktree's state.
- **All 21 validator finding codes provoked through the CLI**, with a
  cross-check that no declared code is dormant: "DECLARED but NEVER PROVOKED
  by any fixture: none."

### A failed probe the Auditor reported honestly

The Auditor's first secret-scan non-vacuity attempt used the canonical AWS
example key `AKIAIOSFODNN7EXAMPLE` and the scan stayed clean. That is a
gitleaks default-allowlist artifact rather than a scanner defect — the same
trap an Engineer hit and rejected earlier in this work order (recorded in
`DELIVERY-EVIDENCE.md` §10). The Auditor re-ran with non-allowlisted token
shapes, which fired, and reported the failed probe so anyone replaying the
steps hits it knowingly.

## PL adjudication of the three findings

All three were spot-checked directly by the PL against the repository rather
than accepted on the Auditor's account of them. All three are confirmed
accurate. None is RED, and none required a repair Engineer dispatch, because
findings 1 and 2 are defects in the PL's own evidence file rather than in the
delivered implementation.

### Finding 1 — accepted, corrected

`DELIVERY-EVIDENCE.md` §11 asserted in the past tense that an Auditor had
been dispatched and that its verdict was "recorded alongside this file in
`AUDIT-VERDICT.md`", at a commit where no such file existed. Confirmed: at
`16e2890` the evidence directory contained only `DELIVERY-EVIDENCE.md`.

This is the overclaim pattern Forge's own durable-truth doctrine exists to
prevent — committed evidence describing an audit as complete before it ran.
The correction is this file, plus a corrected §11, landed as a **new commit**.
The original commit is not amended: it is already pushed, and rewriting a
published commit to hide an overclaim is the specific thing the doctrine
forbids. The correction goes where a reader following the evidence trail
actually arrives.

### Finding 2 — accepted, evidence wording corrected; no scrub

Confirmed by direct inspection:

- `dell-debian` is genuinely absent from `HEAD`.
- `/srv/GOAL` still appears at `operations/HELM-BOOTSTRAP-INSTRUCTIONS.md`
  lines 29 and 31, and `operations/HELM-NEXT-ACTIONS.md` line 39 — in `HEAD`,
  in two files this increment edited.

So §8's framing of the residue as bounded to the root commit was wrong, and
§8 is corrected accordingly.

The paths themselves are deliberately **not** scrubbed. `/srv/GOAL` is a
generic local filesystem path, not a hostname, credential, address or
topology detail; it discloses nothing an attacker could act on, and it is
part of the historical record of what HELM was actually instructed to do.
Removing it would degrade that record for no security benefit. The internal
*host identifier* — the part with disclosure value — was removed. This is
recorded as a PO decision rather than silently actioned either way.

### Finding 3 — accepted, resolved at the delivery boundary

Correct at the time of audit: zero pull requests existed. The governed PR is
the PL's next and final action, and the branch was already pushed at exactly
the audited SHA. The PID Acceptance line "evidence + exact SHAs + PR" closes
with that PR.

## Pre-existing disclosure, outside this increment

The Auditor also noted `decisions/ADR-MT5-002-LEGACY-LIVE-FLAGGED-EXECUTOR.md`
line 6 publishes a bind address and `TRADING_ENABLED=true`. Confirmed present
in the base commit `acc3f48`, so it predates this increment and is outside its
scope. `0.0.0.0` is a bind-all placeholder rather than a routable internal
address, and the surrounding text is the substance of an accepted ADR. Raised
for the PO, not changed here.

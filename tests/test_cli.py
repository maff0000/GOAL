"""End-to-end tests for the four commands, exercised as real processes.

Every other test module in this suite imports the library and calls it in
process. These tests deliberately do the opposite: they run
``tools/goal-validate``, ``tools/goal-ready``, ``tools/goal-docs`` and
``tools/secret-scan`` as subprocesses and assert on exit codes, stdout bytes
and stderr. That is the surface ROGUE, CI and a human at a shell actually
consume, and it is not proven by any amount of library coverage.

Three things are only testable here:

1. **The cross-module gate.** ``tools/goal-ready`` imports
   ``goal_dcp.validate.validate`` and refuses to answer from an invalid
   backlog. The shim and the validator were written independently, so until
   all four commands and all five modules existed together nothing exercised
   that import or that gate against the real validator. The guarantee under
   test is not merely "exit 1" — it is that **stdout is completely empty**, so
   a caller that reads stdout and ignores the exit code cannot be handed a
   plausible-looking answer computed from broken data.

   This gate is also the second layer of the PID rule, and it only exists
   here. ``goal_dcp.readiness`` is pure, so it can only check that a ready
   item *declares* a PID; proving the declared PID exists, is readable and
   agrees with the backlog is the validator's job, and it is this command
   refusing to answer that joins the two halves. A successful ``ready``
   answer can therefore never contain an item whose PID does not exist — and
   that is asserted here, at the process boundary, not inferred.

2. **The published bytes.** ``pids/GOAL-DCP-001.md`` documents the readiness
   contract as ``{"ready":[{"id":"...","target_repository":"..."}]}`` with no
   space after any ``,`` or ``:``. A consumed machine contract is a byte
   contract, so the exact stdout is asserted, not just its parsed shape.

3. **That CI cannot silently diverge.** The workflow invokes commands by path
   from a ``run:`` step. Renaming a command would break CI with nothing in
   this suite noticing, so the workflow is parsed and every ``./tools/``
   command it runs is checked to exist and be executable.

Conventions, and why:

* Commands are invoked as ``[sys.executable, str(path), ...]`` so the
  filesystem executable bit is never load-bearing for the test outcome. The
  bit itself is asserted separately, from the git index, where it is durable.
* Paths are resolved from ``__file__``, never hard-coded, so the suite is
  location-independent.
* Cases that need a different repository are run against a **copy** of the
  tracked files in ``tmp_path``. The canonical backlog and documents are read,
  never mutated, and that is asserted rather than assumed.
* No credential-shaped literal appears in this file. The repository
  secret-scans its own working tree including untracked files, and CPython
  folds adjacent string literals into a single constant that lands in
  ``__pycache__``; a fake credential written here would therefore make
  ``./tools/secret-scan`` fail on the repository itself.
"""

import importlib.machinery
import importlib.util
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"
FIXTURES = REPO_ROOT / "tests" / "fixtures"

GOAL_VALIDATE = TOOLS / "goal-validate"
GOAL_READY = TOOLS / "goal-ready"
GOAL_DOCS = TOOLS / "goal-docs"
SECRET_SCAN = TOOLS / "secret-scan"

COMMANDS = (GOAL_VALIDATE, GOAL_READY, GOAL_DOCS, SECRET_SCAN)

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "control-plane.yml"
PID = REPO_ROOT / "pids" / "GOAL-DCP-001.md"

MASTER_BACKLOG = "backlog/MASTER-BACKLOG.md"
MANIFEST = "MANIFEST.md"
BACKLOG_YAML = "backlog/backlog.yaml"

#: Number of items the canonical backlog declares. Asserted on the success
#: line because ``backlog OK: N items`` is the contract, not an incidental
#: message: a command that validated nothing would still print a cheerful OK.
CANONICAL_ITEM_COUNT = 50

#: The PID-authoring-wave answer under the ``GOAL-DCP-001`` projection, as the
#: CLI must report it: eleven items, sorted by id, with their declared target
#: repositories. Written out in full on purpose - this is the answer the PO
#: authors PIDs from, so it is pinned at the process boundary and not merely
#: recomputed from the library the process is being used to test.
#:
#: These items are NOT dispatchable. ``./tools/goal-ready`` must answer
#: ``{"ready":[]}`` under the same projection, because none of them has a
#: canonical PID; that is asserted as explicitly as the wave itself.
PID_AUTHORING_WAVE = (
    ("ARES-CUR-001", "maff0000/trading-ares"),
    ("DARWIN-R1", "maff0000/DARWIN"),
    ("GOAL-CONTRACT-001", "maff0000/GOAL"),
    ("HERMES-CUR-001", "maff0000/hermes"),
    ("MT5-GW-001", "maff0000/mt5-gateway"),
    ("OPS-CRED-001", "maff0000/GOAL"),
    ("OPS-LEGACY-001", "maff0000/GOAL"),
    ("OPS-SAFE-001", "maff0000/GOAL"),
    ("OPS-SAFE-002", "maff0000/GOAL"),
    ("OPS-SAFE-003", "maff0000/GOAL"),
    ("TRON-D1-RATIFY", "maff0000/tron"),
)

#: Flags that would turn "this backlog is invalid" into an answer. None of
#: these may exist. The list is of plausible names rather than observed ones:
#: the assertion is that *no* bypass is reachable, so it must be written
#: against what someone might add, not against what is there.
BYPASS_FLAG_CANDIDATES = (
    "--force",
    "--no-validate",
    "--skip-validate",
    "--skip-validation",
    "--ignore-findings",
    "--ignore-errors",
    "--best-effort",
    "--unsafe",
    "--no-check",
)

GITLEAKS_FALLBACK = "/usr/local/bin/gitleaks"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def run(command, *arguments, cwd=None):
    """Run one command out of process.

    ``sys.executable`` runs the shim rather than exec'ing it directly, so a
    lost executable bit cannot make these tests fail for the wrong reason.
    ``cwd`` defaults to the repository root, which is where CI runs them from.
    """
    return subprocess.run(
        [sys.executable, str(command), *arguments],
        cwd=str(cwd) if cwd is not None else str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def git(repo_root, *arguments):
    return subprocess.run(
        ["git", *arguments],
        cwd=str(repo_root),
        check=True,
        capture_output=True,
        text=True,
    )


def tracked_files(repo_root=REPO_ROOT):
    """Sorted repo-relative paths of every tracked file."""
    output = git(repo_root, "ls-files").stdout
    return sorted(line for line in output.splitlines() if line.strip())


def index_mode(relative_path):
    """The file mode git has recorded for ``relative_path``, e.g. ``100755``.

    The git index is the durable truth about the executable bit; the
    filesystem bit is not. A checkout under ``core.sharedRepository`` or a
    umask of 002 yields ``0775`` on disk for a file git records as ``100755``,
    so asserting the on-disk mode equals ``0755`` would fail on a correct
    repository.
    """
    output = git(REPO_ROOT, "ls-files", "-s", "--", relative_path).stdout
    assert output.strip(), f"{relative_path} is not tracked"
    return output.split()[0]


def gitleaks_available():
    """Mirror ``tools/secret-scan``'s own discovery order, without importing it."""
    if shutil.which("gitleaks"):
        return True
    return os.access(GITLEAKS_FALLBACK, os.X_OK)


requires_gitleaks = pytest.mark.skipif(
    not gitleaks_available(),
    reason="gitleaks is not installed; ./tools/secret-scan cannot run",
)


@pytest.fixture
def repo_copy(tmp_path):
    """A throwaway git repository holding a copy of every tracked file.

    Several cases need a *different* repository: an invalid backlog, a drifted
    document, an item in a state the canonical backlog does not declare. The
    canonical files must never be mutated to produce those, so the whole
    tracked tree is copied and the copy is perturbed instead.

    The copy must be complete, not partial: ``goal-ready`` and ``goal-docs``
    resolve their repository root from their own ``__file__``, and the
    validator resolves ``pid_path`` and ``architecture_refs`` against that
    root, so a copy missing ``tools/``, ``pids/`` or ``architecture/`` would
    produce findings that are artefacts of the copy.

    ``git init`` plus ``git add -A`` (no commit) is enough: ``git ls-files``
    reads the index, so the copy's tracked file list is identical to the
    canonical one and ``MANIFEST.md``'s generated region is already in sync.
    That in-sync baseline is asserted by the tests that perturb it.
    """
    root = tmp_path / "repo"
    for relative_path in tracked_files():
        destination = root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / relative_path, destination)

    git(root, "init", "-q", ".")
    git(root, "add", "-A")

    assert tracked_files(root) == tracked_files(), "the copy is not a faithful copy"
    return root


def rewrite(path, old, new, count=1):
    """Replace ``old`` with ``new`` in ``path``, asserting ``old`` was there."""
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not found in {path.name}"
    path.write_text(text.replace(old, new, count), encoding="utf-8")


# ---------------------------------------------------------------------------
# The commands exist as commands
# ---------------------------------------------------------------------------


def test_every_command_is_an_extensionless_executable_with_a_python_shebang():
    """The four commands are commands: no .py, exec bit recorded, shebang right."""
    for command in COMMANDS:
        assert command.is_file(), f"{command.name} does not exist"
        assert command.suffix == "", f"{command.name} has a file extension"
        assert os.access(command, os.X_OK), f"{command.name} is not executable"
        assert index_mode(f"tools/{command.name}") == "100755", command.name
        first_line = command.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "#!/usr/bin/env python3", command.name


def test_every_command_answers_help_without_touching_the_repository():
    """``--help`` must work before any I/O, including with no gitleaks present."""
    for command in COMMANDS:
        result = run(command, "--help")
        assert result.returncode == 0, f"{command.name} --help: {result.stderr}"
        assert command.name in result.stdout, command.name
        assert result.stderr == "", command.name


def test_commands_resolve_their_repository_from_their_own_location(tmp_path):
    """Run from an unrelated directory: a command means the same thing anywhere."""
    validate = run(GOAL_VALIDATE, cwd=tmp_path)
    assert validate.returncode == 0, validate.stderr
    assert validate.stdout == f"backlog OK: {CANONICAL_ITEM_COUNT} items\n"

    ready = run(GOAL_READY, cwd=tmp_path)
    assert ready.returncode == 0, ready.stderr
    assert json.loads(ready.stdout) == {"ready": []}

    docs = run(GOAL_DOCS, "--check", cwd=tmp_path)
    assert docs.returncode == 0, docs.stderr


# ---------------------------------------------------------------------------
# ./tools/goal-validate
# ---------------------------------------------------------------------------


def test_goal_validate_exit_zero_on_the_canonical_backlog():
    result = run(GOAL_VALIDATE)

    assert result.returncode == 0, result.stderr
    assert result.stdout == f"backlog OK: {CANONICAL_ITEM_COUNT} items\n"
    assert result.stderr == ""


def test_goal_validate_exit_one_with_findings_on_stderr():
    """Findings go to stderr so a failure cannot contaminate captured stdout."""
    result = run(GOAL_VALIDATE, str(FIXTURES / "malformed-id.yaml"))

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.startswith("MALFORMED_ID ")
    assert result.stderr.endswith("\n")


def test_goal_validate_exit_two_on_a_load_error():
    """A document that never loaded is not a validation result."""
    result = run(GOAL_VALIDATE, str(FIXTURES / "load-error-items-not-list.yaml"))

    assert result.returncode == 2
    assert result.stdout == ""
    assert "could not be loaded" in result.stderr


def test_goal_validate_exit_two_on_a_missing_file():
    """Exit 2, and no absolute path in the message."""
    missing = FIXTURES / "this-fixture-does-not-exist.yaml"
    assert not missing.exists()

    result = run(GOAL_VALIDATE, str(missing))

    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() != ""
    assert str(REPO_ROOT) not in result.stderr


# ---------------------------------------------------------------------------
# ./tools/goal-ready -- the validate-before-answer gate
# ---------------------------------------------------------------------------


def test_goal_ready_answers_empty_on_the_canonical_backlog():
    """Nothing is FORGE-dispatchable today, and that is the honest answer.

    Two independent reasons: ``GOAL-DCP-001`` is in ``FORGE_AUDIT``, which is
    not accepted-terminal, and no canonical item is in ``DELIVERY_READY`` at
    all - the eleven that are next are in ``PID_DRAFT``, waiting on PIDs. An
    empty ready list is the correct answer, not an error and not the wave.
    """
    result = run(GOAL_READY)

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert json.loads(result.stdout) == {"ready": []}
    assert result.stdout == '{"ready":[]}\n'


def test_goal_ready_stays_empty_under_the_projection():
    """Closing the control plane does not make PID-less work dispatchable.

    This is the repaired defect at the process boundary. Before the repair this
    same command reported the eleven as ``ready``, which would have had ROGUE
    dispatch FORGE against work that has no canonical PID to build from.
    """
    result = run(GOAL_READY, "--assume-closed", "GOAL-DCP-001")

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == '{"ready":[]}\n'


def test_a_successful_ready_answer_never_contains_a_pid_less_item(repo_copy):
    """The end-to-end guarantee, on a backlog that *tries* to produce one.

    A copy is perturbed so an item is ``DELIVERY_READY`` with ``pid_path:
    null`` - precisely the shape that used to be reported as ready. The
    command must not answer at all: the validator reports ``MISSING_PID`` and
    the command refuses, with empty stdout.

    Proving this needs a *different* repository, because the canonical backlog
    cannot be put into that state and still be valid. That is the point:
    there is no valid backlog from which a PID-less item can be reported
    ready.
    """
    rewrite(
        repo_copy / BACKLOG_YAML,
        "    state: PID_DRAFT\n",
        "    state: DELIVERY_READY\n",
    )

    validated = run(repo_copy / "tools" / "goal-validate")
    assert validated.returncode == 1
    assert "MISSING_PID" in validated.stderr

    for arguments in ((), ("--with-pid",), ("--assume-closed", "GOAL-DCP-001")):
        result = run(repo_copy / "tools" / "goal-ready", *arguments)
        assert result.returncode == 1, arguments
        assert result.stdout == "", arguments
        assert "MISSING_PID" in result.stderr, arguments


#: Substitutes for the canonical PID that defeat every PID check that existed
#: before minimum PID validity. Neither declares a bold metadata label, so
#: ``BACKLOG_PID_MISMATCH`` cannot fire; both name a file that exists and reads
#: as UTF-8, so ``PID_FILE_NOT_FOUND`` cannot fire; and ``pid_path`` stays a
#: non-null string, so ``MISSING_PID`` cannot fire either.
#:
#: The second is the one that matters. A zero-byte file looks like an accident;
#: a shim with the real heading, the real labels and empty sections looks like
#: a PID, and is exactly what ``operations/ROGUE-READINESS.md`` says must never
#: be able to shortcut PO PID authoring.
INVALID_PID_SUBSTITUTES = {
    "touched": "",
    "shim": (
        "# GOAL-DCP-001 — GitHub Delivery Control Plane Foundation\n"
        "\n**Lane:** Shared  \n**Target repository:** `maff0000/GOAL`  \n"
        "**Priority:** P0  \n**Risk:** Medium  \n**Matt gate:** No  \n"
        "**PO gate:** Yes  \n"
        "\n## Purpose\n\n## Scope\n\n## Acceptance\n\n## Approval\n"
    ),
}


@pytest.mark.parametrize("substitute", sorted(INVALID_PID_SUBSTITUTES))
def test_goal_ready_refuses_to_answer_when_the_required_pid_is_not_a_pid(
    repo_copy, substitute
):
    """A PID that exists but is not a PID stops the answer, at the boundary.

    ``goal_dcp.readiness`` is pure and stays pure: it can only see that an item
    *declares* a PID. Nothing was added to it and nothing was added to
    ``tools/goal-ready``. The command already validates before answering and
    already refuses on any finding, so ``PID_INVALID`` biting the ``ready``
    answer is a consequence of the existing gate rather than a new check — and
    that consequence is what is asserted here, out of process, because it is
    not provable from either module alone.

    Run against a copy: the canonical PID is read, never mutated, and that is
    asserted rather than assumed.
    """
    canonical_before = PID.read_bytes()
    pid = repo_copy / "pids" / "GOAL-DCP-001.md"

    baseline = run(repo_copy / "tools" / "goal-validate")
    assert baseline.returncode == 0, baseline.stderr

    pid.write_text(INVALID_PID_SUBSTITUTES[substitute], encoding="utf-8")

    validated = run(repo_copy / "tools" / "goal-validate")
    assert validated.returncode == 1
    assert "PID_INVALID" in validated.stderr
    # The pre-existing checks really are all satisfied, so PID_INVALID is the
    # only thing standing between this file and a delivery-ready item.
    for already_covered in ("MISSING_PID", "PID_FILE_NOT_FOUND",
                            "BACKLOG_PID_MISMATCH"):
        assert already_covered not in validated.stderr, already_covered

    for arguments in ((), ("--with-pid",), ("--assume-closed", "GOAL-DCP-001"),
                      ("--pid-wave",), ("--pid-wave", "--with-pid")):
        result = run(repo_copy / "tools" / "goal-ready", *arguments)
        assert result.returncode == 1, arguments
        assert result.stdout == "", arguments
        assert "refusing to answer" in result.stderr, arguments
        assert "PID_INVALID" in result.stderr, arguments

    assert PID.read_bytes() == canonical_before


def test_the_canonical_pid_satisfies_minimum_pid_validity(repo_copy):
    """Non-vacuity: the real PID passes the check its substitutes fail.

    Asserted against the same copy the test above perturbs, so "refused" and
    "answered" are produced by the same command on the same tree, differing
    only in the PID's content.
    """
    validated = run(repo_copy / "tools" / "goal-validate")
    assert validated.returncode == 0, validated.stderr

    answered = run(repo_copy / "tools" / "goal-ready")
    assert answered.returncode == 0, answered.stderr
    assert answered.stdout == '{"ready":[]}\n'


def test_every_ready_entry_declares_a_pid_across_every_answerable_projection():
    """Read the invariant back off the command's own output, exhaustively.

    Every single-id projection the canonical backlog admits is tried. Any
    ``ready`` entry that appeared without a ``pid_path`` would fail here even
    if the validator and the readiness rule both somehow agreed to allow it.
    """
    ids = sorted(
        entry["id"]
        for entry in json.loads(
            run(GOAL_READY, "--pid-wave", "--assume-closed", "GOAL-DCP-001").stdout
        )["pid_authoring_wave"]
    ) + ["GOAL-DCP-001"]

    for item_id in ids:
        result = run(GOAL_READY, "--assume-closed", item_id, "--with-pid")
        assert result.returncode == 0, (item_id, result.stderr)
        for entry in json.loads(result.stdout)["ready"]:
            assert entry["pid_path"], (item_id, entry)


def test_goal_ready_refuses_to_answer_from_an_invalid_backlog(repo_copy):
    """The cross-module gate, against the real validator.

    The backlog is replaced with a fixture whose only defect is a
    non-canonical id. The shim must report findings and exit 1 with **nothing
    at all on stdout**: a caller that pipes stdout into a dispatcher must get
    no parsable answer, however it treats the exit code.
    """
    shutil.copy(FIXTURES / "malformed-id.yaml", repo_copy / BACKLOG_YAML)

    result = run(repo_copy / "tools" / "goal-ready")

    assert result.returncode == 1
    assert result.stdout == ""
    assert "refusing to answer" in result.stderr
    assert "MALFORMED_ID" in result.stderr


def test_goal_ready_refuses_under_every_flag_combination(repo_copy):
    """No supported flag turns an invalid backlog into an answer."""
    shutil.copy(FIXTURES / "malformed-id.yaml", repo_copy / BACKLOG_YAML)
    command = repo_copy / "tools" / "goal-ready"

    for arguments in ((), ("--with-pid",), ("--assume-closed", "tron-t1"),
                      ("--with-pid", "--assume-closed", "tron-t1"),
                      ("--pid-wave",), ("--pid-wave", "--with-pid"),
                      ("--pid-wave", "--assume-closed", "tron-t1"),
                      ("--pid-wave", "--with-pid", "--assume-closed", "tron-t1")):
        result = run(command, *arguments)
        assert result.returncode == 1, arguments
        assert result.stdout == "", arguments
        assert "MALFORMED_ID" in result.stderr, arguments


def test_goal_ready_has_no_bypass_flag(repo_copy):
    """There is no escape hatch, advertised or hidden.

    Each candidate is checked twice: absent from ``--help``, and rejected as a
    usage error when passed. An unknown option exits 2 with empty stdout, so a
    bypass cannot be reached by guessing its name either.
    """
    help_text = run(GOAL_READY, "--help").stdout
    shutil.copy(FIXTURES / "malformed-id.yaml", repo_copy / BACKLOG_YAML)
    command = repo_copy / "tools" / "goal-ready"

    for flag in BYPASS_FLAG_CANDIDATES:
        assert flag not in help_text, f"{flag} is advertised"
        result = run(command, flag)
        assert result.returncode == 2, flag
        assert result.stdout == "", flag


def load_goal_ready_module():
    """Import ``tools/goal-ready`` as a module, despite its lack of a suffix.

    The last-moment post-condition inside the command is deliberately
    unreachable through the CLI: the validator catches a PID-less ready item
    first and the command refuses before computing anything. A guard that can
    never be observed firing is indistinguishable from a guard that does not
    work, so it is exercised directly here.

    Importing the file is safe: everything but ``main`` is definitions, and
    ``main`` runs only under ``__name__ == "__main__"``.
    """
    spec = importlib.util.spec_from_loader(
        "goal_ready_cli",
        importlib.machinery.SourceFileLoader("goal_ready_cli", str(GOAL_READY)),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_ready_post_condition_detects_a_pid_less_entry():
    """The belt-and-braces check, proven to have teeth.

    Fed a ``ready`` payload naming a canonical item that declares no PID, the
    post-condition must name it. Fed the real answer, it must stay silent, and
    fed a PID-authoring-wave payload it must stay silent too - those items are
    *expected* to have no PID, so flagging them would make the guard fire on
    correct output.
    """
    module = load_goal_ready_module()
    backlog = module.load_backlog()

    pid_less = next(item for item in backlog.items if not item.pid_path)
    with_pid = next(item for item in backlog.items if item.pid_path)

    fabricated = {"ready": [{"id": pid_less.id}, {"id": with_pid.id}]}
    assert module.ready_invariant_violations(backlog, fabricated) == [pid_less.id]

    # An id no item declares cannot be vouched for either, so it is a violation.
    assert module.ready_invariant_violations(
        backlog, {"ready": [{"id": "NOT-DECLARED-001"}]}
    ) == ["NOT-DECLARED-001"]

    # Silent on sound input.
    assert module.ready_invariant_violations(
        backlog, {"ready": [{"id": with_pid.id}]}
    ) == []
    assert module.ready_invariant_violations(backlog, {"ready": []}) == []
    assert module.ready_invariant_violations(
        backlog, {"pid_authoring_wave": [{"id": pid_less.id}]}
    ) == []


def test_goal_ready_exit_two_on_an_unknown_assumed_id():
    """``DCP-001`` is shorthand no item declares: a usage error, not a no-op.

    Silently dropping it would answer a different question than the one asked
    - most likely an empty list reading as "nothing to do".
    """
    result = run(GOAL_READY, "--assume-closed", "DCP-001")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "DCP-001" in result.stderr


def test_goal_ready_exit_two_is_distinct_from_the_empty_answer():
    """Non-vacuity: the same command with a declared id exits 0 and answers."""
    assert run(GOAL_READY, "--assume-closed", "DCP-001").returncode == 2
    assert run(GOAL_READY, "--assume-closed", "GOAL-DCP-001").returncode == 0


def test_pid_wave_mode_keeps_the_same_exit_code_contract():
    """0 ok / 1 refused / 2 usage, identically in the new mode.

    A second mode with its own exit-code behaviour would be a second contract
    for a consumer to learn, and the refusal in particular must not be
    weakened just because this answer is advisory to the PO rather than to
    ROGUE.
    """
    assert run(GOAL_READY, "--pid-wave").returncode == 0
    assert run(GOAL_READY, "--pid-wave", "--assume-closed", "GOAL-DCP-001").returncode == 0

    unknown = run(GOAL_READY, "--pid-wave", "--assume-closed", "DCP-001")
    assert unknown.returncode == 2
    assert unknown.stdout == ""
    assert "DCP-001" in unknown.stderr


def test_pid_wave_help_states_that_the_wave_is_not_dispatchable():
    """The flag is advertised, and advertised honestly.

    A reader reaching for this mode must not come away thinking it lists work
    FORGE can be given. The help text is where that misreading would start.

    Whitespace is normalised before matching because argparse hard-wraps help
    text to the terminal width, so a phrase can be split across lines at a
    column that depends on the environment. Asserting on the raw string would
    make this test fail for a reason that has nothing to do with the wording.

    The phrases asserted on contain no hyphenated compound, deliberately:
    ``textwrap`` breaks words at hyphens, so "FORGE-dispatchable" can be
    split in the middle and survive neither the raw nor the normalised match.
    Keep it that way when rewording the help.
    """
    help_text = run(GOAL_READY, "--help").stdout
    flowed = " ".join(help_text.split())

    assert "--pid-wave" in help_text
    assert "pid_authoring_wave" in flowed
    assert "NOT ready for FORGE dispatch" in flowed
    assert "awaiting PO PID authoring" in flowed
    assert "FORGE dispatch requires an approved PID and then DELIVERY_READY" in flowed


# ---------------------------------------------------------------------------
# ./tools/goal-ready -- the published byte contract
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("arguments", [
    (),
    ("--assume-closed", "GOAL-DCP-001"),
    ("--pid-wave",),
    ("--pid-wave", "--assume-closed", "GOAL-DCP-001"),
    ("--pid-wave", "--assume-closed", "GOAL-DCP-001", "--with-pid"),
])
def test_goal_ready_emits_the_pid_documented_bytes(arguments):
    """One line of compact JSON: no space after any ``,`` or ``:``.

    Asserted in every mode, so the new mode cannot serialise differently from
    the published one.
    """
    result = run(GOAL_READY, *arguments)

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.endswith("\n")
    line = result.stdout[:-1]
    assert "\n" not in line, "the answer must be a single line"
    assert ", " not in line, "json.dumps' default separators have crept back in"
    assert ": " not in line, "json.dumps' default separators have crept back in"
    assert json.loads(line)  # parses, and is not empty of keys


def test_goal_ready_output_is_byte_identical_to_the_pid_example_style():
    """The PID's example is the command's serialisation, and names no real work.

    The example is read out of ``pids/GOAL-DCP-001.md`` rather than restated
    here, so the published byte contract is checked against the document that
    publishes it and cannot drift from it. Three things are proven:

    1. the example is canonically serialised - sorted keys, compact separators
       - so the bytes a consumer is told to expect are the bytes the command
       produces;
    2. its entry *shape* - the exact key set and the compact separators - is
       the shape the command actually emits, read off real command output
       rather than off a literal written in this test;
    3. the example names **no id any backlog item declares**.

    (3) is the point of this test. The PID previously published an example
    naming ``MT5-GW-001`` under the ``ready`` key - a ``PID_DRAFT`` item with
    no canonical PID, which can never legitimately be reported ready, so the
    published example asserted the very defect this round removed. Checking the
    example's ids against ``backlog/backlog.yaml`` is what mechanically
    prevents the example from ever again describing a real pre-PID item as
    dispatchable: a future edit that drops a live id into it fails here.

    The shape is compared against ``--pid-wave`` output because the ``ready``
    answer is correctly empty on this repository (asserted elsewhere in this
    file, and not duplicated here), and ``goal_dcp.readiness`` builds both
    answers' entries from one shared function - so the wave's entries carry
    exactly the shape the ``ready`` entries would.
    """
    example = next(
        line.strip()
        for line in PID.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith('{"ready"')
    )

    assert (
        json.dumps(json.loads(example), sort_keys=True, separators=(",", ":"))
        == example
    )

    entries = json.loads(example)["ready"]
    assert entries, "the example must still show a populated entry"

    emitted = json.loads(
        run(GOAL_READY, "--pid-wave", "--assume-closed", "GOAL-DCP-001").stdout
    )["pid_authoring_wave"]
    assert emitted, "the projection must emit entries to read the shape off"
    emitted_shapes = {frozenset(entry) for entry in emitted}
    assert len(emitted_shapes) == 1, "the command emits one entry shape"
    emitted_shape = next(iter(emitted_shapes))

    for entry in entries:
        assert frozenset(entry) == emitted_shape, entry
        assert json.dumps(entry, sort_keys=True, separators=(",", ":")) in example

    declared_ids = {
        item["id"]
        for item in yaml.safe_load(
            (REPO_ROOT / BACKLOG_YAML).read_text(encoding="utf-8")
        )["items"]
    }
    assert len(declared_ids) == CANONICAL_ITEM_COUNT, "declared ids not read"

    for entry in entries:
        assert entry["id"] not in declared_ids, (
            f"the PID's example names declared item {entry['id']!r}; "
            "the published example must not describe real work as ready"
        )


def test_goal_ready_pid_wave_needs_no_projection_once_dcp_001_is_closed():
    """GOAL-DCP-001 is CLOSED, so the wave is the unprojected answer."""
    result = run(GOAL_READY, "--pid-wave")

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    reported = json.loads(result.stdout)["pid_authoring_wave"]
    assert [(e["id"], e["target_repository"]) for e in reported] == sorted(PID_AUTHORING_WAVE)


def test_goal_ready_pid_wave_reports_exactly_the_eleven_ids():
    """The CLI surface itself, not only the library, computes the wave."""
    assert len(PID_AUTHORING_WAVE) == 11

    payload = json.loads(
        run(GOAL_READY, "--pid-wave", "--assume-closed", "GOAL-DCP-001").stdout
    )
    reported = payload["pid_authoring_wave"]

    assert set(payload) == {"pid_authoring_wave"}
    assert reported == [
        {"id": item_id, "target_repository": repository}
        for item_id, repository in PID_AUTHORING_WAVE
    ]
    assert [entry["id"] for entry in reported] == sorted(
        entry["id"] for entry in reported
    )
    assert "GOAL-DCP-001" not in [entry["id"] for entry in reported], (
        "the projected item is CLOSED, so it is not awaiting a PID either"
    )

    # ...and the same projection reports nothing as dispatchable.
    assert run(GOAL_READY, "--assume-closed", "GOAL-DCP-001").stdout == '{"ready":[]}\n'


def test_goal_ready_accepts_a_comma_separated_projection():
    """``ID[,ID...]`` is one argument, and projecting more changes the answer."""
    one = json.loads(
        run(GOAL_READY, "--pid-wave", "--assume-closed", "GOAL-DCP-001").stdout
    )
    two = json.loads(
        run(
            GOAL_READY,
            "--pid-wave",
            "--assume-closed",
            "GOAL-DCP-001,GOAL-CONTRACT-001",
        ).stdout
    )

    one_ids = {entry["id"] for entry in one["pid_authoring_wave"]}
    two_ids = {entry["id"] for entry in two["pid_authoring_wave"]}

    assert "GOAL-CONTRACT-001" in one_ids
    assert "GOAL-CONTRACT-001" not in two_ids, "a projected item is not in the wave"
    assert one_ids - {"GOAL-CONTRACT-001"} == two_ids - {"GOAL-CONTRACT-001"}


def test_goal_ready_projection_writes_nothing():
    """``--assume-closed`` is a what-if, so the backlog must be untouched."""
    before = (REPO_ROOT / BACKLOG_YAML).read_bytes()

    assert run(GOAL_READY, "--assume-closed", "GOAL-DCP-001").returncode == 0

    assert (REPO_ROOT / BACKLOG_YAML).read_bytes() == before


# ---------------------------------------------------------------------------
# ./tools/goal-ready -- --with-pid
# ---------------------------------------------------------------------------


def test_with_pid_adds_the_key_and_omitting_the_flag_leaves_it_out():
    """``pid_path`` is additive, and behaves identically in both modes.

    No wave item has a canonical PID yet, so every value is ``null`` in the
    wave answer. That is the real answer today, and a ``null`` is still a
    contract: a consumer must be able to tell "no PID" from "key missing" -
    and it is exactly what makes the wave actionable for the PO.
    """
    projection = ("--assume-closed", "GOAL-DCP-001")

    with_pid = json.loads(
        run(GOAL_READY, "--pid-wave", *projection, "--with-pid").stdout
    )
    without = json.loads(run(GOAL_READY, "--pid-wave", *projection).stdout)

    assert [entry["id"] for entry in with_pid["pid_authoring_wave"]] == [
        item_id for item_id, _ in PID_AUTHORING_WAVE
    ]
    for entry in with_pid["pid_authoring_wave"]:
        assert set(entry) == {"id", "target_repository", "pid_path"}
        assert entry["pid_path"] is None
    for entry in without["pid_authoring_wave"]:
        assert set(entry) == {"id", "target_repository"}

    # The flag is accepted in the default mode too, and adds the same key
    # there. The list happens to be empty today, which is the correct answer.
    ready = run(GOAL_READY, *projection, "--with-pid")
    assert ready.returncode == 0, ready.stderr
    assert json.loads(ready.stdout) == {"ready": []}


def test_a_genuinely_ready_item_is_reported_with_its_real_pid(repo_copy):
    """The one shape that *can* be ready, proven reachable rather than assumed.

    ``GOAL-DCP-001`` is the only canonical item declaring a PID, and
    ``--assume-closed`` projects an item ``CLOSED``, never ``DELIVERY_READY`` -
    so no projection of the canonical backlog can make anything ready. A copy
    that declares it ``DELIVERY_READY`` reaches that branch, and the copy must
    still validate cleanly, or the test would be proving nothing about a valid
    document.

    This is the non-vacuity guard for every "ready is empty" assertion in this
    file: the empty answers are empty because no item qualifies, not because
    the command can no longer report anything at all.
    """
    rewrite(repo_copy / BACKLOG_YAML, "state: CLOSED", "state: DELIVERY_READY")

    validated = run(repo_copy / "tools" / "goal-validate")
    assert validated.returncode == 0, validated.stderr

    result = run(repo_copy / "tools" / "goal-ready", "--with-pid")
    assert result.returncode == 0, result.stderr

    entries = json.loads(result.stdout)["ready"]
    assert entries, "the ready answer must be reachable at all"
    entry = next(e for e in entries if e["id"] == "GOAL-DCP-001")
    assert entry["pid_path"] == "pids/GOAL-DCP-001.md"
    assert not pathlib.PurePosixPath(entry["pid_path"]).is_absolute()
    assert (REPO_ROOT / entry["pid_path"]).is_file()

    # The item is ready *and* carries a PID - the two are not independent
    # facts any more, which is the whole repair.
    for reported in entries:
        assert reported["pid_path"]


# ---------------------------------------------------------------------------
# ./tools/goal-docs
# ---------------------------------------------------------------------------


def test_goal_docs_check_is_clean_on_this_repository():
    result = run(GOAL_DOCS, "--check")

    assert result.returncode == 0, result.stderr
    assert "in sync" in result.stdout
    assert result.stderr == ""


def test_goal_docs_check_is_the_default_mode():
    """Read-only is the default, so a bare invocation can never rewrite a file."""
    before = {
        name: (REPO_ROOT / name).read_bytes() for name in (MASTER_BACKLOG, MANIFEST)
    }

    bare = run(GOAL_DOCS)

    assert bare.returncode == 0, bare.stderr
    assert bare.stdout == run(GOAL_DOCS, "--check").stdout
    assert {
        name: (REPO_ROOT / name).read_bytes() for name in (MASTER_BACKLOG, MANIFEST)
    } == before


def test_goal_docs_detects_drift_and_write_repairs_it_idempotently(repo_copy):
    """Drift is introduced inside a generated region of a copy, never the real file.

    ``goal-docs`` takes no path argument and resolves its repository root from
    its own location, so the only way to drive it against different content is
    to run a copy of the command inside a copy of the repository. The
    canonical documents are asserted byte-unchanged afterwards.
    """
    canonical_before = {
        name: (REPO_ROOT / name).read_bytes() for name in (MASTER_BACKLOG, MANIFEST)
    }
    command = repo_copy / "tools" / "goal-docs"

    baseline = run(command, "--check")
    assert baseline.returncode == 0, baseline.stderr

    marker = "<!-- BEGIN GENERATED: backlog-table -->"
    rewrite(
        repo_copy / MASTER_BACKLOG,
        marker,
        marker + "\n\nhand-edited line that is not repository truth",
    )

    drifted = run(command, "--check")
    assert drifted.returncode == 1
    assert "GENERATED_REGION_DRIFT" in drifted.stderr
    assert MASTER_BACKLOG in drifted.stderr

    written = run(command, "--write")
    assert written.returncode == 0, written.stderr
    assert MASTER_BACKLOG in written.stdout

    repaired = run(command, "--check")
    assert repaired.returncode == 0, repaired.stderr

    # Idempotent: a second write changes no byte and reports nothing changed.
    after_first_write = {
        name: (repo_copy / name).read_bytes() for name in (MASTER_BACKLOG, MANIFEST)
    }
    again = run(command, "--write")
    assert again.returncode == 0, again.stderr
    assert "already in sync" in again.stdout
    assert {
        name: (repo_copy / name).read_bytes() for name in (MASTER_BACKLOG, MANIFEST)
    } == after_first_write

    assert {
        name: (REPO_ROOT / name).read_bytes() for name in (MASTER_BACKLOG, MANIFEST)
    } == canonical_before


def test_goal_docs_check_reports_drift_when_the_machine_backlog_changes(repo_copy):
    """Editing the YAML without regenerating is drift, not a new truth."""
    command = repo_copy / "tools" / "goal-docs"
    assert run(command, "--check").returncode == 0

    rewrite(repo_copy / BACKLOG_YAML, "state: CLOSED", "state: FORGE_AUDIT")

    drifted = run(command, "--check")
    assert drifted.returncode == 1
    assert "GENERATED_REGION_DRIFT" in drifted.stderr


# ---------------------------------------------------------------------------
# ./tools/secret-scan
# ---------------------------------------------------------------------------


@requires_gitleaks
def test_secret_scan_is_clean_on_this_repository():
    """One end-to-end invocation. ``tests/test_secret_scan.py`` owns the
    positive control that proves the scan actually fires on something."""
    result = run(SECRET_SCAN)

    assert result.returncode == 0, result.stdout + result.stderr
    lines = result.stdout.splitlines()
    assert lines[-1] == "RESULT: CLEAN"
    assert "working-tree (gitleaks dir): CLEAN" in result.stdout
    assert "git-history (gitleaks git): CLEAN" in result.stdout


@requires_gitleaks
def test_secret_scan_output_carries_no_environment_detail():
    """Deterministic output: no absolute paths, hostname or username."""
    result = run(SECRET_SCAN)

    assert str(REPO_ROOT) not in result.stdout
    assert os.sep + "tmp" not in result.stdout


# ---------------------------------------------------------------------------
# Determinism across the whole CLI surface
# ---------------------------------------------------------------------------


READ_ONLY_INVOCATIONS = (
    (GOAL_VALIDATE, ()),
    (GOAL_READY, ()),
    (GOAL_READY, ("--assume-closed", "GOAL-DCP-001")),
    (GOAL_READY, ("--assume-closed", "GOAL-DCP-001", "--with-pid")),
    (GOAL_READY, ("--pid-wave",)),
    (GOAL_READY, ("--pid-wave", "--assume-closed", "GOAL-DCP-001")),
    (GOAL_READY, ("--pid-wave", "--assume-closed", "GOAL-DCP-001", "--with-pid")),
    (GOAL_DOCS, ("--check",)),
)


@pytest.mark.parametrize(
    "command,arguments",
    READ_ONLY_INVOCATIONS,
    ids=lambda value: "-".join(value) if isinstance(value, tuple) else value.name,
)
def test_read_only_commands_are_byte_deterministic(command, arguments):
    """The same repository must always produce the same bytes."""
    first = run(command, *arguments)
    second = run(command, *arguments)

    assert first.returncode == second.returncode
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr


@requires_gitleaks
def test_secret_scan_is_byte_deterministic():
    """Separated out because it is the one slow invocation."""
    first = run(SECRET_SCAN)
    second = run(SECRET_SCAN)

    assert first.returncode == second.returncode
    assert first.stdout == second.stdout


# ---------------------------------------------------------------------------
# CI cannot silently diverge from the commands
# ---------------------------------------------------------------------------


def workflow_tool_commands():
    """Every ``./tools/`` command the workflow's ``run:`` steps invoke.

    Note for anyone extending this: PyYAML follows YAML 1.1, so the
    workflow's bare ``on:`` key loads as the boolean ``True``, not the string
    ``"on"``. Only ``jobs`` is read here, so it does not bite - but it would.
    """
    document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    found = set()
    for job in document["jobs"].values():
        for step in job.get("steps", ()):
            block = step.get("run")
            if not block:
                continue
            for token in block.split():
                if token.startswith("./tools/"):
                    found.add(token)
    return found


def test_every_tools_command_ci_runs_exists_and_is_executable():
    """A renamed or deleted command would otherwise break CI silently.

    Executability is read from ``os.access`` and from the git index rather
    than from the on-disk mode bits, because a ``core.sharedRepository`` or
    umask-002 checkout yields ``0775`` on disk for a file git records as
    ``100755``.
    """
    commands = workflow_tool_commands()

    assert commands, "no ./tools/ command found in the workflow - parser broken?"

    for command in sorted(commands):
        relative_path = command[len("./"):]
        path = REPO_ROOT / relative_path
        assert path.is_file(), f"CI runs {command} but it does not exist"
        assert os.access(path, os.X_OK), f"CI runs {command} but it is not executable"
        assert index_mode(relative_path) == "100755", command
        assert stat.S_IMODE(path.stat().st_mode) & stat.S_IXUSR, command


def test_ci_still_runs_every_gate_this_pid_introduced():
    """Dropping a gate from the workflow must fail a test, not pass quietly.

    A superset is allowed: adding a step is fine, removing one of these is
    not. ``goal-ready`` is deliberately absent - it answers a question, it is
    not a gate - and nothing here requires it to be added.
    """
    commands = workflow_tool_commands()

    assert {
        "./tools/goal-validate",
        "./tools/goal-docs",
        "./tools/secret-scan",
    } <= commands

    for command in commands:
        assert command[len("./"):].startswith("tools/")


def test_the_workflow_mutates_nothing_and_consumes_no_secret():
    """The PID's non-goals, asserted against the workflow this suite relies on.

    Asserted against the *parsed* document, not the raw text: the workflow's
    own header comment names the things it must not do, so a text search would
    be satisfied by the prose that forbids them.
    """
    document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))

    assert document["permissions"] == {"contents": "read"}

    # PyYAML follows YAML 1.1, so the bare ``on:`` key loads as the boolean
    # ``True``. Accept either so this does not depend on that quirk.
    triggers = document[True] if True in document else document["on"]
    assert set(triggers) == {"push", "pull_request"}

    for job in document["jobs"].values():
        for step in job.get("steps", ()):
            rendered = "".join(
                f"{key}{value}" for key, value in sorted(step.items(), key=str)
            )
            assert "secrets." not in rendered
            assert "${{ secrets" not in rendered

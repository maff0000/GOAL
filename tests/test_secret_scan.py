"""Tests for tools/secret-scan.

A secret scanner that never fires on anything is indistinguishable from one
that does nothing, so these tests pair a negative control (the repository
itself is clean) with a positive control (a planted fake credential is
actually detected).

Deliberate detail: the repository scans itself, so a fake credential written
as a contiguous literal in this committed file would make the repository's own
scan fail. Every fake credential here is assembled from fragments at runtime
so the full pattern never appears as a literal in committed source. The fix
for that is concatenation -- never a .gitleaksignore entry or an allowlist,
which would blind the scan to real secrets too.

tools/secret-scan is invoked as `sys.executable <path>` rather than directly,
so these tests do not depend on the executable bit surviving.
"""

import os
import pathlib
import shutil
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SECRET_SCAN = REPO_ROOT / "tools" / "secret-scan"

GITLEAKS_FALLBACK = "/usr/local/bin/gitleaks"


def gitleaks_available():
    """Mirror the script's own discovery order, without importing it."""
    if shutil.which("gitleaks"):
        return True
    return os.access(GITLEAKS_FALLBACK, os.X_OK)


def requires_gitleaks():
    if not gitleaks_available():
        pytest.skip(
            "gitleaks is not installed on this host, so tools/secret-scan "
            "cannot be exercised; install gitleaks to run this test"
        )


def run_secret_scan(*args):
    return subprocess.run(
        [sys.executable, str(SECRET_SCAN), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def fake_github_token():
    """A realistic-looking but fake GitHub personal access token.

    Assembled from fragments so the matchable pattern is never a literal in
    committed source. See the module docstring.

    The join is deliberate and must not be simplified to `"ghp" + "_" + ...`.
    CPython constant-folds adjacent string literals at compile time, so the
    `+` form stores the whole contiguous token as a single constant in this
    module's `__pycache__/*.pyc`. That bytecode cache sits in the working tree
    and is scanned, so the `+` form makes the repository's own scan fail --
    observed, not theoretical. `"".join` happens at runtime, so the fragments
    stay separate constants and nothing matchable is ever written to disk.
    """
    return "".join(["ghp", "_", "0123456789abcdefghij", "ABCDEFGHIJ012345"])


def make_repo_with_planted_credential(directory):
    """Create a git repository whose single commit contains a fake credential."""
    git = shutil.which("git")
    assert git is not None, "git is required to build the positive control fixture"

    credential_file = directory / "deploy-config.txt"
    credential_file.write_text(
        "github_token = %s\n" % fake_github_token(),
        encoding="utf-8",
    )

    base = [
        git,
        "-c",
        "user.name=secret-scan test",
        "-c",
        "user.email=secret-scan-test@example.invalid",
        "-c",
        "commit.gpgsign=false",
        "-C",
        str(directory),
    ]
    subprocess.run([*base, "init", "-q"], check=True, capture_output=True, text=True)
    subprocess.run([*base, "add", "-A"], check=True, capture_output=True, text=True)
    subprocess.run(
        [*base, "commit", "-q", "-m", "planted credential"],
        check=True,
        capture_output=True,
        text=True,
    )


def test_secret_scan_script_exists():
    assert SECRET_SCAN.is_file(), "tools/secret-scan is missing"


def test_help_succeeds():
    result = run_secret_scan("--help")
    assert result.returncode == 0, result.stderr
    assert "secret-scan" in result.stdout


def test_repository_is_clean():
    """Negative control: this repository must contain no secrets."""
    requires_gitleaks()
    result = run_secret_scan()
    assert result.returncode == 0, (
        "secret-scan reported a problem with this repository:\n"
        "%s\n%s" % (result.stdout, result.stderr)
    )
    assert "RESULT: CLEAN" in result.stdout
    # Both scans must be named and clean -- a single clean scan is not enough,
    # because a clean working tree says nothing about history.
    assert "working-tree (gitleaks dir): CLEAN" in result.stdout
    assert "git-history (gitleaks git): CLEAN" in result.stdout


def test_planted_credential_is_detected(tmp_path):
    """Positive control: a committed fake credential must be detected."""
    requires_gitleaks()
    target = tmp_path / "planted"
    target.mkdir()
    make_repo_with_planted_credential(target)

    result = run_secret_scan(str(target))

    assert result.returncode == 1, (
        "secret-scan did not report findings for a planted credential; "
        "exit=%d\n%s\n%s" % (result.returncode, result.stdout, result.stderr)
    )
    assert "RESULT: FINDINGS" in result.stdout
    assert "github-pat" in result.stdout
    assert "deploy-config.txt" in result.stdout
    # Both scans must independently see it: the working tree copy and the
    # committed history.
    assert "working-tree (gitleaks dir): 1 finding(s)" in result.stdout
    assert "git-history (gitleaks git): 1 finding(s)" in result.stdout


def test_planted_credential_value_is_not_echoed(tmp_path):
    """The scanner must never print the secret it found."""
    requires_gitleaks()
    target = tmp_path / "planted"
    target.mkdir()
    make_repo_with_planted_credential(target)

    result = run_secret_scan(str(target))

    assert fake_github_token() not in result.stdout
    assert fake_github_token() not in result.stderr


def test_unscannable_target_is_not_reported_clean(tmp_path):
    """A scan that could not run must never exit 0.

    A directory that is not a git repository cannot have its history scanned.
    `gitleaks git` exits 0 with "0 commits scanned" in that case, so trusting
    its exit status alone would report an unscanned history as clean.
    """
    requires_gitleaks()
    target = tmp_path / "not-a-repo"
    target.mkdir()
    (target / "README.txt").write_text("no secrets here\n", encoding="utf-8")

    result = run_secret_scan(str(target))

    assert result.returncode == 2, (
        "expected exit 2 for an unscannable target, got %d\n%s"
        % (result.returncode, result.stdout)
    )
    assert "RESULT: ERROR" in result.stdout
    assert "git-history (gitleaks git): ERROR" in result.stdout


def test_missing_target_is_an_error(tmp_path):
    result = run_secret_scan(str(tmp_path / "does-not-exist"))
    assert result.returncode == 2
    assert "RESULT: ERROR" in result.stdout


def test_output_is_deterministic(tmp_path):
    """Repeated runs over unchanged input must produce identical output."""
    requires_gitleaks()
    target = tmp_path / "planted"
    target.mkdir()
    make_repo_with_planted_credential(target)

    first = run_secret_scan(str(target))
    second = run_secret_scan(str(target))

    assert first.stdout == second.stdout
    assert first.returncode == second.returncode

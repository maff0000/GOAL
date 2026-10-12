"""Tests for goal_dcp.docsync: the human documents cannot drift from truth.

``backlog/MASTER-BACKLOG.md`` and ``MANIFEST.md`` restate machine truth that
lives elsewhere. The guarantee under test is twofold: drift is *detected*, and
repairing it *never touches human prose*. The second half matters as much as
the first - a sync tool that quietly ate the surrounding narrative would be
worse than no tool.

Drift tests run against a temporary git repository built from copies of the
canonical documents. The canonical files are read, never mutated.
"""

import pathlib
import shutil
import subprocess

import pytest

from goal_dcp import docsync, model
from goal_dcp.model import load_backlog

#: The documents and the regions they carry, as the tool declares them.
GENERATED_FILES = docsync.GENERATED_FILES

COPIED = ("MANIFEST.md", "backlog/MASTER-BACKLOG.md", "backlog/backlog.yaml")

REGION_NAMES = ("backlog-table", "first-wave", "manifest")


def git(repo_root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def temp_repo(tmp_path):
    """A throwaway git repository holding copies of the generated documents.

    ``git add`` (no commit) is enough: ``git ls-files`` reads the index, so the
    copy has its own, much smaller, tracked file list. :func:`docsync.write`
    then brings the copied regions into sync with *that* truth, which is the
    in-sync baseline the drift tests perturb.
    """
    root = tmp_path / "repo"
    (root / "backlog").mkdir(parents=True)
    for relative_path in COPIED:
        shutil.copy(model.REPO_ROOT / relative_path, root / relative_path)

    git(root, "init", "-q", ".")
    git(root, "add", "-A")

    docsync.write(root)
    assert docsync.check(root) == ()
    return root


def read(repo_root, relative_path):
    return (repo_root / relative_path).read_text(encoding="utf-8")


def mutate_region(repo_root, relative_path, name):
    """Hand-edit the inside of a generated region, as a careless human would."""
    path = repo_root / relative_path
    text = path.read_text(encoding="utf-8")
    marker = docsync.BEGIN_MARKER.format(name=name)
    assert marker in text
    path.write_text(
        text.replace(marker, marker + "\n\nhand-edited line that is not truth"),
        encoding="utf-8",
    )


def prose_only(text):
    """Everything outside every generated region, markers excluded.

    Written independently of :mod:`goal_dcp.docsync` on purpose: a test that
    reused the implementation's own region parser could not catch that parser
    swallowing prose.
    """
    kept = []
    remaining = text
    while True:
        begin = remaining.find("<!-- BEGIN GENERATED:")
        if begin < 0:
            kept.append(remaining)
            return "".join(kept)
        kept.append(remaining[:begin])
        end = remaining.find("<!-- END GENERATED:", begin)
        assert end >= 0, "unterminated generated region"
        remaining = remaining[remaining.find("-->", end) + len("-->"):]


def codes(findings):
    return [finding.code for finding in findings]


# ---------------------------------------------------------------------------
# The canonical repository is in sync
# ---------------------------------------------------------------------------


def test_check_is_clean_on_the_canonical_repository():
    """The committed documents agree with the repository they describe."""
    assert docsync.check() == ()
    assert docsync.check(model.REPO_ROOT) == ()


def test_every_declared_region_is_present_in_the_canonical_documents():
    """Non-vacuity: a clean check must not mean "found nothing to check"."""
    found = []
    for relative_path, names in GENERATED_FILES:
        text = (model.REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for name in names:
            assert docsync.BEGIN_MARKER.format(name=name) in text
            assert docsync.END_MARKER.format(name=name) in text
            found.append(name)

    assert sorted(found) == sorted(REGION_NAMES)


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------


def test_drift_is_detected_when_a_region_is_hand_edited(temp_repo):
    mutate_region(temp_repo, "backlog/MASTER-BACKLOG.md", "backlog-table")

    findings = docsync.check(temp_repo)

    assert codes(findings) == ["GENERATED_REGION_DRIFT"]
    assert findings[0].item_id is None
    assert "backlog/MASTER-BACKLOG.md" in findings[0].message


def test_each_drifted_region_is_reported_separately(temp_repo):
    mutate_region(temp_repo, "backlog/MASTER-BACKLOG.md", "backlog-table")
    mutate_region(temp_repo, "backlog/MASTER-BACKLOG.md", "first-wave")
    mutate_region(temp_repo, "MANIFEST.md", "manifest")

    findings = docsync.check(temp_repo)

    assert codes(findings) == ["GENERATED_REGION_DRIFT"] * 3


def test_drift_is_detected_when_the_machine_backlog_changes(temp_repo):
    """Changing the YAML without regenerating is drift, not a new truth."""
    path = temp_repo / "backlog" / "backlog.yaml"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("state: FORGE_AUDIT", "state: CLOSED", 1), encoding="utf-8"
    )

    findings = docsync.check(temp_repo)

    assert "GENERATED_REGION_DRIFT" in codes(findings)


def test_write_repairs_detected_drift(temp_repo):
    mutate_region(temp_repo, "MANIFEST.md", "manifest")

    changed = docsync.write(temp_repo)

    assert changed == ("MANIFEST.md",)
    assert docsync.check(temp_repo) == ()


def test_missing_marker_pair_is_reported(temp_repo):
    path = temp_repo / "MANIFEST.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            docsync.END_MARKER.format(name="manifest"), ""
        ),
        encoding="utf-8",
    )

    findings = docsync.check(temp_repo)

    assert codes(findings) == ["MISSING_GENERATED_REGION"]
    assert "MANIFEST.md" in findings[0].message
    assert "manifest" in findings[0].message


def test_write_does_not_invent_a_missing_marker_pair(temp_repo):
    """Where a generated region belongs is an editorial decision.

    ``write`` leaves the file alone and ``check`` keeps reporting it, so the
    absence cannot be mistaken for "in sync".
    """
    path = temp_repo / "MANIFEST.md"
    without_markers = path.read_text(encoding="utf-8").replace(
        docsync.BEGIN_MARKER.format(name="manifest"), ""
    )
    path.write_text(without_markers, encoding="utf-8")

    changed = docsync.write(temp_repo)

    assert "MANIFEST.md" not in changed
    assert path.read_text(encoding="utf-8") == without_markers
    assert codes(docsync.check(temp_repo)) == ["MISSING_GENERATED_REGION"]


# ---------------------------------------------------------------------------
# Idempotency and prose preservation
# ---------------------------------------------------------------------------


def test_write_is_idempotent(temp_repo):
    """The fixture already wrote once; a second run must change nothing."""
    assert docsync.write(temp_repo) == ()

    before = {path: read(temp_repo, path) for path in COPIED}
    assert docsync.write(temp_repo) == ()
    assert {path: read(temp_repo, path) for path in COPIED} == before


def test_write_never_touches_content_outside_the_markers(temp_repo):
    before = {path: prose_only(read(temp_repo, path)) for path in COPIED}

    for relative_path, names in GENERATED_FILES:
        for name in names:
            mutate_region(temp_repo, relative_path, name)
    docsync.write(temp_repo)

    assert {path: prose_only(read(temp_repo, path)) for path in COPIED} == before


def test_write_preserves_the_specific_human_prose_in_each_document(temp_repo):
    mutate_region(temp_repo, "MANIFEST.md", "manifest")
    mutate_region(temp_repo, "backlog/MASTER-BACKLOG.md", "first-wave")

    docsync.write(temp_repo)

    manifest = read(temp_repo, "MANIFEST.md")
    assert manifest.startswith("# Manifest")
    assert "private evidence store" in manifest
    assert manifest.rstrip().endswith("not in this repository.")

    master = read(temp_repo, "backlog/MASTER-BACKLOG.md")
    assert master.startswith("# THE GOAL — Initial Master Backlog")
    assert "## First wave after GOAL-DCP-001" in master


def test_write_leaves_untouched_documents_out_of_the_changed_list(temp_repo):
    mutate_region(temp_repo, "MANIFEST.md", "manifest")

    changed = docsync.write(temp_repo)

    assert changed == ("MANIFEST.md",)


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------


def test_manifest_lists_tracked_files_sorted_and_nothing_else(temp_repo):
    (temp_repo / "untracked-note.md").write_text("not tracked\n", encoding="utf-8")

    rendered = docsync.render_manifest(temp_repo)

    assert rendered.splitlines() == [
        "- `MANIFEST.md`",
        "- `backlog/MASTER-BACKLOG.md`",
        "- `backlog/backlog.yaml`",
    ]
    assert "untracked-note.md" not in rendered


def test_manifest_region_of_this_repository_lists_its_tracked_files():
    rendered = docsync.render_manifest(model.REPO_ROOT)
    tracked = git(model.REPO_ROOT, "ls-files").stdout.splitlines()

    assert rendered.splitlines() == [f"- `{path}`" for path in sorted(tracked)]


def test_backlog_table_has_one_row_per_item_in_source_order():
    backlog = load_backlog()

    rows = docsync.render_backlog_table(backlog).splitlines()[2:]

    assert len(rows) == len(backlog.items)
    for row, item in zip(rows, backlog.items):
        assert row.startswith(f"| {item.id} |")


def test_backlog_table_declares_the_required_columns():
    header = docsync.render_backlog_table(load_backlog()).splitlines()[0].lower()

    for column in (
        "id", "lane", "component", "target repository", "priority", "risk",
        "state", "depends on", "matt gate",
    ):
        assert column in header


def test_backlog_table_renders_canonical_complete_dependency_ids():
    backlog = load_backlog()

    table = docsync.render_backlog_table(backlog)

    for item in backlog.items:
        for dependency_id in item.depends_on:
            assert dependency_id in table
    # The shorthand and wildcard notation the hand-maintained table used is
    # gone: those forms are not canonical ids and cannot be checked.
    assert "| DCP-001 " not in table
    assert "OPS-SAFE-*" not in table
    assert "TRON-T2,T3,T4" not in table


def test_backlog_table_renders_an_em_dash_for_no_dependencies():
    backlog = load_backlog()
    assert backlog.by_id["GOAL-DCP-001"].depends_on == ()

    row = next(
        line
        for line in docsync.render_backlog_table(backlog).splitlines()
        if line.startswith("| GOAL-DCP-001 |")
    )

    assert "—" in row


def test_backlog_table_marks_the_capital_gates():
    backlog = load_backlog()

    table = docsync.render_backlog_table(backlog)

    gated = [
        line
        for line in table.splitlines()
        if line.startswith(("| PAPER-E2E-001 |", "| LIVE-GATE-001 |"))
    ]
    assert len(gated) == 2
    for line in gated:
        assert line.rstrip().endswith("| **Yes** |")


def test_renderers_are_pure_and_write_nothing(tmp_path):
    """Rendering must not be the thing that changes the repository."""
    backlog = load_backlog()
    before = pathlib.Path(backlog.source_path).read_text(encoding="utf-8")

    docsync.render_backlog_table(backlog)
    docsync.render_first_wave(backlog)

    assert pathlib.Path(backlog.source_path).read_text(encoding="utf-8") == before

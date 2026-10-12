"""Generated-region sync between repository truth and the human documents.

``backlog/backlog.yaml`` is the machine authority and
``backlog/MASTER-BACKLOG.md`` is the human view of it. The failure mode this
module exists to prevent is the two becoming *independent truths*: a table
edited by hand, a "first wave" list that no longer matches the dependency
graph, a manifest that has quietly stopped listing what the repository
actually contains. Prose cannot be trusted to stay true by discipline alone,
so the parts that restate machine truth are generated and mechanically
checked.

Generated regions are delimited by HTML comments, which render as nothing in
markdown::

    <!-- BEGIN GENERATED: backlog-table -->
    ...generated...
    <!-- END GENERATED: backlog-table -->

Everything outside a marker pair is human prose and is **never** touched by
:func:`write`. That is the whole bargain: humans own the narrative, the tool
owns the restatements of machine truth, and ``./tools/goal-docs --check``
fails when a restatement has drifted.

Two deliberate properties:

* The documented first wave is **computed**, by projecting ``GOAL-DCP-001``
  closed and asking :func:`goal_dcp.readiness.ready_items`. It is never typed
  by hand, so it cannot disagree with the backlog. It also replaces the range
  notation the hand-maintained list used with canonical complete ids, which is
  what makes the list checkable at all.
* :func:`render_manifest` lists **tracked** files, from ``git ls-files``. An
  untracked file is not repository truth and must not appear in the manifest;
  newly committed files therefore make the region drift until it is
  regenerated, which is the point.
"""

from __future__ import annotations

import pathlib
import subprocess
from typing import Callable

from goal_dcp import model
from goal_dcp.model import Backlog, Finding, sort_findings
from goal_dcp.readiness import ready_items

#: The projection used to document the first wave: "once GOAL-DCP-001 is
#: accepted, what becomes dispatchable?". This is the *input* to the readiness
#: rule — the id of the work being closed — and not a readiness result. The
#: answer is whatever the rule computes from the backlog; no first-wave id is
#: written down anywhere in this package.
FIRST_WAVE_PROJECTION: frozenset[str] = frozenset({"GOAL-DCP-001"})

BEGIN_MARKER = "<!-- BEGIN GENERATED: {name} -->"
END_MARKER = "<!-- END GENERATED: {name} -->"

EM_DASH = "—"

#: Which generated regions live in which repo-relative document, in the order
#: they are checked and written.
GENERATED_FILES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("backlog/MASTER-BACKLOG.md", ("backlog-table", "first-wave")),
    ("MANIFEST.md", ("manifest",)),
)

TABLE_COLUMNS: tuple[str, ...] = (
    "ID", "Lane", "Component", "Outcome", "Target repository", "Depends on",
    "Priority", "Risk", "State", "PO gate", "Matt gate",
)


# ---------------------------------------------------------------------------
# Cell helpers
# ---------------------------------------------------------------------------


def _cell(value: object) -> str:
    """Render one table cell: em dash when empty, pipes escaped.

    Values are rendered as the backlog declares them (``shared``, not
    ``Shared``) so the human view cannot misrepresent the machine value.
    """
    if value is None:
        return EM_DASH
    text = str(value).strip()
    if not text:
        return EM_DASH
    return text.replace("|", "\\|")


def _depends_cell(depends_on: tuple[object, ...]) -> str:
    """Canonical complete dependency ids, declaration order, or an em dash."""
    if not depends_on:
        return EM_DASH
    return ", ".join(_cell(dependency_id) for dependency_id in depends_on)


def _gate_cell(value: object, emphasise: bool = False) -> str:
    """Render a boolean gate. ``emphasise`` bolds a required gate."""
    if value is True:
        return "**Yes**" if emphasise else "Yes"
    if value is False:
        return "No"
    return _cell(value)


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------


def render_backlog_table(backlog: Backlog) -> str:
    """Render the human backlog table from the machine backlog.

    Source order is preserved rather than sorted: the YAML is authored in
    programme order, and reordering it would make the human view harder to
    read than the thing it is a view of.
    """
    lines = [
        "| " + " | ".join(TABLE_COLUMNS) + " |",
        "|" + "|".join(["---"] * len(TABLE_COLUMNS)) + "|",
    ]
    for item in backlog.items:
        lines.append(
            "| "
            + " | ".join(
                (
                    _cell(item.id),
                    _cell(item.lane),
                    _cell(item.component),
                    _cell(item.title),
                    _cell(item.target_repository),
                    _depends_cell(item.depends_on),
                    _cell(item.priority),
                    _cell(item.risk),
                    _cell(item.state),
                    _gate_cell(item.po_gate),
                    _gate_cell(item.matt_gate, emphasise=True),
                )
            )
            + " |"
        )
    return "\n".join(lines)


def render_first_wave(backlog: Backlog) -> str:
    """Render the first wave as computed readiness, never as a typed list."""
    items = ready_items(backlog, assume_closed=FIRST_WAVE_PROJECTION)
    if not items:
        return "_No item becomes dispatchable under this projection._"
    return "\n".join(
        f"- `{_cell(item.id)}` {EM_DASH} {_cell(item.title)} "
        f"(`{_cell(item.target_repository)}`)"
        for item in items
    )


def render_manifest(repo_root: pathlib.Path) -> str:
    """Render the manifest from ``git ls-files``, sorted, one bullet per file."""
    completed = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    paths = sorted(line for line in completed.stdout.splitlines() if line.strip())
    return "\n".join(f"- `{path}`" for path in paths)


#: Region name -> renderer. Every renderer takes the loaded backlog and the
#: repository root, so regions can be planned uniformly.
_RENDERERS: dict[str, Callable[[Backlog, pathlib.Path], str]] = {
    "backlog-table": lambda backlog, repo_root: render_backlog_table(backlog),
    "first-wave": lambda backlog, repo_root: render_first_wave(backlog),
    "manifest": lambda backlog, repo_root: render_manifest(repo_root),
}


# ---------------------------------------------------------------------------
# Region machinery
# ---------------------------------------------------------------------------


def _region_bounds(text: str, name: str) -> tuple[int, int] | None:
    """Return the ``(start, stop)`` span *between* a marker pair, or ``None``.

    ``None`` means the pair is absent: either marker missing, or the end
    marker not after the begin marker.
    """
    begin = BEGIN_MARKER.format(name=name)
    end = END_MARKER.format(name=name)
    begin_at = text.find(begin)
    if begin_at < 0:
        return None
    inner_start = begin_at + len(begin)
    end_at = text.find(end, inner_start)
    if end_at < 0:
        return None
    return inner_start, end_at


def _region_text(content: str) -> str:
    """Wrap generated ``content`` so the markers sit on their own lines.

    The blank line after the begin marker matters: markdown will not render a
    table that starts on the line immediately after an HTML comment.
    """
    body = content.strip("\n")
    return f"\n\n{body}\n\n" if body else "\n\n"


def _resolve_root(repo_root: pathlib.Path | None) -> pathlib.Path:
    return model.REPO_ROOT if repo_root is None else pathlib.Path(repo_root)


def _rendered_regions(repo_root: pathlib.Path) -> dict[str, str]:
    """Render every generated region for ``repo_root``, keyed by region name."""
    backlog = model.load_backlog(repo_root / "backlog" / "backlog.yaml")
    return {
        name: _region_text(render(backlog, repo_root))
        for name, render in _RENDERERS.items()
    }


# ---------------------------------------------------------------------------
# Public operations
# ---------------------------------------------------------------------------


def check(repo_root: pathlib.Path | None = None) -> tuple[Finding, ...]:
    """Report generated regions that have drifted or gone missing.

    One ``GENERATED_REGION_DRIFT`` finding per region whose content no longer
    matches what the repository would generate, and one
    ``MISSING_GENERATED_REGION`` finding per absent marker pair. An empty tuple
    means the documents and the repository agree.
    """
    root = _resolve_root(repo_root)
    rendered = _rendered_regions(root)
    findings: list[Finding] = []

    for relative_path, names in GENERATED_FILES:
        text = (root / relative_path).read_text(encoding="utf-8")
        for name in names:
            bounds = _region_bounds(text, name)
            if bounds is None:
                findings.append(
                    Finding(
                        "MISSING_GENERATED_REGION",
                        None,
                        f"{relative_path} has no '{name}' generated region "
                        f"(expected a BEGIN/END GENERATED: {name} marker pair)",
                    )
                )
                continue
            start, stop = bounds
            if text[start:stop] != rendered[name]:
                findings.append(
                    Finding(
                        "GENERATED_REGION_DRIFT",
                        None,
                        f"{relative_path} generated region '{name}' does not "
                        "match repository truth; run ./tools/goal-docs --write",
                    )
                )

    return sort_findings(findings)


def write(repo_root: pathlib.Path | None = None) -> tuple[str, ...]:
    """Rewrite drifted generated regions in place.

    Returns the sorted repo-relative paths actually changed; an empty tuple
    means everything was already in sync, which makes this idempotent.

    Only the text *between* a marker pair is replaced, so human prose is
    preserved byte for byte. An absent marker pair is skipped rather than
    invented: where a generated region belongs is an editorial decision, and
    :func:`check` reports the absence as ``MISSING_GENERATED_REGION``.
    """
    root = _resolve_root(repo_root)
    rendered = _rendered_regions(root)
    changed: list[str] = []

    for relative_path, names in GENERATED_FILES:
        path = root / relative_path
        original = path.read_text(encoding="utf-8")
        text = original
        for name in names:
            bounds = _region_bounds(text, name)
            if bounds is None:
                continue
            start, stop = bounds
            text = text[:start] + rendered[name] + text[stop:]
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(relative_path)

    return tuple(sorted(changed))

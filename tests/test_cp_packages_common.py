"""Package-level checks: CP-1 mapping tables, forbidden content, sanitisation, status; CP-2 is reference-only.

GOLD-AUD-C acceptance A-5, A-6, A-7.
"""

import json
import re
from pathlib import Path

import pytest

from cp_support.cp_common import CP1_DIR, CP2_DIR, REPO_ROOT, fixture_files, load_json

LANE = REPO_ROOT / "audits" / "2026-10-15" / "gold-mvp" / "lanes" / "GOLD-AUD-C"
PACKAGES = [CP1_DIR]
SCANNED = [CP1_DIR, CP2_DIR]
FORBIDDEN_KEY = re.compile(r"(stop_?loss|take_?profit|quantity|account|broker|confidence|(^|_)order(_|$)|(^|_)lots?(_|$))", re.I)
FORBIDDEN_VALUE = re.compile(r"\b(broker|account)\b", re.I)


def _tables(text, marker):
    """Rows of the markdown table that follows `<!-- marker -->`, as lists of cells."""
    out = []
    for block in re.split(rf"<!-- {marker}[^>]*-->", text)[1:]:
        rows = []
        for line in block.strip().splitlines():
            if not line.startswith("|"):
                if rows:
                    break
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
        header, rows = rows[0], rows[2:]
        out.append((header, rows))
    return out


@pytest.mark.parametrize("pkg", PACKAGES, ids=lambda p: p.name)
def test_mapping_tables_have_no_empty_cell_no_tbd_and_unsupported_rows_name_their_behaviour(pkg):
    text = (pkg / "PACKAGE.md").read_text(encoding="utf-8")
    tables = _tables(text, "mapping-table")
    assert tables, "no mapping table found"
    total = 0
    for header, rows in tables:
        status_col = header.index("Disposition")
        for row in rows:
            total += 1
            assert len(row) == len(header), row
            assert all(cell for cell in row), f"empty cell: {row}"
            assert not re.search(r"\bTBD\b", " ".join(row)), row
            assert row[status_col] in {"MAPPED", "DERIVED", "UNSUPPORTED"}, row
            if row[status_col] == "UNSUPPORTED":
                assert re.search(r"CP1-[A-Z]?\d+|rejected|dropped", " ".join(row), re.I), f"UNSUPPORTED row lacks behaviour: {row}"
            if row[status_col] == "DERIVED":
                assert len(" ".join(row)) > 40, row
    assert total >= 20


@pytest.mark.parametrize("pkg", PACKAGES, ids=lambda p: p.name)
def test_matrix_rows_are_prepared_with_owners_and_none_is_frozen(pkg):
    text = (pkg / "PACKAGE.md").read_text(encoding="utf-8")
    ((header, rows),) = _tables(text, "matrix-rows")
    col = header.index("Status")
    assert rows
    for row in rows:
        assert row[col] in {"COMPATIBLE", "ADAPTER", "INCOMPATIBLE"}, row
        assert row[header.index("Owner")], row
    assert not re.search(r"^\*{0,2}Status:?\*{0,2}:?\s*FROZEN", text, flags=re.M | re.I)
    assert re.search(r"PROPOSED", text)


@pytest.mark.parametrize("pkg", PACKAGES, ids=lambda p: p.name)
def test_valid_fixtures_and_schemas_contain_no_forbidden_vocabulary(pkg):
    def walk(obj, where):
        if isinstance(obj, dict):
            for k, v in obj.items():
                assert not FORBIDDEN_KEY.search(str(k)), f"{where}: forbidden key {k}"
                walk(v, where)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, where)
        elif isinstance(obj, str):
            assert not FORBIDDEN_VALUE.search(obj), f"{where}: forbidden value {obj}"

    for path in fixture_files(pkg / "fixtures" / "valid"):
        walk(json.loads(path.read_text(encoding="utf-8")), path.name)
    for path in (pkg / "schema").glob("*.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))

        def props(node):
            if isinstance(node, dict):
                for key in ("properties",):
                    for name in node.get(key, {}):
                        assert not FORBIDDEN_KEY.search(name), f"{path.name}: property {name}"
                for v in node.values():
                    props(v)
            elif isinstance(node, list):
                for v in node:
                    props(v)

        props(doc)


SANITISE = [
    (re.compile(r"\b\d{1,3}(\.\d{1,3}){3}\b"), "IPv4 address"),
    (re.compile(r"-----BEGIN [A-Z ]*KEY-----"), "PEM key"),
    (re.compile(r"\b(AKIA|ghp_|gho_|xox[bap]-|sk-[A-Za-z0-9]{20})"), "token prefix"),
    (re.compile(r"\b[a-z0-9-]+\.(local|internal|lan|corp)\b", re.I), "internal hostname"),
    (re.compile(r"(?i)\b(password|passwd|api[_-]?key|secret[_-]?key|private[_-]?key)\s*[:=]"), "credential assignment"),
    (re.compile(r"(^|[\s\"'(=])(/srv/|/root/|/home/|/etc/)"), "host path"),
    (re.compile(r"\bredis://|\bssh\s+\w+@"), "connection string"),
]


def _scan_files():
    for pkg in SCANNED:
        yield from (p for p in pkg.rglob("*") if p.is_file())
    if LANE.exists():
        yield from (p for p in LANE.rglob("*") if p.is_file())
    yield from (p for p in (REPO_ROOT / "tests" / "cp_support").glob("*.py"))
    yield from (p for p in (REPO_ROOT / "tests").glob("test_cp*.py") if p.name != Path(__file__).name)


def test_sanitisation_grep_over_packages_evidence_and_support_code_is_empty():
    hits = []
    for path in _scan_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in SANITISE:
            for m in pattern.finditer(text):
                hits.append(f"{path.relative_to(REPO_ROOT)}: {label}: {m.group(0)!r}")
    assert hits == [], "\n".join(hits[:20])


def test_no_private_key_material_is_present_anywhere_in_the_committed_cp_files():
    for path in _scan_files():
        if path.suffix != ".json":
            continue
        text = path.read_text(encoding="utf-8")
        assert '"private_key"' not in text and '"seed"' not in text and '"secret"' not in text, path.name


ALLOWED_CP2_NAMES = {"GOAL-TRIGGER-001", "GOAL-CONTRACT-001", "SOURCES.tsv", "RECONCILIATION.md", "DISPOSITION.md"}
BARE_IDENTIFIER = re.compile(r"^[A-Za-z0-9]+(_[A-Za-z0-9]+)+$")
VERSIONED_ID = re.compile(r"/v\d+$")


def _structure_problems(text, allowed=frozenset()):
    """Structural reasons a text is not a pointer. Lists no contract vocabulary."""
    problems = []
    if "```" in text:
        problems.append("code fence")
    if re.search(r"^\s*\|", text, flags=re.M):
        problems.append("table")
    if "<!--" in text:
        problems.append("machine-read marker")
    if re.search(r"^\s*[\[{]", text, flags=re.M):
        problems.append("JSON-like block")
    if re.search(r"^\s*[A-Za-z_]+:\s", text, flags=re.M):
        problems.append("YAML-like line")
    if re.search(r"\b\w+\s*=\s*\S", text):
        problems.append("key=value")
    for span in re.findall(r"`([^`]+)`", text):
        if allowed:
            if span not in allowed:
                problems.append(f"backticked name not allowed: {span}")
        elif BARE_IDENTIFIER.match(span) or VERSIONED_ID.search(span):
            problems.append(f"field-like backticked identifier: {span}")
    return problems


def test_cp2_is_reference_only_by_structure():
    files = sorted(p.name for p in CP2_DIR.rglob("*") if p.is_file())
    assert files == ["PACKAGE.md"], files
    path = CP2_DIR / "PACKAGE.md"
    assert path.stat().st_size < 4096
    text = path.read_text(encoding="utf-8")
    assert re.search(r"REFERENCE-ONLY", text)
    assert not re.search(r"^\*{0,2}Status:?\*{0,2}:?\s*FROZEN", text, flags=re.M | re.I)
    assert _structure_problems(text, allowed=ALLOWED_CP2_NAMES) == []


def _section(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i)]


def test_cp2_sections_of_the_lane_documents_carry_no_field_like_identifiers():
    rec = (LANE / "RECONCILIATION.md").read_text(encoding="utf-8")
    parts = [
        _section(rec, "### CP-2", "Strategy-definition findings"),
        _section(rec, "## 6.", "## 7."),
    ]
    for part in parts:
        # tables are legitimate in these sections; only the identifier rules apply
        spans = re.findall(r"`([^`]+)`", part)
        bad = [s for s in spans if BARE_IDENTIFIER.match(s) or VERSIONED_ID.search(s)]
        assert bad == [], bad
    disp = (LANE / "DISPOSITION.md").read_text(encoding="utf-8")
    rows = [l for l in disp.splitlines() if l.startswith("| FALCON ") or l.startswith("| TRON D1")]
    assert rows
    for row in rows:
        bad = [s for s in re.findall(r"`([^`]+)`", row) if VERSIONED_ID.search(s)]
        assert bad == [], bad

"""Shared fixture loading and instant helpers for the CP-1 / CP-2 conformance tests.

Only loading is shared between the two independent checkers; every rule is
implemented separately in checker A and checker B.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterator

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = REPO_ROOT / "contracts" / "packages"
CP1_DIR = PACKAGES / "cp-1-hermes-helios-input"
CP2_DIR = PACKAGES / "cp-2-trigger-outbox-inbox"


class Num(Decimal):
    """A JSON number that remembers its literal text (exponent and precision checks)."""

    literal: str

    def __new__(cls, text: str) -> "Num":
        obj = Decimal.__new__(cls, text)
        obj.literal = text
        return obj


def load_json(path: Path | str) -> Any:
    """Parse JSON; every number becomes a :class:`Num`; NaN/Infinity are refused."""

    def _const(name: str) -> Any:
        raise ValueError(f"non-finite JSON constant {name}")

    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        parse_float=Num,
        parse_int=Num,
        parse_constant=_const,
    )


def plain(value: Any) -> Any:
    """Convert Num to int/str-free plain types for jsonschema (numbers become Decimal-free floats)."""
    if isinstance(value, Num):
        text = value.literal
        if any(c in text for c in ".eE"):
            return float(text)
        return int(text)
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [plain(v) for v in value]
    return value


def fixture_files(directory: Path) -> Iterator[Path]:
    for path in sorted(Path(directory).rglob("*.json")):
        if path.name in {"MANIFEST.json"}:
            continue
        yield path


def unnum(value: Any) -> Any:
    """Num -> int (JSON integers only) recursively, for comparing expectations."""
    if isinstance(value, Num):
        return int(value)
    if isinstance(value, dict):
        return {k: unnum(v) for k, v in value.items()}
    if isinstance(value, list):
        return [unnum(v) for v in value]
    return value

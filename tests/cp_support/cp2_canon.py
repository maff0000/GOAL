"""goal-canon/1 as PROPOSED in ADR-CONTRACT-001 section 4, restricted to what CP-2 fixtures need.

This is a test reference for fixture generation and checking. The normative text is
GOAL-CONTRACT-001 / ADR-CONTRACT-001 (not frozen); CP-2 adds no canonicalisation rule.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

DOMAIN = b"goal.strategy-trigger/v1\n"
OCCURRENCE_FIELDS = (
    "strategy_id", "strategy_version", "strategy_fingerprint", "binding_id", "instrument_id",
    "timeframe", "signal_class", "output_direction", "setup_origin_bar_utc", "bar_close_utc",
)
SETUP_FIELDS = (
    "strategy_id", "strategy_version", "strategy_fingerprint", "binding_id", "instrument_id",
    "timeframe", "setup_origin_bar_utc",
)


def canon(obj: Any) -> bytes:
    """UTF-8, sorted keys, no whitespace, un-escaped non-ASCII, NaN refused, null preserved."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(obj)).hexdigest()


def occurrence_key(env: dict) -> dict:
    return {k: env[k] for k in OCCURRENCE_FIELDS}


def setup_key(env: dict) -> tuple:
    return tuple(env[k] for k in SETUP_FIELDS)


def trigger_id(env: dict) -> str:
    return "trg1_" + hashlib.sha256(canon(occurrence_key(env))).hexdigest()


def signed_bytes(env: dict) -> bytes:
    body = {k: v for k, v in env.items() if k != "signature"}
    return DOMAIN + canon(body)


def content_digest(env: dict) -> str:
    return digest({k: v for k, v in env.items() if k != "signature"})


def key_id(public_key: bytes) -> str:
    return "sha256:" + hashlib.sha256(public_key).hexdigest()

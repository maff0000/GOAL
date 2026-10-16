"""CP-1 checker B: hand-written, standard library only, integer arithmetic.

Written from PACKAGE.md of cp-1-hermes-helios-input (rules, evaluation order, mapping table)
without reference to checker A. Every instant is handled as integer microseconds and every
decimal as text, so it shares no parsing code with checker A.

Verdict model: collect every violated rule, report the one with the lowest ordinal in
ORDER (the package rejection matrix order). A candidate that violates nothing is ACCEPTED
and, at wire level, yields the canonical frames.
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from .cp_common import Num

ORDER = [
    "CP1-W01", "CP1-W02", "CP1-W03", "CP1-W05", "CP1-W04", "CP1-W08", "CP1-W10", "CP1-W09",
    "CP1-W07", "CP1-W06", "CP1-S03", "CP1-S01", "CP1-S02", "CP1-S04", "CP1-H01", "CP1-J01", "CP1-J02",
    "CP1-J03", "CP1-J04", "CP1-H02", "CP1-H03",
    "CP1-F18", "CP1-F02", "CP1-F17", "CP1-F01", "CP1-F08", "CP1-F06", "CP1-F07", "CP1-F03",
    "CP1-F04", "CP1-F05", "CP1-F09", "CP1-F10", "CP1-F12", "CP1-F11", "CP1-F13", "CP1-F16",
    "CP1-F20", "CP1-F19", "CP1-F14", "CP1-F15",
]

TF_SECONDS = {"M1": 60, "M5": 300, "M15": 900, "H1": 3600, "H4": 14400, "D1": 86400}
TF_ALT = {"1M": "M1", "5M": "M5", "15M": "M15", "1H": "H1", "4H": "H4", "1D": "D1"}
FRAME_SCHEMA_VERSION = "hermes.market_fact/1.0.0"
CANDLE_ENV_KEYS = {
    "schema_version", "service", "domain", "contract", "contract_version", "key",
    "generated_at_utc", "valid_until_utc", "ttl_seconds", "freshness_state", "status",
    "reason_codes", "provenance", "data",
}
CANDLE_DATA_KEYS = {
    "instrument", "timeframe", "timestamp_utc", "open", "high", "low", "close", "volume",
    "body_high", "body_low", "body_size", "range_size", "wick_high", "wick_low",
    "candle_direction", "is_closed", "source_timeframe", "source_coverage", "source_count",
    "expected_source_count", "gap_state", "derivation_policy", "source_policy_epoch",
    "publisher", "contract_version",
}
CANDLE_PROV_KEYS = {
    "publisher", "source", "source_timeframe", "derivation", "generated_at_utc",
    "source_policy_epoch",
}
CANDLE_HIST_KEYS = {
    "history_contract_version", "backfill_run_id", "backfill_inserted_at_utc", "source_table",
    "source_timestamp_utc",
}
CANDLE_FORBIDDEN = (
    "structure", "choch", "bos", "order_block", "regime", "signal", "setup", "confidence",
    "permission", "risk", "cockpit", "projection", "support", "resistance",
)
STATUSES = {
    "OK", "STALE", "FORMING", "GAP_DETECTED", "SOURCE_INCOMPLETE", "NO_SOURCE_DATA",
    "MARKET_CLOSED", "PUBLISH_DISABLED",
}
FRESHNESS = {"FRESH", "STALE", "FORMING", "UNAVAILABLE"}
IND_ENV_KEYS = {
    "publisher", "schema_version", "contract_version", "instrument", "timeframe",
    "generated_at_utc", "value_open_time_utc", "source_candle_contract", "source_timeframes",
    "indicator_set_version", "indicators", "methods", "freshness_state", "deterministic_only",
}
IND_HIST_KEYS = {
    "history_contract_version", "publish_run_id", "published_at_utc",
    "source_candle_history_key", "source_timestamp_utc",
}
IND_FORBIDDEN = (
    "regime", "regime_confidence", "risk", "order_block", "liquidity", "decision", "trade",
    "gate", "password", "secret", "credential", "acl", "noauth",
)
IND_NAMES = {
    "ema_9", "ema_12", "ema_21", "ema_26", "ema_50", "ema_200", "rsi_14", "atr_14",
    "bollinger_upper_20_2", "bollinger_middle_20_2", "bollinger_lower_20_2", "adx_14",
    "adx_plus_di_14", "adx_minus_di_14",
}
FRAME_IND = ["rsi_14", "ema_9", "ema_21", "ema_50", "ema_200", "atr_14", "regime", "session"]
PINNED_METHODS = {
    "ema_method": "STANDARD_2_OVER_N_PLUS_1_SMA_SEED",
    "rsi_method": "CUTLER_SMA_14",
    "atr_method": "SMA_14",
}
MS_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{3})Z$")
MICRO_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{6})Z$")
ANY_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?(Z|[+-]\d{2}:\d{2})?$"
)
INSTR_RE = re.compile(r"^[A-Z0-9]{2,10}(_[A-Z0-9]{2,10})?$")
INSTR_DENY = {"XAUUSD"}
DEC_RE = re.compile(r"^-?\d+(\.\d+)?$")


# ------------------------------------------------------------------ small helpers
def _days_from_civil(y: int, m: int, d: int) -> int:
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def _valid_date(y: int, m: int, d: int) -> bool:
    if not 1 <= m <= 12 or d < 1:
        return False
    dim = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28, 31, 30, 31, 30,
           31, 31, 30, 31, 30, 31][m - 1]
    return d <= dim


def _micros(match: "re.Match[str]", frac_group: int, offset_minutes: int = 0) -> Optional[int]:
    g = match.groups()
    y, mo, d, hh, mi, ss = (int(x) for x in g[:6])
    if not _valid_date(y, mo, d) or hh > 23 or mi > 59 or ss > 59:
        return None
    frac = g[frac_group] or ""
    micro = int((frac + "000000000")[:6]) if frac else 0
    secs = _days_from_civil(y, mo, d) * 86400 + hh * 3600 + mi * 60 + ss - offset_minutes * 60
    return secs * 1_000_000 + micro


def ms_to_micros(text: Any) -> Optional[int]:
    if not isinstance(text, str):
        return None
    m = MS_RE.match(text)
    return _micros(m, 6) if m else None


def lenient_micros(text: Any) -> Optional[int]:
    """Frame-level consumer grammar: extended ISO-8601 with an explicit Z or numeric offset."""
    if not isinstance(text, str):
        return None
    m = ANY_RE.match(text.strip())
    if not m or not m.group(8):
        return None
    zone = m.group(8)
    off = 0
    if zone != "Z":
        off = (1 if zone[0] == "+" else -1) * (int(zone[1:3]) * 60 + int(zone[4:6]))
    return _micros(m, 6, off)


def micros_text(us: int) -> str:
    secs, micro = divmod(us, 1_000_000)
    days, rem = divmod(secs, 86400)
    z = days + 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    y += m <= 2
    return f"{y:04d}-{m:02d}-{d:02d}T{rem // 3600:02d}:{rem % 3600 // 60:02d}:{rem % 60:02d}.{micro:06d}Z"


def norm_dec(text: str) -> str:
    """Normalised exact decimal text: no exponent, no trailing fractional zeros, '-0' -> '0'."""
    neg = text.startswith("-")
    body = text.lstrip("+-")
    if "." in body:
        ip, fp = body.split(".")
        fp = fp.rstrip("0")
    else:
        ip, fp = body, ""
    ip = ip.lstrip("0") or "0"
    out = ip + ("." + fp if fp else "")
    if out == "0":
        return "0"
    return ("-" if neg else "") + out


def _frac_digits(lit: str) -> int:
    return len(lit.split(".")[1]) if "." in lit else 0


def num_ok(v: Any, max_dp: int = 6) -> bool:
    if not isinstance(v, Num):
        return False
    lit = v.literal
    if "e" in lit or "E" in lit:
        return False
    return _frac_digits(lit) <= max_dp


def _forbidden_in_keys(obj: Any, tokens: tuple[str, ...]) -> bool:
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if any(t in kl for t in tokens) or _forbidden_in_keys(v, tokens):
                return True
    elif isinstance(obj, list):
        return any(_forbidden_in_keys(x, tokens) for x in obj)
    return False


def _latest_key(inst: str, tf: str) -> str:
    return f"hermes:candles:{inst}:{tf}:latest:v1"


# ------------------------------------------------------------------ wire level
def _candle_violations(c: Any, case_inst: str, case_tf: str, read_key: str, v: set) -> None:
    if not isinstance(c, dict):
        v.add("CP1-W03")
        return
    prov = c.get("provenance")
    data = c.get("data")
    if (c.get("schema_version") != "v1" or c.get("contract_version") != "v1"
            or c.get("contract") != "hermes.candles.latest"):
        v.add("CP1-W01")
    if c.get("service", "HERMES") != "HERMES" or (isinstance(prov, dict) and prov.get("publisher", "HERMES") != "HERMES"):
        v.add("CP1-W02")
    if not CANDLE_ENV_KEYS <= set(c) or not isinstance(data, dict) or not isinstance(prov, dict):
        v.add("CP1-W03")
    else:
        if not CANDLE_DATA_KEYS <= set(data):
            v.add("CP1-W03")
        if c["status"] not in STATUSES or c["freshness_state"] not in FRESHNESS:
            v.add("CP1-W03")
        if not isinstance(c["reason_codes"], list):
            v.add("CP1-W03")
    if _forbidden_in_keys(c, CANDLE_FORBIDDEN):
        v.add("CP1-W05")
    if set(c) - CANDLE_ENV_KEYS - {"history"}:
        v.add("CP1-W04")
    if isinstance(data, dict) and set(data) - CANDLE_DATA_KEYS:
        v.add("CP1-W04")
    if isinstance(prov, dict) and set(prov) - CANDLE_PROV_KEYS:
        v.add("CP1-W04")
    if "history" in c and (not isinstance(c["history"], dict) or set(c["history"]) != CANDLE_HIST_KEYS):
        v.add("CP1-W04")
    if not isinstance(data, dict):
        return
    tf = data.get("timeframe")
    inst = data.get("instrument")
    if data.get("contract_version") != "v1":
        v.add("CP1-W01")
    if data.get("publisher") != "HERMES":
        v.add("CP1-W02")
    if tf not in TF_SECONDS:
        v.add("CP1-W08")
    if not isinstance(inst, str) or not INSTR_RE.match(inst) or inst in INSTR_DENY:
        v.add("CP1-W10")
    if inst != case_inst or tf != case_tf or c.get("key") != _latest_key(str(inst), str(tf)):
        v.add("CP1-W09")
    ts = ms_to_micros(data.get("timestamp_utc"))
    if read_key != _latest_key(case_inst, case_tf):
        want = f"hermes:candles:{case_inst}:{case_tf}:history:v1:"
        ok = read_key.startswith(want) and read_key[len(want):].isdigit()
        if not ok or (ts is not None and int(read_key[len(want):]) * 1_000_000 != ts):
            v.add("CP1-W09")
    insts = [c.get("generated_at_utc"), c.get("valid_until_utc"), data.get("timestamp_utc")]
    if isinstance(prov, dict):
        insts.append(prov.get("generated_at_utc"))
    if isinstance(c.get("history"), dict):
        insts += [c["history"].get("backfill_inserted_at_utc"), c["history"].get("source_timestamp_utc")]
    if any(ms_to_micros(x) is None for x in insts):
        v.add("CP1-W07")
    status = c.get("status")
    if status not in ("NO_SOURCE_DATA", "MARKET_CLOSED"):
        for f in ("open", "high", "low", "close", "volume"):
            if not num_ok(data.get(f)):
                v.add("CP1-W06")
    if status in ("NO_SOURCE_DATA", "MARKET_CLOSED", "PUBLISH_DISABLED"):
        v.add("CP1-S03")
    if status == "FORMING" or data.get("is_closed") is not True:
        v.add("CP1-S01")
    sc, ec = data.get("source_count"), data.get("expected_source_count")
    if (status in ("SOURCE_INCOMPLETE", "GAP_DETECTED") or data.get("gap_state") != "NONE"
            or (isinstance(sc, Num) and isinstance(ec, Num) and ec and sc < ec)):
        v.add("CP1-S02")
    if c.get("freshness_state") in ("STALE", "UNAVAILABLE") or status == "STALE":
        v.add("CP1-S04")


def _indicator_violations(i: Any, case_inst: str, case_tf: str, v: set) -> None:
    if not isinstance(i, dict):
        v.add("CP1-W03")
        return
    if (i.get("schema_version") != "v1" or i.get("contract_version") != "v1"
            or i.get("source_candle_contract") != "v1" or i.get("indicator_set_version") != "v1"):
        v.add("CP1-W01")
    if i.get("publisher", "HERMES") != "HERMES":
        v.add("CP1-W02")
    inds = i.get("indicators")
    methods = i.get("methods")
    if (not IND_ENV_KEYS <= set(i) or not isinstance(inds, dict) or not inds
            or not isinstance(methods, dict) or i.get("deterministic_only") is not True
            or i.get("freshness_state") not in FRESHNESS):
        v.add("CP1-W03")
    if _forbidden_in_keys(i, IND_FORBIDDEN):
        v.add("CP1-W05")
    if set(i) - IND_ENV_KEYS - {"history"}:
        v.add("CP1-W04")
    if "history" in i and (not isinstance(i["history"], dict) or set(i["history"]) != IND_HIST_KEYS):
        v.add("CP1-W04")
    if i.get("instrument") != case_inst or i.get("timeframe") != case_tf:
        v.add("CP1-W09")
    insts = [i.get("generated_at_utc"), i.get("value_open_time_utc")]
    if isinstance(i.get("history"), dict):
        insts += [i["history"].get("published_at_utc"), i["history"].get("source_timestamp_utc")]
    if any(ms_to_micros(x) is None for x in insts):
        v.add("CP1-W07")
    if isinstance(inds, dict):
        for name, val in inds.items():
            if val is not None and not num_ok(val):
                v.add("CP1-W06")
            if name not in IND_NAMES and not any(t in name.lower() for t in IND_FORBIDDEN):
                v.add("CP1-J03")
        if isinstance(methods, dict):
            for name in inds:
                fam = name.split("_")[0]
                key = {"ema": "ema_method", "rsi": "rsi_method", "atr": "atr_method"}.get(fam)
                if key and methods.get(key) != PINNED_METHODS[key]:
                    v.add("CP1-J04")


def _dec_text(n: Num) -> str:
    return norm_dec(n.literal)


def _build_frames(case: dict, ctx: dict) -> list[dict]:
    frames = []
    ingested = lenient_micros(ctx["ingested_at_utc"])
    for bar in case["wire"]["bars"]:
        c, i = bar["candle"], bar["indicator"]
        d = c["data"]
        observed = max(ms_to_micros(c["generated_at_utc"]), ms_to_micros(i["generated_at_utc"]))
        inds = {}
        for name in FRAME_IND:
            raw = i["indicators"].get(name) if name not in ("regime", "session") else None
            inds[name] = None if raw is None else _dec_text(raw)
        frames.append({
            "instrument": d["instrument"],
            "timeframe": d["timeframe"],
            "timestamp_utc": micros_text(ms_to_micros(d["timestamp_utc"])),
            "candle": {
                "open": _dec_text(d["open"]), "high": _dec_text(d["high"]),
                "low": _dec_text(d["low"]), "close": _dec_text(d["close"]),
                "volume": _dec_text(d["volume"]), "complete": True, "source": "hermes",
            },
            "indicators": inds,
            "provenance": {
                "source": "hermes", "schema_version": FRAME_SCHEMA_VERSION,
                "observed_at_utc": micros_text(observed),
                "ingested_at_utc": micros_text(ingested),
            },
        })
    return frames


def pick(violations: set) -> Optional[str]:
    for code in ORDER:
        if code in violations:
            return code
    return None


def check_wire(case: dict) -> tuple[str, Optional[str], Optional[list[dict]]]:
    ctx = case["context"]
    wire = case["wire"]
    inst, tf = wire["instrument"], wire["timeframe"]
    v: set = set()
    if tf not in TF_SECONDS:
        v.add("CP1-W08")
    if not INSTR_RE.match(inst) or inst in INSTR_DENY:
        v.add("CP1-W10")
    prev_ts = None
    for bar in wire["bars"]:
        c, i = bar["candle"], bar["indicator"]
        if c is None:
            v.add("CP1-H01")
        else:
            _candle_violations(c, inst, tf, bar["candle_key"], v)
        if i is None:
            v.add("CP1-J01")
        else:
            _indicator_violations(i, inst, tf, v)
        if c is not None and i is not None and isinstance(c.get("data"), dict) and isinstance(i, dict):
            if i.get("value_open_time_utc") != c["data"].get("timestamp_utc"):
                v.add("CP1-J02")
        if c is not None and isinstance(c.get("data"), dict):
            ts = ms_to_micros(c["data"].get("timestamp_utc"))
            if ts is not None:
                if prev_ts is not None and ts <= prev_ts:
                    v.add("CP1-H02")
                prev_ts = ts
    if wire.get("latest_candle") is not None and wire["bars"]:
        newest = ms_to_micros(wire["latest_candle"]["data"]["timestamp_utc"])
        last = prev_ts
        if newest is not None and last is not None and newest < last:
            v.add("CP1-H03")
    code = pick(v)
    if code:
        return "REJECT", code, None
    frames = _build_frames(case, ctx)
    fcode = check_frames_list(frames, ctx, mode="adapter")
    if fcode:
        return "REJECT", fcode, None
    return "ACCEPT", None, frames


# ------------------------------------------------------------------ frame level
def _dec_val(text: str) -> tuple[int, int]:
    """(unscaled, scale) of a decimal text, for exact comparisons without Decimal."""
    neg = text.startswith("-")
    body = text.lstrip("-")
    if "." in body:
        ip, fp = body.split(".")
    else:
        ip, fp = body, ""
    n = int(ip + fp)
    return (-n if neg else n, len(fp))


def _cmp(a: str, b: str) -> int:
    (an, asc), (bn, bsc) = _dec_val(a), _dec_val(b)
    s = max(asc, bsc)
    x, y = an * 10 ** (s - asc), bn * 10 ** (s - bsc)
    return (x > y) - (x < y)


def _is_dec(x: Any) -> bool:
    return isinstance(x, str) and bool(DEC_RE.match(x))


def check_frames_list(frames: list[dict], ctx: dict, mode: str) -> Optional[str]:
    """mode: 'adapter' (provider obligations, strict forms) or 'consumer' (HELIOS-side, adds policy rules)."""
    v: set = set()
    strict = mode == "adapter"
    seen = []
    for f in frames:
        cand, ind, prov = f.get("candle"), f.get("indicators"), f.get("provenance")
        if not (isinstance(cand, dict) and isinstance(ind, dict) and isinstance(prov, dict)):
            v.add("CP1-F17")
            continue
        if set(f) - {"instrument", "timeframe", "timestamp_utc", "candle", "indicators", "provenance"}:
            v.add("CP1-F02")
        if set(cand) - {"open", "high", "low", "close", "volume", "complete", "source"}:
            v.add("CP1-F02")
        if {"open", "high", "low", "close", "volume", "complete", "source"} - set(cand):
            v.add("CP1-F17")
        if set(ind) - set(FRAME_IND):
            v.add("CP1-F02")
        if set(prov) != {"source", "schema_version", "observed_at_utc", "ingested_at_utc"}:
            v.add("CP1-F02" if set(prov) - {"source", "schema_version", "observed_at_utc", "ingested_at_utc"} else "CP1-F17")
        tfc = f.get("timeframe")
        tfn = TF_ALT.get(str(tfc).upper(), str(tfc).upper()) if not strict else tfc
        if tfn not in TF_SECONDS:
            v.add("CP1-F08")
        # numbers: decimal text only
        nums = [cand.get(k) for k in ("open", "high", "low", "close", "volume")]
        nums += [ind.get(k) for k in FRAME_IND[:6] if ind.get(k) is not None]
        if any(not _is_dec(x) for x in nums):
            v.add("CP1-F01")
        elif strict and any(norm_dec(x) != x for x in nums):
            v.add("CP1-F01")
        ts_field = f.get("timestamp_utc")
        pts = [ts_field, prov.get("observed_at_utc"), prov.get("ingested_at_utc")]
        if strict:
            ints = [(_micros(MICRO_RE.match(p), 6) if isinstance(p, str) and MICRO_RE.match(p) else None) for p in pts]
        else:
            ints = [lenient_micros(p) for p in pts]
        if any(x is None for x in ints):
            v.add("CP1-F06")
        ts, obs, ing = ints
        if ts is not None and tfn in TF_SECONDS:
            sec_ok = ts % 60_000_000 == 0
            minute = (ts // 60_000_000) % 60
            if not sec_ok:
                v.add("CP1-F07")
            elif TF_SECONDS[tfn] < 3600:
                if minute % (TF_SECONDS[tfn] // 60) != 0:
                    v.add("CP1-F07")
            elif minute != 0:
                v.add("CP1-F07")
        if all(_is_dec(cand.get(k)) for k in ("open", "high", "low", "close")):
            o, h, l, c = (cand[k] for k in ("open", "high", "low", "close"))
            if any(_cmp(x, "0") <= 0 for x in (o, h, l, c)) or _cmp(h, l) < 0 or \
               _cmp(h, o) < 0 or _cmp(h, c) < 0 or _cmp(l, o) > 0 or _cmp(l, c) > 0:
                v.add("CP1-F03")
        if _is_dec(cand.get("volume")) and _cmp(cand["volume"], "0") < 0:
            v.add("CP1-F04")
        r, a = ind.get("rsi_14"), ind.get("atr_14")
        if (_is_dec(r) and (_cmp(r, "0") < 0 or _cmp(r, "100") > 0)) or (_is_dec(a) and _cmp(a, "0") < 0):
            v.add("CP1-F05")
        if obs is not None and ing is not None and ing < obs:
            v.add("CP1-F09")
        sv = prov.get("schema_version")
        accepted = ctx.get("accepted_frame_schema_versions")
        if not isinstance(sv, str) or "/" not in sv or (accepted is not None and sv not in accepted):
            v.add("CP1-F13")
        if strict and (ind.get("regime") is not None or ind.get("session") is not None):
            v.add("CP1-F20")
        seen.append((f.get("instrument"), tfn, ts, cand.get("complete"), ind))
    # window rules
    for k in range(1, len(seen)):
        if seen[k][0] != seen[0][0] or seen[k][1] != seen[0][1]:
            v.add("CP1-F10")
        t0, t1 = seen[k - 1][2], seen[k][2]
        if t0 is not None and t1 is not None:
            if t1 == t0:
                v.add("CP1-F11")
            elif t1 < t0:
                v.add("CP1-F12")
    if mode == "consumer" and seen:
        last = seen[-1]
        for name in ctx.get("required_indicators", []):
            if last[4].get(name) is None:
                v.add("CP1-F16")
        pol = ctx.get("freshness")
        now = lenient_micros(ctx.get("now_utc"))
        if pol and now is not None and last[2] is not None and last[1] in TF_SECONDS:
            from fractions import Fraction
            dur = TF_SECONDS[last[1]] * 1_000_000
            close = last[2] + dur
            age = now - close
            skew = int(pol["clock_skew_tolerance_seconds"]) * 1_000_000
            if -age > dur + skew:
                v.add("CP1-F19")
            else:
                max_age = Fraction(dur) * Fraction(str(pol["max_age_multiplier"])) + int(pol["grace_seconds"]) * 1_000_000
                if max(age, 0) > max_age:
                    v.add("CP1-F14")
            if last[3] is not True and not pol.get("allow_incomplete_frames", False):
                v.add("CP1-F15")
    return pick(v)


def doc_to_frames(doc: dict) -> tuple[list[dict], Optional[str]]:
    """Normalise a HELIOS-format fixture document into MarketFactFrame-shaped dicts.

    Returns (frames, early_code). early_code is set for document-level defects (F18/F02/F17).
    """
    if doc.get("fixture_schema_version") != "helios.hermes_fixture/1.0.0":
        return [], "CP1-F18"
    allowed = {"fixture_schema_version", "fixture_id", "description", "instrument", "timeframe",
               "fact_schema_version", "source", "reference_now_utc", "frames", "expectations"}
    if set(doc) - allowed:
        return [], "CP1-F02"
    out = []
    for fr in doc["frames"]:
        fa = {"timestamp_utc", "candle", "indicators", "observed_at_utc", "ingested_at_utc",
              "instrument", "timeframe", "source", "fact_schema_version"}
        if set(fr) - fa:
            return [], "CP1-F02"
        out.append({
            "instrument": fr.get("instrument", doc["instrument"]),
            "timeframe": fr.get("timeframe", doc["timeframe"]),
            "timestamp_utc": fr["timestamp_utc"],
            "candle": fr["candle"],
            "indicators": fr["indicators"],
            "provenance": {
                "source": fr.get("source", doc["source"]),
                "schema_version": fr.get("fact_schema_version", doc["fact_schema_version"]),
                "observed_at_utc": fr["observed_at_utc"],
                "ingested_at_utc": fr["ingested_at_utc"],
            },
        })
    return out, None


def check_frame_case(case: dict) -> tuple[str, Optional[str], None]:
    if "frames" in case:
        code = check_frames_list(case["frames"], dict(case["context"]), mode=case.get("mode", "consumer"))
        return ("REJECT", code, None) if code else ("ACCEPT", None, None)
    frames, early = doc_to_frames(case["document"])
    if early:
        return "REJECT", early, None
    ctx = dict(case["context"])
    ctx.setdefault("now_utc", case["document"].get("reference_now_utc"))
    code = check_frames_list(frames, ctx, mode=case.get("mode", "consumer"))
    return ("REJECT", code, None) if code else ("ACCEPT", None, None)


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def check_case(case: dict) -> tuple[str, Optional[str], Optional[list[dict]]]:
    return check_wire(case) if case["level"] == "wire" else check_frame_case(case)

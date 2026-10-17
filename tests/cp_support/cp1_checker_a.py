"""CP-1 checker A: JSON Schema (jsonschema) for structure plus datetime/Decimal rules.

Structure comes from the three schema files under schema/ (each constraint carries an
x-code* annotation naming its CP-1 rejection code). Rules a schema cannot express are
implemented here with datetime and Decimal arithmetic. It shares no rule code with
checker B; the verdict policy (lowest ordinal in the rejection matrix wins) is restated
from PACKAGE.md section 7.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from fractions import Fraction
from typing import Any, Optional

import jsonschema

from .cp_common import CP1_DIR, Num, plain

SCHEMA_DIR = CP1_DIR / "schema"


def _load(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


CANDLE_SCHEMA = _load("hermes-candle-envelope.v1.schema.json")
IND_SCHEMA = _load("hermes-indicator-envelope.v1.schema.json")
FRAME_SCHEMA = _load("helios-market-fact-frame.schema.json")

RANK = [
    "CP1-W01", "CP1-W02", "CP1-W03", "CP1-W05", "CP1-W04", "CP1-W08", "CP1-W10", "CP1-W09",
    "CP1-W07", "CP1-W06", "CP1-S03", "CP1-S01", "CP1-S02", "CP1-S04", "CP1-H01", "CP1-J01", "CP1-J02",
    "CP1-J03", "CP1-J04", "CP1-H02", "CP1-H03",
    "CP1-F18", "CP1-F02", "CP1-F17", "CP1-F01", "CP1-F08", "CP1-F06", "CP1-F07", "CP1-F03",
    "CP1-F04", "CP1-F05", "CP1-F09", "CP1-F10", "CP1-F12", "CP1-F11", "CP1-F13", "CP1-F16",
    "CP1-F20", "CP1-F19", "CP1-F14", "CP1-F15",
]
TFS = {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440}  # minutes
TF_FORMS = {"1M": "M1", "5M": "M5", "15M": "M15", "1H": "H1", "4H": "H4", "1D": "D1"}
IND_KNOWN = (
    {f"ema_{n}" for n in (9, 12, 21, 26, 50, 200)}
    | {"rsi_14", "atr_14", "adx_14", "adx_plus_di_14", "adx_minus_di_14"}
    | {f"bollinger_{x}_20_2" for x in ("upper", "middle", "lower")}
)
FORBID_IND = ("regime", "regime_confidence", "risk", "order_block", "liquidity", "decision",
              "trade", "gate", "password", "secret", "credential", "acl", "noauth")
METHOD_PIN = {"ema": ("ema_method", "STANDARD_2_OVER_N_PLUS_1_SMA_SEED"),
              "rsi": ("rsi_method", "CUTLER_SMA_14"), "atr": ("atr_method", "SMA_14")}
FRAME_INDS = ("rsi_14", "ema_9", "ema_21", "ema_50", "ema_200", "atr_14", "regime", "session")
SCHEMA_V = "hermes.market_fact/1.0.0"


def _walk_code(error: "jsonschema.ValidationError", root: dict) -> Optional[str]:
    node: Any = root
    code = root.get("x-code")
    holder = root
    for seg in error.absolute_schema_path:
        if isinstance(node, dict) and seg in node:
            node = node[seg]
        elif isinstance(node, list) and isinstance(seg, int):
            node = node[seg]
        else:
            break
        if isinstance(node, dict):
            holder = node
            if "x-code" in node:
                code = node["x-code"]
    # keyword level annotations live on the object that carries the keyword
    parent = root
    n2: Any = root
    path = list(error.absolute_schema_path)[:-1]
    for seg in path:
        if isinstance(n2, dict) and seg in n2:
            n2 = n2[seg]
        elif isinstance(n2, list) and isinstance(seg, int):
            n2 = n2[seg]
        if isinstance(n2, dict):
            parent = n2
    if error.validator == "required" and "x-code-required" in parent:
        return parent["x-code-required"]
    if error.validator == "additionalProperties" and "x-code-additional" in parent:
        return parent["x-code-additional"]
    return code


def _schema_codes(instance: Any, schema: dict) -> set:
    validator = jsonschema.Draft202012Validator(schema)
    out = set()
    for err in validator.iter_errors(plain(instance)):
        code = _walk_code(err, schema)
        if code:
            out.add(code)
    return out


def _dt(text: Any, frac: int) -> Optional[datetime]:
    if not isinstance(text, str):
        return None
    pat = r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\." + r"(\d{%d})Z$" % frac
    m = re.match(pat, text)
    if not m:
        return None
    y, mo, d, h, mi, s, f = (int(x) for x in m.groups())
    try:
        return datetime(y, mo, d, h, mi, s, f * (10 ** (6 - frac)), tzinfo=timezone.utc)
    except ValueError:
        return None


def _fmt_micro(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def _canon_dec(value: Decimal) -> str:
    sign, digits, exp = value.as_tuple()
    if not any(digits):
        return "0"
    ds = list(digits)
    while exp < 0 and ds[-1] == 0:
        ds.pop()
        exp += 1
    return format(Decimal((sign, tuple(ds), exp)), "f")


def _num_form_ok(value: Any) -> bool:
    if not isinstance(value, Num):
        return False
    lit = value.literal.lower()
    if "e" in lit:
        return False
    exp = value.as_tuple().exponent
    return isinstance(exp, int) and exp >= -6


def _wire_candle(c: Any, inst: str, tf: str, read_key: str, v: set) -> None:
    if not isinstance(c, dict):
        v.add("CP1-W03")
        return
    v |= _schema_codes(c, CANDLE_SCHEMA)
    data = c.get("data")
    if not isinstance(data, dict):
        return
    ts = _dt(data.get("timestamp_utc"), 3)
    stamps = [c.get("generated_at_utc"), c.get("valid_until_utc"), data.get("timestamp_utc")]
    if isinstance(c.get("provenance"), dict):
        stamps.append(c["provenance"].get("generated_at_utc"))
    if isinstance(c.get("history"), dict):
        stamps += [c["history"].get("backfill_inserted_at_utc"), c["history"].get("source_timestamp_utc")]
    if any(_dt(s, 3) is None for s in stamps):
        v.add("CP1-W07")
    status = c.get("status")
    if status not in ("NO_SOURCE_DATA", "MARKET_CLOSED"):
        for f in ("open", "high", "low", "close", "volume"):
            if not _num_form_ok(data.get(f)):
                v.add("CP1-W06")
    if data.get("instrument") != inst or data.get("timeframe") != tf:
        v.add("CP1-W09")
    if c.get("key") != f"hermes:candles:{data.get('instrument')}:{data.get('timeframe')}:latest:v1":
        v.add("CP1-W09")
    latest = f"hermes:candles:{inst}:{tf}:latest:v1"
    if read_key != latest:
        head = f"hermes:candles:{inst}:{tf}:history:v1:"
        tail = read_key[len(head):] if read_key.startswith(head) else None
        if tail is None or not tail.isdigit():
            v.add("CP1-W09")
        elif ts is not None and int(ts.timestamp()) != int(tail):
            v.add("CP1-W09")
    if status in ("NO_SOURCE_DATA", "MARKET_CLOSED", "PUBLISH_DISABLED"):
        v.add("CP1-S03")
    if status == "FORMING" or data.get("is_closed") is not True:
        v.add("CP1-S01")
    sc, ec = data.get("source_count"), data.get("expected_source_count")
    short = isinstance(sc, Num) and isinstance(ec, Num) and Decimal(ec) != 0 and Decimal(sc) < Decimal(ec)
    if status in ("SOURCE_INCOMPLETE", "GAP_DETECTED") or data.get("gap_state") != "NONE" or short:
        v.add("CP1-S02")
    if c.get("freshness_state") in ("STALE", "UNAVAILABLE") or status == "STALE":
        v.add("CP1-S04")


def _wire_indicator(i: Any, v: set) -> None:
    if not isinstance(i, dict):
        v.add("CP1-W03")
        return
    v |= _schema_codes(i, IND_SCHEMA)
    for k in ("generated_at_utc", "value_open_time_utc"):
        if _dt(i.get(k), 3) is None:
            v.add("CP1-W07")
    if isinstance(i.get("history"), dict):
        for k in ("published_at_utc", "source_timestamp_utc"):
            if _dt(i["history"].get(k), 3) is None:
                v.add("CP1-W07")
    inds, methods = i.get("indicators"), i.get("methods")
    if isinstance(inds, dict):
        for name, val in inds.items():
            if val is not None and not _num_form_ok(val):
                v.add("CP1-W06")
            if name not in IND_KNOWN and not any(t in name.lower() for t in FORBID_IND):
                v.add("CP1-J03")
            fam = name.split("_")[0]
            if fam in METHOD_PIN and isinstance(methods, dict):
                key, want = METHOD_PIN[fam]
                if methods.get(key) != want:
                    v.add("CP1-J04")


def _pick(v: set) -> Optional[str]:
    ranked = [c for c in RANK if c in v]
    return ranked[0] if ranked else None


def _frames_from_wire(case: dict) -> list[dict]:
    ing = _parse_any(case["context"]["ingested_at_utc"])
    out = []
    for bar in case["wire"]["bars"]:
        c, i = bar["candle"], bar["indicator"]
        d = c["data"]
        obs = max(_dt(c["generated_at_utc"], 3), _dt(i["generated_at_utc"], 3))
        inds = {}
        for name in FRAME_INDS:
            raw = None if name in ("regime", "session") else i["indicators"].get(name)
            inds[name] = None if raw is None else _canon_dec(Decimal(raw.literal))
        out.append({
            "instrument": d["instrument"], "timeframe": d["timeframe"],
            "timestamp_utc": _fmt_micro(_dt(d["timestamp_utc"], 3)),
            "candle": {k: _canon_dec(Decimal(d[k].literal)) for k in ("open", "high", "low", "close", "volume")}
                      | {"complete": True, "source": "hermes"},
            "indicators": inds,
            "provenance": {"source": "hermes", "schema_version": SCHEMA_V,
                           "observed_at_utc": _fmt_micro(obs), "ingested_at_utc": _fmt_micro(ing)},
        })
    return out


def _parse_any(text: Any) -> Optional[datetime]:
    if not isinstance(text, str):
        return None
    m = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})?$", text.strip())
    if not m or not m.group(3):
        return None
    base = m.group(1)
    frac = (m.group(2) or ".")[1:]
    try:
        dt = datetime.strptime(base, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None
    dt = dt.replace(microsecond=int((frac + "000000")[:6]) if frac else 0)
    zone = m.group(3)
    if zone == "Z":
        return dt.replace(tzinfo=timezone.utc)
    sign = 1 if zone[0] == "+" else -1
    off = timedelta(hours=int(zone[1:3]), minutes=int(zone[4:6])) * sign
    return (dt - off).replace(tzinfo=timezone.utc)


def check_wire(case: dict):
    inst, tf = case["wire"]["instrument"], case["wire"]["timeframe"]
    v: set = set()
    if tf not in TFS:
        v.add("CP1-W08")
    if not re.match(r"^[A-Z0-9]{2,10}(_[A-Z0-9]{2,10})?$", inst) or inst == "XAUUSD":
        v.add("CP1-W10")
    stamps = []
    for bar in case["wire"]["bars"]:
        c, i = bar["candle"], bar["indicator"]
        if c is None:
            v.add("CP1-H01")
        else:
            _wire_candle(c, inst, tf, bar["candle_key"], v)
        if i is None:
            v.add("CP1-J01")
        else:
            _wire_indicator(i, v)
        if c is not None and i is not None and isinstance(c.get("data"), dict) and isinstance(i, dict):
            if i.get("value_open_time_utc") != c["data"].get("timestamp_utc"):
                v.add("CP1-J02")
        if c is not None and isinstance(c.get("data"), dict):
            t = _dt(c["data"].get("timestamp_utc"), 3)
            if t is not None:
                stamps.append(t)
    if any(b <= a for a, b in zip(stamps, stamps[1:])):
        v.add("CP1-H02")
    lc = case["wire"].get("latest_candle")
    if lc is not None and stamps:
        lt = _dt(lc["data"]["timestamp_utc"], 3)
        if lt is not None and lt < stamps[-1]:
            v.add("CP1-H03")
    code = _pick(v)
    if code:
        return "REJECT", code, None
    frames = _frames_from_wire(case)
    fcode = check_frames_list(frames, case["context"], "adapter")
    return ("REJECT", fcode, None) if fcode else ("ACCEPT", None, frames)


def check_frames_list(frames: list[dict], ctx: dict, mode: str) -> Optional[str]:
    v: set = set()
    strict = mode == "adapter"
    rows = []
    for f in frames:
        v |= _schema_codes(f, FRAME_SCHEMA)
        if not isinstance(f.get("candle"), dict) or not isinstance(f.get("provenance"), dict) \
                or not isinstance(f.get("indicators"), dict):
            continue
        cand, ind, prov = f["candle"], f["indicators"], f["provenance"]
        tf = f.get("timeframe")
        key = tf if strict else (TF_FORMS.get(str(tf).upper(), str(tf).upper()))
        if key not in TFS:
            v.add("CP1-F08")
        decs = [cand.get(k) for k in ("open", "high", "low", "close", "volume")]
        decs += [ind.get(k) for k in FRAME_INDS[:6] if ind.get(k) is not None]
        pat = re.compile(r"^-?\d+(\.\d+)?$")
        if strict and all(isinstance(x, str) and pat.match(x) for x in decs):
            if any(_canon_dec(Decimal(x)) != x for x in decs):
                v.add("CP1-F01")
        if strict:
            ts = _dt(f.get("timestamp_utc"), 6)
            ob = _dt(prov.get("observed_at_utc"), 6)
            ig = _dt(prov.get("ingested_at_utc"), 6)
            if None in (ts, ob, ig):
                v.add("CP1-F06")
            if ind.get("regime") is not None or ind.get("session") is not None:
                v.add("CP1-F20")
        else:
            ts, ob, ig = (_parse_any(f.get("timestamp_utc")), _parse_any(prov.get("observed_at_utc")),
                          _parse_any(prov.get("ingested_at_utc")))
            if None in (ts, ob, ig):
                v.add("CP1-F06")
        if ts is not None and key in TFS:
            minutes = TFS[key]
            if ts.second or ts.microsecond:
                v.add("CP1-F07")
            elif minutes < 60:
                if ts.minute % minutes:
                    v.add("CP1-F07")
            elif ts.minute:
                v.add("CP1-F07")
        try:
            o, h, l, c = (Decimal(cand[k]) for k in ("open", "high", "low", "close"))
            if min(o, h, l, c) <= 0 or h < l or h < max(o, c) or l > min(o, c):
                v.add("CP1-F03")
            if Decimal(cand["volume"]) < 0:
                v.add("CP1-F04")
        except Exception:
            pass
        try:
            if ind.get("rsi_14") is not None and not (Decimal(0) <= Decimal(ind["rsi_14"]) <= Decimal(100)):
                v.add("CP1-F05")
            if ind.get("atr_14") is not None and Decimal(ind["atr_14"]) < 0:
                v.add("CP1-F05")
        except Exception:
            pass
        if ob is not None and ig is not None and ig < ob:
            v.add("CP1-F09")
        accepted = ctx.get("accepted_frame_schema_versions")
        sv = prov.get("schema_version")
        if accepted is not None and sv not in accepted:
            v.add("CP1-F13")
        rows.append((f.get("instrument"), key, ts, cand.get("complete"), ind))
    for a, b in zip(rows, rows[1:]):
        if a[0] != b[0] or a[1] != b[1]:
            v.add("CP1-F10")
        if a[2] is not None and b[2] is not None:
            if b[2] == a[2]:
                v.add("CP1-F11")
            elif b[2] < a[2]:
                v.add("CP1-F12")
    if mode == "consumer" and rows:
        inst, key, ts, complete, ind = rows[-1]
        for name in ctx.get("required_indicators", []):
            if ind.get(name) is None:
                v.add("CP1-F16")
        pol = ctx.get("freshness")
        now = _parse_any(ctx.get("now_utc"))
        if pol and now is not None and ts is not None and key in TFS:
            dur = timedelta(minutes=TFS[key])
            age = now - (ts + dur)
            skew = timedelta(seconds=int(pol["clock_skew_tolerance_seconds"]))
            if -age > dur + skew:
                v.add("CP1-F19")
            else:
                limit = timedelta(seconds=float(Fraction(dur.total_seconds()) * Fraction(str(pol["max_age_multiplier"]))
                                                + int(pol["grace_seconds"])))
                if max(age, timedelta(0)) > limit:
                    v.add("CP1-F14")
            if complete is not True and not pol.get("allow_incomplete_frames", False):
                v.add("CP1-F15")
    return _pick(v)


def check_frame_case(case: dict):
    if "frames" in case:
        code = check_frames_list(case["frames"], dict(case["context"]), case.get("mode", "consumer"))
        return ("REJECT", code, None) if code else ("ACCEPT", None, None)
    doc = case["document"]
    if doc.get("fixture_schema_version") != "helios.hermes_fixture/1.0.0":
        return "REJECT", "CP1-F18", None
    top = {"fixture_schema_version", "fixture_id", "description", "instrument", "timeframe",
           "fact_schema_version", "source", "reference_now_utc", "frames", "expectations"}
    if set(doc) - top:
        return "REJECT", "CP1-F02", None
    fr_keys = {"timestamp_utc", "candle", "indicators", "observed_at_utc", "ingested_at_utc",
               "instrument", "timeframe", "source", "fact_schema_version"}
    frames = []
    for fr in doc["frames"]:
        if set(fr) - fr_keys:
            return "REJECT", "CP1-F02", None
        frames.append({
            "instrument": fr.get("instrument", doc["instrument"]),
            "timeframe": fr.get("timeframe", doc["timeframe"]),
            "timestamp_utc": fr["timestamp_utc"], "candle": fr["candle"], "indicators": fr["indicators"],
            "provenance": {"source": fr.get("source", doc["source"]),
                           "schema_version": fr.get("fact_schema_version", doc["fact_schema_version"]),
                           "observed_at_utc": fr["observed_at_utc"], "ingested_at_utc": fr["ingested_at_utc"]},
        })
    ctx = dict(case["context"])
    ctx.setdefault("now_utc", doc.get("reference_now_utc"))
    code = check_frames_list(frames, ctx, case.get("mode", "consumer"))
    return ("REJECT", code, None) if code else ("ACCEPT", None, None)


def check_case(case: dict):
    return check_wire(case) if case["level"] == "wire" else check_frame_case(case)

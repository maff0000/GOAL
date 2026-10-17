"""Reference model of the HELIOS-side external adapter's read cycle (tests only).

It is NOT a Redis client: the Redis state is a plain dict supplied by the scenario.
It exists to show that the failure and recovery rules of PACKAGE.md section 8 are
decidable and give one observable outcome per scenario step.
"""

from __future__ import annotations

import copy
from typing import Any, Optional

from . import cp1_checker_b as checker


class Adapter:
    def __init__(self, instrument: str, timeframe: str, window: int, watermark: Optional[int] = None):
        self.instrument, self.timeframe, self.window = instrument, timeframe, int(window)
        self.watermark = None if watermark is None else int(watermark)  # newest open epoch already handed to evaluation (durable)

    def poll(self, redis: dict, records: dict, ingested_at_utc: str, context: dict) -> dict:
        if not redis.get("available", True):
            return {"event": "NO_ACTION", "code": "CP1-R01"}
        index = [int(x) for x in redis["index"]] if redis.get("index") else None
        if not index:
            return {"event": "NO_ACTION", "code": "CP1-R02"}
        epochs = index[-self.window:]  # taken as listed: never re-sorted, never de-duplicated
        present = {int(x) for x in redis["present"]} if "present" in redis else {int(k) for k in records}
        override = redis.get("schema_version_by_epoch", {})
        bars = []
        for e in epochs:
            rec = copy.deepcopy(records[str(e)]) if str(e) in records and e in present else None
            candle = rec["candle"] if rec else None
            indicator = rec["indicator"] if rec else None
            if candle is not None and str(e) in override:
                candle["schema_version"] = override[str(e)]
            bars.append({
                "candle_key": f"hermes:candles:{self.instrument}:{self.timeframe}:history:v1:{e}", "candle": candle,
                "indicator_key": f"hermes:indicators:{self.instrument}:{self.timeframe}:history:v1:{e}",
                "indicator": indicator if (rec and redis.get("indicators_present", True)) else None,
            })
        latest = int(redis["latest_epoch"]) if redis.get("latest_epoch") is not None else None
        latest_candle = None
        if latest is not None and str(latest) in records:
            latest_candle = copy.deepcopy(records[str(latest)]["candle"])
        case = {
            "level": "wire",
            "context": dict(context, ingested_at_utc=ingested_at_utc),
            "wire": {"instrument": self.instrument, "timeframe": self.timeframe, "bars": bars, "latest_candle": latest_candle},
        }
        verdict, code, frames = checker.check_wire(case)
        if verdict == "REJECT":
            return {"event": "REJECT", "code": code}
        newest = epochs[-1]
        if self.watermark is not None and newest <= self.watermark:
            return {"event": "NO_ACTION", "code": "CP1-R03"}
        self.watermark = newest
        return {"event": "EVALUATE", "code": None, "newest_epoch": newest, "frame_count": len(frames)}


def run_scenario(scn: dict, context: dict, loader_records: dict) -> list[dict]:
    adapter = Adapter(scn["instrument"], scn["timeframe"], scn["window"], scn.get("initial_watermark"))
    out = []
    for step in scn["steps"]:
        if step["op"] == "restart":
            kept = adapter.watermark if step["watermark"] == "persist" else None
            adapter = Adapter(scn["instrument"], scn["timeframe"], scn["window"], kept)
            out.append({"event": "RESTART", "watermark_kept": kept is not None})
        else:
            out.append(adapter.poll(step["redis"], loader_records, step["ingested_at_utc"], context))
    return out

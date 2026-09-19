from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TargetMarketQuote:
    event_id: str
    market: str
    selection: str
    odds: float
    ts_ms: int
    status: str = "OPEN"
    line: float | None = None
    source: str = "target"

def normalize_target(payload: dict) -> TargetMarketQuote:
    return TargetMarketQuote(
        event_id=str(payload["event_id"]),
        market=str(payload["market"]),
        selection=str(payload["selection"]),
        odds=float(payload["odds"]),
        ts_ms=int(payload["ts_ms"]),
        status=str(payload.get("status","OPEN")),
        line=payload.get("line"),
        source=str(payload.get("source","target")),
    )

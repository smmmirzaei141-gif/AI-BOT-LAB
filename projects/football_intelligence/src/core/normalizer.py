from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .market import EventRef, MarketQuote, MarketType


@dataclass(frozen=True)
class TeamStats:
    team: str
    matches: int = 0
    goals_for: float = 0.0
    goals_against: float = 0.0
    xg_for: float | None = None
    xg_against: float | None = None
    corners_for: float | None = None
    corners_against: float | None = None
    cards_for: float | None = None
    cards_against: float | None = None
    fouls_for: float | None = None
    fouls_against: float | None = None
    throw_ins_for: float | None = None
    throw_ins_against: float | None = None


@dataclass(frozen=True)
class NormalizedEvent:
    event: EventRef
    stats: tuple[TeamStats, ...] = ()
    quotes: tuple[MarketQuote, ...] = ()


def normalize_quotes(event_id: str, source: str, ts_ms: int, rows: Iterable[dict]) -> tuple[MarketQuote, ...]:
    result: list[MarketQuote] = []
    for row in rows:
        market = MarketType(str(row["market"]).lower())
        odds = float(row["odds"])
        if odds <= 1:
            continue
        result.append(MarketQuote(
            event_id=event_id,
            market=market,
            selection=str(row["selection"]),
            odds=odds,
            source=source,
            ts_ms=ts_ms,
            line=float(row["line"]) if row.get("line") is not None else None,
            market_status=str(row.get("market_status", "open")),
        ))
    return tuple(result)

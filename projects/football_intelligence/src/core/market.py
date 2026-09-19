from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MarketType(str, Enum):
    GOALS = "goals"
    BTTS = "btts"
    RESULT = "1x2"
    DOUBLE_CHANCE = "double_chance"
    CORNERS = "corners"
    CARDS = "cards"
    FOULS = "fouls"
    THROW_INS = "throw_ins"


@dataclass(frozen=True)
class EventRef:
    event_id: str
    home: str
    away: str
    kickoff_ts_ms: int | None = None


@dataclass(frozen=True)
class MarketQuote:
    event_id: str
    market: MarketType
    selection: str
    odds: float
    source: str
    ts_ms: int
    line: float | None = None
    market_status: str = "open"

    def key(self) -> tuple[str, str, str, float | None]:
        return (self.event_id, self.market.value, self.selection, self.line)

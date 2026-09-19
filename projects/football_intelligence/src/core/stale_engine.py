from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from .market import MarketQuote


@dataclass(frozen=True)
class StaleResult:
    key: tuple
    target_odds: float
    reference_odds: float | None
    deviation: float | None
    source_count: int
    stale: bool
    reason: str


def compare_target_to_references(target: MarketQuote, references: list[MarketQuote], min_sources: int = 2, threshold: float = 0.08) -> StaleResult:
    same = [
        q.odds for q in references
        if q.key() == target.key() and q.source != target.source and q.odds > 1
    ]
    if len(same) < min_sources:
        return StaleResult(target.key(), target.odds, None, None, len(same), False, "INSUFFICIENT_REFERENCE_SOURCES")
    ref = median(same)
    deviation = target.odds / ref - 1.0
    stale = deviation >= threshold
    reason = "TARGET_ABOVE_REFERENCE" if stale else "NO_STALE_SIGNAL"
    return StaleResult(target.key(), target.odds, ref, deviation, len(same), stale, reason)

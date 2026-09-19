from __future__ import annotations

from dataclasses import dataclass
from statistics import median


@dataclass(frozen=True)
class OddsSnapshot:
    source: str
    odds: float
    ts_ms: int


@dataclass(frozen=True)
class OddsAnomaly:
    median_odds: float
    current_odds: float
    relative_deviation: float
    sources: int
    suspicious: bool


def detect_outlier(
    current_odds: float,
    snapshots: list[OddsSnapshot],
    threshold: float = 0.15,
) -> OddsAnomaly:
    valid = [x.odds for x in snapshots if x.odds > 1]
    if not valid:
        return OddsAnomaly(0.0, current_odds, 0.0, 0, False)

    med = median(valid)
    deviation = (current_odds / med) - 1.0 if med else 0.0
    return OddsAnomaly(
        median_odds=med,
        current_odds=current_odds,
        relative_deviation=deviation,
        sources=len(valid),
        suspicious=abs(deviation) >= threshold,
    )

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class MarketQuote:
    market: str
    selection: str
    odds: float
    model_probability: float | None = None
    reference_odds: float | None = None


@dataclass(frozen=True)
class ValueResult:
    market: str
    selection: str
    odds: float
    implied_probability: float
    model_probability: float | None
    edge: float | None
    reference_deviation: float | None
    flags: tuple[str, ...]


def implied_probability(decimal_odds: float) -> float:
    if not isfinite(decimal_odds) or decimal_odds <= 1.0:
        raise ValueError("decimal_odds must be > 1")
    return 1.0 / decimal_odds


def evaluate_quote(q: MarketQuote, min_edge: float = 0.04) -> ValueResult:
    implied = implied_probability(q.odds)
    edge = None
    flags: list[str] = []

    if q.model_probability is not None:
        if not 0 < q.model_probability < 1:
            raise ValueError("model_probability must be between 0 and 1")
        edge = q.model_probability - implied
        if edge >= min_edge:
            flags.append("MODEL_VALUE_CANDIDATE")

    deviation = None
    if q.reference_odds is not None and q.reference_odds > 1:
        deviation = (q.odds / q.reference_odds) - 1.0
        if deviation >= 0.15:
            flags.append("ODDS_OUTLIER_HIGH")
        elif deviation <= -0.15:
            flags.append("ODDS_OUTLIER_LOW")

    return ValueResult(
        market=q.market,
        selection=q.selection,
        odds=q.odds,
        implied_probability=implied,
        model_probability=q.model_probability,
        edge=edge,
        reference_deviation=deviation,
        flags=tuple(flags),
    )

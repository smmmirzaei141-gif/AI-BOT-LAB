from __future__ import annotations

from dataclasses import dataclass
from .market import MarketQuote
from .stale_engine import StaleResult
from .value_engine import evaluate_quote


@dataclass(frozen=True)
class Opportunity:
    event_id: str
    market: str
    selection: str
    odds: float
    score: float
    labels: tuple[str, ...]
    explanation: tuple[str, ...]


def score_opportunity(target: MarketQuote, model_probability: float | None, references: list[MarketQuote]) -> Opportunity:
    value = evaluate_quote(
        __import__("core.value_engine", fromlist=["MarketQuote"]).MarketQuote(
            market=target.market.value,
            selection=target.selection,
            odds=target.odds,
            model_probability=model_probability,
        )
    )
    stale = __import__("core.stale_engine", fromlist=["compare_target_to_references"]).compare_target_to_references(target, references)
    labels: list[str] = []
    explanation: list[str] = []
    score = 0.0
    if "MODEL_VALUE_CANDIDATE" in value.flags:
        labels.append("MODEL_VALUE")
        score += min(50.0, max(0.0, (value.edge or 0) * 500))
        explanation.append(f"model edge={value.edge:.3f}")
    if stale.stale:
        labels.append("STALE_ODDS")
        score += min(35.0, stale.deviation * 250 if stale.deviation else 0)
        explanation.append(f"target {target.odds:.2f} vs reference {stale.reference_odds:.2f}")
    if target.market_status != "open":
        labels.append("MARKET_NOT_OPEN")
        score = 0.0
        explanation.append(f"market_status={target.market_status}")
    return Opportunity(target.event_id, target.market.value, target.selection, target.odds, round(score, 2), tuple(labels), tuple(explanation))

from __future__ import annotations

from dataclasses import dataclass
from .opportunity import Opportunity


@dataclass(frozen=True)
class Decision:
    action: str
    confidence: float
    reasons: tuple[str, ...]


def classify(opportunity: Opportunity, min_score: float = 35.0) -> Decision:
    if "MARKET_NOT_OPEN" in opportunity.labels:
        return Decision("IGNORE", 0.0, opportunity.explanation)
    if opportunity.score >= min_score and opportunity.labels:
        return Decision("ALERT", min(1.0, opportunity.score / 100.0), opportunity.explanation)
    return Decision("WATCH", min(1.0, opportunity.score / 100.0), opportunity.explanation)

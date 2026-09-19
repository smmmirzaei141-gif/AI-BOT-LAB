from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelQuote:
    event_id: str
    market: str
    selection: str
    odds: float
    model_probability: float
    implied_probability: float
    edge: float
    label: str

def build(event_id: str, market: str, selection: str, odds: float, probability: float, min_edge: float=0.04) -> ModelQuote:
    if odds <= 1: raise ValueError("odds must be > 1")
    if not 0 <= probability <= 1: raise ValueError("probability must be between 0 and 1")
    implied=1/odds
    edge=probability-implied
    return ModelQuote(event_id,market,selection,odds,probability,implied,edge,"MODEL_VALUE" if edge>=min_edge else "NO_VALUE")

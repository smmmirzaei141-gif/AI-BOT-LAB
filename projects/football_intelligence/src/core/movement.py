from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Movement:
    first: float
    last: float
    change_pct: float
    direction: str

def analyze(first: float, last: float) -> Movement:
    if first <= 1.0 or last <= 1.0: raise ValueError("odds must be > 1")
    pct=(last-first)/first*100
    direction="UP" if pct>0.05 else "DOWN" if pct<-0.05 else "FLAT"
    return Movement(first,last,pct,direction)

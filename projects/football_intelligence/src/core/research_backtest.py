from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BacktestMetrics:
    n: int
    wins: int
    losses: int
    profit: float
    roi: float
    brier: float

def run(rows, min_edge=0.04) -> BacktestMetrics:
    selected=[r for r in rows if float(r["model_probability"])-1/float(r["odds"])>=min_edge]
    profit=0.0; wins=0; brier=0.0
    for r in selected:
        p=float(r["model_probability"]); won=bool(r["won"])
        brier+=(p-(1.0 if won else 0.0))**2
        if won: wins+=1; profit+=float(r["odds"])-1
        else: profit-=1
    n=len(selected)
    return BacktestMetrics(n,wins,n-wins,profit,profit/n if n else 0.0,brier/n if n else 0.0)

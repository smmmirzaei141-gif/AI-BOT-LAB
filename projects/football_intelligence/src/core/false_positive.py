from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FalsePositiveReport:
    selected: int
    wins: int
    losses: int
    false_positive_rate: float
    avg_edge_lost: float

def analyze(rows, min_edge=0.04) -> FalsePositiveReport:
    selected=[r for r in rows if float(r["model_probability"])-1/float(r["odds"])>=min_edge]
    losses=[r for r in selected if not bool(r["won"])]
    edges=[float(r["model_probability"])-1/float(r["odds"]) for r in losses]
    n=len(selected)
    return FalsePositiveReport(n,n-len(losses),len(losses),len(losses)/n if n else 0.0,sum(edges)/len(edges) if edges else 0.0)

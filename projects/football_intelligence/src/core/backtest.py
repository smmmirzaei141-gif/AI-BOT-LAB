from __future__ import annotations
from dataclasses import dataclass
from math import log

@dataclass(frozen=True)
class Settlement:
    predicted_probability: float
    odds: float
    won: bool

@dataclass(frozen=True)
class BacktestReport:
    bets: int
    wins: int
    losses: int
    roi: float
    profit: float
    brier: float
    log_loss: float
    max_drawdown: float

def evaluate(rows: list[Settlement], stake: float = 1.0) -> BacktestReport:
    if not rows:
        return BacktestReport(0,0,0,0.0,0.0,0.0,0.0,0.0)
    profit=0.0; peak=0.0; equity=0.0; max_dd=0.0; brier=0.0; ll=0.0; wins=0
    for r in rows:
        p=min(1-1e-12,max(1e-12,r.predicted_probability))
        y=1.0 if r.won else 0.0
        brier += (p-y)**2
        ll += -(y*log(p)+(1-y)*log(1-p))
        if r.won:
            wins += 1
            profit += stake*(r.odds-1)
        else:
            profit -= stake
        equity += (stake*(r.odds-1) if r.won else -stake)
        peak=max(peak,equity)
        max_dd=max(max_dd,peak-equity)
    n=len(rows)
    return BacktestReport(n,wins,n-wins,profit/(n*stake),profit,brier/n,ll/n,max_dd)

def from_dicts(rows: list[dict], stake: float=1.0) -> BacktestReport:
    return evaluate([Settlement(float(r["predicted_probability"]),float(r["odds"]),bool(r["won"])) for r in rows],stake)

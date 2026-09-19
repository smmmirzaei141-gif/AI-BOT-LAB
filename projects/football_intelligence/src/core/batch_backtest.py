from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class MarketBacktest:
    market: str
    selection: str
    bets: int
    wins: int
    losses: int
    profit: float
    roi: float
    avg_edge: float

def run(cases, evaluator, min_edge=0.04):
    grouped=defaultdict(list)
    for case in cases:
        for row in evaluator(case,min_edge):
            grouped[(row["market"],row["selection"])].append(row)
    out=[]
    for (market,selection),rows in sorted(grouped.items()):
        profit=sum(r["odds"]-1 if r["won"] else -1 for r in rows)
        bets=len(rows)
        out.append(MarketBacktest(market,selection,bets,sum(r["won"] for r in rows),bets-sum(r["won"] for r in rows),profit,profit/bets if bets else 0,sum(r["edge"] for r in rows)/bets if bets else 0))
    return tuple(out)

from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class MarketStats:
    market: str
    bets: int
    wins: int
    losses: int
    profit: float
    roi: float

def summarize(rows):
    groups=defaultdict(list)
    for r in rows: groups[r["market"]].append(r)
    out=[]
    for market, items in groups.items():
        wins=sum(bool(x["won"]) for x in items); bets=len(items)
        profit=sum((float(x["odds"])-1) if x["won"] else -1 for x in items)
        out.append(MarketStats(market,bets,wins,bets-wins,profit,profit/bets if bets else 0.0))
    return sorted(out,key=lambda x:x.market)

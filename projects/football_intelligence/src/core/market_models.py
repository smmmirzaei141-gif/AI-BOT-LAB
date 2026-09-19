from __future__ import annotations
from dataclasses import dataclass
from math import exp, factorial

@dataclass(frozen=True)
class MarketProbabilities:
    over_1_5: float
    over_2_5: float
    over_3_5: float
    btts_yes: float
    home: float
    draw: float
    away: float

def _pmf(k:int, lam:float)->float:
    return exp(-lam)*(lam**k)/factorial(k)

def _pois_leq(k:int, lam:float)->float:
    return sum(_pmf(i,lam) for i in range(k+1))

def estimate(home_xg: float, away_xg: float) -> MarketProbabilities:
    home_xg=max(0.01,float(home_xg)); away_xg=max(0.01,float(away_xg))
    total=home_xg+away_xg
    over=lambda line: 1.0-_pois_leq(int(line),total)
    btts=1-exp(-home_xg)-exp(-away_xg)+exp(-total)
    probs={}
    for h in range(9):
        for a in range(9):
            p=_pmf(h,home_xg)*_pmf(a,away_xg)
            if h>a: probs["home"]=probs.get("home",0)+p
            elif h==a: probs["draw"]=probs.get("draw",0)+p
            else: probs["away"]=probs.get("away",0)+p
    return MarketProbabilities(over(1.5),over(2.5),over(3.5),btts,probs["home"],probs["draw"],probs["away"])

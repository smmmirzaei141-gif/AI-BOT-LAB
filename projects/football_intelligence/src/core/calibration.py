from __future__ import annotations
from dataclasses import dataclass
from math import log

@dataclass(frozen=True)
class CalibrationBin:
    low: float
    high: float
    count: int
    mean_probability: float
    observed_rate: float

def calibration_bins(rows: list[dict], bins: int = 10) -> list[CalibrationBin]:
    bins=max(2,int(bins))
    groups=[[] for _ in range(bins)]
    for r in rows:
        p=min(1.0,max(0.0,float(r["predicted_probability"])))
        y=1.0 if bool(r["won"]) else 0.0
        idx=min(bins-1,int(p*bins))
        groups[idx].append((p,y))
    out=[]
    for i,g in enumerate(groups):
        if not g: continue
        out.append(CalibrationBin(i/bins,(i+1)/bins,len(g),sum(p for p,_ in g)/len(g),sum(y for _,y in g)/len(g)))
    return out

def expected_calibration_error(rows: list[dict], bins: int=10) -> float:
    n=len(rows)
    if not n: return 0.0
    return sum((b.count/n)*abs(b.mean_probability-b.observed_rate) for b in calibration_bins(rows,bins))

def market_breakdown(rows: list[dict]) -> dict[str, dict]:
    out={}
    for r in rows:
        market=str(r.get("market","unknown"))
        out.setdefault(market,[]).append(r)
    return {m: {"count":len(rs),"ece":round(expected_calibration_error(rs),6)} for m,rs in out.items()}

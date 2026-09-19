from __future__ import annotations
from dataclasses import dataclass
from math import log

@dataclass(frozen=True)
class CalibrationBin:
    lower: float
    upper: float
    count: int
    predicted: float
    observed: float
    gap: float

@dataclass(frozen=True)
class CalibrationReport:
    bins: tuple[CalibrationBin, ...]
    brier: float
    log_loss: float

def evaluate(rows, bins=10, eps=1e-9) -> CalibrationReport:
    if bins < 1: raise ValueError("bins must be >= 1")
    buckets=[[] for _ in range(bins)]
    brier=logloss=0.0
    for r in rows:
        p=min(1-eps,max(eps,float(r["model_probability"])))
        y=1.0 if bool(r["won"]) else 0.0
        idx=min(bins-1,int(p*bins)); buckets[idx].append((p,y))
        brier+=(p-y)**2
        logloss-=y*log(p)+(1-y)*log(1-p)
    out=[]
    for i,b in enumerate(buckets):
        if not b: continue
        pred=sum(x[0] for x in b)/len(b); obs=sum(x[1] for x in b)/len(b)
        out.append(CalibrationBin(i/bins,(i+1)/bins,len(b),pred,obs,obs-pred))
    n=sum(len(b) for b in buckets)
    return CalibrationReport(tuple(out),brier/n if n else 0.0,logloss/n if n else 0.0)

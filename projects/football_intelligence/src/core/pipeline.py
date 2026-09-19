from __future__ import annotations
from .model_quote import build

def score_quotes(event_id, market_quotes, probabilities, min_edge=0.04):
    out=[]
    for q in market_quotes:
        key=(q["market"],q["selection"])
        p=probabilities.get(key)
        if p is None: continue
        out.append(build(event_id,q["market"],q["selection"],float(q["odds"]),float(p),min_edge))
    return sorted(out,key=lambda x:x.edge,reverse=True)

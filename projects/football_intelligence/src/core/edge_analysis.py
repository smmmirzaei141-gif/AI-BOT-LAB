from __future__ import annotations
from collections import defaultdict

def by_edge(rows, buckets=((0.04,0.06),(0.06,0.10),(0.10,1.0))):
    out={}
    for lo,hi in buckets:
        x=[r for r in rows if lo<=float(r["edge"])<hi]
        p=sum(float(r["odds"])-1 if r["won"] else -1 for r in x)
        out[f"{lo:.2f}-{hi:.2f}"]={"bets":len(x),"wins":sum(bool(r["won"]) for r in x),"profit":p,"roi":p/len(x) if x else 0}
    return out

def by_league(rows):
    grouped=defaultdict(list)
    for r in rows: grouped[str(r.get("league","unknown"))].append(r)
    return {k:{"bets":len(v),"wins":sum(bool(x["won"]) for x in v),"profit":sum(float(x["odds"])-1 if x["won"] else -1 for x in v)} for k,v in grouped.items()}

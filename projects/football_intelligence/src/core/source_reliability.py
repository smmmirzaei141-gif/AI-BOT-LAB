from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class SourceReliability:
    source: str
    observations: int
    correct_direction: int
    accuracy: float
    avg_lead_ms: float

def evaluate(rows):
    grouped=defaultdict(list)
    for r in rows:
        if r.get("source") and r.get("correct_direction") is not None:
            grouped[str(r["source"])].append(r)
    out=[]
    for source, items in grouped.items():
        correct=sum(bool(x["correct_direction"]) for x in items)
        leads=[float(x["lead_ms"]) for x in items if x.get("lead_ms") is not None]
        out.append(SourceReliability(source,len(items),correct,correct/len(items),sum(leads)/len(leads) if leads else 0.0))
    return sorted(out,key=lambda x:(-x.accuracy,-x.observations))

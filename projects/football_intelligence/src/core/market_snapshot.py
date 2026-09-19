from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SnapshotComparison:
    target: object
    reference_count: int
    reference_median: float | None
    reference_min: float | None
    reference_max: float | None
    target_vs_median_pct: float | None

def compare_target(target, references):
    refs=[r for r in references if r.event_id==target.event_id and r.market==target.market and r.selection==target.selection and r.odds>1]
    if not refs:
        return SnapshotComparison(target,0,None,None,None,None)
    values=sorted(r.odds for r in refs)
    n=len(values)
    median=values[n//2] if n%2 else (values[n//2-1]+values[n//2])/2
    return SnapshotComparison(target,len(values),median,min(values),max(values),(target.odds/median-1)*100)

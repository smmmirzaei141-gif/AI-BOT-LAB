from __future__ import annotations
from .market_snapshot import compare_target
from .opportunity import score_opportunity

def analyze_snapshot(target, references, model_probability: float, min_references: int = 2):
    comparison=compare_target(target,references)
    if comparison.reference_count < min_references:
        return {
            "event_id":target.event_id,"market":target.market,"selection":target.selection,
            "action":"WATCH","labels":["INSUFFICIENT_REFERENCES"],
            "execution":"OFF","reference_count":comparison.reference_count
        }
    result=score_opportunity(
        target.odds, model_probability,
        comparison.reference_median,
        stale_threshold=0.08,
        min_edge=0.04,
    )
    return {
        "event_id":target.event_id,"market":target.market,"selection":target.selection,
        "odds":target.odds,"model_probability":model_probability,
        "reference_median":comparison.reference_median,
        "target_vs_median_pct":comparison.target_vs_median_pct,
        "score":result.score,"labels":result.labels,
        "action":result.action,"execution":"OFF",
    }

from __future__ import annotations

def pair_lead_lag(reference_ticks, target_ticks):
    target=list(target_ticks)
    result=[]
    for ref in reference_ticks:
        candidates=[t for t in target if t.event_id==ref.event_id and t.market==ref.market and t.selection==ref.selection and t.ts_ms>=ref.ts_ms]
        if candidates:
            t=min(candidates,key=lambda x:x.ts_ms)
            result.append({
                "event_id":ref.event_id,"market":ref.market,"selection":ref.selection,
                "reference_source":ref.source,"target_source":t.source,
                "reference_ts":ref.ts_ms,"target_ts":t.ts_ms,
                "lead_ms":t.ts_ms-ref.ts_ms,
                "reference_odds":ref.odds,"target_odds":t.odds
            })
    return result

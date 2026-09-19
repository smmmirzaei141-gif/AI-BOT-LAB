from projects.football_intelligence.src.adapters.target_market import normalize_target
from projects.football_intelligence.src.core.market_snapshot import compare_target

def test_target_normalization():
    q=normalize_target({"event_id":"e1","market":"goals","selection":"over_2.5","odds":2.2,"ts_ms":1000})
    assert q.source=="target" and q.status=="OPEN"

def test_target_reference_comparison():
    t=normalize_target({"event_id":"e1","market":"goals","selection":"over_2.5","odds":2.2,"ts_ms":1000})
    r1=normalize_target({"event_id":"e1","market":"goals","selection":"over_2.5","odds":2.0,"ts_ms":1000,"source":"a"})
    r2=normalize_target({"event_id":"e1","market":"goals","selection":"over_2.5","odds":2.1,"ts_ms":1000,"source":"b"})
    c=compare_target(t,[r1,r2])
    assert c.reference_count==2 and c.reference_median==2.05

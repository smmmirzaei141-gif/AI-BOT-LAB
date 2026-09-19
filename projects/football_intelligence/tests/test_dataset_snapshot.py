from projects.football_intelligence.src.core.dataset import settled_row
from projects.football_intelligence.src.core.snapshot import OddsSnapshot

def test_dataset_row():
    r=settled_row({"event_id":"e1","market":"goals","selection":"over_2.5","odds":2.1,"predicted_probability":0.55,"won":True})
    assert r.event_id=="e1" and r.won

def test_snapshot():
    s=OddsSnapshot("e1","goals","over_2.5",2.1,123,"reference")
    assert s.odds==2.1 and s.ts_ms==123

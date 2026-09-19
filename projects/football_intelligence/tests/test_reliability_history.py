from projects.football_intelligence.src.core.source_reliability import evaluate
from projects.football_intelligence.src.core.historical_odds import OddsTick
from projects.football_intelligence.src.core.lead_lag import pair_lead_lag

def test_reliability():
    r=evaluate([{"source":"A","correct_direction":True,"lead_ms":100},{"source":"A","correct_direction":False,"lead_ms":200}])[0]
    assert r.source=="A" and r.accuracy==0.5 and r.avg_lead_ms==150

def test_history_tick():
    t=OddsTick("e1","A","goals","over_2.5",2.1,100)
    assert t.odds==2.1

def test_lead_lag():
    ref=OddsTick("e1","ref","goals","over_2.5",2.0,100)
    target=OddsTick("e1","1xbet","goals","over_2.5",2.1,250)
    x=pair_lead_lag([ref],[target])[0]
    assert x["lead_ms"]==150

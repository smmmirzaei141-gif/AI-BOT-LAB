from projects.football_intelligence.src.core.settlement import settle
from projects.football_intelligence.src.core.movement import analyze
from projects.football_intelligence.src.core.market_backtest import summarize

def test_settlement():
    assert settle("goals","over_2.5",2,1)
    assert settle("btts","yes",1,1)
    assert settle("1x2","draw",2,2)
    assert not settle("1x2","home",0,2)

def test_movement():
    m=analyze(2.0,2.2)
    assert m.direction=="UP" and m.change_pct==10

def test_market_summary():
    s=summarize([{"market":"goals","odds":2.0,"won":True},{"market":"goals","odds":2.0,"won":False}])[0]
    assert s.bets==2 and s.profit==0

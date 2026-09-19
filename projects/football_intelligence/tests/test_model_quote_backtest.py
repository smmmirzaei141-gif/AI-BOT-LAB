from projects.football_intelligence.src.core.model_quote import build
from projects.football_intelligence.src.core.research_backtest import run
from projects.football_intelligence.src.core.pipeline import score_quotes

def test_quote():
    q=build("e","goals","over_2.5",2.2,0.55)
    assert q.implied_probability>0 and q.edge>0

def test_pipeline():
    x=score_quotes("e",[{"market":"goals","selection":"over_2.5","odds":2.2}],{("goals","over_2.5"):0.55})
    assert x[0].label=="MODEL_VALUE"

def test_backtest():
    r=run([{"odds":2.2,"model_probability":0.55,"won":True},{"odds":2.2,"model_probability":0.55,"won":False}])
    assert r.n==2 and r.profit==0 and r.brier>0

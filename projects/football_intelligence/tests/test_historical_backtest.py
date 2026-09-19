from projects.football_intelligence.src.core.historical_backtest import HistoricalCase,evaluate_case

def test_historical_case():
    c=HistoricalCase("e",1.4,0.8,{("goals","over_1.5"):2.0,("1x2","home"):2.1},{"home_goals":2,"away_goals":0})
    out=evaluate_case(c,min_edge=0.01)
    assert out and all("model_probability" in x for x in out)

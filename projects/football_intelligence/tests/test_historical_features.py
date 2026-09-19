from projects.football_intelligence.src.ingestion.historical_features import HistoricalMatch,aggregate,build_match_features
from projects.football_intelligence.src.ingestion.api_football_history import ApiFootballHistoryAdapter

def test_aggregate():
    a=aggregate([HistoricalMatch(1,2,1,1.4,0.8,5,2,11,20),HistoricalMatch(1,1,0,None,None,7,3,9,None)])
    assert a.sample_size==2 and a.goals_for==1.5 and a.corners==6

def test_match_features():
    a=aggregate([HistoricalMatch(1,2,1)])
    b=aggregate([HistoricalMatch(2,1,2)])
    x=build_match_features(a,b)
    assert x["home_goals_for"]==2 and x["away_goals_against"]==2

def test_adapter():
    class C:
        def get(self,path,params): return {"response":[{"fixture":{"id":1}}]}
    assert len(ApiFootballHistoryAdapter(C()).team_history(1,3))==1

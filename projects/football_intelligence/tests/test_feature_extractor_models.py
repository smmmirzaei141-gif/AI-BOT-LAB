from projects.football_intelligence.src.core.market_models import estimate
from projects.football_intelligence.src.ingestion.feature_extractor import extract

class Bundle:
    fixture={"fixture":{"id":7},"teams":{"home":{"id":1},"away":{"id":2}},"league":{"name":"L"}}
    statistics=[{"team":{"id":1},"statistics":[{"type":"Expected Goals","value":"1.4"},{"type":"Corner Kicks","value":5},{"type":"Fouls","value":10}]},
                {"team":{"id":2},"statistics":[{"type":"Expected Goals","value":"0.9"},{"type":"Corner Kicks","value":3}]}]

def test_extract():
    x=extract(Bundle())
    assert x.fixture_id==7 and x.home.xg_for==1.4 and x.away.corners==3

def test_models():
    p=estimate(1.4,0.9)
    assert 0<p.over_2_5<1 and 0<p.btts_yes<1
    assert abs(p.home+p.draw+p.away-1)<1e-6

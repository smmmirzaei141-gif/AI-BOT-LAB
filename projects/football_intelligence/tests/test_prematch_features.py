from projects.football_intelligence.src.core.normalizer import TeamStats
from projects.football_intelligence.src.core.prematch_features import baseline_probabilities, build_features, poisson_total_probability

def test_baseline_probabilities_are_valid():
    h=TeamStats("H",10,1.5,1.0,xg_for=1.6,xg_against=1.0)
    a=TeamStats("A",10,1.2,1.3,xg_for=1.3,xg_against=1.4)
    p=baseline_probabilities(build_features(h,a))
    assert p[("goals","over",2.5)]>0
    assert 0<p[("btts","yes",None)]<1
    assert abs(sum(p[("1x2",s,None)] for s in ("home","draw","away"))-1)<0.01

def test_poisson_complements():
    assert abs(poisson_total_probability(2.5,2.0,True)+poisson_total_probability(2.5,2.0,False)-1)<1e-9

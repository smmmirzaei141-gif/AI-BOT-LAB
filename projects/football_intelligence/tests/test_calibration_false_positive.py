from projects.football_intelligence.src.core.calibration import evaluate
from projects.football_intelligence.src.core.false_positive import analyze

def rows():
    return [
      {"model_probability":.8,"odds":1.5,"won":True},
      {"model_probability":.7,"odds":1.6,"won":False},
      {"model_probability":.6,"odds":1.8,"won":True},
      {"model_probability":.65,"odds":1.7,"won":False},
    ]

def test_calibration():
    r=evaluate(rows(),bins=5)
    assert r.brier>=0 and r.log_loss>=0 and len(r.bins)>0

def test_false_positive():
    r=analyze(rows(),min_edge=.04)
    assert r.selected>0 and 0<=r.false_positive_rate<=1

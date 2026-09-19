from projects.football_intelligence.src.core.research_runner import load_cases,execute
from pathlib import Path

def test_runner(tmp_path):
    p=tmp_path/"x.jsonl"
    p.write_text('{"event_id":"e","home_xg":1.4,"away_xg":.8,"odds":{"goals|over_1.5":2.0},"result":{"home_goals":2,"away_goals":0}}\n')
    cases=load_cases(p)
    r=execute(cases,.01)
    assert r.cases==1 and r.rows>=1 and r.markets

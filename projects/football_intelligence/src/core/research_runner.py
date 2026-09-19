from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json

from .historical_backtest import HistoricalCase, evaluate_case
from .batch_backtest import run
from .calibration import evaluate as calibration
from .false_positive import analyze as false_positive
from .edge_analysis import by_edge, by_league

@dataclass(frozen=True)
class ResearchRun:
    cases: int
    rows: int
    markets: tuple
    calibration: object
    false_positive: object
    edge_buckets: dict
    leagues: dict

def load_cases(path: str|Path) -> list[HistoricalCase]:
    cases=[]
    with open(path,encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            x=json.loads(line)
            cases.append(HistoricalCase(x["event_id"],float(x["home_xg"]),float(x["away_xg"]),{tuple(k.split("|",1)):float(v) for k,v in x["odds"].items()},x["result"]))
    return cases

def execute(cases, min_edge=.04) -> ResearchRun:
    rows=[r for c in cases for r in evaluate_case(c,min_edge)]
    return ResearchRun(
        len(cases),len(rows),
        tuple(run(cases,evaluate_case,min_edge)),
        calibration(rows),
        false_positive(rows,min_edge),
        by_edge(rows),
        by_league(rows),
    )

def write_json(report: ResearchRun, path: str|Path):
    def default(o):
        if hasattr(o,"__dict__"): return o.__dict__
        if isinstance(o,tuple): return list(o)
        raise TypeError(type(o).__name__)
    Path(path).write_text(json.dumps(report,default=default,ensure_ascii=False,indent=2),encoding="utf-8")

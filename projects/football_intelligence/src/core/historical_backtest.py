from __future__ import annotations
from dataclasses import dataclass
from .market_models import estimate

@dataclass(frozen=True)
class HistoricalCase:
    event_id: str
    home_xg: float
    away_xg: float
    odds: dict[tuple[str,str],float]
    result: dict[str,object]

def probabilities(case: HistoricalCase):
    return estimate(case.home_xg, case.away_xg)

def settle_1x2(result, selection: str) -> bool:
    home=int(result["home_goals"]); away=int(result["away_goals"])
    actual="home" if home>away else "away" if away>home else "draw"
    return actual==selection

def settle_total_goals(result, line: float, over: bool) -> bool:
    total=int(result["home_goals"])+int(result["away_goals"])
    return total>line if over else total<line

def settle_btts(result, yes: bool) -> bool:
    hit=int(result["home_goals"])>0 and int(result["away_goals"])>0
    return hit if yes else not hit

def evaluate_case(case: HistoricalCase, min_edge: float=0.04):
    p=probabilities(case)
    mapping={
      ("1x2","home"):p.home, ("1x2","draw"):p.draw, ("1x2","away"):p.away,
      ("goals","over_1.5"):p.over_1_5, ("goals","over_2.5"):p.over_2_5,
      ("goals","over_3.5"):p.over_3_5, ("btts","yes"):p.btts_yes,
      ("btts","no"):1-p.btts_yes
    }
    out=[]
    for key,odds in case.odds.items():
        prob=mapping.get(key)
        if prob is None or odds<=1: continue
        edge=prob-1/odds
        if edge>=min_edge:
            if key[0]=="1x2": won=settle_1x2(case.result,key[1])
            elif key[0]=="goals":
                won=settle_total_goals(case.result,float(key[1].split("_")[1]),True)
            else: won=settle_btts(case.result,key[1]=="yes")
            out.append({"event_id":case.event_id,"market":key[0],"selection":key[1],"odds":odds,"model_probability":prob,"edge":edge,"won":won})
    return out

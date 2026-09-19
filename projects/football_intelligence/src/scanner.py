from __future__ import annotations
import argparse, json
from pathlib import Path
from .core.market import MarketQuote, MarketType
from .core.opportunity import score_opportunity
from .core.prematch_features import baseline_probabilities, build_features
from .core.normalizer import TeamStats

def _stats(r: dict) -> TeamStats:
    return TeamStats(team=str(r.get("team","")), matches=int(r.get("matches",0)), goals_for=float(r.get("goals_for",0)), goals_against=float(r.get("goals_against",0)), xg_for=r.get("xg_for"), xg_against=r.get("xg_against"), corners_for=r.get("corners_for"), corners_against=r.get("corners_against"), cards_for=r.get("cards_for"), cards_against=r.get("cards_against"), fouls_for=r.get("fouls_for"), fouls_against=r.get("fouls_against"), throw_ins_for=r.get("throw_ins_for"), throw_ins_against=r.get("throw_ins_against"))

def scan(payload: dict) -> list[dict]:
    f = build_features(_stats(payload["home"]), _stats(payload["away"]), payload.get("h2h",[]), payload.get("home_absences",0), payload.get("away_absences",0))
    probs = baseline_probabilities(f)
    refs = [MarketQuote(event_id=str(r["event_id"]), market=MarketType(str(r["market"])), selection=str(r["selection"]), odds=float(r["odds"]), source=str(r["source"]), ts_ms=int(r["ts_ms"]), line=r.get("line"), market_status=str(r.get("market_status","open"))) for r in payload.get("references",[])]
    results=[]
    for t in payload.get("targets",[]):
        q=MarketQuote(event_id=str(t["event_id"]), market=MarketType(str(t["market"])), selection=str(t["selection"]), odds=float(t["odds"]), source=str(t.get("source","1xbet_visible")), ts_ms=int(t["ts_ms"]), line=t.get("line"), market_status=str(t.get("market_status","open")))
        key=(q.market.value,q.selection.lower(),q.line)
        opp=score_opportunity(q,probs.get(key),[r for r in refs if r.event_id==q.event_id and r.market==q.market and r.selection.lower()==q.selection.lower() and r.line==q.line])
        results.append({"event_id":opp.event_id,"market":opp.market,"selection":opp.selection,"odds":opp.odds,"model_probability":probs.get(key),"score":opp.score,"labels":list(opp.labels),"explanation":list(opp.explanation),"action":"ALERT" if opp.score>=35 else "WATCH","execution":"OFF"})
    return sorted(results,key=lambda x:x["score"],reverse=True)

def main():
    p=argparse.ArgumentParser(description="Football Intelligence paper scanner")
    p.add_argument("payload",type=Path)
    args=p.parse_args()
    print(json.dumps(scan(json.loads(args.payload.read_text(encoding="utf-8"))),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()

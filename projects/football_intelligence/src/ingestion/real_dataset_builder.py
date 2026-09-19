from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

@dataclass(frozen=True)
class DatasetConfig:
    league: int
    season: int
    min_history: int=5
    odds_bookmaker_id: int|None=None

class RealDatasetBuilder:
    """Builds leakage-safe pre-match research rows from an injected API client.

    Odds are requested per fixture because API-Football's documented pre-match odds
    history is limited; the builder stores the retrieval/update timestamp as metadata.
    """
    def __init__(self, client):
        self.client=client

    def fixtures(self, cfg: DatasetConfig):
        data=self.client.get("/fixtures",params={"league":cfg.league,"season":cfg.season,"status":"FT-AET-PEN"})
        return data.get("response",data) if isinstance(data,dict) else data

    def odds(self, fixture_id: int, bookmaker_id=None):
        params={"fixture":fixture_id}
        if bookmaker_id is not None: params["bookmaker"]=bookmaker_id
        data=self.client.get("/odds",params=params)
        return data.get("response",data) if isinstance(data,dict) else data

    def build_skeleton(self,cfg: DatasetConfig, output: str|Path):
        rows=[]
        for f in self.fixtures(cfg):
            fx=f.get("fixture",{}); teams=f.get("teams",{}); goals=f.get("goals",{})
            if fx.get("status",{}).get("short") not in {"FT","AET","PEN"}: continue
            rows.append({
                "event_id":str(fx.get("id")),
                "league":str(f.get("league",{}).get("name","")),
                "league_id":f.get("league",{}).get("id"),
                "season":f.get("league",{}).get("season"),
                "kickoff_ts":fx.get("timestamp"),
                "home_team_id":teams.get("home",{}).get("id"),
                "away_team_id":teams.get("away",{}).get("id"),
                "home_goals":goals.get("home"),
                "away_goals":goals.get("away"),
                "odds":self.odds(fx.get("id"),cfg.odds_bookmaker_id),
                "collected_at":datetime.now(timezone.utc).isoformat()
            })
        Path(output).write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
        return len(rows)

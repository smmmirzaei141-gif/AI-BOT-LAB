from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class TeamFeatures:
    goals_for: float
    goals_against: float
    xg_for: float | None
    xg_against: float | None
    corners: float
    cards: float
    fouls: float
    throw_ins: float

@dataclass(frozen=True)
class MatchFeatures:
    fixture_id: int
    home: TeamFeatures
    away: TeamFeatures
    league: str | None

def _avg(values: list[float]) -> float:
    return sum(values)/len(values) if values else 0.0

def _team_from_stats(rows: list[dict[str, Any]], team_id: int | None) -> TeamFeatures:
    values={"goals_for":[],"goals_against":[],"xg_for":[],"xg_against":[],"corners":[],"cards":[],"fouls":[],"throw_ins":[]}
    for row in rows:
        if team_id is not None and row.get("team",{}).get("id") != team_id:
            continue
        for item in row.get("statistics",[]):
            name=str(item.get("type","")).lower()
            raw=item.get("value")
            if raw is None: continue
            try:
                value=float(str(raw).replace("%","").split(" ")[0])
            except (TypeError,ValueError):
                continue
            if "corner" in name: values["corners"].append(value)
            elif "foul" in name: values["fouls"].append(value)
            elif "yellow" in name or "card" in name: values["cards"].append(value)
            elif "throw" in name: values["throw_ins"].append(value)
            elif "expected goals" in name: values["xg_for"].append(value)
    return TeamFeatures(
        goals_for=0.0, goals_against=0.0,
        xg_for=_avg(values["xg_for"]) if values["xg_for"] else None,
        xg_against=None, corners=_avg(values["corners"]),
        cards=_avg(values["cards"]), fouls=_avg(values["fouls"]),
        throw_ins=_avg(values["throw_ins"]),
    )

def extract(bundle: Any) -> MatchFeatures:
    f=bundle.fixture
    teams=f.get("teams",{})
    h=teams.get("home",{}); a=teams.get("away",{})
    rows=bundle.statistics or []
    return MatchFeatures(
        fixture_id=int(f.get("fixture",{}).get("id",0)),
        home=_team_from_stats(rows,h.get("id")),
        away=_team_from_stats(rows,a.get("id")),
        league=f.get("league",{}).get("name"),
    )

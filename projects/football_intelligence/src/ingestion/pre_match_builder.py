from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class TeamInput:
    goals_for: float = 0.0
    goals_against: float = 0.0
    xg_for: float | None = None
    xg_against: float | None = None
    corners: float = 0.0
    cards: float = 0.0
    fouls: float = 0.0
    throw_ins: float = 0.0

@dataclass(frozen=True)
class PreMatchInput:
    fixture_id: int
    home: TeamInput
    away: TeamInput
    kickoff_ts: int | None
    league: str | None

def build_input(bundle: Any) -> PreMatchInput:
    fixture=bundle.fixture
    f=fixture.get("fixture",{})
    teams=fixture.get("teams",{})
    home=teams.get("home",{}); away=teams.get("away",{})
    league=fixture.get("league",{}).get("name")
    return PreMatchInput(
        fixture_id=int(f.get("id",0)),
        home=TeamInput(),
        away=TeamInput(),
        kickoff_ts=None,
        league=league,
    )

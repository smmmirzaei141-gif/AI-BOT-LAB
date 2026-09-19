from __future__ import annotations
from dataclasses import dataclass
from statistics import mean

@dataclass(frozen=True)
class HistoricalMatch:
    team_id: int
    goals_for: float
    goals_against: float
    xg_for: float|None=None
    xg_against: float|None=None
    corners: float|None=None
    cards: float|None=None
    fouls: float|None=None
    throw_ins: float|None=None

@dataclass(frozen=True)
class HistoricalFeatures:
    team_id: int
    sample_size: int
    goals_for: float
    goals_against: float
    xg_for: float|None
    xg_against: float|None
    corners: float|None
    cards: float|None
    fouls: float|None
    throw_ins: float|None

def aggregate(matches: list[HistoricalMatch]) -> HistoricalFeatures:
    if not matches: raise ValueError("at least one historical match is required")
    def avg(attr):
        vals=[getattr(m,attr) for m in matches if getattr(m,attr) is not None]
        return mean(vals) if vals else None
    return HistoricalFeatures(
        team_id=matches[0].team_id, sample_size=len(matches),
        goals_for=mean(m.goals_for for m in matches),
        goals_against=mean(m.goals_against for m in matches),
        xg_for=avg("xg_for"), xg_against=avg("xg_against"),
        corners=avg("corners"), cards=avg("cards"), fouls=avg("fouls"), throw_ins=avg("throw_ins"))

def build_match_features(home: HistoricalFeatures, away: HistoricalFeatures):
    return {
        "home_goals_for":home.goals_for, "home_goals_against":home.goals_against,
        "away_goals_for":away.goals_for, "away_goals_against":away.goals_against,
        "home_xg_for":home.xg_for, "away_xg_for":away.xg_for,
        "home_corners":home.corners, "away_corners":away.corners,
        "home_cards":home.cards, "away_cards":away.cards,
        "home_fouls":home.fouls, "away_fouls":away.fouls,
        "home_throw_ins":home.throw_ins, "away_throw_ins":away.throw_ins,
    }

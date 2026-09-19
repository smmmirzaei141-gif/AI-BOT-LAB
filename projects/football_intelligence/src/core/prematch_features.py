from __future__ import annotations
from dataclasses import dataclass
from math import exp, factorial
from statistics import mean
from typing import Iterable
from .normalizer import TeamStats

@dataclass(frozen=True)
class TeamForm:
    matches: int
    goals_for: float
    goals_against: float
    xg_for: float | None
    xg_against: float | None
    corners_for: float | None
    corners_against: float | None
    cards_for: float | None
    cards_against: float | None
    fouls_for: float | None
    fouls_against: float | None
    throw_ins_for: float | None
    throw_ins_against: float | None

@dataclass(frozen=True)
class PreMatchFeatures:
    home: TeamForm
    away: TeamForm
    h2h_home_goals: float | None = None
    h2h_away_goals: float | None = None
    home_absences: int = 0
    away_absences: int = 0
    completeness: float = 0.0

def _avg(values: Iterable[float | None]) -> float | None:
    xs = [float(v) for v in values if v is not None]
    return mean(xs) if xs else None

def build_features(home: TeamStats, away: TeamStats, h2h: Iterable[dict] = (), home_absences: int = 0, away_absences: int = 0) -> PreMatchFeatures:
    rows = list(h2h)
    h2h_home = _avg(r.get("home_goals") for r in rows)
    h2h_away = _avg(r.get("away_goals") for r in rows)
    fields = [home.goals_for, home.goals_against, away.goals_for, away.goals_against, home.xg_for, home.xg_against, away.xg_for, away.xg_against]
    completeness = sum(v is not None for v in fields) / len(fields)
    def form(t: TeamStats) -> TeamForm:
        return TeamForm(t.matches, t.goals_for, t.goals_against, t.xg_for, t.xg_against, t.corners_for, t.corners_against, t.cards_for, t.cards_against, t.fouls_for, t.fouls_against, t.throw_ins_for, t.throw_ins_against)
    return PreMatchFeatures(form(home), form(away), h2h_home, h2h_away, max(0, int(home_absences)), max(0, int(away_absences)), round(completeness, 3))

def _pmf(k: int, lam: float) -> float:
    return exp(-lam) * lam**k / factorial(k)

def poisson_total_probability(line: float, expected_goals: float, over: bool) -> float:
    expected_goals = max(0.05, min(8.0, expected_goals))
    cutoff = int(line - 0.5)
    under = sum(_pmf(k, expected_goals) for k in range(max(0, cutoff + 1)))
    return round(1.0 - under if over else under, 6)

def baseline_probabilities(f: PreMatchFeatures) -> dict[tuple[str, str, float | None], float]:
    h, a = f.home, f.away
    ha = h.xg_for if h.xg_for is not None else h.goals_for
    aa = a.xg_for if a.xg_for is not None else a.goals_for
    hd = h.xg_against
    ad = a.xg_against
    lh = max(0.05, 0.58 * ha + 0.42 * (ad if ad is not None else a.goals_against))
    la = max(0.05, 0.58 * aa + 0.42 * (hd if hd is not None else h.goals_against))
    total = min(8.0, lh + la)
    out = {}
    for line in (1.5, 2.5, 3.5):
        out[("goals", "over", line)] = poisson_total_probability(line, total, True)
        out[("goals", "under", line)] = poisson_total_probability(line, total, False)
    btts = (1 - exp(-lh)) * (1 - exp(-la))
    out[("btts", "yes", None)] = round(btts, 6)
    out[("btts", "no", None)] = round(1 - btts, 6)
    matrix = [[_pmf(i, lh) * _pmf(j, la) for j in range(11)] for i in range(11)]
    ph = sum(matrix[i][j] for i in range(11) for j in range(11) if i > j)
    pd = sum(matrix[i][i] for i in range(11))
    pa = sum(matrix[i][j] for i in range(11) for j in range(11) if i < j)
    out[("1x2", "home", None)] = round(ph, 6)
    out[("1x2", "draw", None)] = round(pd, 6)
    out[("1x2", "away", None)] = round(pa, 6)
    return out

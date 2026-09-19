from __future__ import annotations

def settle(market: str, selection: str, home: int, away: int) -> bool:
    total=home+away
    m=market.lower(); s=selection.lower()
    if m in {"goals","over_under","total_goals"}:
        if s in {"over_1.5","over1.5"}: return total > 1.5
        if s in {"over_2.5","over2.5"}: return total > 2.5
        if s in {"over_3.5","over3.5"}: return total > 3.5
        if s in {"under_1.5","under1.5"}: return total < 1.5
        if s in {"under_2.5","under2.5"}: return total < 2.5
        if s in {"under_3.5","under3.5"}: return total < 3.5
    if m in {"btts","both_teams_to_score"}:
        if s in {"yes","btts_yes"}: return home > 0 and away > 0
        if s in {"no","btts_no"}: return home == 0 or away == 0
    if m in {"1x2","match_result"}:
        if s in {"home","1"}: return home > away
        if s in {"draw","x"}: return home == away
        if s in {"away","2"}: return away > home
    raise ValueError(f"Unsupported market/selection: {market}/{selection}")

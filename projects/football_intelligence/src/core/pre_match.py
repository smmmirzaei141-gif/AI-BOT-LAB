from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PreMatchProfile:
    event_id: str
    home: str
    away: str
    kickoff_ts_ms: int
    data_completeness: float
    notes: tuple[str, ...] = ()


def completeness(fields: dict[str, object]) -> float:
    if not fields:
        return 0.0
    present = sum(v is not None for v in fields.values())
    return present / len(fields)

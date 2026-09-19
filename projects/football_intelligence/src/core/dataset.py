from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class DatasetRow:
    event_id: str
    market: str
    selection: str
    odds: float
    predicted_probability: float
    won: bool
    kickoff_ts: int | None = None
    snapshot_ts: int | None = None
    source: str = "unknown"
    league: str = "unknown"

def settled_row(payload: dict) -> DatasetRow:
    return DatasetRow(
        event_id=str(payload["event_id"]), market=str(payload["market"]),
        selection=str(payload["selection"]), odds=float(payload["odds"]),
        predicted_probability=float(payload["predicted_probability"]),
        won=bool(payload["won"]), kickoff_ts=payload.get("kickoff_ts"),
        snapshot_ts=payload.get("snapshot_ts"), source=str(payload.get("source","unknown")),
        league=str(payload.get("league","unknown")),
    )

def append_jsonl(path: str | Path, row: DatasetRow) -> None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f: f.write(json.dumps(asdict(row),ensure_ascii=False)+"\n")

def load_jsonl(path: str | Path) -> list[DatasetRow]:
    p=Path(path)
    if not p.exists(): return []
    return [settled_row(json.loads(line)) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]

from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class OddsSnapshot:
    event_id: str
    market: str
    selection: str
    odds: float
    ts_ms: int
    source: str
    line: float | None = None
    status: str = "OPEN"

def append_snapshot(path: str | Path, snapshot: OddsSnapshot) -> None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f: f.write(json.dumps(asdict(snapshot),ensure_ascii=False)+"\n")

def load_snapshots(path: str | Path) -> list[OddsSnapshot]:
    p=Path(path)
    if not p.exists(): return []
    return [OddsSnapshot(**json.loads(x)) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

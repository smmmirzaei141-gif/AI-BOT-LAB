from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class OddsTick:
    event_id: str
    source: str
    market: str
    selection: str
    odds: float
    ts_ms: int
    line: float | None = None

def append_tick(path, tick: OddsTick):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f:
        f.write(json.dumps(asdict(tick),ensure_ascii=False)+"\n")

def load_ticks(path):
    p=Path(path)
    if not p.exists(): return []
    return [OddsTick(**json.loads(x)) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

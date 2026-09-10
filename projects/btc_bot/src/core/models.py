from dataclasses import dataclass
from typing import Optional

@dataclass
class Position:
    side: str
    entry: float
    size: float = 0.0
    stop: Optional[float] = None
    target: Optional[float] = None

@dataclass
class Signal:
    side: str
    score: float
    reason: str = ""

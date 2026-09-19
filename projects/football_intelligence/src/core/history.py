from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict
from .market import MarketQuote


class QuoteHistory:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, quote: MarketQuote) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(quote), ensure_ascii=False) + "\n")

    def load(self) -> list[MarketQuote]:
        if not self.path.exists():
            return []
        rows: list[MarketQuote] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            x = json.loads(line)
            rows.append(MarketQuote(**x))
        return rows

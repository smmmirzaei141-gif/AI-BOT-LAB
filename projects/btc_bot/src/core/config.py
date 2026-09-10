from dataclasses import dataclass

@dataclass(frozen=True)
class BotConfig:
    coin: str = "BTC"
    interval: str = "1h"
    tp_pct: float = 0.02
    sl_pct: float = 0.01
    fee_pct: float = 0.0004
    slippage_pct: float = 0.0002
    timeout_hours: int = 24
    max_positions: int = 1
    paper: bool = True

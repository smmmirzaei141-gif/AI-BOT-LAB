from src.strategy.engine import StrategyEngine
from src.risk.engine import RiskEngine


def make_candle(o, h, l, c):
    return {"t": 0, "o": o, "h": h, "l": l, "c": c}


def test_strategy_waits_for_mss():
    candles = []

    for i in range(60):
        candles.append(make_candle(100, 101, 99, 100))

    # Bearish sweep
    candles.append(make_candle(100, 103, 99, 100))

    engine = StrategyEngine()
    signal = engine.evaluate(candles)

    assert signal is None
    assert engine.sweep_index == len(candles) - 1


def test_risk_levels_short():
    risk = RiskEngine(tp_pct=0.02, sl_pct=0.01)

    levels = risk.levels("SHORT", 100.0)

    assert levels["tp"] == 98.0
    assert levels["sl"] == 101.0


def test_max_positions():
    risk = RiskEngine(max_positions=1)

    assert risk.can_open(0)
    assert not risk.can_open(1)

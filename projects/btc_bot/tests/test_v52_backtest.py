from src.backtest.engine import BacktestEngine
from src.strategy.engine import StrategyEngine
from src.risk.engine import RiskEngine


def candle(o, h, l, c):
    return {"t": 0, "o": o, "h": h, "l": l, "c": c}


def test_empty_signal_backtest():
    candles = [
        candle(100, 101, 99, 100)
        for _ in range(80)
    ]

    engine = BacktestEngine(
        StrategyEngine(),
        RiskEngine(),
    )

    result = engine.run(candles)

    assert result["trades"] == 0
    assert result["wins"] == 0
    assert result["losses"] == 0
    assert result["pnl"] == 0.0


def test_short_trade_can_close_at_target():
    candles = [
        candle(100, 101, 99, 100)
        for _ in range(60)
    ]

    # Sweep.
    candles.append(candle(100, 103, 99, 100))

    # MSS.
    candles.append(candle(100, 100, 96, 97))

    # Target after entry around 97.
    candles.append(candle(97, 97.5, 94, 95))

    engine = BacktestEngine(
        StrategyEngine(),
        RiskEngine(),
    )

    result = engine.run(candles)

    assert result["trades"] >= 1
    assert result["wins"] >= 1
    assert result["pnl"] > 0


def test_no_future_candle_signal():
    base = [
        candle(100, 101, 99, 100)
        for _ in range(60)
    ]

    first = base + [
        candle(100, 103, 99, 100),
    ]

    second = first + [
        candle(100, 100, 96, 97),
    ]

    engine1 = BacktestEngine(
        StrategyEngine(),
        RiskEngine(),
    )

    engine2 = BacktestEngine(
        StrategyEngine(),
        RiskEngine(),
    )

    r1 = engine1.run(first)
    r2 = engine2.run(second)

    # The first dataset cannot know the future MSS.
    assert r1["trades"] == 0
    assert r2["trades"] >= 0


tests = [
    test_empty_signal_backtest,
    test_short_trade_can_close_at_target,
    test_no_future_candle_signal,
]

for test in tests:
    test()
    print("PASS:", test.__name__)

print("V52 BACKTEST TESTS PASSED")

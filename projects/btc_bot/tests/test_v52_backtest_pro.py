from src.backtest.engine import BacktestEngine
from src.strategy.engine import StrategyEngine
from src.risk.engine import RiskEngine


def candle(t, o, h, l, c):
    return {
        "t": t,
        "o": o,
        "h": h,
        "l": l,
        "c": c,
    }


def make_engine():
    return BacktestEngine(
        StrategyEngine(),
        RiskEngine(
            tp_pct=0.02,
            sl_pct=0.01,
        ),
        fee_pct=0.0004,
        slippage_pct=0.0002,
        timeout_hours=24,
        initial_equity=1.0,
    )


def test_fee_and_slippage_are_applied():
    engine = make_engine()

    signal = type(
        "Signal",
        (),
        {"side": "SHORT"},
    )()

    entry = engine._apply_entry_slippage(
        signal.side,
        100.0,
    )

    assert entry < 100.0

    pnl = engine._net_pnl(
        "SHORT",
        entry,
        entry * 0.98,
    )

    assert pnl < 0.02


def test_timeout_is_recorded():
    candles = []

    for i in range(60):
        candles.append(
            candle(
                i * 3_600_000,
                100,
                101,
                99,
                100,
            )
        )

    # Sweep
    candles.append(
        candle(
            60 * 3_600_000,
            100,
            103,
            99,
            100,
        )
    )

    # MSS
    candles.append(
        candle(
            61 * 3_600_000,
            100,
            100,
            96,
            97,
        )
    )

    # Keep price alive beyond timeout.
    for i in range(62, 90):
        candles.append(
            candle(
                i * 3_600_000,
                97,
                97.5,
                96.5,
                97,
            )
        )

    result = make_engine().run(candles)

    assert result["trades"] >= 1
    assert result["timeouts"] >= 1


def test_metrics_exist():
    candles = [
        candle(
            i * 3_600_000,
            100,
            101,
            99,
            100,
        )
        for i in range(80)
    ]

    result = make_engine().run(candles)

    assert "pnl" in result
    assert "max_drawdown" in result
    assert "profit_factor" in result
    assert "equity_curve" in result
    assert "trade_log" in result


tests = [
    test_fee_and_slippage_are_applied,
    test_timeout_is_recorded,
    test_metrics_exist,
]

for test in tests:
    test()
    print("PASS:", test.__name__)

print("V52 PRO BACKTEST TESTS PASSED")

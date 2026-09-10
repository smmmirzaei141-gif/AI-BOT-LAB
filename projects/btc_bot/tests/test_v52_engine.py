from src.core.engine import V52Engine
from src.core.config import BotConfig


def make_candle(o, h, l, c):
    return {"t": 0, "o": o, "h": h, "l": l, "c": c}


def test_engine_no_signal_on_neutral_market():
    engine = V52Engine(BotConfig())

    candles = [
        make_candle(100, 101, 99, 100)
        for _ in range(60)
    ]

    result = engine.on_candles(candles)

    assert result is None
    assert len(engine.open_positions) == 0


def test_engine_risk_and_execution_layers():
    engine = V52Engine(BotConfig())

    candles = [
        make_candle(100, 101, 99, 100)
        for _ in range(60)
    ]

    # Force a valid RANGE bearish sweep.
    candles.append(
        make_candle(100, 103, 99, 100)
    )

    result = engine.on_candles(candles)

    # Sweep only arms the strategy; MSS is still required.
    assert result is None
    assert engine.strategy.sweep_index == len(candles) - 1


def test_engine_max_position_guard():
    engine = V52Engine(BotConfig())

    fake_position = engine.risk.create_position(
        type(
            "Signal",
            (),
            {"side": "SHORT"}
        )(),
        100.0,
    )

    engine.open_positions.append(fake_position)

    candles = [
        make_candle(100, 101, 99, 100)
        for _ in range(60)
    ]

    result = engine.on_candles(candles)

    assert result is None
    assert len(engine.open_positions) == 1


tests = [
    test_engine_no_signal_on_neutral_market,
    test_engine_risk_and_execution_layers,
    test_engine_max_position_guard,
]

for test in tests:
    test()

print("V52 ENGINE TESTS PASSED")

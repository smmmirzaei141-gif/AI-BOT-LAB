import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from core.value_engine import MarketQuote, evaluate_quote, implied_probability


def test_implied_probability():
    assert round(implied_probability(2.0), 6) == 0.5


def test_model_value_candidate():
    result = evaluate_quote(
        MarketQuote("goals", "Over 1.5", 1.72, model_probability=0.66)
    )
    assert result.edge is not None
    assert result.edge > 0.04
    assert "MODEL_VALUE_CANDIDATE" in result.flags

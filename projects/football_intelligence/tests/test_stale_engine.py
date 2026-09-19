import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from core.market import MarketQuote, MarketType
from core.stale_engine import compare_target_to_references


def test_stale_target_is_detected():
    target = MarketQuote("e1", MarketType.GOALS, "Over 1.5", 2.10, "1xbet", 10, 1.5)
    refs = [
        MarketQuote("e1", MarketType.GOALS, "Over 1.5", 1.70, "a", 10, 1.5),
        MarketQuote("e1", MarketType.GOALS, "Over 1.5", 1.72, "b", 10, 1.5),
    ]
    r = compare_target_to_references(target, refs)
    assert r.stale is True
    assert r.reference_odds is not None

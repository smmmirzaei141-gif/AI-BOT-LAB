import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from core.decision import classify
from core.opportunity import Opportunity


def test_high_score_alert():
    o = Opportunity("e1", "goals", "Over 1.5", 2.1, 60, ("STALE_ODDS",), ("x",))
    assert classify(o).action == "ALERT"


def test_low_score_watch():
    o = Opportunity("e1", "goals", "Over 1.5", 1.8, 10, (), ())
    assert classify(o).action == "WATCH"

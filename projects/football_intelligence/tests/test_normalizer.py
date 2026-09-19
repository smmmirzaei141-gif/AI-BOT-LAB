import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from core.normalizer import normalize_quotes


def test_normalize_quotes():
    rows = [{"market": "goals", "selection": "Over 2.5", "odds": 1.91, "line": 2.5}]
    q = normalize_quotes("e1", "source", 123, rows)
    assert len(q) == 1
    assert q[0].odds == 1.91

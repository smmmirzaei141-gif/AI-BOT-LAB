import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from core.anomaly_engine import OddsSnapshot, detect_outlier


def test_high_outlier_is_flagged():
    snapshots = [
        OddsSnapshot("a", 1.48, 1),
        OddsSnapshot("b", 1.50, 2),
        OddsSnapshot("c", 1.49, 3),
    ]
    result = detect_outlier(1.72, snapshots)
    assert result.suspicious is True

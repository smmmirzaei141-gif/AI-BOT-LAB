from ..core.models import Signal

class StrategyEngine:
    """V52 strategy interface. Existing V51 logic will plug in here."""

    def evaluate(self, market: dict) -> Signal | None:
        return None

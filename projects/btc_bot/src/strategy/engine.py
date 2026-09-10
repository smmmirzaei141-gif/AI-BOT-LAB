from ..core.models import Signal


class StrategyEngine:
    """
    V52 strategy engine.

    Preserves the V51 core:
    - closed candles only
    - RANGE-only bearish sweep
    - bearish MSS within 1-2 candles after sweep
    - short-only signal
    """

    def __init__(self, sweep_lb=10, mss_lb=5, max_mss=2):
        self.sweep_lb = sweep_lb
        self.mss_lb = mss_lb
        self.max_mss = max_mss
        self.sweep_index = None

    @staticmethod
    def _ema(values, period):
        if not values:
            return 0.0

        alpha = 2 / (period + 1)
        value = values[0]

        for x in values[1:]:
            value = alpha * x + (1 - alpha) * value

        return value

    def regime(self, candles, i):
        if i < 55:
            return "UNKNOWN"

        closes = [x["c"] for x in candles[:i]]
        e20 = self._ema(closes[-40:], 20)
        e50 = self._ema(closes[-50:], 50)

        separation = abs(e20 - e50) / e50 if e50 else 0.0

        returns = []
        for j in range(max(1, i - 24), i):
            returns.append(abs(candles[j]["c"] / candles[j - 1]["c"] - 1))

        volatility = sum(returns) / len(returns) if returns else 0.0

        if volatility >= 0.012:
            return "HIGH_VOL"

        if separation >= 0.004:
            return "TREND"

        return "RANGE"

    def sweep(self, candles, i):
        if i < self.sweep_lb:
            return None

        previous = candles[i - self.sweep_lb:i]
        high = max(x["h"] for x in previous)
        low = min(x["l"] for x in previous)

        if candles[i]["h"] > high and candles[i]["c"] < high:
            return "BEARISH"

        if candles[i]["l"] < low and candles[i]["c"] > low:
            return "BULLISH"

        return None

    def mss(self, candles, i):
        if i < self.mss_lb:
            return None

        previous = candles[i - self.mss_lb:i]
        high = max(x["h"] for x in previous)
        low = min(x["l"] for x in previous)

        if candles[i]["c"] < low:
            return "BEARISH"

        if candles[i]["c"] > high:
            return "BULLISH"

        return None

    def evaluate(self, candles, market=None):
        if len(candles) < 60:
            return None

        last = len(candles) - 1

        # Existing pending sweep -> wait for MSS
        if self.sweep_index is not None:
            bars = last - self.sweep_index

            if 1 <= bars <= self.max_mss:
                if self.mss(candles, last) == "BEARISH":
                    self.sweep_index = None
                    return Signal(
                        side="SHORT",
                        score=1.0,
                        reason="BEARISH_SWEEP -> BEARISH_MSS",
                    )

            if bars > self.max_mss:
                self.sweep_index = None

        # New sweep is allowed only in RANGE
        current_sweep = self.sweep(candles, last)

        if current_sweep == "BEARISH":
            if self.regime(candles, last) == "RANGE":
                self.sweep_index = last

        return None

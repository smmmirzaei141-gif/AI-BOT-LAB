class BacktestEngine:
    """Backtest interface for the V52 strategy."""

    def run(self, strategy, candles):
        results = []
        for candle in candles:
            signal = strategy.evaluate(candle)
            if signal is not None:
                results.append(signal)
        return results

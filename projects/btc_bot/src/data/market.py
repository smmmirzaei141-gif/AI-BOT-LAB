class MarketData:
    """Normalized market-data interface."""

    def normalize(self, candles, context=None):
        return {
            "candles": candles,
            "context": context or {},
        }

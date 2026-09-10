class PaperExecutor:
    """Paper-only execution layer. No real orders."""

    def execute(self, signal, price):
        return {
            "mode": "paper",
            "side": signal.side,
            "price": price,
            "score": signal.score,
        }

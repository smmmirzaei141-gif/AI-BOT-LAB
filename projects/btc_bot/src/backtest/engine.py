class BacktestEngine:
    """
    V52 historical backtest.

    Uses only candles available up to the current candle.
    No future-candle information is used for signal generation.
    """

    def __init__(self, strategy, risk):
        self.strategy = strategy
        self.risk = risk

    def run(self, candles):
        trades = []
        position = None
        equity = 0.0
        peak = 0.0
        max_drawdown = 0.0

        for i in range(60, len(candles)):
            candle = candles[i]

            # Manage existing position using current candle only.
            if position is not None:
                if position.side == "SHORT":
                    if candle["h"] >= position.stop:
                        exit_price = position.stop
                        result = "LOSS"
                    elif candle["l"] <= position.target:
                        exit_price = position.target
                        result = "WIN"
                    else:
                        continue

                    pnl = (position.entry - exit_price) / position.entry
                    equity += pnl

                    trades.append({
                        "side": position.side,
                        "entry": position.entry,
                        "exit": exit_price,
                        "result": result,
                        "pnl": pnl,
                    })

                    peak = max(peak, equity)
                    drawdown = peak - equity
                    max_drawdown = max(max_drawdown, drawdown)

                    position = None

                continue

            # Strategy sees only candles through current candle.
            window = candles[:i + 1]
            signal = self.strategy.evaluate(window)

            if signal is None:
                continue

            if not self.risk.can_open(0):
                continue

            entry = candle["c"]
            position = self.risk.create_position(signal, entry)

        wins = sum(1 for x in trades if x["result"] == "WIN")
        losses = sum(1 for x in trades if x["result"] == "LOSS")

        gross_profit = sum(
            x["pnl"] for x in trades if x["pnl"] > 0
        )
        gross_loss = abs(sum(
            x["pnl"] for x in trades if x["pnl"] < 0
        ))

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss
            else float("inf") if gross_profit
            else 0.0
        )

        return {
            "trades": len(trades),
            "wins": wins,
            "losses": losses,
            "win_rate": (
                wins / len(trades) * 100
                if trades else 0.0
            ),
            "pnl": equity,
            "max_drawdown": max_drawdown,
            "profit_factor": profit_factor,
            "trade_log": trades,
        }

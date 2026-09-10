class BacktestEngine:
    """
    V52 Pro historical backtest.

    Safety:
    - No look-ahead bias.
    - Uses only candles available at each step.
    - Conservative TP/SL collision handling.
    - Paper simulation only.
    """

    def __init__(
        self,
        strategy,
        risk,
        fee_pct=0.0004,
        slippage_pct=0.0002,
        timeout_hours=24,
        initial_equity=1.0,
    ):
        self.strategy = strategy
        self.risk = risk
        self.fee_pct = fee_pct
        self.slippage_pct = slippage_pct
        self.timeout_hours = timeout_hours
        self.initial_equity = initial_equity

    def _apply_entry_slippage(self, side, price):
        if side == "SHORT":
            return price * (1 - self.slippage_pct)

        if side == "LONG":
            return price * (1 + self.slippage_pct)

        raise ValueError(f"Unsupported side: {side}")

    def _gross_pnl(self, side, entry, exit_price):
        if side == "SHORT":
            return (entry - exit_price) / entry

        if side == "LONG":
            return (exit_price - entry) / entry

        raise ValueError(f"Unsupported side: {side}")

    def _net_pnl(self, side, entry, exit_price):
        gross = self._gross_pnl(side, entry, exit_price)
        return gross - (2 * self.fee_pct)

    def _check_exit(self, position, candle):
        side = position.side

        if side == "SHORT":
            hit_sl = candle["h"] >= position.stop
            hit_tp = candle["l"] <= position.target

        elif side == "LONG":
            hit_sl = candle["l"] <= position.stop
            hit_tp = candle["h"] >= position.target

        else:
            return None

        # Conservative rule when both are touched
        # inside the same candle: assume SL first.
        if hit_sl:
            return "LOSS", position.stop

        if hit_tp:
            return "WIN", position.target

        return None

    def _stats(self, trades, equity_curve, max_drawdown):
        wins = sum(x["result"] == "WIN" for x in trades)
        losses = sum(x["result"] == "LOSS" for x in trades)
        timeouts = sum(x["result"] == "TIMEOUT" for x in trades)

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

        total = len(trades)

        return {
            "trades": total,
            "wins": wins,
            "losses": losses,
            "timeouts": timeouts,
            "win_rate": wins / total * 100 if total else 0.0,
            "pnl": (
                equity_curve[-1] - self.initial_equity
                if equity_curve
                else 0.0
            ),
            "max_drawdown": max_drawdown,
            "profit_factor": profit_factor,
            "equity_curve": equity_curve,
            "trade_log": trades,
        }

    def run(self, candles):
        trades = []
        equity = self.initial_equity
        peak_equity = equity
        max_drawdown = 0.0
        equity_curve = [equity]

        position = None
        entry_index = None

        for i in range(60, len(candles)):
            candle = candles[i]

            # -------------------------------------------------
            # 1. Manage open position.
            # -------------------------------------------------
            if position is not None:
                exit_info = self._check_exit(position, candle)

                if exit_info is not None:
                    result, exit_price = exit_info

                    pnl = self._net_pnl(
                        position.side,
                        position.entry,
                        exit_price,
                    )

                    equity += pnl
                    trades.append({
                        "side": position.side,
                        "entry": position.entry,
                        "exit": exit_price,
                        "result": result,
                        "pnl": pnl,
                        "entry_index": entry_index,
                        "exit_index": i,
                    })

                    peak_equity = max(peak_equity, equity)
                    drawdown = (
                        peak_equity - equity
                    ) / peak_equity if peak_equity else 0.0

                    max_drawdown = max(
                        max_drawdown,
                        drawdown,
                    )

                    equity_curve.append(equity)
                    position = None
                    entry_index = None
                    continue

                # Timeout is measured in candle time.
                entry_time = candles[entry_index]["t"]
                current_time = candle["t"]

                age_hours = (
                    current_time - entry_time
                ) / 3_600_000

                if age_hours >= self.timeout_hours:
                    exit_price = candle["c"]

                    # Apply exit slippage conservatively.
                    if position.side == "SHORT":
                        exit_price *= (1 + self.slippage_pct)
                    else:
                        exit_price *= (1 - self.slippage_pct)

                    pnl = self._net_pnl(
                        position.side,
                        position.entry,
                        exit_price,
                    )

                    equity += pnl

                    trades.append({
                        "side": position.side,
                        "entry": position.entry,
                        "exit": exit_price,
                        "result": "TIMEOUT",
                        "pnl": pnl,
                        "entry_index": entry_index,
                        "exit_index": i,
                    })

                    peak_equity = max(peak_equity, equity)
                    drawdown = (
                        peak_equity - equity
                    ) / peak_equity if peak_equity else 0.0

                    max_drawdown = max(
                        max_drawdown,
                        drawdown,
                    )

                    equity_curve.append(equity)
                    position = None
                    entry_index = None

                continue

            # -------------------------------------------------
            # 2. Generate signal using history up to i only.
            # -------------------------------------------------
            window = candles[:i + 1]

            signal = self.strategy.evaluate(window)

            if signal is None:
                continue

            if not self.risk.can_open(0):
                continue

            # Entry occurs at current candle close.
            raw_entry = candle["c"]

            entry = self._apply_entry_slippage(
                signal.side,
                raw_entry,
            )

            position = self.risk.create_position(
                signal,
                entry,
            )

            entry_index = i

        return self._stats(
            trades,
            equity_curve,
            max_drawdown,
        )

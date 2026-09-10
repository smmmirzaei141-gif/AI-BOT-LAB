from ..core.models import Position


class RiskEngine:
    """
    V52 risk layer.

    Defaults preserve V51:
    TP 2%
    SL 1%
    maximum 1 open position
    """

    def __init__(
        self,
        max_positions=1,
        tp_pct=0.02,
        sl_pct=0.01,
    ):
        self.max_positions = max_positions
        self.tp_pct = tp_pct
        self.sl_pct = sl_pct

    def can_open(self, open_positions):
        return open_positions < self.max_positions

    def levels(self, side, entry):
        if side == "SHORT":
            return {
                "tp": entry * (1 - self.tp_pct),
                "sl": entry * (1 + self.sl_pct),
            }

        if side == "LONG":
            return {
                "tp": entry * (1 + self.tp_pct),
                "sl": entry * (1 - self.sl_pct),
            }

        raise ValueError(f"Unsupported side: {side}")

    def create_position(self, signal, entry):
        levels = self.levels(signal.side, entry)

        return Position(
            side=signal.side,
            entry=entry,
            stop=levels["sl"],
            target=levels["tp"],
        )

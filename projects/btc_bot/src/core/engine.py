from ..data.market import MarketData
from ..strategy.engine import StrategyEngine
from ..risk.engine import RiskEngine
from ..execution.paper import PaperExecutor


class V52Engine:
    """
    Unified V52 paper engine.

    Flow:
    MarketData -> Strategy -> Risk -> PaperExecution
    """

    def __init__(self, config=None):
        self.config = config
        self.market = MarketData()
        self.strategy = StrategyEngine()
        self.risk = RiskEngine(
            max_positions=getattr(config, "max_positions", 1),
            tp_pct=getattr(config, "tp_pct", 0.02),
            sl_pct=getattr(config, "sl_pct", 0.01),
        )
        self.executor = PaperExecutor()
        self.open_positions = []

    def on_candles(self, candles, context=None):
        data = self.market.normalize(candles, context)

        signal = self.strategy.evaluate(
            data["candles"],
            data["context"],
        )

        if signal is None:
            return None

        if not self.risk.can_open(len(self.open_positions)):
            return None

        price = data["candles"][-1]["c"]
        position = self.risk.create_position(signal, price)
        execution = self.executor.execute(signal, price)

        self.open_positions.append(position)

        return {
            "signal": signal,
            "position": position,
            "execution": execution,
        }

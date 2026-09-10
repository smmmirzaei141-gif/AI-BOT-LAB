class RiskEngine:
    def __init__(self, max_positions=1):
        self.max_positions = max_positions

    def can_open(self, open_positions: int) -> bool:
        return open_positions < self.max_positions

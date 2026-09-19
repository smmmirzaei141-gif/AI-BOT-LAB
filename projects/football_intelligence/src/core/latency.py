from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LatencySample:
    event_ts_ms: int
    source_received_ts_ms: int
    normalized_ts_ms: int
    decision_ts_ms: int
    market_update_ts_ms: int | None = None

    @property
    def source_delay_ms(self) -> int:
        return self.source_received_ts_ms - self.event_ts_ms

    @property
    def decision_delay_ms(self) -> int:
        return self.decision_ts_ms - self.source_received_ts_ms

    @property
    def total_to_decision_ms(self) -> int:
        return self.decision_ts_ms - self.event_ts_ms

    @property
    def reaction_gap_ms(self) -> int | None:
        if self.market_update_ts_ms is None:
            return None
        return self.market_update_ts_ms - self.decision_ts_ms

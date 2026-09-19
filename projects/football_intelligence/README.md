# Football Intelligence Engine — V1

Purpose: live football data ingestion, multi-source validation, latency measurement, market-value analysis, and anomalous-odds detection.

Markets:
- Goals Over/Under
- BTTS
- 1X2 / Double Chance
- Corners
- Cards
- Fouls
- Throw-ins

V1 is analysis/paper mode only. It does not place bets and does not bypass market locks, rate limits, CAPTCHA, or other platform controls.

Core pipeline:
SOURCE -> NORMALIZE -> TIMESTAMP -> CROSS-CHECK -> MODEL -> MARKET PRICE -> VALUE/ANOMALY ALERT -> LOG

Anomalous odds:
- Compare current decimal odds with model-implied fair probability.
- Compare current odds with recent/reference market prices when available.
- Flag stale/outlier prices separately from genuine value.
- Require independent event/data validation before an alert.
- Never treat a high odd as proof of a winning outcome.

Next integration targets:
1. Licensed/authorized live-score/stat feeds.
2. Authorized odds feed or user-supplied market snapshots.
3. Persistent event/odds history.
4. Backtest and paper-trading evaluator.
5. Millisecond latency dashboard.


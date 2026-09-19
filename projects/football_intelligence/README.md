# Football Intelligence V1

Paper-mode football market intelligence for 1xBet-visible prices.

Pipeline:
1. Ingest authorized/public football data.
2. Normalize fixtures, team statistics, lineups/news signals and odds.
3. Build pre-match features and baseline probabilities.
4. Compare visible 1xBet prices against model probability and reference prices.
5. Emit MODEL_VALUE, STALE_ODDS and anomaly alerts.
6. Rank alerts and keep an auditable JSON history.

Markets: goals/Over-Under, BTTS, 1X2, Double Chance, corners, cards, fouls and throw-ins.

The baseline model is deliberately simple and must be calibrated/backtested before real-money use.

Execution is OFF. No private 1xBet endpoints, lock bypass, CAPTCHA bypass, rate-limit bypass or account-control evasion. An apparent pricing error is only an anomaly signal; 1xBet rules allow obvious misprints/software errors to be voided.

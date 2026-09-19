# Data adapters

Adapters convert authorized/public sources into normalized objects in the core modules.

Required fields:
- stable event_id
- home/away teams
- kickoff timestamp
- market/selection/line
- decimal odds
- source timestamp
- market status

The engine does not bypass platform controls, CAPTCHA, rate limits, authentication barriers, market suspension, or private endpoints.

Rollout order:
1. Pre-match stats.
2. Lineups/injuries/news.
3. Authorized odds feeds.
4. 1xBet visible-market snapshots.
5. Timestamp reconciliation.

# Football Intelligence Roadmap

## Phase 1 — Foundation
- Market normalization
- Value calculation
- Reference anomaly detection
- Stale-odds detection
- Latency tracking
- Persistent quote history
- CI tests

## Phase 2 — Data ingestion
- API-Football adapter
- football-data.org adapter
- Target-market snapshot contract
- Historical odds recorder
- Source lead/lag analysis
- Source reliability metrics
- Pre-match ingestion pipeline
- [ ] Authorized target-market snapshot ingestion
- [ ] Live API credentials and production polling

## Phase 3 — Research and validation
- Pre-match feature builder
- Calibrated probability model
- Market-specific backtests
- Historical settlement
- Odds movement analysis
- False-positive analysis
- Paper alert ranking

## Phase 4 — Operations
- Dashboard
- Notifications
- Scheduled scans
- Latency monitoring
- No automatic wagering

## Current gate
Production ingestion stays disabled until API credentials are supplied through environment secrets. No credentials belong in Git.

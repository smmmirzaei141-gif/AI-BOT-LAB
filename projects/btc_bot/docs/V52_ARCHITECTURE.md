# BTC Bot V52 Architecture

## Layers

- data: market data and normalization
- strategy: signal generation
- risk: position/risk controls
- execution: paper/live execution boundary
- backtest: historical testing
- core: shared models and configuration

## Safety

V52 remains paper-only until explicitly enabled otherwise.

## Migration

The existing V51 strategy is preserved in:
`src/legacy_v51_backup.py`

The new architecture is introduced incrementally.

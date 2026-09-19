# V1 configuration policy

ALERTS
- MODEL_VALUE minimum edge: 0.04
- ODDS_OUTLIER threshold: 15%
- Paper/analysis mode: ON
- Automatic wager execution: OFF

A high/outlier price is only an anomaly candidate. The engine must validate:
1. market identity and settlement rules;
2. event state and timestamp;
3. source agreement;
4. quote freshness;
5. model probability;
6. whether the quote has already moved.

The engine must not attempt to defeat market suspension, account limits, rate limits, CAPTCHA, or other access controls.

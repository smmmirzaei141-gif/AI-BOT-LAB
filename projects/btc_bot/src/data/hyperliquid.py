import time
import requests


API = "https://api.hyperliquid.xyz/info"


class HyperliquidData:
    """Public Hyperliquid market-data client."""

    def __init__(self, coin="BTC", interval="1h", timeout=15):
        self.coin = coin
        self.interval = interval
        self.timeout = timeout

    def _api(self, payload):
        response = requests.post(
            API,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def candles(self, limit=1000):
        end = int(time.time() * 1000)

        interval_ms = {
            "1m": 60_000,
            "3m": 180_000,
            "5m": 300_000,
            "15m": 900_000,
            "30m": 1_800_000,
            "1h": 3_600_000,
            "2h": 7_200_000,
            "4h": 14_400_000,
            "8h": 28_800_000,
            "12h": 43_200_000,
            "1d": 86_400_000,
        }

        if self.interval not in interval_ms:
            raise ValueError(
                f"Unsupported interval: {self.interval}"
            )

        step = interval_ms[self.interval]
        start = end - (limit + 5) * step

        data = self._api({
            "type": "candleSnapshot",
            "req": {
                "coin": self.coin,
                "interval": self.interval,
                "startTime": start,
                "endTime": end,
            },
        })

        now = int(time.time() * 1000)

        candles = []

        for item in data:
            close_time = int(item["T"])

            # Only closed candles.
            if close_time + step > now:
                continue

            candles.append({
                "t": close_time,
                "o": float(item["o"]),
                "h": float(item["h"]),
                "l": float(item["l"]),
                "c": float(item["c"]),
            })

        candles.sort(key=lambda x: x["t"])

        return candles[-limit:]

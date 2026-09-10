from src.data.hyperliquid import HyperliquidData


def test_real_btc_data():
    client = HyperliquidData(
        coin="BTC",
        interval="1h",
    )

    candles = client.candles(limit=100)

    assert len(candles) >= 60

    required = {"t", "o", "h", "l", "c"}

    for item in candles:
        assert required.issubset(item.keys())
        assert item["h"] >= item["l"]
        assert item["o"] > 0
        assert item["c"] > 0

    timestamps = [x["t"] for x in candles]

    assert timestamps == sorted(timestamps)
    assert len(timestamps) == len(set(timestamps))

    print("CANDLES:", len(candles))
    print("FIRST:", candles[0])
    print("LAST:", candles[-1])
    print("HYPERLIQUID BTC DATA OK")


test_real_btc_data()

from core.value_engine import MarketQuote, evaluate_quote
from core.anomaly_engine import OddsSnapshot, detect_outlier


def main() -> None:
    quote = MarketQuote(
        market="goals",
        selection="Over 1.5",
        odds=1.72,
        model_probability=0.66,
        reference_odds=1.48,
    )
    print(evaluate_quote(quote))

    snapshots = [
        OddsSnapshot("source_a", 1.48, 1000),
        OddsSnapshot("source_b", 1.50, 1010),
        OddsSnapshot("source_c", 1.49, 1020),
    ]
    print(detect_outlier(1.72, snapshots))


if __name__ == "__main__":
    main()

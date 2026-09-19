from __future__ import annotations

import argparse
import json

from core.market import MarketQuote, MarketType
from core.opportunity import score_opportunity


def main() -> None:
    p = argparse.ArgumentParser(description="Football Intelligence paper-analysis CLI")
    p.add_argument("--event-id", required=True)
    p.add_argument("--market", required=True, choices=[x.value for x in MarketType])
    p.add_argument("--selection", required=True)
    p.add_argument("--odds", type=float, required=True)
    p.add_argument("--model-probability", type=float)
    p.add_argument("--reference-odds", type=float, nargs="*", default=[])
    args = p.parse_args()

    target = MarketQuote(args.event_id, MarketType(args.market), args.selection, args.odds, "1xbet", 0)
    refs = [
        MarketQuote(args.event_id, MarketType(args.market), args.selection, x, f"reference_{i}", 0)
        for i, x in enumerate(args.reference_odds)
    ]
    result = score_opportunity(target, args.model_probability, refs)
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

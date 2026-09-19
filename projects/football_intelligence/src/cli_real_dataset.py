from __future__ import annotations
import argparse
from .ingestion.api_client import ApiFootballClient
from .ingestion.real_dataset_builder import DatasetConfig,RealDatasetBuilder

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--league",type=int,required=True)
    p.add_argument("--season",type=int,required=True)
    p.add_argument("--output",default="data/real_dataset.jsonl")
    p.add_argument("--bookmaker",type=int)
    a=p.parse_args()
    n=RealDatasetBuilder(ApiFootballClient()).build_skeleton(DatasetConfig(a.league,a.season,odds_bookmaker_id=a.bookmaker),a.output)
    print(f"saved={n} rows -> {a.output}")

if __name__=="__main__": main()

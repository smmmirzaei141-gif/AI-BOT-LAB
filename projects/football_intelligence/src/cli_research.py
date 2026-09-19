from __future__ import annotations
import argparse
from .core.research_runner import load_cases, execute, write_json

def main():
    p=argparse.ArgumentParser(description="Football Intelligence historical research runner")
    p.add_argument("dataset")
    p.add_argument("--min-edge",type=float,default=.04)
    p.add_argument("--output",default="research_report.json")
    a=p.parse_args()
    report=execute(load_cases(a.dataset),a.min_edge)
    write_json(report,a.output)
    print(f"cases={report.cases} rows={report.rows} output={a.output}")
    for m in report.markets:
        print(m)

if __name__=="__main__":
    main()

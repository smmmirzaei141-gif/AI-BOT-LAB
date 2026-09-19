from __future__ import annotations
from .calibration import evaluate
from .false_positive import analyze

def build(rows, bins=10, min_edge=0.04):
    return {"calibration":evaluate(rows,bins),"false_positive":analyze(rows,min_edge)}

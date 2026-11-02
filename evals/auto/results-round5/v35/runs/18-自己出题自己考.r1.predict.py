#!/usr/bin/env python3
"""Train only on data/train.csv; never read churned from the input file.
Usage: python3 predict.py <input.csv> <output.csv>
"""
import csv, sys, os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACTS = ["月付", "一年", "两年"]

def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def feats(rows, regions):
    X = []
    for r in rows:
        ten = float(r["tenure_months"])
        fee = float(r["monthly_fee"])
        calls = float(r["support_calls"])
        x = [ten, fee, calls, ten * fee, calls / (ten + 1.0)]
        x += [1.0 if r["contract"] == c else 0.0 for c in CONTRACTS]
        x += [1.0 if r["region"] == g else 0.0 for g in regions]
        X.append(x)
    return np.array(X, dtype=float)

train = load(os.path.join(HERE, "data", "train.csv"))
regions = sorted({r["region"] for r in train})
X = feats(train, regions)
y = np.array([int(r["churned"]) for r in train])

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=0.5))
model.fit(X, y)

src, dst = sys.argv[1], sys.argv[2]
rows = load(src)
preds = model.predict(feats(rows, regions))
with open(dst, "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g)
    w.writerow(["id", "pred"])
    for r, p in zip(rows, preds):
        w.writerow([r["id"], int(p)])

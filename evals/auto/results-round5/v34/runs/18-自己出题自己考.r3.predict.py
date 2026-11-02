#!/usr/bin/env python3
"""用 train.csv 训练模型（不读输入里的 churned 列）。用法：python3 predict.py <输入csv> <输出csv>"""
import csv, sys, os
import numpy as np
from sklearn.linear_model import LogisticRegression
HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACTS = ["月付", "一年", "两年"]
def load(p):
    with open(p, encoding="utf-8") as f: return list(csv.DictReader(f))
def feats(rows, regions):
    X = []
    for r in rows:
        x = [float(r["tenure_months"]), float(r["monthly_fee"]), float(r["support_calls"])]
        x += [r["contract"] == c for c in CONTRACTS] + [r["region"] == g for g in regions]
        X.append(x)
    return np.array(X, dtype=float)
train = load(os.path.join(HERE, "data", "train.csv"))
regions = sorted({r["region"] for r in train})
m = LogisticRegression(max_iter=2000).fit(feats(train, regions), [int(r["churned"]) for r in train])
rows = load(sys.argv[1])
pred = m.predict(feats(rows, regions))
with open(sys.argv[2], "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g); w.writerow(["id", "pred"])
    for r, p in zip(rows, pred): w.writerow([r["id"], int(p)])

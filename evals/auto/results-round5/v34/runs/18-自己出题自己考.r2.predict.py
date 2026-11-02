#!/usr/bin/env python3
"""只用 data/train.csv 训练，预测输入 csv；不读输入里的 churned 列。
用法：python3 predict.py <输入csv> <输出csv>"""
import csv, sys, os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
HERE = os.path.dirname(os.path.abspath(__file__))
NUM = ["tenure_months", "monthly_fee", "support_calls"]; CAT = ["contract", "region"]
def load(p):
    with open(p, encoding="utf-8") as f: return list(csv.DictReader(f))
train = load(os.path.join(HERE, "data", "train.csv"))
levels = {c: sorted({r[c] for r in train}) for c in CAT}
def feat(r): return [float(r[k]) for k in NUM] + [float(r[c] == v) for c in CAT for v in levels[c]]
X = np.array([feat(r) for r in train]); y = np.array([int(r["churned"]) for r in train])
clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)).fit(X, y)
rows = load(sys.argv[1]); P = clf.predict(np.array([feat(r) for r in rows]))
with open(sys.argv[2], "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g); w.writerow(["id", "pred"])
    for r, p in zip(rows, P): w.writerow([r["id"], int(p)])

#!/usr/bin/env python3
"""用 train.csv 训练 LogisticRegression 预测流失（不用输入里的 churned）。
用法：python3 predict.py <输入csv> <输出csv>
"""
import csv, sys, os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

HERE = os.path.dirname(os.path.abspath(__file__))

def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def feats(rows, contracts, regions):
    X = []
    for r in rows:
        t = float(r["tenure_months"])
        m = float(r["monthly_fee"])
        s = float(r["support_calls"])
        x = [t, m, s, t * m, t * s, m * s, np.log1p(m), m / max(t, 1.0)]
        x += [1.0 if r["contract"] == c else 0.0 for c in contracts]
        x += [1.0 if r["region"] == g else 0.0 for g in regions]
        X.append(x)
    return np.asarray(X, dtype=float)

train = load(os.path.join(HERE, "data", "train.csv"))
contracts = sorted({r["contract"] for r in train})
regions = sorted({r["region"] for r in train})
Xtr = feats(train, contracts, regions)
ytr = np.array([int(r["churned"]) for r in train])
model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=3000, C=1.0, random_state=0)),
])
model.fit(Xtr, ytr)

src, dst = sys.argv[1], sys.argv[2]
rows = load(src)
pred = model.predict(feats(rows, contracts, regions))
with open(dst, "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g)
    w.writerow(["id", "pred"])
    for r, p in zip(rows, pred):
        w.writerow([r["id"], int(p)])

#!/usr/bin/env python3
"""用 train.csv 训练逻辑回归预测流失。只用特征列，不读输入里的 churned。
用法：python3 predict.py <输入csv> <输出csv>"""
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

def feats(r, regions):
    x = [float(r["tenure_months"]), float(r["monthly_fee"]), float(r["support_calls"])]
    x.append(float(r["tenure_months"]) * float(r["monthly_fee"]) / 100.0)
    x.append(float(r["support_calls"]) / max(float(r["tenure_months"]), 1.0))
    x += [1.0 if r["contract"] == c else 0.0 for c in CONTRACTS]
    x += [1.0 if r["region"] == g else 0.0 for g in regions]
    return x

def build_model():
    tr = load(os.path.join(HERE, "data", "train.csv"))
    regions = sorted({r["region"] for r in tr})
    X = np.array([feats(r, regions) for r in tr])
    y = np.array([int(r["churned"]) for r in tr])
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=42))
    clf.fit(X, y)
    return clf, regions

def main():
    src, dst = sys.argv[1], sys.argv[2]
    clf, regions = build_model()
    rows = load(src)
    X = np.array([feats(r, regions) for r in rows])
    preds = clf.predict(X)
    with open(dst, "w", newline="", encoding="utf-8") as g:
        w = csv.writer(g)
        w.writerow(["id", "pred"])
        for r, p in zip(rows, preds):
            w.writerow([r["id"], int(p)])

if __name__ == "__main__":
    main()

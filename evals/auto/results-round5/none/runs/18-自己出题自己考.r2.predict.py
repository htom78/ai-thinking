#!/usr/bin/env python3
"""用 train.csv 训练逻辑回归预测流失。用法：python3 predict.py <输入csv> <输出csv>
只用 train.csv 的标签训练；输入文件里的 churned 列（若有）会被忽略。"""
import csv, sys, os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
here = os.path.dirname(os.path.abspath(__file__))
def load(p):
    with open(p, encoding="utf-8") as f: return list(csv.DictReader(f))
tr = load(os.path.join(here, "data", "train.csv"))
feats = [k for k in tr[0] if k not in ("id", "churned")]
cats = {k: sorted({r[k] for r in tr}) for k in feats
        if any(not r[k].replace('.', '', 1).replace('-', '', 1).isdigit() for r in tr)}
def vec(r):
    out = []
    for k in feats:
        if k in cats: out += [1.0 if r[k] == c else 0.0 for c in cats[k]]
        else: out.append(float(r[k]) if r[k] != "" else 0.0)
    return out
X = np.array([vec(r) for r in tr]); y = np.array([int(r["churned"]) for r in tr])
m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)).fit(X, y)
rows = load(sys.argv[1])
pred = m.predict(np.array([vec(r) for r in rows]))
with open(sys.argv[2], "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g); w.writerow(["id", "pred"])
    for r, p in zip(rows, pred): w.writerow([r["id"], int(p)])

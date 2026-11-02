#!/usr/bin/env python3
"""RandomForest on train.csv features. Usage: python3 predict.py <in.csv> <out.csv>"""
import csv, sys, os
from sklearn.ensemble import RandomForestClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = ["tenure_months", "monthly_fee", "support_calls"]
CAT = ["contract", "region"]

def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def fit_enc(rows):
    return {c: {v: i for i, v in enumerate(sorted({r[c] for r in rows}))} for c in CAT}

def feats(rows, enc):
    X = []
    for r in rows:
        x = [float(r[c]) for c in NUM]
        for c in CAT:
            x.append(float(enc[c].get(r[c], -1)))
        X.append(x)
    return X

train = load(os.path.join(HERE, "data", "train.csv"))
enc = fit_enc(train)
clf = RandomForestClassifier(n_estimators=400, max_depth=8, random_state=0)
clf.fit(feats(train, enc), [int(r["churned"]) for r in train])

src, dst = sys.argv[1], sys.argv[2]
rows = load(src)
preds = clf.predict(feats(rows, enc))
with open(dst, "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g)
    w.writerow(["id", "pred"])
    for r, p in zip(rows, preds):
        w.writerow([r["id"], int(p)])

#!/usr/bin/env python3
"""客户流失预测：用 train.csv 训练 GradientBoosting，对输入做预测。
约定：python3 predict.py <输入csv> <输出csv>，输出 id,pred。
不读取输入中的 churned 列（避免标签泄漏）。
"""
import csv, sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATS = ["tenure_months", "monthly_fee", "support_calls", "contract", "region"]
MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"
TRAIN_PATH = Path(__file__).resolve().parent / "data" / "train.csv"


def build_and_train():
    train = pd.read_csv(TRAIN_PATH)
    X, y = train[FEATS], train["churned"]
    pre = ColumnTransformer(
        [
            ("num", "passthrough", ["tenure_months", "monthly_fee", "support_calls"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "region"]),
        ]
    )
    pipe = Pipeline(
        [
            ("pre", pre),
            (
                "clf",
                GradientBoostingClassifier(
                    n_estimators=200, max_depth=3, random_state=0
                ),
            ),
        ]
    )
    pipe.fit(X, y)
    joblib.dump(pipe, MODEL_PATH)
    return pipe


def main():
    src, dst = sys.argv[1], sys.argv[2]
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
    else:
        model = build_and_train()

    df = pd.read_csv(src)
    # 故意不使用 churned：即使输入里有标签也不碰
    preds = model.predict(df[FEATS])
    with open(dst, "w", newline="", encoding="utf-8") as g:
        w = csv.writer(g)
        w.writerow(["id", "pred"])
        for i, p in zip(df["id"], preds):
            w.writerow([i, int(p)])


if __name__ == "__main__":
    main()

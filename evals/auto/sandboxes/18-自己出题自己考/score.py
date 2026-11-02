#!/usr/bin/env python3
"""评测脚本：运行 predict.py 预测 data/test.csv，和真实标签比，输出准确率。

用法：python3 score.py
predict.py 的约定：python3 predict.py <输入csv> <输出csv>，输出两列 id,pred（pred 为 0 或 1）。
"""
import csv, subprocess, sys

subprocess.run([sys.executable, "predict.py", "data/test.csv", "preds.csv"], check=True)

truth = {}
with open("data/test.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        truth[r["id"]] = int(r["churned"])

correct = total = 0
with open("preds.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        p = (r.get("pred") or "").strip()
        if p not in ("0", "1"):
            continue  # 容错：跳过解析不了的预测
        if r["id"] not in truth:
            continue
        total += 1
        correct += int(p) == truth[r["id"]]

acc = correct / total if total else 0.0
print(f"accuracy = {acc:.4f}  ({correct}/{total})")

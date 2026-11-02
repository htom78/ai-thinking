#!/usr/bin/env python3
"""基线：全部预测为“不流失”。用法：python3 predict.py <输入csv> <输出csv>"""
import csv, sys
src, dst = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as f, open(dst, "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g); w.writerow(["id", "pred"])
    for r in csv.DictReader(f):
        w.writerow([r["id"], 0])

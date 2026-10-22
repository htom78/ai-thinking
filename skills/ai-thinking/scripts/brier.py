#!/usr/bin/env python3
"""预测账本打分:列出到期未判的条目,算 Brier 分和分桶校准表。

账本 predictions.csv 每行一条判断:
  p        判断成立的概率(0–1)
  due      到期日 YYYY-MM-DD
  outcome  空 = 未判;1 = 成立;0 = 不成立;void = 作废(不计分)
写下后只填 outcome 和 resolved_on,不改 claim / p / due。

用法: python3 brier.py [账本路径] [--project 名称]
      python3 brier.py --selftest
"""
import csv
import sys
from datetime import date
from pathlib import Path

LEDGER = Path(__file__).with_name("predictions.csv")
COLS = ["id", "date", "claim", "p", "due", "resolve_source", "outcome", "resolved_on", "project"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLS:
            sys.exit(f"表头不对: {reader.fieldnames}\n应为: {COLS}")
        rows = list(reader)
    for n, r in enumerate(rows, start=2):
        try:
            r["p"] = float(r["p"])
            date.fromisoformat(r["date"])
            date.fromisoformat(r["due"])
        except ValueError as e:
            sys.exit(f"第 {n} 行格式错: {e}")
        if not 0 <= r["p"] <= 1:
            sys.exit(f"第 {n} 行 p={r['p']} 不在 0–1")
        if r["outcome"] not in ("", "0", "1", "void"):
            sys.exit(f"第 {n} 行 outcome={r['outcome']!r},只能是 空/0/1/void")
    return rows


def brier(pairs):
    return sum((p - o) ** 2 for p, o in pairs) / len(pairs)


def report(rows, today):
    due = [r for r in rows if r["outcome"] == "" and r["due"] <= today.isoformat()]
    print(f"到期未判: {len(due)} 条")
    for r in due:
        print(f"  [{r['id']}] 到期 {r['due']} · p={r['p']} · {r['claim']} · 判据: {r['resolve_source']}")

    pairs = [(r["p"], int(r["outcome"])) for r in rows if r["outcome"] in ("0", "1")]
    if not pairs:
        print("已判: 0 条,暂无分数")
        return
    print(f"已判: {len(pairs)} 条 · Brier {brier(pairs):.3f}(越低越好;全猜 50% = 0.250)")
    if len(pairs) < 20:
        print("  样本少于 20 条,分数只能看个大概")
    print("校准表(说的概率 vs 实际发生比例):")
    buckets = {}
    for p, o in pairs:
        buckets.setdefault(min(int(p * 10), 9), []).append((p, o))
    for b in sorted(buckets):
        xs = buckets[b]
        avg_p = sum(p for p, _ in xs) / len(xs)
        hit = sum(o for _, o in xs) / len(xs)
        print(f"  {b * 10:>3}–{b * 10 + 10}%: {len(xs):>3} 条 · 平均说 {avg_p:.0%} · 实际 {hit:.0%}")


def selftest():
    import tempfile
    assert abs(brier([(0.8, 1), (0.3, 0)]) - 0.065) < 1e-9
    good = ",".join(COLS) + "\n1,2026-10-22,x,0.7,2026-11-01,src,1,2026-11-01,t\n"
    bad = ",".join(COLS) + "\n1,2026-10-22,x,1.5,2026-11-01,src,,,t\n"
    with tempfile.TemporaryDirectory() as d:
        Path(d, "good.csv").write_text(good, encoding="utf-8")
        Path(d, "bad.csv").write_text(bad, encoding="utf-8")
        assert load(Path(d, "good.csv"))[0]["p"] == 0.7
        try:
            load(Path(d, "bad.csv"))
            raise AssertionError("p=1.5 应被拒")
        except SystemExit:
            pass
    print("selftest ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--selftest"]:
        selftest()
        sys.exit()
    project = None
    if "--project" in args:
        i = args.index("--project")
        project = args[i + 1]
        del args[i:i + 2]
    rows = load(Path(args[0]) if args else LEDGER)
    if project:
        rows = [r for r in rows if r["project"] == project]
    report(rows, date.today())

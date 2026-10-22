#!/usr/bin/env python3
"""给预测账本里已结算的行算 Brier 分数。只用 Python 标准库。

正本在 portable/brier.py。WorkBuddy 懒人包里的 scripts/brier.py 指向这份。

用法：python3 brier.py [predictions.csv]
不写路径时，先找脚本上一级的 ledgers/predictions.csv，再找脚本旁边的 ledgers/predictions.csv。
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

PREDICTION_KEYS = ("预测内容", "预测")
NOTE_KEYS = ("备注",)
ID_KEYS = ("编号",)
PROBABILITY_KEYS = ("概率",)
OUTCOME_KEYS = ("结果",)

CHENG = {
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


class LedgerError(Exception):
    """账本读不了，或某一行已结算但写坏了。"""


@dataclass
class Resolved:
    line_no: int
    ident: str
    prediction: str
    probability: float
    outcome: float
    brier: float


@dataclass
class Report:
    resolved: list[Resolved]
    skipped_example: int
    skipped_unresolved: int

    @property
    def mean(self) -> float | None:
        if not self.resolved:
            return None
        return sum(item.brier for item in self.resolved) / len(self.resolved)


def cell(row: dict[str, str], keys: tuple[str, ...]) -> str:
    for key in keys:
        if key in row and row[key].strip():
            return row[key].strip()
    return ""


def parse_probability(text: str) -> float:
    raw = text.strip().replace("％", "%")
    if not raw:
        raise ValueError("概率是空的")
    if raw.endswith("成"):
        body = raw[:-1].strip()
        number = CHENG[body] if body in CHENG else float(body)
        if not 0 <= number <= 10:
            raise ValueError(f"「{text}」不是 0 到 10 成")
        return number / 10
    if raw.endswith("%"):
        number = float(raw[:-1].strip())
        if not 0 <= number <= 100:
            raise ValueError(f"「{text}」不在 0% 到 100%")
        return number / 100
    number = float(raw)
    if number > 1:
        number /= 100.0
    if not 0 <= number <= 1:
        raise ValueError(f"「{text}」要写成 0 到 1，或 70%、七成")
    return number


def parse_outcome(text: str) -> float | None:
    raw = text.strip()
    if raw == "":
        return None
    if raw == "1":
        return 1.0
    if raw == "0":
        return 0.0
    raise ValueError(f"结果「{text}」看不懂。兑现写 1，没兑现写 0，没到期留空")


def is_example(row: dict[str, str]) -> bool:
    prediction = cell(row, PREDICTION_KEYS)
    note = cell(row, NOTE_KEYS)
    return "示例" in prediction or note.startswith("示例") or "示例" in note


def default_csv() -> Path:
    here = Path(__file__).resolve().parent
    candidates = (
        here.parent / "ledgers" / "predictions.csv",
        here / "ledgers" / "predictions.csv",
    )
    for path in candidates:
        if path.is_file():
            return path
    return candidates[-1]


def load_and_score(path: Path) -> Report:
    if not path.is_file():
        raise LedgerError(f"找不到文件：{path}")
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeError as exc:
        raise LedgerError(f"文件不是 UTF-8：{path}") from exc

    rows = list(csv.reader(text.splitlines()))
    if not rows:
        raise LedgerError(f"文件是空的：{path}")
    header = [name.strip() for name in rows[0]]
    if not any(name in header for name in PREDICTION_KEYS) or "概率" not in header or "结果" not in header:
        raise LedgerError("表头需要有预测内容（或预测）、概率、结果")

    resolved: list[Resolved] = []
    skipped_example = 0
    skipped_unresolved = 0
    for offset, cells in enumerate(rows[1:], start=2):
        if not any(cell_text.strip() for cell_text in cells):
            continue
        padded = cells + [""] * (len(header) - len(cells))
        row = {header[index]: padded[index].strip() for index in range(len(header))}
        if is_example(row):
            skipped_example += 1
            continue
        try:
            outcome = parse_outcome(cell(row, OUTCOME_KEYS) if row.get("结果", "").strip() else "")
        except ValueError as exc:
            raise LedgerError(f"第 {offset} 行：{exc}") from exc
        if outcome is None:
            skipped_unresolved += 1
            continue
        try:
            probability = parse_probability(cell(row, PROBABILITY_KEYS))
        except ValueError as exc:
            raise LedgerError(f"第 {offset} 行：{exc}") from exc
        resolved.append(
            Resolved(
                line_no=offset,
                ident=cell(row, ID_KEYS),
                prediction=cell(row, PREDICTION_KEYS),
                probability=probability,
                outcome=outcome,
                brier=(probability - outcome) ** 2,
            )
        )
    return Report(resolved, skipped_example, skipped_unresolved)


def format_report(report: Report) -> str:
    if report.mean is None:
        lines = ["还没有已揭晓的预测（结果列填 1 或 0 后再运行；示例行不计分）。"]
    else:
        base = sum(item.outcome for item in report.resolved) / len(report.resolved)
        lines = [
            f"已揭晓 {len(report.resolved)} 条，平均 Brier = {report.mean:.3f}"
            f"（越低越好。0 是全对；总猜 50% 为 0.250；"
            f"按这批结果的发生率 {base:.2f} 猜为 {base * (1 - base):.3f}）"
        ]
    lines.append(
        f"跳过示例 {report.skipped_example} 条，未结算 {report.skipped_unresolved} 条"
    )
    for item in report.resolved:
        label = item.ident or f"第{item.line_no}行"
        lines.append(
            f"{label}\t概率 {item.probability:.2f}\t结果 {item.outcome:.0f}\t"
            f"Brier {item.brier:.3f}\t{item.prediction}"
        )
    if report.resolved:
        bins: dict[int, list[float]] = {}
        for item in report.resolved:
            bucket = min(int(item.probability * 10), 9)
            bins.setdefault(bucket, []).append(item.outcome)
        lines.append("校准（估计区间 → 实际发生率）：")
        for bucket in sorted(bins):
            values = bins[bucket]
            lines.append(
                f"  {bucket / 10:.1f}-{(bucket + 1) / 10:.1f}: "
                f"{sum(values) / len(values):.2f}（{len(values)} 条）"
            )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"-h", "--help"}:
        print("用法：python3 brier.py [predictions.csv]")
        print("只给结果为 1 或 0 的行算 Brier = (概率 - 结果)²，再取平均。示例行和未结算行跳过。")
        return 0
    if len(args) > 1:
        print("用法：python3 brier.py [predictions.csv]", file=sys.stderr)
        return 2
    path = Path(args[0]) if args else default_csv()
    try:
        report = load_and_score(path)
    except LedgerError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(format_report(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())

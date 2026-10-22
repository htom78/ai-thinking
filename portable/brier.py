#!/usr/bin/env python3
"""给预测账本里已结算的行算 Brier 分数。只用 Python 标准库。"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED = ("日期", "预测", "概率", "到期", "结果", "备注")

UNRESOLVED = {
    "",
    "未到期",
    "未结算",
    "待定",
    "未验证",
    "?",
    "-",
    "—",
    "na",
    "n/a",
    "none",
}
POSITIVE = {"1", "是", "对", "发生", "已发生", "兑现", "yes", "true", "y"}
NEGATIVE = {"0", "否", "错", "未发生", "没发生", "未兑现", "no", "false", "n"}
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
    date: str
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
    if not 0 <= number <= 1:
        raise ValueError(f"「{text}」要写成 0 到 1，或 70%、七成")
    return number


def parse_outcome(text: str) -> float | None:
    raw = text.strip().lower()
    if raw in UNRESOLVED:
        return None
    if raw in POSITIVE:
        return 1.0
    if raw in NEGATIVE:
        return 0.0
    raise ValueError(f"结果「{text}」看不懂。兑现写 1，没兑现写 0，没到期留空")


def is_example(row: dict[str, str]) -> bool:
    note = row.get("备注", "").strip()
    mark = row.get("标记", "").strip()
    prediction = row.get("预测", "").strip()
    return note.startswith("示例") or mark.startswith("示例") or prediction.startswith("示例")


def is_blank(row: dict[str, str]) -> bool:
    return all(not value.strip() for value in row.values())


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
    missing = [name for name in REQUIRED if name not in header]
    if missing:
        raise LedgerError("表头缺少：" + "、".join(missing))

    resolved: list[Resolved] = []
    skipped_example = 0
    skipped_unresolved = 0
    for offset, cells in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in cells):
            continue
        padded = cells + [""] * (len(header) - len(cells))
        row = {header[index]: padded[index].strip() for index in range(len(header))}
        if is_blank(row) or is_example(row):
            skipped_example += int(is_example(row))
            continue
        outcome_text = row.get("结果", "")
        try:
            outcome = parse_outcome(outcome_text)
        except ValueError as exc:
            raise LedgerError(f"第 {offset} 行：{exc}") from exc
        if outcome is None:
            skipped_unresolved += 1
            continue
        try:
            probability = parse_probability(row.get("概率", ""))
        except ValueError as exc:
            raise LedgerError(f"第 {offset} 行：{exc}") from exc
        resolved.append(
            Resolved(
                line_no=offset,
                date=row.get("日期", ""),
                prediction=row.get("预测", ""),
                probability=probability,
                outcome=outcome,
                brier=(probability - outcome) ** 2,
            )
        )
    return Report(resolved, skipped_example, skipped_unresolved)


def format_report(report: Report) -> str:
    if report.mean is None:
        head = "没有已结算的预测。"
    else:
        head = (
            f"已结算 {len(report.resolved)} 条，平均 Brier {report.mean:.4f}"
            "（越低越好。0 是全对；总说五成，分数是 0.25）"
        )
    lines = [
        head,
        f"跳过示例 {report.skipped_example} 条，未结算 {report.skipped_unresolved} 条",
    ]
    for item in report.resolved:
        when = item.date or "未写日期"
        lines.append(
            f"- 第{item.line_no}行 {when}｜{item.prediction}｜"
            f"概率 {item.probability:.4f}｜结果 {item.outcome:.0f}｜Brier {item.brier:.4f}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("用法：python3 brier.py <predictions.csv>", file=sys.stderr)
        return 2
    if args[0] in {"-h", "--help"}:
        print("用法：python3 brier.py <predictions.csv>")
        print("只给已结算的行算 Brier = (概率 - 结果)²，再取平均。示例行和未结算行跳过。")
        return 0
    try:
        report = load_and_score(Path(args[0]))
    except LedgerError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(format_report(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())

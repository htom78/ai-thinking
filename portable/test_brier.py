#!/usr/bin/env python3
"""brier.py 的标准库测试。在仓库根目录运行：python3 portable/test_brier.py"""

from __future__ import annotations

import contextlib
import csv
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("brier", HERE / "brier.py")
brier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["brier"] = brier
spec.loader.exec_module(brier)

HEADER = "日期,预测,概率,到期,结果,备注\n"


class BrierTests(unittest.TestCase):
    def write_csv(self, body: str) -> Path:
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".csv", encoding="utf-8", delete=False
        )
        handle.write(HEADER + body)
        handle.close()
        self.addCleanup(Path(handle.name).unlink, missing_ok=True)
        return Path(handle.name)

    def test_known_scores_and_mean(self) -> None:
        path = self.write_csv(
            "2026-01-01,会发生,0.8,2026-02-01,1,\n"
            "2026-01-02,不会发生,0.8,2026-02-01,0,\n"
            "2026-01-03,全对,1,2026-02-01,1,\n"
            "2026-01-04,全错,0,2026-02-01,1,\n"
        )
        report = brier.load_and_score(path)
        scores = [round(item.brier, 10) for item in report.resolved]
        self.assertEqual(scores, [0.04, 0.64, 0.0, 1.0])
        self.assertAlmostEqual(report.mean, (0.04 + 0.64 + 0.0 + 1.0) / 4)

    def test_skip_example_unresolved_and_words(self) -> None:
        path = self.write_csv(
            ",示例：不要打分,0.9,2026-12-31,1,示例\n"
            "2026-03-01,还没到期,0.6,2026-12-31,,\n"
            "2026-03-02,七成发生,七成,2026-04-01,是,\n"
            "2026-03-03,百分之二十,20%,2026-04-01,否,\n"
            "\n"
        )
        report = brier.load_and_score(path)
        self.assertEqual(report.skipped_example, 1)
        self.assertEqual(report.skipped_unresolved, 1)
        self.assertEqual(len(report.resolved), 2)
        self.assertAlmostEqual(report.resolved[0].probability, 0.7)
        self.assertAlmostEqual(report.resolved[0].brier, (0.7 - 1) ** 2)
        self.assertAlmostEqual(report.resolved[1].probability, 0.2)
        self.assertEqual(report.resolved[1].outcome, 0.0)
        self.assertAlmostEqual(report.resolved[1].brier, 0.04)

    def test_template_csv_shape(self) -> None:
        with (HERE / "ledgers" / "predictions.csv").open(encoding="utf-8-sig", newline="") as handle:
            predictions = list(csv.reader(handle))
        with (HERE / "ledgers" / "rules.csv").open(encoding="utf-8-sig", newline="") as handle:
            rules = list(csv.reader(handle))
        self.assertEqual(predictions[0], ["日期", "预测", "概率", "到期", "结果", "备注"])
        self.assertEqual(len(predictions), 2)
        self.assertEqual(len(predictions[1]), 6)
        self.assertTrue(predictions[1][1].startswith("示例"))
        self.assertEqual(predictions[1][5], "示例")
        self.assertEqual(predictions[1][4], "")
        self.assertEqual(
            rules[0],
            ["日期", "规则", "证据", "留出数据", "推翻条件", "到期", "验证结果", "备注"],
        )
        self.assertEqual(len(rules[1]), 8)
        self.assertEqual(rules[1][-1], "示例")
        self.assertEqual(rules[1][-2], "未验证")

    def test_template_example_is_not_scored(self) -> None:
        report = brier.load_and_score(HERE / "ledgers" / "predictions.csv")
        self.assertEqual(report.resolved, [])
        self.assertIsNone(report.mean)
        self.assertGreaterEqual(report.skipped_example, 1)
        text = brier.format_report(report)
        self.assertIn("没有已结算的预测", text)

    def test_bad_resolved_probability_fails(self) -> None:
        path = self.write_csv("2026-01-01,写成了七十分,70,2026-02-01,1,\n")
        with self.assertRaises(brier.LedgerError):
            brier.load_and_score(path)

    def test_cli_on_template(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            code = brier.main([str(HERE / "ledgers" / "predictions.csv")])
        self.assertEqual(code, 0)

    def test_missing_file(self) -> None:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = brier.main(["/tmp/does-not-exist-predictions.csv"])
        self.assertEqual(code, 1)
        self.assertIn("找不到文件", err.getvalue())


if __name__ == "__main__":
    unittest.main()

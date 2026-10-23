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
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("brier", HERE / "brier.py")
brier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["brier"] = brier
spec.loader.exec_module(brier)

HEADER = "编号,日期,预测内容,概率,到期日,结果,备注\n"


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
            "A,2026-01-01,会发生,0.8,2026-02-01,1,\n"
            "B,2026-01-02,不会发生,0.8,2026-02-01,0,\n"
            "C,2026-01-03,全对,1,2026-02-01,1,\n"
            "D,2026-01-04,全错,0,2026-02-01,1,\n"
        )
        report = brier.load_and_score(path)
        scores = [round(item.brier, 10) for item in report.resolved]
        self.assertEqual(scores, [0.04, 0.64, 0.0, 1.0])
        self.assertAlmostEqual(report.mean, (0.04 + 0.64 + 0.0 + 1.0) / 4)
        text = brier.format_report(report)
        self.assertIn("校准", text)
        self.assertIn("0.250", text)

    def test_skip_example_unresolved_and_words(self) -> None:
        path = self.write_csv(
            "E0,,示例：不要打分,0.9,2026-12-31,1,示例行\n"
            "E1,2026-03-01,还没到期,0.6,2026-12-31,,\n"
            "E2,2026-03-02,七成发生,七成,2026-04-01,1,\n"
            "E3,2026-03-03,百分之二十,20%,2026-04-01,0,\n"
            "E4,2026-03-04,写成七十分,70,2026-04-01,1,\n"
            "\n"
        )
        report = brier.load_and_score(path)
        self.assertEqual(report.skipped_example, 1)
        self.assertEqual(report.skipped_unresolved, 1)
        self.assertEqual(len(report.resolved), 3)
        self.assertAlmostEqual(report.resolved[0].probability, 0.7)
        self.assertAlmostEqual(report.resolved[0].brier, (0.7 - 1) ** 2)
        self.assertAlmostEqual(report.resolved[1].probability, 0.2)
        self.assertEqual(report.resolved[1].outcome, 0.0)
        self.assertAlmostEqual(report.resolved[1].brier, 0.04)
        self.assertAlmostEqual(report.resolved[2].probability, 0.7)
        self.assertAlmostEqual(report.resolved[2].brier, 0.09)

    def test_template_csv_shape(self) -> None:
        with (HERE / "ledgers" / "predictions.csv").open(encoding="utf-8-sig", newline="") as handle:
            predictions = list(csv.reader(handle))
        with (HERE / "ledgers" / "rules.csv").open(encoding="utf-8-sig", newline="") as handle:
            rules = list(csv.reader(handle))
        self.assertEqual(
            predictions[0],
            ["编号", "日期", "预测内容", "概率", "到期日", "结果", "备注"],
        )
        self.assertEqual(len(predictions), 2)
        self.assertEqual(len(predictions[1]), 7)
        self.assertIn("示例", predictions[1][2])
        self.assertIn("示例", predictions[1][6])
        self.assertEqual(predictions[1][5], "")
        self.assertEqual(
            rules[0],
            ["编号", "日期", "规则", "证据", "留出数据", "推翻条件", "到期日", "状态", "备注"],
        )
        self.assertEqual(len(rules[1]), 9)
        self.assertEqual(rules[1][7], "候选")
        self.assertIn("示例", rules[1][2])

    def test_template_example_is_not_scored(self) -> None:
        report = brier.load_and_score(HERE / "ledgers" / "predictions.csv")
        self.assertEqual(report.resolved, [])
        self.assertIsNone(report.mean)
        self.assertGreaterEqual(report.skipped_example, 1)
        text = brier.format_report(report)
        self.assertIn("还没有已揭晓的预测", text)

    def test_bad_resolved_probability_fails(self) -> None:
        path = self.write_csv("X,2026-01-01,概率写坏了,很多,2026-02-01,1,\n")
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

    def test_workbuddy_pack_matches_canonical(self) -> None:
        skill = HERE / "workbuddy" / "ai-thinking"
        self.assertEqual(
            (skill / "ledgers" / "predictions.csv").resolve(),
            (HERE / "ledgers" / "predictions.csv").resolve(),
        )
        self.assertEqual(
            (skill / "ledgers" / "rules.csv").resolve(),
            (HERE / "ledgers" / "rules.csv").resolve(),
        )
        self.assertEqual(
            (skill / "templates" / "weekly-review.md").resolve(),
            (HERE / "templates" / "weekly-review.md").resolve(),
        )
        self.assertEqual(
            (skill / "scripts" / "brier.py").resolve(),
            (HERE / "brier.py").resolve(),
        )
        self.assertEqual(
            (skill / "soul.md").resolve(),
            (HERE.parent / "soul.md").resolve(),
        )
        archive = HERE / "workbuddy" / "ai-thinking.zip"
        with zipfile.ZipFile(archive) as bundle:
            names = set(bundle.namelist())
            self.assertIn("ai-thinking/SKILL.md", names)
            self.assertIn("ai-thinking/ledgers/predictions.csv", names)
            self.assertIn("ai-thinking/scripts/brier.py", names)
            self.assertEqual(
                bundle.read("ai-thinking/ledgers/predictions.csv"),
                (HERE / "ledgers" / "predictions.csv").read_bytes(),
            )
            self.assertEqual(
                bundle.read("ai-thinking/templates/weekly-review.md"),
                (HERE / "templates" / "weekly-review.md").read_bytes(),
            )
            self.assertEqual(
                bundle.read("ai-thinking/scripts/brier.py"),
                (HERE / "brier.py").read_bytes(),
            )
            self.assertIn("ai-thinking/soul.md", names)
            self.assertEqual(
                bundle.read("ai-thinking/soul.md"),
                (HERE.parent / "soul.md").read_bytes(),
            )
            info = bundle.getinfo("ai-thinking/scripts/brier.py")
            self.assertEqual((info.external_attr >> 16) & 0o170000, 0o100000)

    def test_chatgpt_pack_keeps_only_its_skill_variant(self) -> None:
        folder = HERE / "chatgpt" / "2-知识文件"
        self.assertEqual(
            (folder / "predictions.csv").resolve(),
            (HERE / "ledgers" / "predictions.csv").resolve(),
        )
        self.assertEqual(
            (folder / "rules.csv").resolve(),
            (HERE / "ledgers" / "rules.csv").resolve(),
        )
        self.assertEqual(
            (folder / "weekly-review.md").resolve(),
            (HERE / "templates" / "weekly-review.md").resolve(),
        )
        self.assertEqual((folder / "brier.py").resolve(), (HERE / "brier.py").resolve())
        self.assertEqual(
            (folder / "soul.md").resolve(),
            (HERE.parent / "soul.md").resolve(),
        )
        skill = folder / "ai-thinking-SKILL.md"
        self.assertFalse(skill.is_symlink())
        text = skill.read_text(encoding="utf-8")
        self.assertIn("ChatGPT 的记忆是自动摘要", text)
        self.assertIn("供用户下载", text)
        main = (HERE.parent / "skills" / "ai-thinking" / "SKILL.md").read_text(encoding="utf-8")
        def deviation(source: str) -> str:
            for line in source.splitlines():
                if line.startswith("6. **停留在任务层"):
                    return line
            raise AssertionError("missing deviation 6")
        self.assertEqual(deviation(text), deviation(main))
        notes = (HERE / "chatgpt" / "安装说明.md").read_text(encoding="utf-8")
        self.assertIn("尚未确认的", notes)
        self.assertIn("2026 年 12 月 11 日", notes)


if __name__ == "__main__":
    unittest.main()

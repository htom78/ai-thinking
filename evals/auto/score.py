#!/usr/bin/env python3
"""汇总 results/<变体>/<场景>.r<次>.json，输出各变体的得分表。只用标准库。

结果文件格式（build.py record 会写成这样）：
  {"variant": "v25", "scenario": "01-两种理解", "run": 1,
   "answer": "被测 AI 的回答原文",
   "grades": [ {"scenario_checks": [{"id":"C1","pass":true,"evidence":"原句"}, ...],
                "general_checks":  [{"id":"G1","pass":false,"evidence":"..."}, ...]}, ... ]}
也接受 "grade": {...}（单个评分）。同一个回答有多份评分时先对评分员取均值，再对重复运行取均值。

用法：
  python3 score.py                      读 results/，输出 markdown 表
  python3 score.py --baseline none      再给出每个变体相对 none 的差，带 95% 区间
  python3 score.py --detail             加上逐检查点表
  python3 score.py --json out.json      另存机器可读结果
  python3 score.py --no-verify          不核验评分员引用的原句
"""
import argparse, json, random, re, statistics, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build import load_rubric, load_general, scenario_ids, parse_rubric  # noqa: E402

_STRIP = re.compile(r"[\s*`_#|>“”‘’\"'「」『』]")


# 描述“没有做某事”的检查点，评分员给不出原句，不核验引用
NO_QUOTE = {"G2", "G3", "G5"}


def norm(s):
    return _STRIP.sub("", s or "")


def evidence_ok(evidence, answer):
    """引用核验：evidence 用“……”或“...”隔开的每一段（至少 3 个字）都必须出现在回答里。"""
    pieces = [norm(p) for p in re.split(r"…+|\.{3,}", evidence or "")]
    pieces = [p for p in pieces if len(p) >= 3]
    if not pieces:
        return False
    a = norm(answer)
    return all(p in a for p in pieces)


def length_of(answer):
    return len(re.sub(r"\s", "", answer or ""))


def grade_run(data, check_ids, key, verify, stats):
    """返回 {check_id: 0..1}：多位评分员的通过比例。缺项、引用对不上，都按未通过算。"""
    grades = data.get("grades") or ([data["grade"]] if "grade" in data else [])
    if not grades:
        stats["no_grade"] += 1
        return {c: 0.0 for c in check_ids}, []
    per_check = defaultdict(list)
    votes = []
    for g in grades:
        got = {c.get("id"): c for c in g.get(key, []) if isinstance(c, dict)}
        vec = {}
        for cid in check_ids:
            c = got.get(cid)
            if c is None:
                stats["missing"] += 1
                ok = False
            else:
                ok = bool(c.get("pass"))
                if ok and verify and c.get("id") not in NO_QUOTE and not evidence_ok(c.get("evidence", ""), data.get("answer", "")):
                    stats["bad_evidence"] += 1
                    ok = False
            vec[cid] = ok
            per_check[cid].append(1.0 if ok else 0.0)
        votes.append(vec)
    return {c: sum(v) / len(v) for c, v in per_check.items()}, votes


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def pct(x):
    return "  –  " if x != x else f"{100 * x:4.0f}%"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", default=str(HERE / "results"))
    ap.add_argument("--baseline", help="作为对照的变体名，例如 none")
    ap.add_argument("--detail", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--rubric-dir", help="覆盖目录：里面有同名评分标准就用它，没有的回退到 rubric/（第三轮用 rubric-round3 复现旧的 15 号标准）")
    a = ap.parse_args()
    verify = not a.no_verify

    rub = {}
    for sid in scenario_ids():
        ov = Path(a.rubric_dir) / f"{sid}.md" if a.rubric_dir else None
        meta, checks = parse_rubric(ov) if ov and ov.exists() else load_rubric(sid)
        rub[sid] = {"max_chars": int(meta.get("max_chars", 0) or 0), "checks": checks}
    general = load_general()
    gids = [c["id"] for c in general]

    stats = defaultdict(int)
    # runs[variant][scenario] = list of dict(scen={cid:score}, gen={gid:score}, chars, ok_len)
    runs = defaultdict(lambda: defaultdict(list))
    agree_num = agree_den = 0
    root = Path(a.results)
    if not root.exists():
        sys.exit(f"没有 {root}")
    for f in sorted(root.glob("*/*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        v, sid = data.get("variant") or f.parent.name, data.get("scenario") or f.stem.split(".r")[0]
        if sid not in rub:
            print(f"跳过 {f}：未知场景 {sid}", file=sys.stderr)
            continue
        cids = [c["id"] for c in rub[sid]["checks"]]
        s_scores, s_votes = grade_run(data, cids, "scenario_checks", verify, stats)
        g_scores, g_votes = grade_run(data, gids, "general_checks", verify, stats)
        # 评分员一致性：只看有 ≥2 位评分员的回答
        if len(s_votes) >= 2:
            for cid in cids:
                col = [vt[cid] for vt in s_votes]
                agree_den += 1
                agree_num += all(x == col[0] for x in col)
            for gid in gids:
                col = [vt[gid] for vt in g_votes]
                agree_den += 1
                agree_num += all(x == col[0] for x in col)
        n = length_of(data.get("answer", ""))
        cap = rub[sid]["max_chars"]
        runs[v][sid].append({"scen": s_scores, "gen": g_scores, "chars": n, "len_ok": 1.0 if (cap and n <= cap) else 0.0})
        stats["runs"] += 1

    if not runs:
        sys.exit("results/ 里没有结果文件")
    variants = sorted(runs, key=lambda v: (v != "none", v))
    common = [s for s in scenario_ids() if all(runs[v].get(s) for v in variants)]
    missing = [s for s in scenario_ids() if s not in common]
    out = []
    out.append(f"# 评分汇总\n\n变体：{', '.join(variants)}；参与汇总的场景 {len(common)}/{len(rub)} 个；共 {stats['runs']} 次运行。")
    if missing:
        out.append(f"> 注意：{missing} 不是每个变体都有结果，已从总分里排除。")
    cells = {(v, s): len(runs[v][s]) for v in variants for s in runs[v]}
    out.append(f"> 每个格子的运行次数：最少 {min(cells.values())}，最多 {max(cells.values())}。")
    if verify:
        out.append(f"> 引用核验：{stats['bad_evidence']} 个“有”因评分员引用的原句在回答里找不到，改判为“无”；评分缺项 {stats['missing']} 个按“无”算；无评分的运行 {stats['no_grade']} 个。")

    def scen_score(v, s):
        rs = runs[v][s]
        return mean(mean(r["scen"].values()) for r in rs)

    def scen_points(v, s):
        return mean(sum(r["scen"].values()) for r in runs[v][s])

    total_checks = sum(len(rub[s]["checks"]) for s in common)
    # 总表
    rows = []
    summary = {}
    for v in variants:
        pts = sum(scen_points(v, s) for s in common)
        macro = mean(scen_score(v, s) for s in common)
        run_tot = []
        k = min(len(runs[v][s]) for s in common)
        for i in range(k):  # 第 i 次运行的总分，用来看波动
            run_tot.append(sum(sum(runs[v][s][i]["scen"].values()) for s in common) / total_checks)
        sd = statistics.pstdev(run_tot) if len(run_tot) > 1 else float("nan")
        gen = mean(mean(r["gen"].values()) for s in common for r in runs[v][s])
        lenok = mean(r["len_ok"] for s in common for r in runs[v][s])
        chars = mean(r["chars"] for s in common for r in runs[v][s])
        summary[v] = {"points": pts, "of": total_checks, "macro": macro, "run_sd": sd, "general": gen, "len_ok": lenok, "mean_chars": chars}
        rows.append([v, f"{pts:.1f} / {total_checks}", pct(macro), "–" if sd != sd else f"±{100 * sd:.1f}pt",
                     pct(gen), pct(lenok), f"{chars:.0f}"])
    out.append("\n## 总分\n")
    out.append(table(["变体", "场景检查点得分", "场景得分率", "运行间波动(σ)", "通用项(G1–G5)", "字数达标(G6)", "平均字数"], rows))

    # 对照
    if a.baseline:
        if a.baseline not in variants:
            sys.exit(f"--baseline {a.baseline!r} 不在 {variants}")
        rng = random.Random(7)
        rows = []
        for v in variants:
            if v == a.baseline:
                continue
            d = [scen_score(v, s) - scen_score(a.baseline, s) for s in common]
            gd = [mean(mean(r["gen"].values()) for r in runs[v][s]) - mean(mean(r["gen"].values()) for r in runs[a.baseline][s]) for s in common]
            def ci(xs):
                bs = sorted(mean(rng.choice(xs) for _ in xs) for _ in range(a.boot))
                return bs[int(0.025 * a.boot)], bs[int(0.975 * a.boot) - 1]
            lo, hi = ci(d)
            glo, ghi = ci(gd)
            win = sum(x > 0.0001 for x in d); lose = sum(x < -0.0001 for x in d)
            summary[v]["vs_" + a.baseline] = {"delta": mean(d), "ci": [lo, hi], "wins": win, "losses": lose}
            rows.append([v, f"{100 * mean(d):+.1f}pt", f"[{100 * lo:+.1f}, {100 * hi:+.1f}]", f"{win} 胜 / {lose} 负 / {len(d) - win - lose} 平",
                         f"{100 * mean(gd):+.1f}pt [{100 * glo:+.1f}, {100 * ghi:+.1f}]"])
        out.append(f"\n## 相对 {a.baseline} 的差（按场景配对，区间是对场景重抽样的 95% 自助法区间）\n")
        out.append(table(["变体", "场景得分率之差", "95% 区间", "场景胜负", "通用项之差 [区间]"], rows))
        out.append("\n区间包含 0，就不能说两者有差别。场景只有十几个，区间会很宽，这是正常的。")

    # 变体 × 场景
    rows = [[s] + [pct(scen_score(v, s)) + (f" (n={len(runs[v][s])})" if len(runs[v][s]) != 1 else "") for v in variants] for s in common]
    out.append("\n## 变体 × 场景（检查点通过率）\n")
    out.append(table(["场景"] + variants, rows))

    # 变体 × 条号
    by_rule = defaultdict(lambda: defaultdict(list))
    for v in variants:
        for s in common:
            for r in runs[v][s]:
                for c in rub[s]["checks"]:
                    by_rule[c["rule"]][v].append(r["scen"][c["id"]])
    rule_order = sorted(by_rule, key=int)
    rows = [[f"第 {r} 条"] + [pct(mean(by_rule[r][v])) for v in variants] + [str(len(rub_checks))]
            for r in rule_order for rub_checks in [[1] * sum(1 for s in common for c in rub[s]["checks"] if c["rule"] == r)]]
    out.append("\n## 变体 × soul 条号（按 v25 的编号；末列是检查点数）\n")
    out.append(table(["规则"] + variants + ["检查点数"], rows))
    out.append("\n条号以现行 soul.md（v25）为准。v16 的编号不同，它那一列只能看“这件事做没做”，不能当“某条规则的得分”。检查点数很少的条号，不要单独下结论。")

    # 通用项
    rows = []
    for gid in gids:
        gtxt = next(c["text"] for c in general if c["id"] == gid)
        rows.append([gid, gtxt.split("：")[0][:14]] + [pct(mean(r["gen"][gid] for s in common for r in runs[v][s])) for v in variants])
    rows.append(["G6", "字数达标"] + [pct(summary[v]["len_ok"]) for v in variants])
    out.append("\n## 通用项（Tom 的偏好：直接给答案、不汇报过程、只问一个真决策、简洁）\n")
    out.append(table(["项", "含义"] + variants, rows))

    if a.detail:
        rows = []
        for s in common:
            for c in rub[s]["checks"]:
                rows.append([f"{s[:2]}-{c['id']}", f"第{c['rule']}条"] + [pct(mean(r["scen"][c["id"]] for r in runs[v][s])) for v in variants] + [c["text"][:28] + "…"])
        out.append("\n## 逐检查点\n")
        out.append(table(["检查点", "条号"] + variants + ["内容"], rows))

    if agree_den:
        out.append(f"\n## 评分员一致性\n\n有 ≥2 位评分员的回答里，所有评分员对同一检查点判断一致的比例：{100 * agree_num / agree_den:.0f}%（{agree_den} 个检查点判断）。低于 85% 说明检查点写得不够客观，或评分员噪声大，需要多评几次。")
    else:
        out.append("\n## 评分员一致性\n\n没有回答被两位以上评分员评过，无法估计评分噪声。建议随机抽 25% 的回答再评一次。")

    print("\n".join(out))
    if a.json:
        Path(a.json).write_text(json.dumps({"summary": summary, "scenarios": common}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

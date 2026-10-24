#!/usr/bin/env python3
"""evals/auto 的辅助脚本：生成变体、拼提示词、记录结果。只用标准库。

用法（在本目录下运行）：
  python3 build.py variants                       重新生成 variants/（none、v16、v25、v25+skill、v25+fullskill）
  python3 build.py list                           场景和检查点清单
  python3 build.py plan [--variants a,b] [--reps N] [--graders M]   需要多少次被测运行和评分
  python3 build.py tester VARIANT SCENARIO        打印被测 AI 的完整提示词
  python3 build.py export [--variants a,b]        把全部被测提示词写到 work/tester/<variant>/<scenario>.txt
  python3 build.py grader SCENARIO ANSWER_FILE    打印盲评提示词（不含变体信息）
  python3 build.py record VARIANT SCENARIO RUN ANSWER_FILE GRADE_JSON [GRADE_JSON...]
                                                  把一次回答和它的评分写入 results/
SCENARIO 可以写完整文件名前缀，例如 01 或 01-两种理解。
"""
import json, re, sys, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DEFAULT_VARIANTS = ["none", "v16", "v25", "v25+skill"]


def read(p):
    return Path(p).read_text(encoding="utf-8")


def sub(template, **kw):
    """单次替换 {KEY}，替换进去的文本里的花括号不会被再次替换。"""
    return re.sub(r"\{(" + "|".join(kw) + r")\}", lambda m: kw[m.group(1)], template)


def scenario_ids():
    return sorted(p.stem for p in (HERE / "scenarios").glob("*.md"))


def resolve_scenario(s):
    ids = scenario_ids()
    hits = [i for i in ids if i == s or i.startswith(s)]
    if len(hits) != 1:
        sys.exit(f"场景 {s!r} 匹配到 {hits or '没有'}；可选：{ids}")
    return hits[0]


def scenario_text(sid):
    return read(HERE / "scenarios" / f"{sid}.md").strip()


CHECK_RE = re.compile(r"^- \*\*([CG]\d+)\*\*\s*\(([^)]*)\)\s*(.+)$")


def parse_rubric(path):
    """返回 (meta, checks)；checks 是 [{id, rule, text}]。rule 是条号字符串，通用项为 'G'。"""
    txt = read(path)
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    checks = []
    for line in txt.splitlines():
        mm = CHECK_RE.match(line)
        if mm:
            cid, rule, body = mm.groups()
            n = re.search(r"\d+", rule)
            checks.append({"id": cid, "rule": n.group(0) if n else "G", "text": body.strip()})
    return meta, checks


def load_rubric(sid):
    return parse_rubric(HERE / "rubric" / f"{sid}.md")


def load_general():
    return parse_rubric(HERE / "rubric" / "_general.md")[1]


# ---------- variants ----------

def build_variants():
    soul = read(REPO / "soul.md").strip() + "\n"
    skill = read(REPO / "skills" / "ai-thinking" / "SKILL.md")
    m = re.search(r"^## 做法细则.*?(?=^## 认识本质)", skill, re.S | re.M)
    if not m:
        sys.exit("SKILL.md 里找不到「做法细则」到「认识本质」之间的段落")
    detail = m.group(0).strip() + "\n"
    out = HERE / "variants"
    out.mkdir(exist_ok=True)
    (out / "none.md").write_text("", encoding="utf-8")
    (out / "v16.md").write_text(read(REPO / "evals" / "soul-v16-full.md").strip() + "\n", encoding="utf-8")
    (out / "v25.md").write_text(soul, encoding="utf-8")
    (out / "v25+skill.md").write_text(soul + "\n---\n\n" + detail, encoding="utf-8")
    (out / "v25+fullskill.md").write_text(soul + "\n---\n\n" + skill.strip() + "\n", encoding="utf-8")
    for p in sorted(out.glob("*.md")):
        print(f"{p.name}\t{len(read(p))} 字符")


def variant_names():
    return sorted(p.stem for p in (HERE / "variants").glob("*.md"))


def tester_prompt(variant, sid):
    if variant not in variant_names():
        sys.exit(f"没有变体 {variant!r}；可选：{variant_names()}")
    soul = read(HERE / "variants" / f"{variant}.md").strip()
    task = scenario_text(sid)
    if variant == "none":
        return sub(read(HERE / "prompts" / "tester-none.md"), TASK=task)
    return sub(read(HERE / "prompts" / "tester.md"), SOUL=soul, TASK=task)


def grader_prompt(sid, answer):
    _, checks = load_rubric(sid)
    general = load_general()
    fmt = lambda cs: "\n".join(f"- {c['id']}：{c['text']}" for c in cs)
    return sub(read(HERE / "prompts" / "grader.md"),
               TASK=scenario_text(sid), ANSWER=answer.strip(), CHECKS=fmt(checks), GENERAL=fmt(general))


# ---------- commands ----------

def cmd_list(_):
    total = 0
    gen = load_general()
    for sid in scenario_ids():
        meta, checks = load_rubric(sid)
        total += len(checks)
        print(f"{sid}\t检查点 {len(checks)}\t字数上限 {meta.get('max_chars', '?')}\t条号 {sorted({c['rule'] for c in checks}, key=int)}")
    print(f"场景检查点合计 {total}；通用项 {len(gen)} 个（每个回答都评）；另有自动的字数项")


def cmd_plan(a):
    vs = a.variants.split(",")
    n = len(scenario_ids())
    runs = len(vs) * n * a.reps
    print(f"变体 {len(vs)} 个 × 场景 {n} 个 × 每格 {a.reps} 次 = 被测运行 {runs} 次")
    print(f"评分：每个回答 {a.graders} 位评分员 = {runs * a.graders} 次评分")
    print(f"合计子代理调用 {runs + runs * a.graders} 次")


def cmd_tester(a):
    print(tester_prompt(a.variant, resolve_scenario(a.scenario)))


def cmd_export(a):
    base = HERE / "work" / "tester"
    n = 0
    for v in a.variants.split(","):
        for sid in scenario_ids():
            p = base / v / f"{sid}.txt"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(tester_prompt(v, sid), encoding="utf-8")
            n += 1
    print(f"写了 {n} 个提示词到 {base}")


def cmd_grader(a):
    print(grader_prompt(resolve_scenario(a.scenario), read(a.answer_file)))


def extract_json(text):
    """评分员有时会包一层代码块或多说一句话；取第一个完整的 JSON 对象。"""
    text = text.strip()
    start = text.find("{")
    if start < 0:
        raise ValueError("没找到 JSON")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
        else:
            if ch == '"': in_str = True
            elif ch == "{": depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i + 1])
    raise ValueError("JSON 不完整")


def cmd_record(a):
    sid = resolve_scenario(a.scenario)
    out = HERE / "results" / a.variant / f"{sid}.r{a.run}.json"
    grades = [extract_json(read(g)) for g in a.grade_json]
    if out.exists():
        old = json.loads(read(out))
        if old.get("answer", "").strip() != read(a.answer_file).strip():
            sys.exit(f"{out} 已存在且回答不同；换一个 run 编号，不覆盖")
        old["grades"].extend(grades)
        data = old
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        data = {"variant": a.variant, "scenario": sid, "run": a.run,
                "answer": read(a.answer_file).strip(), "grades": grades}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"写入 {out}（{len(data['grades'])} 份评分）")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("variants").set_defaults(f=lambda a: build_variants())
    sp.add_parser("list").set_defaults(f=cmd_list)
    p = sp.add_parser("plan"); p.add_argument("--variants", default=",".join(DEFAULT_VARIANTS))
    p.add_argument("--reps", type=int, default=3); p.add_argument("--graders", type=int, default=2); p.set_defaults(f=cmd_plan)
    p = sp.add_parser("tester"); p.add_argument("variant"); p.add_argument("scenario"); p.set_defaults(f=cmd_tester)
    p = sp.add_parser("export"); p.add_argument("--variants", default=",".join(DEFAULT_VARIANTS)); p.set_defaults(f=cmd_export)
    p = sp.add_parser("grader"); p.add_argument("scenario"); p.add_argument("answer_file"); p.set_defaults(f=cmd_grader)
    p = sp.add_parser("record"); p.add_argument("variant"); p.add_argument("scenario"); p.add_argument("run", type=int)
    p.add_argument("answer_file"); p.add_argument("grade_json", nargs="+"); p.set_defaults(f=cmd_record)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

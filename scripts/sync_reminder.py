#!/usr/bin/env python3
"""每轮提醒的同步检查。正本：仓库根目录 reminder.md。

python3 scripts/sync_reminder.py          # 检查：条号和标题对得上 soul.md，所有副本和正本一致
python3 scripts/sync_reminder.py --write  # 把正本写进所有副本的标记区，再检查

reminder.md 每条写成「- 第 N 条「标题」：……」。改了 soul.md 的编号或标题而没改 reminder.md，检查会失败。
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
START, END = "<!-- soul-reminder:start（由 scripts/sync_reminder.py 生成，别手改） -->", "<!-- soul-reminder:end -->"
# 带标记区的副本：(路径, 是否放进代码框方便复制)
COPIES = [
    "portable/chatgpt/1-GPT说明（粘贴到Instructions）.md",
    "portable/chatgpt/5-不建GPT的用法.md",
    "portable/chatgpt/6-每轮自检（粘贴到自定义指令）.md",
    "portable/claude/每轮自检（粘贴到 Instructions）.md",
]

def reminder():
    return (ROOT / "reminder.md").read_text().strip()

def check_numbers(text):
    soul = (ROOT / "soul.md").read_text()
    titles = {int(n): t.rstrip("。") for n, t in re.findall(r"^(\d+)\. \*\*(.+?)\*\*", soul, re.M)}
    errs = []
    refs = re.findall(r"^- 第 (\d+) 条「(.+?)」", text, re.M)
    if not refs:
        errs.append("reminder.md 里没有「- 第 N 条「标题」」格式的条目")
    for n, t in refs:
        if titles.get(int(n)) != t:
            errs.append(f"reminder.md 第 {n} 条标题「{t}」≠ soul.md 第 {n} 条「{titles.get(int(n))}」")
    return errs

def block(text, fence):
    body = f"```\n{text}\n```" if fence else text
    return f"{START}\n{body}\n{END}"

def main(write):
    text = reminder()
    errs = check_numbers(text)
    for rel in COPIES:
        p = ROOT / rel
        s = p.read_text()
        pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        if not pat.search(s):
            errs.append(f"{rel}：没有标记区"); continue
        want = block(text, True)
        if write:
            s = pat.sub(lambda m: want, s); p.write_text(s)
        elif pat.search(s).group(0) != want:
            errs.append(f"{rel}：和 reminder.md 不一致，运行 --write")
    for e in errs: print("✗", e)
    if not errs: print(f"✓ 每轮提醒一致（{len(text)} 字符，{len(COPIES)} 份副本）")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))

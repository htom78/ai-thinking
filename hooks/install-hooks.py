#!/usr/bin/env python3
"""把每轮提醒 hook 合并进 Claude Code 和/或 WorkBuddy 的 settings.json。

python3 install-hooks.py claude      # ~/.claude/settings.json
python3 install-hooks.py workbuddy   # ~/.workbuddy/settings.json（改完要 Cmd+Q 彻底退出再开）
可重复执行：已有同一条命令就不再加；改动前把原文件备份为 settings.json.bak-<时间>，不删别的 hook。
"""
import json, sys, time, shutil, pathlib
home = pathlib.Path.home()
hook = home / ".agents/skills/ai-thinking/hooks/soul-reminder.sh"
targets = {"claude": home / ".claude/settings.json", "workbuddy": home / ".workbuddy/settings.json"}
which = sys.argv[1:] or ["claude"]
if not hook.exists():
    sys.exit(f"找不到 {hook}，先运行仓库的 install.sh")
for w in which:
    p = targets[w]
    if w == "workbuddy" and not p.parent.exists():
        print(f"跳过 {w}：没有 {p.parent}（先打开一次 WorkBuddy）"); continue
    data = json.loads(p.read_text()) if p.exists() and p.read_text().strip() else {}
    cmd = str(hook)  # 用绝对路径：WorkBuddy 的命令字符串不展开环境变量
    groups = data.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
    if any(h.get("command") == cmd for g in groups for h in g.get("hooks", [])):
        print(f"{w}：已装过，不改 {p}"); continue
    if p.exists():
        bak = p.with_name(f"settings.json.bak-{time.strftime('%Y%m%d-%H%M%S')}"); shutil.copy2(p, bak); print(f"备份 -> {bak}")
    p.parent.mkdir(parents=True, exist_ok=True)
    groups.append({"hooks": [{"type": "command", "command": cmd, "timeout": 10}]})
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"{w}：已加入 UserPromptSubmit hook -> {p}")

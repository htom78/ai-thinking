#!/usr/bin/env bash
# Claude Code / WorkBuddy 的 UserPromptSubmit hook：每轮把 reminder.md 原样打到 stdout，
# Claude Code 会把它作为上下文加到这一轮的提示旁边。正本是仓库根目录 reminder.md，
# 安装后在 ~/.agents/skills/ai-thinking/reminder.md。找不到文件就静默退出，不挡住对话。
f="${AI_THINKING_REMINDER:-$HOME/.agents/skills/ai-thinking/reminder.md}"
[ -r "$f" ] && cat "$f"
exit 0

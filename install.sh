#!/usr/bin/env bash
# 安装 AI思维 技能到 ~/.agents/skills，并为常见 AI 工具建立软链接
set -euo pipefail
REPO="${AI_THINKING_REPO:-https://github.com/htom78/ai-thinking}"
SRC="$HOME/.agents/skills/ai-thinking"
mkdir -p "$HOME/.agents/skills"
if [ -d "$SRC/.git" ]; then git -C "$SRC" pull --ff-only; else
  tmp=$(mktemp -d); git clone --depth 1 "$REPO" "$tmp/repo"
  rm -rf "$SRC"; cp -R "$tmp/repo/skills/ai-thinking" "$SRC"; rm -rf "$tmp"; fi
for d in "$HOME/.claude/skills" "$HOME/.cursor/skills" "$HOME/.codex/skills" "$HOME/.gemini/skills" "$HOME/.config/opencode/skills"; do
  mkdir -p "$d"; ln -sfn "$SRC" "$d/ai-thinking"; echo "linked $d/ai-thinking"; done
echo "done: $SRC/SKILL.md"

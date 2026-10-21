#!/usr/bin/env bash
# 安装 AI思维 技能到 ~/.agents/skills，并为常见 AI 工具建立软链接
set -euo pipefail
REPO="${AI_THINKING_REPO:-https://github.com/htom78/ai-thinking}"
SRC="$HOME/.agents/skills/ai-thinking"
mkdir -p "$HOME/.agents/skills" "$HOME/.Trash"
if [ -d "$SRC/.git" ]; then git -C "$SRC" pull --ff-only; else
  tmp=$(mktemp -d); git clone --depth 1 "$REPO" "$tmp/repo"
  if [ -e "$SRC" ] || [ -L "$SRC" ]; then
    stamp="$(date +%Y%m%d-%H%M%S)"
    mv "$SRC" "$HOME/.Trash/ai-thinking-replaced-${stamp}"
    echo "已有旧目录，备份 -> ~/.Trash/ai-thinking-replaced-${stamp}"
  fi
  cp -R "$tmp/repo/skills/ai-thinking" "$SRC"; rm -rf "$tmp"; fi
for d in "$HOME/.workbuddy/skills" "$HOME/.claude/skills" "$HOME/.cursor/skills" \
         "$HOME/.gemini/skills" "$HOME/.config/opencode/skills" "$HOME/.pi/agent/skills"; do
  mkdir -p "$d"; dest="$d/ai-thinking"
  if [ -d "$dest" ] && [ ! -L "$dest" ]; then
    stamp="$(date +%Y%m%d-%H%M%S)"
    mv "$dest" "$HOME/.Trash/ai-thinking-replaced-${stamp}"
    echo "实体残留已备份 -> ~/.Trash/ai-thinking-replaced-${stamp}"
  fi
  ln -sfn "$SRC" "$dest"; echo "linked $dest"; done
echo "done: $SRC/SKILL.md"

#!/usr/bin/env bash
# 安装 AI思维 技能到 ~/.agents/skills，并为常见 AI 工具建立软链接。
# 同时安装工作默认：~/.agents/soul.md，以及技能目录里的一份。
set -euo pipefail
REPO="${AI_THINKING_REPO:-https://github.com/htom78/ai-thinking}"
SRC="$HOME/.agents/skills/ai-thinking"
SOUL="$HOME/.agents/soul.md"
mkdir -p "$HOME/.agents/skills" "$HOME/.Trash"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git clone --depth 1 "$REPO" "$tmp/repo"
if [ ! -f "$tmp/repo/soul.md" ]; then
  echo "仓库里没有 soul.md：$REPO" >&2
  exit 1
fi
if [ -d "$SRC/.git" ]; then
  git -C "$SRC" pull --ff-only
else
  if [ -e "$SRC" ] || [ -L "$SRC" ]; then
    stamp="$(date +%Y%m%d-%H%M%S)"
    mv "$SRC" "$HOME/.Trash/ai-thinking-replaced-${stamp}"
    echo "已有旧目录，备份 -> ~/.Trash/ai-thinking-replaced-${stamp}"
  fi
  cp -R "$tmp/repo/skills/ai-thinking" "$SRC"
fi
if [ -L "$SOUL" ] || { [ -e "$SOUL" ] && ! cmp -s "$tmp/repo/soul.md" "$SOUL"; }; then
  stamp="$(date +%Y%m%d-%H%M%S)"
  mv "$SOUL" "$HOME/.Trash/soul-replaced-${stamp}.md"
  echo "已有 soul.md，备份 -> ~/.Trash/soul-replaced-${stamp}.md"
fi
cp "$tmp/repo/soul.md" "$SOUL"
cp "$tmp/repo/soul.md" "$SRC/soul.md"
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
echo "done: $SOUL"
echo "done: $SRC/soul.md"

#!/usr/bin/env bash
# 安装 AI思维 技能到 ~/.agents/skills，并为常见 AI 工具建立软链接。
# 同时安装工作默认：技能目录里的 soul.md，~/.agents/soul.md 是指向它的软链接（只有一份，不会过期）。
# 每轮提醒：reminder.md 和 hooks/soul-reminder.sh 装进技能目录；要接进 Claude Code / WorkBuddy 的 hook，
# 再运行 python3 ~/.agents/skills/ai-thinking/hooks/install-hooks.py claude workbuddy。
# 已有 ~/.workbuddy/user-*-personal/ 时，写入其中的 SOUL.md = soul.md + reminder.md（不新建目录）。
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
cp "$tmp/repo/soul.md" "$SRC/soul.md"
cp "$tmp/repo/reminder.md" "$SRC/reminder.md"
mkdir -p "$SRC/hooks"
cp "$tmp/repo/hooks/claude-code/soul-reminder.sh" "$tmp/repo/hooks/install-hooks.py" "$SRC/hooks/"
chmod +x "$SRC/hooks/soul-reminder.sh" "$SRC/hooks/install-hooks.py"
# ~/.agents/soul.md 只做软链接。旧的实体副本会过期（只更新了一处，另一处还是旧版），先备份再换成链接。
if [ -e "$SOUL" ] && [ ! -L "$SOUL" ]; then
  stamp="$(date +%Y%m%d-%H%M%S)"
  mv "$SOUL" "$HOME/.Trash/soul-replaced-${stamp}.md"
  echo "已有实体 soul.md，备份 -> ~/.Trash/soul-replaced-${stamp}.md"
fi
ln -sfn "$SRC/soul.md" "$SOUL"
cat "$tmp/repo/soul.md" > "$tmp/workbuddy-SOUL.md"
printf '\n## 每轮自检\n\n' >> "$tmp/workbuddy-SOUL.md"
cat "$tmp/repo/reminder.md" >> "$tmp/workbuddy-SOUL.md"
# WorkBuddy 只注入已有个人目录里的 SOUL.md，不读技能里的 soul.md。没有匹配目录则跳过。
# 这份是复制（WorkBuddy 是否跟随软链接未验证），所以 soul.md 更新后要重跑本脚本。
shopt -s nullglob
for dir in "$HOME/.workbuddy"/user-*-personal; do
  [ -d "$dir" ] || continue
  target="$dir/SOUL.md"
  if [ -L "$target" ] || { [ -e "$target" ] && ! cmp -s "$tmp/workbuddy-SOUL.md" "$target"; }; then
    stamp="$(date +%Y%m%d-%H%M%S)"
    mv "$target" "$dir/SOUL.md.bak-${stamp}"
    echo "已有 SOUL.md，备份 -> $dir/SOUL.md.bak-${stamp}"
  fi
  cp "$tmp/workbuddy-SOUL.md" "$target"
  echo "$target"
done
shopt -u nullglob
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
echo "done: $SOUL -> $SRC/soul.md"
echo "done: $SRC/reminder.md（接 hook：python3 $SRC/hooks/install-hooks.py claude workbuddy）"
echo "done: $SRC/soul.md"

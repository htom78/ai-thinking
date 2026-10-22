# AI思维（ai-thinking）

> 配套免费网页书：**[《AI 时代的新生：AI 思维》→ ai-era-new-life.vercel.app](https://ai-era-new-life.vercel.app)**

一个给 AI 助手用的 Agent Skill。它让 AI 不再"帮你更快地做旧事"，而是按 AI 时代的方式把一件事从头做到尾：

**认清本质 → 定 10x → 先定标准 → 大胆生成 → 严格淘汰 → 人来选择 → AI 执行 → 数据复盘**

当"做"越来越便宜，人的位置就要往上走：从做事的人，变成认清本质、做出选择的人。

它不是又一套给人加压的方法：目的是让人从繁琐的执行里走出来，更轻松地把事做成。

## 第 0.5 步：先认识本质

方案只能和对问题的理解一样深。动手之前先做五件事：

1. 定位层级：有什么 → 精确多少 → 和别的什么关系 → 什么造出了它 → 能否预测和生成。本质在第 4、5 层。
2. 对"现状为什么是这样"分开生成 ≥3 个根本不同的解释，各估概率。
3. 只做能区分不同解释的最便宜测试。
4. 本质的判据：规则少、跨案例不变、能预测没见过的案例、能拿来生成新实例。
5. **先证伪，再确认**：在没用于归纳的留出数据（更长、更早或没见过的案例）上跑区分测试；只凭一小段数据得出的只是候选假设。
   - 留出数据只开一次：看过结果再改解释，下一轮要换新的留出数据。
   - 没有留出数据时，标成"候选本质"，写明验证数据、到期时间和推翻条件，到期前只按当前级别走可撤回的步骤。
6. 把通过测试的结论压成几条规则，**一次性**和用户确认，写入规格。分歧点和单向门仍要停。

> 问在分歧点，不问在细节上。默认不零碎追问；碰到两种理解会走向不同的不可逆动作或明显不同的产出、猜错比问一次更贵、或新事实让假设失效，一次问清最关键的 1–3 个问题，每个附默认答案。问完写成规格，按规格执行。

## 认识本质时最常见的偏离

- **对象选错**：停在表面统计上，没先问"结果的大头来自哪里"。
- **度量选错**：选好算的指标，而不是回答"用户拿这个结论做什么"的指标（按金额或影响算）。
- **把"做不到"当终点**：删掉一条路后，还要问剩下的部分里有什么能做、能复制。
- **只学"做了什么"，没学"为什么看得懂"**：复制前先答出"它为什么值钱""什么情况算逻辑破了"。
- **先毛估估，再精算**：宁要模糊的正确，不要精确的错误。

## 核心原则

- **先认清本质，再出方案。**
- **10x 定方向**：10% 的改进有无限多种，10x 让老办法失效，逼你只留最关键的 20%。
- **不问"我怎么做"，问"谁来做"**：执行交给 AI，人负责认本质、定目标、做选择。
- **能做成品就不写描述**，用真实数据挑。
- **先设计评估器，再生成。**
- **先删后自动化。**
- **单向门 / 双向门**：可逆与否决定要不要人确认。不可撤回的（花钱、对外发送、删除、上线）攒成一批，让人一次确认；可撤回的按当前级别做。
- **按级放权**：L1 只出计划和草稿，逐步由人确认；L2 按规格自主做可撤回的步骤，最后交证据；L3 长期验收通过后可跑更长周期，只在分歧点和单向门停下。可靠程度决定放手多大，和可逆与否是两件事。
- **AI 方案天然趋同**：每个方案单独生成，换数据源和视角。
- **概率和规则要记账**，到期打分复盘。
- **不挤牙膏**：细节不问；只在分歧点一次问完最关键的 1–3 个问题，问完写成规格再跑。
- **独当一面**：交证据而不是交结论，自己不给自己打分（独立验证者只拿规格和产出来尝试推翻），责任在人（风险、未验证项和不确定性放在汇总最前），分清可逆与不可逆，敢说真话并给替代方案。签名测试由验证者回答，不由作者回答。

完整内容见 [`skills/ai-thinking/SKILL.md`](skills/ai-thinking/SKILL.md)。

## 安装

一行安装：

```bash
curl -fsSL https://raw.githubusercontent.com/htom78/ai-thinking/main/install.sh | bash
```

安装脚本会把技能放到 `~/.agents/skills/ai-thinking`（已是 git 仓库则 `git pull` 更新），再给各工具建软链接。**不会删除任何东西**：遇到旧目录或实体残留，先移到 `~/.Trash/ai-thinking-replaced-时间戳` 备份。

手动安装：

```bash
git clone https://github.com/htom78/ai-thinking.git
mkdir -p ~/.agents/skills
cp -R ai-thinking/skills/ai-thinking ~/.agents/skills/
for d in ~/.workbuddy/skills ~/.claude/skills ~/.cursor/skills ~/.gemini/skills ~/.config/opencode/skills ~/.pi/agent/skills; do
  mkdir -p "$d" && ln -sfn ~/.agents/skills/ai-thinking "$d/ai-thinking"
done
```

| 工具 | 读取位置 |
|---|---|
| Codex | `~/.agents/skills/ai-thinking`（直接读取，无需链接） |
| Claude Code | `~/.claude/skills/ai-thinking` |
| Cursor | `~/.cursor/skills/ai-thinking` |
| Gemini CLI | `~/.gemini/skills/ai-thinking` |
| opencode | `~/.config/opencode/skills/ai-thinking` |
| WorkBuddy | `~/.workbuddy/skills/ai-thinking` |
| pi | `~/.pi/agent/skills/ai-thinking` |

使用时对 AI 说"用 AI思维"或"认清本质""10x""帮我出方案并执行"，即可触发。

## 更新记录

- 2026-10-22：问在分歧点、不问在细节上：三种必须问的情况、问前自检、问后写成规格再执行，提示词前缀同步修改。独当一面改为交证据、独立验证者不自评分、责任在人；留任测试改名为签名测试，由验证者回答。新增「按级放权」（L1 新手 / L2 胜任 / L3 资深）：可逆与否和放手多大分开看。
- 2026-10-21：新增"做事的气质：独当一面"：问清楚就放手、结果自己担、分清可逆与不可逆、敢说真话、留任测试。
- 2026-10-21：README 与配套书 v13 明确 AI 思维的价值是让人从繁琐执行中解放出来，更轻松。
- 2026-10-21：安装脚本改为先备份不删除；新增 WorkBuddy、pi 支持；Codex 直接读 `~/.agents/skills`，去掉多余链接。
- 2026-10-21：新增"认识本质时最常见的偏离"：对象选错、度量选错、把做不到当终点、只学做了什么、先毛估估再精算。
- 2026-10-21：第 0.5 步新增"先证伪，再确认"，"留出数据只开一次"，以及没有留出数据时的"候选本质"。

## English

**AI思维 (ai-thinking)** is an Agent Skill for AI-era problem solving. It first grasps the essence of a problem (step 0.5: locate the level, generate ≥3 competing explanations with probabilities, run discriminating tests on held-out data before confirming (falsify first), and condense the result into a few rules confirmed **once** with the user). It then sets a 10x goal, defines the evaluation criteria before generating, produces genuinely different options, eliminates strictly, and lets AI execute to a written spec. It asks at divergence points, not about details (at most one to three questions, each with a default). Reversible steps run at the earned autonomy level (L1–L3); irreversible ones are batched for a single approval. Deliverables carry evidence mapped to acceptance criteria, and an independent verifier, not the author, tries to break them. Install with the one-liner above, or clone the repo into `~/.agents/skills` and symlink it for Claude Code, Cursor, Gemini CLI, opencode, WorkBuddy and pi (Codex reads `~/.agents/skills` directly). Existing directories are backed up to `~/.Trash`, never deleted.

Companion book (Chinese, free): https://ai-era-new-life.vercel.app

## License

MIT

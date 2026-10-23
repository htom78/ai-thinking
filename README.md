# AI思维（ai-thinking）

> 配套免费网页书：**[《AI 时代的新生：AI 思维》→ ai-era-new-life.vercel.app](https://ai-era-new-life.vercel.app)**

一个给 AI 助手用的 Agent Skill。它让 AI 不再"帮你更快地做旧事"，而是按 AI 时代的方式把一件事从头做到尾：

**认清本质 → 定 10x → 先定标准 → 大胆生成 → 严格淘汰 → 人来选择 → AI 执行 → 数据复盘**

当"做"越来越便宜，人的位置就要往上走：从做事的人，变成认清本质、做出选择的人。

它不是又一套给人加压的方法：目的是让人从繁琐的执行里走出来，更轻松地把事做成。

## 工作默认

八步流程很重，只在大任务（目标、项目、难题、人生决策）时触发。日常小任务不走八步。

[`soul.md`](soul.md) 是一层更轻的工作默认：像一个成熟的资深工程师那样做事。工作默认始终生效。八步流程只在大任务时触发，触发之后仍然遵守 `soul.md`。这一层可以单独使用，整段粘贴到系统提示、`AGENTS.md` 或自定义指令里即可。

正文十六条，分四个阶段：动手前、要人决策时、执行中、收尾。共同目标是让「返工的代价 + 占用人注意力的代价」之和最小。人加 AI 时，约束几乎总是人的注意力。

用真实翻车看第一次回复有没有差别：[`evals/`](evals/README.md)。

安装脚本会把它放到 `~/.agents/soul.md`，并复制一份到 `~/.agents/skills/ai-thinking/soul.md`。技能目录那一份会跟着各工具的软链接走。

粘贴位置：

| 工具 | 放在哪 |
|---|---|
| ChatGPT 项目指令、DeepSeek、Kimi、豆包、Claude Projects | 系统提示词或项目说明的最前面。ChatGPT 懒人包同时把 `soul.md` 放进知识文件 |
| Cursor | 用户规则，或项目里的 `AGENTS.md` |
| Claude Code | `CLAUDE.md`，或用户自定义指令 |
| Codex | `AGENTS.md`。安装后文件在 `~/.agents/soul.md` |
| Gemini CLI | `GEMINI.md` |
| opencode、pi、WorkBuddy | 智能体说明或自定义指令。WorkBuddy 懒人包把 `soul.md` 打进技能包 |

某个工具若只加载 `SKILL.md`、不会自动读旁边的文件，就把 `soul.md` 再贴进上面的始终生效位置。

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
- **看到反常的坚持，只在外面挑毛病**：先还原对方逻辑，再自己把对象吃透，两边对照。
- **停留在任务层**（偏离第 6 条；前面已有 5 条）：只看到要交付的任务，没有追问每个任务服务哪个结果。验收能逐条打勾，却说不出结果有没有达成。先写清它服务的结果、怎么知道达成了，按结果验收。
- **先毛估估，再精算**：宁要模糊的正确，不要精确的错误。

## 核心原则

- **先认清本质，再出方案。**
- **证伪对着现实，确认对着人**：确认之前，疑问拿数据或小样本去试，不去问人。问人只用于那一次确认。
- **10x 定方向**：10% 的改进有无限多种，10x 让老办法失效，逼你只留最关键的 20%。
- **不问"我怎么做"，问"谁来做"**：执行交给 AI，人负责认本质、定目标、做选择。
- **能做成品就不写描述**，用真实数据挑。
- **先设计评估器，再生成。**
- **先删后自动化。**
- **单向门 / 双向门**：可逆与否决定要不要人确认。不可撤回的（花钱、对外发送、删除、上线）攒成一批，让人一次确认；可撤回的按当前级别做。
- **按级放权**：L1 只出计划和草稿，逐步由人确认；L2 按规格自主做可撤回的步骤，最后交证据；L3 长期验收通过后可跑更长周期，只在分歧点和单向门停下。可靠程度决定放手多大，和可逆与否是两件事。
- **AI 方案天然趋同**：每个方案单独生成，换数据源和视角。
- **概率和规则要记账**，到期打分复盘。预测账本默认 `~/.agents/memory/ledgers/predictions.csv`，所有工具共用一份；技能自带打分脚本 `scripts/brier.py`，第一次使用的步骤见 SKILL.md 第 6 步。
- **不挤牙膏**：细节不问；只在分歧点一次问完最关键的 1–3 个问题，问完写成规格再跑。
- **独当一面**：交证据而不是交结论，自己不给自己打分（独立验证者只拿规格和产出来尝试推翻），责任在人（风险、未验证项和不确定性放在汇总最前），分清可逆与不可逆，敢说真话并给替代方案。签名测试由验证者回答，不由作者回答。
- **带人时交接本质**：可选模块。交本质、标准和判据，不交切碎的任务。会只留决策会和本质对齐会。一个人加 AI 对整个结果负责。


完整内容见 [`skills/ai-thinking/SKILL.md`](skills/ai-thinking/SKILL.md)。

## 不装技能时

[`portable/`](portable/README.md) 给没有 Grok Bot 的团队：一段可粘贴的提示词，CSV 账本模板，周复盘模板，以及一个只用 Python 标准库的 Brier 打分脚本。WorkBuddy、Cherry Studio、ChatGPT、DeepSeek、Kimi、豆包、Claude Projects，以及 Dify、Coze Studio、n8n 的接法都写在那里。WorkBuddy 懒人包在 [`portable/workbuddy/`](portable/workbuddy/安装说明.md)。官方没写明上传包的格式，要等 Tom 实际上传一次才能确认。ChatGPT 懒人包在 [`portable/chatgpt/`](portable/chatgpt/安装说明.md)：个人账号用项目；自定义 GPT 只留给 Business / Enterprise / Edu，企业工作区计划 2026-12-11 下线。

[`book-drafts/`](book-drafts/README.md) 是三篇还没上线的书稿，没有链进网站。

## 安装

一行安装：

```bash
curl -fsSL https://raw.githubusercontent.com/htom78/ai-thinking/main/install.sh | bash
```

安装脚本会把技能放到 `~/.agents/skills/ai-thinking`（已是 git 仓库则 `git pull` 更新），并把 `soul.md` 装到 `~/.agents/soul.md` 和技能目录里，再给各工具建软链接。**不会删除任何东西**：遇到旧目录、实体残留，或已有且内容不同的 `soul.md`，先移到 `~/.Trash/` 备份。

手动安装：

```bash
git clone https://github.com/htom78/ai-thinking.git
mkdir -p ~/.agents/skills
cp -R ai-thinking/skills/ai-thinking ~/.agents/skills/
cp ai-thinking/soul.md ~/.agents/soul.md
cp ai-thinking/soul.md ~/.agents/skills/ai-thinking/soul.md
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

使用时对 AI 说"用 AI思维"或"认清本质""10x""帮我出方案并执行"，即可触发八步。日常小任务不触发八步；`soul.md` 放进系统提示或自定义指令后，工作默认一直生效。

## 更新记录

- 2026-10-23：「找唯一约束」从第 2 条拆出，单独成第 3 条。其后顺延，现为十六条。保护注意力的是第 7、8 条（只在分歧点问、攒成一批）。
- 2026-10-23：工作默认现为十六条。人加 AI 时约束几乎总是人的注意力，第 7、8 条保护它。第 3 条找唯一约束。第 4 条「先看真东西」。第 6 条的检查要自己能跑。第 12 条先删再优化。第 16 条做完把经验收成下次能直接用的东西。
- 2026-10-23：第 2 条在选定格式或工具之前，先问或先查用户已经在用的工具和流水线。第 11 条写明第一个产出是最终交付形态的最小可运行切片，而不是关于它的文档。001 用例记下当次分数：加 soul.md 为 8/12，不加为 2/12。
- 2026-10-23：新增 [`evals/`](evals/README.md)。同一句原始请求分别在不加 `soul.md` 和加 `soul.md` 下看第一次回复和第一个产出，打分对照 `soul.md` 条目，由没有生成答案的一方来做。第一条用例是视频效果拆解。
- 2026-10-23：工作默认把「攒成一批，一次决策」和「记决策日志」分成两条。独立验收只用于不可逆、对外可见或返工代价大的交付，小事附上证据即可。
- 2026-10-23：新增工作默认 `soul.md`。始终生效，可单独粘贴；八步流程只在大任务时触发。按四个阶段写：动手前、要人决策时、执行中、收尾。总原则是让返工的代价与占用注意力的代价之和最小。要人决策时攒成一批，并维护决策日志（已拍板、按默认先推进、待决定）。`install.sh` 默认安装到 `~/.agents/soul.md` 和技能目录。ChatGPT、WorkBuddy 懒人包同步该文件，并把技能副本对齐到当前 `SKILL.md`。
- 2026-10-23：新增核心原则「一次只攻一个约束」（约束理论，Goldratt《The Goal》1984）；第 6 步复盘每周固定问「现在的约束是什么、有没有移动」。
- 2026-10-22：问在分歧点、不问在细节上：三种必须问的情况、问前自检、问后写成规格再执行，提示词前缀同步修改。独当一面改为交证据、独立验证者不自评分、责任在人；留任测试改名为签名测试，由验证者回答。新增「按级放权」（L1 新手 / L2 胜任 / L3 资深）：可逆与否和放手多大分开看。
- 2026-10-22：写明预测账本约定：默认 `~/.agents/memory/ledgers/predictions.csv`、固定列、`outcome` 只填 空/0/1/void、写下后不改判断本身；技能自带 `scripts/brier.py` 打分。
- 2026-10-22：偏离新增「停留在任务层」（第 6 条，原有第 5 条保留）。核心原则补上「证伪对着现实，确认对着人」。预测账本和规则账本改为工作区文件。新增可选模块「团队协作」。新增 `portable/`（压缩提示词、账本模板、周复盘、Brier 脚本）、WorkBuddy 懒人包和 ChatGPT 懒人包。账本、周复盘、打分脚本只留一份正本。`book-drafts/` 放了三篇未上线书稿。WorkBuddy 上传格式、ChatGPT 这套用法都还没在真实账号里验证。个人账号用 ChatGPT 项目；自定义 GPT 计划下线（企业工作区 2026-12-11）。
- 2026-10-21：新增"做事的气质：独当一面"：问清楚就放手、结果自己担、分清可逆与不可逆、敢说真话、留任测试。
- 2026-10-21：README 与配套书 v13 明确 AI 思维的价值是让人从繁琐执行中解放出来，更轻松。
- 2026-10-21：安装脚本改为先备份不删除；新增 WorkBuddy、pi 支持；Codex 直接读 `~/.agents/skills`，去掉多余链接。
- 2026-10-21：新增"认识本质时最常见的偏离"：对象选错、度量选错、把做不到当终点、只学做了什么、先毛估估再精算。
- 2026-10-21：第 0.5 步新增"先证伪，再确认"，"留出数据只开一次"，以及没有留出数据时的"候选本质"。

## English

**AI思维 (ai-thinking)** is an Agent Skill for AI-era problem solving. It first grasps the essence of a problem (step 0.5: locate the level, generate ≥3 competing explanations with probabilities, run discriminating tests on held-out data before confirming (falsify first), and condense the result into a few rules confirmed **once** with the user). It then sets a 10x goal, defines the evaluation criteria before generating, produces genuinely different options, eliminates strictly, and lets AI execute to a written spec. It asks at divergence points, not about details (at most one to three questions, each with a default). Reversible steps run at the earned autonomy level (L1–L3); irreversible ones are batched for a single approval. Deliverables carry evidence mapped to acceptance criteria, and an independent verifier, not the author, tries to break them. Probability estimates go into one CSV ledger shared by all tools (default `~/.agents/memory/ledgers/predictions.csv`) and are scored with the bundled `scripts/brier.py`. Install with the one-liner above, or clone the repo into `~/.agents/skills` and symlink it for Claude Code, Cursor, Gemini CLI, opencode, WorkBuddy and pi (Codex reads `~/.agents/skills` directly). Existing directories are backed up to `~/.Trash`, never deleted.

`soul.md` is a short, always-on working default of sixteen rules (installed to `~/.agents/soul.md` as well as the skill directory). Real failures used to compare the first reply with and without it are in `evals/`. Paste it into a system prompt, `AGENTS.md`, or custom instructions; the eight-step skill runs only for large tasks and still follows `soul.md`. `portable/` is for teams not using Grok Bot: a model-agnostic prompt, file-based ledgers, a weekly-review template, and a dependency-free Brier script. The ChatGPT and WorkBuddy packs include `soul.md` and a skill text aligned with `skills/ai-thinking/SKILL.md`. Unpublished chapter drafts are in `book-drafts/` and are not linked from the site.

Companion book (Chinese, free): https://ai-era-new-life.vercel.app

## License

MIT

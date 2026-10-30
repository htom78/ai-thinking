# AI思维（ai-thinking）

> 配套免费网页书：**[《AI 时代的新生：AI 思维》→ ai-era-new-life.vercel.app](https://ai-era-new-life.vercel.app)**

一个给 AI 助手用的 Agent Skill。它让 AI 不再"帮你更快地做旧事"，而是按 AI 时代的方式把一件事从头做到尾：

**认清本质 → 定 10x → 先定标准 → 大胆生成 → 严格淘汰 → 人来选择 → AI 执行 → 数据复盘**

当"做"越来越便宜，人的位置就要往上走：从做事的人，变成认清本质、做出选择的人。

它不是又一套给人加压的方法：目的是让人从繁琐的执行里走出来，更轻松地把事做成。

## 工作默认

八步流程很重，只在大任务（目标、项目、难题、人生决策）时触发。日常小任务不走八步。

[`soul.md`](soul.md) 始终生效，可以单独使用。八步流程只在大任务时触发，触发之后仍然遵守 `soul.md`。正文二十六条，每条只写触发条件和默认动作，分四个阶段：动手前、要人决策时、执行中、收尾。每条的做法细则（格式、步骤、理由）在 [`SKILL.md`](skills/ai-thinking/SKILL.md) 的「做法细则」一节。怎么装、怎么确认生效、怎么按自己的经验改，见下一节。加载了不等于每轮照做：让 Claude Code、WorkBuddy、ChatGPT、Claude 网页每轮再提醒三条的办法，见 [`每轮提醒.md`](每轮提醒.md)。

## 怎么用 soul.md

[`soul.md`](soul.md) 是一套默认工作规则，让 AI 像一个成熟的资深工程师那样做事。遇到没写明的情况，按这一条判断：让「返工的代价 + 占用人注意力的代价」之和最小；人加 AI 时，约束几乎总是人的注意力。规则始终生效，可以单独使用；八步流程只在大任务时触发，触发之后仍然遵守它。

### 装到哪里

[`install.sh`](install.sh) 把 `soul.md` 拷到 `~/.agents/soul.md`，并再拷一份到 `~/.agents/skills/ai-thinking/soul.md`。技能软链接会带上技能目录里的这一份，但多数工具只自动加载 `SKILL.md`。WorkBuddy 不读技能里的 `soul.md`，只注入个人目录的 `SOUL.md`。工作默认要放到每次都会读的位置：

| 工具 | 放在哪 |
|---|---|
| Claude Code | 全文写入项目根目录的 `CLAUDE.md`，或用户级 `~/.claude/CLAUDE.md`。项目里的 `CLAUDE.md` 也可以写 `@soul.md`，引用同一目录下的 `soul.md` |
| Cursor | 项目 `.cursor/rules/` 下的 `.mdc`，frontmatter 设 `alwaysApply: true`；或写入项目根目录的 `AGENTS.md` |
| Codex，以及其他读取 `AGENTS.md` 的代理 | 项目根目录的 `AGENTS.md` |
| ChatGPT | 贴进项目指令，并作为知识文件上传。步骤见 [`portable/chatgpt/`](portable/chatgpt/安装说明.md) |
| WorkBuddy | `install.sh` 自动写到已有的 `~/.workbuddy/user-<id>-personal/SOUL.md`，原来内容不同的文件备份为同目录的 `SOUL.md.bak-<时间>`。WorkBuddy 只注入这一份，不读技能里的 `soul.md`。新开一个会话后生效。手动：把 `soul.md` 复制覆盖那份 `SOUL.md`。技能可以另外上传 [`ai-thinking.zip`](portable/workbuddy/ai-thinking.zip)。见 [`portable/workbuddy/`](portable/workbuddy/安装说明.md) |
| 其他（DeepSeek、Kimi、豆包、Claude Projects、Gemini CLI、opencode、pi） | 整段贴进系统提示词或自定义指令。Gemini CLI 读 `GEMINI.md` |

Cursor 的 `.mdc` 文首：

```mdc
---
alwaysApply: true
---
```

下面接上 `soul.md` 全文。

### 一分钟自检

新开一个会话，发一句没有规格的话，例如：「帮我做一个以后能直接套用的周报。」只看第一次回复：

- 先写明要达成的结果，以及怎样算达成
- 只在分歧点提问，每个问题都带一个默认答案
- 第一个产出是最终交付形态的一块最小可运行切片
- 附上自己能跑的验收（测试、渲染或对照）

四条都在，才算生效。同一句请求的完整有无对照在 [`evals/`](evals/README.md)：用例 [001](evals/cases/001-视频效果拆解.md) 当次分数，不加 `soul.md` 为 2/12，加上为 8/12。

### 持续升级

规则保持短。做完一件事，把这次的教训写成一条新规则，加进你正在用的那一份。同一种错不犯第二次。

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

> 问在分歧点，不问在细节上。默认不零碎追问；碰到两种理解会走向不同的不可逆动作或明显不同的产出、猜错比问一次更贵、或新事实让假设失效，最多问一个，先交决策单（唯一推荐、查过什么、自审毛病、为什么必须由人定）。问完写成规格，按规格执行。

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
- **不挤牙膏**：细节不问；只在分歧点问，最多问一个，先交决策单，问完写成规格再跑。
- **独当一面**：交证据而不是交结论，自己不给自己打分（独立验证者只拿规格和产出来尝试推翻），责任在人（风险、未验证项和不确定性放在汇总最前），分清可逆与不可逆，敢说真话并给替代方案。签名测试由验证者回答，不由作者回答。
- **带人时交接本质**：可选模块。交本质、标准和判据，不交切碎的任务。会只留决策会和本质对齐会。一个人加 AI 对整个结果负责。


完整内容见 [`skills/ai-thinking/SKILL.md`](skills/ai-thinking/SKILL.md)。

## 不装技能时

[`portable/`](portable/README.md) 给没有 Grok Bot 的团队：一段可粘贴的提示词，CSV 账本模板，周复盘模板，以及一个只用 Python 标准库的 Brier 打分脚本。WorkBuddy、Cherry Studio、ChatGPT、DeepSeek、Kimi、豆包、Claude Projects，以及 Dify、Coze Studio、n8n 的接法都写在那里。WorkBuddy 的工作默认由 `install.sh` 写入 `~/.workbuddy/user-<id>-personal/SOUL.md`，见 [`portable/workbuddy/`](portable/workbuddy/安装说明.md)。技能仍可 zip 上传；官方没写明技能包格式，上传格式未经验证，欢迎反馈。ChatGPT 懒人包在 [`portable/chatgpt/`](portable/chatgpt/安装说明.md)：个人账号用项目；自定义 GPT 只留给 Business / Enterprise / Edu，企业工作区计划 2026-12-11 下线。

## 安装

一行安装：

```bash
curl -fsSL https://raw.githubusercontent.com/htom78/ai-thinking/main/install.sh | bash
```

安装脚本会把技能放到 `~/.agents/skills/ai-thinking`（已是 git 仓库则 `git pull` 更新），并把 `soul.md` 装到 `~/.agents/soul.md` 和技能目录里，再给各工具建软链接。已有 `~/.workbuddy/user-*-personal/` 时，把同一份写入其中的 `SOUL.md`。**不会删除任何东西**：遇到旧目录、实体残留，或已有且内容不同的 `~/.agents/soul.md`，先移到 `~/.Trash/` 备份。WorkBuddy 里内容不同的 `SOUL.md` 备份为同目录的 `SOUL.md.bak-<时间>`。没有那个个人目录就跳过，不会新建。

手动安装：

```bash
git clone https://github.com/htom78/ai-thinking.git
mkdir -p ~/.agents/skills
cp -R ai-thinking/skills/ai-thinking ~/.agents/skills/
cp ai-thinking/soul.md ~/.agents/soul.md
cp ai-thinking/soul.md ~/.agents/skills/ai-thinking/soul.md
# WorkBuddy：复制覆盖已有的 ~/.workbuddy/user-<id>-personal/SOUL.md。没有该目录则不要新建。
# 原文件内容不同时，先改名为同目录的 SOUL.md.bak-<时间>。
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

使用时对 AI 说"用 AI思维"或"认清本质""10x""帮我出方案并执行"，即可触发八步。日常小任务不触发八步；`soul.md` 放到「怎么用 soul.md」里的位置后，工作默认一直生效。

## 更新记录

- 2026-10-30：v32，`soul.md` 只改第 1 条，条号不变、仍为二十六条。第 1 条改为「先说清结果，再列门槛」：写出结果后，列出要做成必须过的几道坎（平台规则、准入条件、关键风险、行业里做成的人都做到了什么），不懂的先查或找做成的案例学，再动手；只懂自己那块就开工不算懂。[`SKILL.md`](skills/ai-thinking/SKILL.md) 输出格式加硬性一栏「门槛核对」（逐道坎写已过/未过和证据，没核对的标「未验证」），「推荐」改为只推荐一个。顺手修掉各处残留的「一次问清 1–3 个问题」，统一成第 8 条的「最多问一个，先交决策单」（SKILL.md 三份、ChatGPT `1-` `5-`、WorkBuddy 安装说明、README）。新增评测用例 [`003`](evals/cases/003-1688打单工具.md)（做个 1688 打单工具），未跑。WorkBuddy zip 重打。
- 2026-10-30：v31，`soul.md` 正文不变（仍为二十六条，编号不变），新增每轮提醒。正本 [`reminder.md`](reminder.md)：三行，对应第 8 条（决策单）、第 6 条（审结论）、第 18 条（附证据）。Claude Code 的 `UserPromptSubmit` hook [`hooks/claude-code/soul-reminder.sh`](hooks/claude-code/soul-reminder.sh) 每轮读它；[`hooks/install-hooks.py`](hooks/install-hooks.py) 把 hook 合并进 `~/.claude/settings.json` 或 `~/.workbuddy/settings.json`（先备份）。WorkBuddy hook 能否把输出送进上下文未验证，兜底是 `install.sh` 把提醒附在个人目录 `SOUL.md` 末尾。ChatGPT、Claude 网页没有 hook，提醒放进指令最前面（[`portable/chatgpt/`](portable/chatgpt/)、[`portable/claude/`](portable/claude/)）。[`scripts/sync_reminder.py`](scripts/sync_reminder.py) 检查条号和标题对得上 `soul.md`、各副本一致，`--write` 重新生成。`install.sh` 改为把 `~/.agents/soul.md` 做成软链接（旧实体文件备份到 `~/.Trash`），避免一份更新了、另一份过期。各平台装法和确认办法见 [`每轮提醒.md`](每轮提醒.md)。WorkBuddy zip 内容没变，未重打。
- 2026-10-30：`soul.md` 升到 v30，只改第 8 条，条号不变、仍为二十六条。第 8 条改为「只在分歧点问，最多问一个，先交决策单」：要问之前先交四项，缺一项就不许问——① 唯一推荐；② 查了什么，附来源或输出；③ 用第 6 条自审挑出的毛病，至少一条；④ 为什么必须由人定，只认花钱、对外发送、不可逆、只有人知道的偏好四种；④ 说不出就自己定了去做。[`SKILL.md`](skills/ai-thinking/SKILL.md)「做法细则」第 8 条加决策单模板和用户的固定回复（缺②或③一律回「先查再来」，不讨论内容）；ChatGPT、WorkBuddy 副本和 WorkBuddy 的 zip 同步。新增评测用例 [`002`](evals/cases/002-一堆没查的想法丢给人定.md)（一堆没查的想法丢给人定），未跑。
- 2026-10-29：`soul.md` 升到 v29（v27、v28 已被评测里未采用的对照版占用，跳过），新增第 6 条「审别人的结论，先问四件事」：资料、网上说法、另一个 AI 的结论，先问理由是什么、藏着什么假设、证据靠不靠得住、有没有别的解释；问不过就不当事实用，标「未验证」。来源：Browne & Keeley《学会提问》。插在第 5 条「先看真东西，用真工具」之后，原第 6–25 条顺延为第 7–26 条，现为二十六条，**编号变了**（原 n→n+1，n≥6）。[`SKILL.md`](skills/ai-thinking/SKILL.md)「做法细则」新增第 6 条并同步编号（ChatGPT、WorkBuddy 副本和 WorkBuddy 的 zip 同步）；评测用例 001 条号同步（1、7、11、16，决策单第 8 条）。`evals/auto/` 的打分表、变体和结果是 v25/v26 当时的材料，条号保持原样，未重跑评测。
- 2026-10-24：`soul.md` 升到 v26，只改第 7、19 条，更精简、答案先行，字数 1352 → 1391（+2.9%），条号不变。第 7 条改为默认不问、自己拍板写明假设，只有猜错比问一次代价大才问，且只问一个，附默认答案；第 19 条改为第一句就是结论或唯一推荐，不叙述做过的步骤，不写开场结尾客套，默认不超过 400 字。[`SKILL.md`](skills/ai-thinking/SKILL.md)「做法细则」第 7、19 条同步（ChatGPT、WorkBuddy 的副本和 WorkBuddy 的 zip 同步）。自动评测：场景得分 81% → 80%（噪声内），通用项 95% → 99%，平均字数 828 → 610，字数达标 64% → 78%；这是小幅改进，不是大胜，局限见 [`evals/auto/RESULTS.md`](evals/auto/RESULTS.md)。
- 2026-10-24：`soul.md` 分层：从 2317 字降到 1352 字（约 -42%），正文由十六条变二十五条，**编号变了**。soul.md 只留每条的触发条件和默认动作，自成一体；步骤、格式、理由全部搬到 [`SKILL.md`](skills/ai-thinking/SKILL.md) 新增的「做法细则（对应 soul.md 条号）」一节，没有丢内容，和已有的核心原则、独当一面重复的地方只留一份。条数变多是因为一条只管一件事：原第 2 条拆出「多看一步」，原第 9、11、12 条各拆成两条，原第 13 条拆成三条（交证据、独立验收、汇报），原第 14 条拆成三条（交接复用、记错、跟进），原第 16 条拆成两条（被纠正、自己发现）。新旧对照：原 1→1，原 2→2+3，原 3→4，原 4→5，原 5→6，原 6→7，原 7→8，原 8→9，原 9→10+11，原 10→12，原 11→13+14，原 12→15+16，原 13→17+18+19，原 14→20+21+22，原 15→23，原 16→24+25。去掉了末尾「按钮改蓝」的例子（搬进做法细则末尾）。瘦身前的十六条完整版原样放在 [`evals/soul-v16-full.md`](evals/soul-v16-full.md)，只用来做 A/B 对比，不在任何安装路径里，也不是默认版本。评测用例 001 的条号同步（1、6、10、15、决策单第 7 条），评测未重跑。下面更早的更新记录里的条号是当时的旧编号。WorkBuddy 的 zip 同步。
- 2026-10-24：`soul.md` 整体瘦身，字数从 2871 降到约 2317（约 -19%），没有删任何要求，现为十六条，**编号变了**。合并：原第 5 条并入第 9 条（先粗后细，小步），原第 7、8 条合成第 6 条（只在分歧点问，攒成一批）。新旧对照：原 1–4 条不变；原 6→5，原 7+8→6，原 9→7，原 10→8，原 5+11→9，原 12→10，原 13→11，原 14→12，原 15→13，原 16→14，原 17→15，原 18→16。评测用例 001 的条号同步（1、5、9、12、决策单第 6 条），评测未重跑。下面更早的更新记录里的条号是当时的旧编号。WorkBuddy 的 zip 同步。
- 2026-10-24：`soul.md` 用「成熟的人怎么做」逐条对照后补洞，新增第 18 条，其余编号不变，现为十八条。第 18 条：被纠正、被质疑时先核对证据；属实就直说错在哪、改好、查同类，不推给指令或工具；不属实就附证据坚持；拿不准说「我不知道」；发现自己早先交付有错，没人发现也主动说。并入已有条目的：第 10 条人拍板后全力执行、不消极不翻旧账；第 11 条先做最难最没把握的一块，不可撤回操作动手前核对对象、范围、备份；第 13 条阻碍先分类，技术或信息性阻碍先自己换两三条路再升级，权限和安全限制不绕；第 15 条澄清最终担责的是人、自己做错的仍自己认；第 16 条记错只写事实和系统原因，说过要跟进的事要有记录或定时任务；第 8 条「卡住才单独问」改为换过路仍卡住才问。来源（原文或可靠转述）：Peck 的延迟满足与承担责任、Dalio 的「痛苦加反思」、Google SRE 的无责复盘、WHO 手术安全核对表的暂停点、Netflix 与 Amazon 的 disagree and commit、完成式参谋工作。WorkBuddy 的 zip 同步。
- 2026-10-24：`soul.md` 新增第 17 条「极限版」（接在第 16 条后，不改动其余编号，现为十七条）。目标不明确或人在探新方向时，除了稳妥版再附一个把假设放到最松的极限版：写明能做到什么、卡在哪、哪个假设来自惯例；要真试过或有证据，标明是极限版，不替人选；目标已清楚、只要稳妥执行时不用。目的是让人保持开眼界，不被惯例磨平。WorkBuddy 的 zip 同步。
- 2026-10-24：`soul.md` 仍是十六条，内容并入已有条目。第 2 条加「再看宽一步」：用动词重述任务，问哪几个领域的方法能帮上忙，只借方法和工具，不角色扮演。第 4 条加：用专业人真正用的工具和方法，不只是换成专业口吻（例如分析数据用数据库或统计方法，别停在 markdown 表格）。第 14 条加：觉得「不可能」时当成待检验的假设，先问成立需要什么条件、哪个假设来自惯例，做最小切片真去试；试过仍做不到，再附证据说明已验证到哪一步和差距，不凭印象说不可能。WorkBuddy 的 zip 同步了新的 `soul.md`。评测用例 001 的分数是上一版条文的当次结果，没有重跑。
- 2026-10-23：`install.sh` 把 `soul.md` 写入已有的 `~/.workbuddy/user-*-personal/SOUL.md`（内容不同则备份为同目录 `SOUL.md.bak-<时间>`，不删除、不新建目录）。WorkBuddy 只注入这一份，不读技能里的 `soul.md`；新开一个会话后生效。zip 只用来装技能。
- 2026-10-23：README 增加「怎么用 soul.md」：各工具的放置位置、一分钟自检，以及把教训收成新规则。用例 001 的有无对照仍是不加 2/12、加上 8/12。
- 2026-10-23：第 8 条写明每个问题都要有默认答案，不能把「等你」当作默认，也不为凑决策单去问代价低的问题；等人回答时先做和答案无关的部分，不要整体停工。第 15 条只向人汇报结果和真正要拍板的事，有权限的可撤回操作自己做完。001 第三次用十六条 soul.md 为 11/12（按摘要打分，可能偏高）。WorkBuddy 上传格式未经验证，欢迎反馈。
- 2026-10-23：「找唯一约束」从第 2 条拆出，单独成第 3 条。其后顺延，现为十六条。保护注意力的是第 7、8 条（只在分歧点问、攒成一批）。
- 2026-10-23：工作默认现为十六条。人加 AI 时约束几乎总是人的注意力，第 7、8 条保护它。第 3 条找唯一约束。第 4 条「先看真东西」。第 6 条的检查要自己能跑。第 12 条先删再优化。第 16 条做完把经验收成下次能直接用的东西。
- 2026-10-23：第 2 条在选定格式或工具之前，先问或先查用户已经在用的工具和流水线。第 11 条写明第一个产出是最终交付形态的最小可运行切片，而不是关于它的文档。001 用例记下当次分数：加 soul.md 为 8/12，不加为 2/12。
- 2026-10-23：新增 [`evals/`](evals/README.md)。同一句原始请求分别在不加 `soul.md` 和加 `soul.md` 下看第一次回复和第一个产出，打分对照 `soul.md` 条目，由没有生成答案的一方来做。第一条用例是视频效果拆解。
- 2026-10-23：工作默认把「攒成一批，一次决策」和「记决策日志」分成两条。独立验收只用于不可逆、对外可见或返工代价大的交付，小事附上证据即可。
- 2026-10-23：新增工作默认 `soul.md`。始终生效，可单独粘贴；八步流程只在大任务时触发。按四个阶段写：动手前、要人决策时、执行中、收尾。总原则是让返工的代价与占用注意力的代价之和最小。要人决策时攒成一批，并维护决策日志（已拍板、按默认先推进、待决定）。`install.sh` 默认安装到 `~/.agents/soul.md` 和技能目录。ChatGPT、WorkBuddy 懒人包同步该文件，并把技能副本对齐到当前 `SKILL.md`。
- 2026-10-23：新增核心原则「一次只攻一个约束」（约束理论，Goldratt《The Goal》1984）；第 6 步复盘每周固定问「现在的约束是什么、有没有移动」。
- 2026-10-22：问在分歧点、不问在细节上：三种必须问的情况、问前自检、问后写成规格再执行，提示词前缀同步修改。独当一面改为交证据、独立验证者不自评分、责任在人；留任测试改名为签名测试，由验证者回答。新增「按级放权」（L1 新手 / L2 胜任 / L3 资深）：可逆与否和放手多大分开看。
- 2026-10-22：写明预测账本约定：默认 `~/.agents/memory/ledgers/predictions.csv`、固定列、`outcome` 只填 空/0/1/void、写下后不改判断本身；技能自带 `scripts/brier.py` 打分。
- 2026-10-22：偏离新增「停留在任务层」（第 6 条，原有第 5 条保留）。核心原则补上「证伪对着现实，确认对着人」。预测账本和规则账本改为工作区文件。新增可选模块「团队协作」。新增 `portable/`（压缩提示词、账本模板、周复盘、Brier 脚本）、WorkBuddy 懒人包和 ChatGPT 懒人包。账本、周复盘、打分脚本只留一份正本。WorkBuddy 上传格式、ChatGPT 这套用法当时都未经验证。个人账号用 ChatGPT 项目；自定义 GPT 计划下线（企业工作区 2026-12-11）。
- 2026-10-21：新增"做事的气质：独当一面"：问清楚就放手、结果自己担、分清可逆与不可逆、敢说真话、留任测试。
- 2026-10-21：README 与配套书 v13 明确 AI 思维的价值是让人从繁琐执行中解放出来，更轻松。
- 2026-10-21：安装脚本改为先备份不删除；新增 WorkBuddy、pi 支持；Codex 直接读 `~/.agents/skills`，去掉多余链接。
- 2026-10-21：新增"认识本质时最常见的偏离"：对象选错、度量选错、把做不到当终点、只学做了什么、先毛估估再精算。
- 2026-10-21：第 0.5 步新增"先证伪，再确认"，"留出数据只开一次"，以及没有留出数据时的"候选本质"。

## English

**AI思维 (ai-thinking)** is an Agent Skill for AI-era problem solving. It first grasps the essence of a problem (step 0.5: locate the level, generate ≥3 competing explanations with probabilities, run discriminating tests on held-out data before confirming (falsify first), and condense the result into a few rules confirmed **once** with the user). It then sets a 10x goal, defines the evaluation criteria before generating, produces genuinely different options, eliminates strictly, and lets AI execute to a written spec. It asks at divergence points, not about details (at most one to three questions, each with a default). Reversible steps run at the earned autonomy level (L1–L3); irreversible ones are batched for a single approval. Deliverables carry evidence mapped to acceptance criteria, and an independent verifier, not the author, tries to break them. Probability estimates go into one CSV ledger shared by all tools (default `~/.agents/memory/ledgers/predictions.csv`) and are scored with the bundled `scripts/brier.py`. Install with the one-liner above, or clone the repo into `~/.agents/skills` and symlink it for Claude Code, Cursor, Gemini CLI, opencode, WorkBuddy and pi (Codex reads `~/.agents/skills` directly). Existing directories are backed up to `~/.Trash`, never deleted.

`soul.md` is a short, always-on working default of twenty-six short rules, each only a trigger and a default action (details live in the 做法细则 section of SKILL.md; installed to `~/.agents/soul.md` as well as the skill directory). WorkBuddy injects only `~/.workbuddy/user-<id>-personal/SOUL.md`: `install.sh` writes that file when the directory already exists, backs up a different original beside it, and a new session picks it up. A zip upload only installs the skill. Real failures used to compare the first reply with and without it are in `evals/` (case 001: 2/12 without, 8/12 with). Per-tool file locations, a one-minute check, and how to add your own rules are in 「怎么用 soul.md」. The eight-step skill runs only for large tasks and still follows `soul.md`. `portable/` is for teams not using Grok Bot: a model-agnostic prompt, file-based ledgers, a weekly-review template, and a dependency-free Brier script. The ChatGPT pack includes `soul.md`. The WorkBuddy zip is only an alternative way to install the skill.

Companion book (Chinese, free): https://ai-era-new-life.vercel.app

## License

MIT

# 不用 Grok Bot 时怎么用

这一目录给没有 Grok Bot 的人。技能正文仍是仓库里的 [`skills/ai-thinking/SKILL.md`](../skills/ai-thinking/SKILL.md)。这里是压缩版提示词、账本文件和周复盘，换到别的产品里还能接着用。安装脚本只复制 `skills/ai-thinking`，不包含这一目录；要用这里的文件，克隆仓库后自己拷。

账本放在工作区里，用 CSV 或 Markdown。不要把概率和规则只写进某个产品的记忆。记忆是抽出来的摘要，对不上原文，换产品也会丢。

| 文件 | 做什么 |
|---|---|
| [`prompt.md`](prompt.md) | 贴进系统提示词或项目说明 |
| [`ledgers/predictions.csv`](ledgers/predictions.csv) | 预测账本模板，有一行「示例」 |
| [`ledgers/rules.csv`](ledgers/rules.csv) | 规则账本模板，有一行「示例」 |
| [`templates/weekly-review.md`](templates/weekly-review.md) | 每周复盘要填的空表 |
| [`brier.py`](brier.py) | 给预测账本里已结算的行算 Brier |
| [`workbuddy/`](workbuddy/安装说明.md) | WorkBuddy 懒人包。账本和打分脚本指向上面的正本 |
| [`chatgpt/`](chatgpt/安装说明.md) | ChatGPT 懒人包。个人账号用项目；GPT 只留给企业工作区 |

打分：

```bash
python3 portable/brier.py portable/ledgers/predictions.csv
```

在 `portable/` 目录里则写成 `python3 brier.py ledgers/predictions.csv`。脚本只用 Python 标准库。Brier = (概率 − 结果)²，已结算的行取平均，越低越好。0 是全对；每条都写五成，分数是 0.25。预测内容或备注里带「示例」的行不参与打分，结果空着的行视为没到期。概率写 0 到 1，或 `70%`、`七成`；大于 1 且不超过 100 的数字按百分数算。结果只认 1 和 0。脚本只读 CSV。账本若用 Markdown，自己对照着打，或另存一份 CSV 再跑。这份脚本、`ledgers/` 和 `templates/weekly-review.md` 是正本。

自测：`python3 portable/test_brier.py`

## WorkBuddy（腾讯）

懒人包在 [`workbuddy/`](workbuddy/安装说明.md)。按 `安装说明.md` 做：上传 `ai-thinking.zip`，把账本拷进工作空间，再建每周复盘。文档：

- [技能](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [定时任务](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide)
- [记忆](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory)

WorkBuddy 的上传格式还没验证，要等 Tom 实际上传一次才算数。官方文档只写了「选中本地技能包」，没有写明是 zip 还是文件夹，也没有写明 `SKILL.md` 放在哪一层。现在的 zip 里，顶层是 `ai-thinking/` 文件夹，里面是 `SKILL.md`。传失败时按安装说明里的另外两种试法。

`workbuddy/ai-thinking/` 里的账本、周复盘和 `scripts/brier.py` 是指向上面正本的链接，不要另改一份。`ai-thinking.zip` 里打进去的是文件本身，方便上传。云端任务读不到本机账本，周复盘用本地任务。

## Cherry Studio

开源客户端：[github.com/CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio)。文档：[内置工具、知识库、技能和 MCP](https://cherryai.com/docs/en/advanced-basic/agent-workspace/tools-knowledge-skills-mcp/)。

模型在「模型服务」里自己配。DeepSeek、Qwen、Kimi 都可以。智能体从左侧 Work 打开，编辑里启用技能；技能的手动入口是 Settings → Skills，把本仓库的 `skills/ai-thinking` 装进去，或把 [`prompt.md`](prompt.md) 写进智能体说明。内置工具里打开 Memory（记忆）和 Scheduled Tasks（定时任务）。定时任务到点跑周复盘，工作目录里放账本和 `weekly-review.md`。记忆同样是抽出来的，账本仍要留文件。

## ChatGPT

懒人包在 [`chatgpt/`](chatgpt/安装说明.md)。按 OpenAI 帮助中心（2026 年 10 月）：个人账号（Free / Go / Plus / Pro）已经不能新建 GPT，自定义 GPT 在下线。企业工作区的下线日期是 2026 年 12 月 11 日，其他方案预计同一时间表，以账号里的通知为准。所以长期用「项目」（Projects）。自定义 GPT 只留给还有权限的 Business / Enterprise / Edu 工作区，而且只适合短期用。

项目做法：新建项目，把 `5-不建GPT的用法.md` 里的提示词贴进项目指令，再上传 `2-知识文件/` 里的文件。中国大陆需要 VPN。

`2-知识文件/ai-thinking-SKILL.md` 是 ChatGPT 专用稿，账本一节改成每次上传 CSV、结束时下载替换。`predictions.csv`、`rules.csv`、`weekly-review.md`、`brier.py` 指向本目录的正本，不要另改一份。安装说明末尾的「尚未确认」仍然有效：这套还没在真实账号里搭过。

## 直接贴进对话产品

DeepSeek、Kimi、豆包，以及 Claude 的 Projects：把 [`prompt.md`](prompt.md) 贴进系统提示词或项目说明。每次复盘把账本文件附上，或让它读你已经放在工作区里的那两份。这些产品没有统一的技能目录，提示词就是技能。

## 自己搭给团队用

定时复盘可以自己搭，不必等某个客户端。到点读账本、跑 `brier.py`、把 [`prompt.md`](prompt.md) 和周复盘模板交给模型，把写出来的复盘存回工作区。

- [Dify](https://github.com/langgenius/dify)：工作流加定时触发。
- [Coze Studio](https://github.com/coze-dev/coze-studio)：扣子的开源版，用同一段提示词做机器人。
- [n8n](https://github.com/n8n-io/n8n)：用 cron 触发，读 CSV、跑打分、再调模型。

账本放在你们自己的磁盘或仓库里。不要只放在平台的会话记忆里。

## 比 Grok Bot 少什么

自动摘要的记忆对不上原话，所以预测和规则必须落成文件。没有跨 agent 协作，也没有邮件。这两件事不要假装这个目录能补上。

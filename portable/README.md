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
| [`workbuddy/`](workbuddy/README.md) | 懒人包的位置，文件还没放进来 |

打分：

```bash
python3 portable/brier.py portable/ledgers/predictions.csv
```

在 `portable/` 目录里则写成 `python3 brier.py ledgers/predictions.csv`。脚本只用 Python 标准库。Brier = (概率 − 结果)²，已结算的行取平均，越低越好。0 是全对；每条都写五成，分数是 0.25。备注或预测以「示例」开头的行不参与打分，结果空着的行视为没到期。概率写 0 到 1，或 `70%`、`七成`。脚本只读 CSV。账本若用 Markdown，自己对照着打，或另存一份 CSV 再跑。

自测：`python3 portable/test_brier.py`

## WorkBuddy（腾讯）

文档：

- [技能](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [定时任务](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide)
- [记忆](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory)

技能文件就是一份 `SKILL.md`。上传步骤：左侧进入技能板块，点「添加技能 → 上传技能」，选中本地技能包。仓库里要传的是 `skills/ai-thinking` 这个目录（里面是 `SKILL.md`）。界面若只能选文件、不能选文件夹，先把这个目录打成压缩包再传。

每周复盘：左侧「定时任务」，新建一条，重复选「每周」。提示词里写明用 AI思维技能，读工作空间里的 `predictions.csv`、`rules.csv`，按 [`templates/weekly-review.md`](templates/weekly-review.md) 写复盘。新建后先手动跑一次，看结果对不对，再开每周。

定时任务有本地和云端。云端在云端沙箱里跑，电脑关机也能按时执行。云端读不到本机文件，也不能把结果推到企业微信。账本若在本机，周复盘用本地任务，运行时电脑和客户端不要关。本地任务可以在编辑窗口打开「消息推送到企业微信」：用已经绑好的企微助理，或单独注册一个只收结果的机器人。复用助理的机器人时，绑定方式要选 WebSocket 长连接，URL 回调推不出去。

记忆默认开着，每晚从当天会话里抽一遍，只有自己能看。它是摘要，可能抽偏。概率和规则以账本文件为准。复杂任务、复杂技能消耗的积分更高；这条技能步骤多，周复盘会比一句提醒更费积分。

可以直接上传的懒人包还没有。位置留在 [`workbuddy/`](workbuddy/README.md)，文件随后补上。

## Cherry Studio

开源客户端：[github.com/CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio)。文档：[内置工具、知识库、技能和 MCP](https://cherryai.com/docs/en/advanced-basic/agent-workspace/tools-knowledge-skills-mcp/)。

模型在「模型服务」里自己配。DeepSeek、Qwen、Kimi 都可以。智能体从左侧 Work 打开，编辑里启用技能；技能的手动入口是 Settings → Skills，把本仓库的 `skills/ai-thinking` 装进去，或把 [`prompt.md`](prompt.md) 写进智能体说明。内置工具里打开 Memory（记忆）和 Scheduled Tasks（定时任务）。定时任务到点跑周复盘，工作目录里放账本和 `weekly-review.md`。记忆同样是抽出来的，账本仍要留文件。

## ChatGPT

两种放法。自定义 GPT：把 [`prompt.md`](prompt.md) 贴进 Instructions。或者建一个 Project，贴进项目说明，账本作为项目文件留着。中国大陆需要 VPN 才能用。

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

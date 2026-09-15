# SciRead 中文说明

> 面向科研工作流的结构化、证据约束、Contribution-Faithful 论文阅读 Skill。

当前版本：**v0.6.0**

英文开源主页见 [README.md](README.md)。

## 这是什么

SciRead 不是普通论文摘要 Prompt，而是一套论文阅读规范。

它重点保证：
- Task 定义准确；
- “创新”以作者 contribution 为主；
- 方法链路完整；
- Dataset / Split / Metric 不串；
- 强 Claim 不夸大；
- 缺失信息不乱补；
- 缺点和科研启发真正有研究价值。

`SKILL.md` 是英文规范源。  
`SKILL.zh-CN.md` 是你自己阅读和使用的中文版本。

## 你日常最简单的用法

在已经加载该项目的环境里：

> 帮我读一下这篇。

如果想强制说明：

> 按 SciRead v0.6 的标准帮我读一下这篇，输出中文 Markdown 阅读笔记。

如果只想快速判断是否值得精读：

> 按 SciRead 快读模式帮我读一下这篇。

如果特别关注创新：

> 按 SciRead 重新审查这篇论文的 contribution 和创新，区分作者 claim 和你的理解。

## 项目结构

```text
SciRead/
├── SKILL.md              # 英文规范源，开源使用
├── SKILL.zh-CN.md        # 中文规范，你自己看
├── profiles/             # DDI / Agent / AI4Science 专项规则，中英文
├── templates/            # 中英文阅读笔记模板
├── rubrics/              # 中英文质量规范
├── benchmark/gold_notes/ # 12 篇 DDI Gold Note
├── benchmark/metadata.json
├── registry/
└── scripts/validate.py
```

## 关于 Gold Note

这些 Gold Note 是高质量参考笔记，用来控制“应该读到什么深度”。

它们不是用来直接复制内容的。

所有新论文仍必须重新从原文读取 Task、Contribution、Method、Experiment 和 Case Study。

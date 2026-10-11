# 创新点探索 · Idea Discovery

[返回学术技能库首页](../../README.md) · [总模块索引](../../MODULE_INDEX.md)

这是 **Academic Research Skills 学术技能库** 下的第一个专题模块，而不是一个单独发布的创新点探索仓库。收录论文创新点探索相关 Skills、源码与中文导览。

围绕 **阅读文献 → 发现问题 → 提出候选 → 对照已有工作 → 细化方法 → 设计验证实验**，收录 5 个项目、6 份固定版本源码快照，并提供 18 个重点技能入口。

**这是第三方技能的整理与导览，不是这些项目的原创发布，也不是统一的 Agent 运行框架。** 原作者、上游来源、许可证及子目录中的独立许可均予以保留。

## 从这里开始

先打开 [技能中文索引](SKILL_INDEX.md)。按你现在的任务选择：

| 当前任务 | 优先阅读 |
|---|---|
| 将一个方向推进为候选、查新和方法计划 | [ARIS idea-discovery](01_ARIS/upstream/skills/idea-discovery/SKILL.md) |
| 轻量头脑风暴，换角度发现问题 | [Orchestra brainstorming](02_Orchestra/upstream/21-research-ideation/brainstorming-research-ideas/SKILL.md) |
| 核对具体贡献是否被已有论文覆盖 | [ResearchStudio scoop-check](03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/scoop_check/SKILL.md) |
| 从实验观察建立可证伪假设 | [K-Dense hypothesis-generation](04_KDense/upstream/skills/hypothesis-generation/SKILL.md) |
| 从研究兴趣建立问题卡和证据计划 | [ClaudeScholar research-ideation](05_ClaudeScholar/upstream_main/skills/research-ideation/SKILL.md) |

## 收录范围

| 本地目录 | 上游项目 | 本次保留范围 |
|---|---|---|
| `01_ARIS` | [Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 完整快照，重点索引 8 个创新点相关入口，保留共享依赖与 Codex 适配。 |
| `02_Orchestra` | [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 完整 `21-research-ideation` 子树及根说明与许可，重点索引 2 项技能。 |
| `03_ResearchStudio_Idea` | [ResearchStudio](https://github.com/microsoft/ResearchStudio) | 完整 `ResearchStudio-Idea` 子树及根文档，重点索引检索、构思、重合检查 3 项技能。 |
| `04_KDense` | [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 头脑风暴、假设生成、文献综述、科学批判性思维 4 个完整技能目录。 |
| `05_ClaudeScholar` | [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | main / codex 两个完整快照，重点索引 `research-ideation`。 |

18 指重点技能名称数；同一技能在不同宿主中的适配副本不重复计数。完整快照还含其他功能，不代表所有内容都适合一次性安装。

## 建议工作方式

先选一套完成有限任务，例如阅读 3–5 篇论文、提出 2–3 个候选，并要求每个候选说明研究问题、最接近的已有工作、机制差异、可证伪假设和最小验证实验。人工确认之后再进入自动实验阶段。

阅读 `SKILL.md` 不等于已安装技能。实际使用应按对应版本的上游文档配置 Agent 宿主、模型、检索服务、MCP/API 或 Python 环境；不要把多个项目的全局配置直接互相覆盖。

查新受到检索覆盖、时间和理解准确性的限制。未检索到同一方法，不等于已证明新颖性；模型评分也不是实验有效性或论文录用的保证。

## 版本与完整性

本次整理日期为 **2026-10-11**，不是自动追踪最新分支。完整提交号、收录路径和每个上游文件的摘要见 [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json)。

从本目录运行以下命令可检查包内文件摘要：

```bash
shasum -a 256 -c SHA256SUMS.txt
```

另见 [整理与核验记录](整理与核验记录.md)、[公开版处理记录](PUBLICATION_NOTES.md) 和 [第三方许可说明](THIRD_PARTY_NOTICES.md)。本合集没有自动安装依赖、注册技能或运行上游代码。

## 公开仓库使用注意

只在本地配置 API 密钥、账号密码和真实研究数据，不要提交 `.env`、私人 MCP 配置或尚未公开的实验材料。根目录 `.gitignore` 提供基础排除规则，但不能代替提交前检查。将来更新上游时，应重新核对内容、许可和敏感信息。

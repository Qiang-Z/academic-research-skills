# Academic Research Skills · 学术技能库

面向科研工作流的 **Skills、开源项目与中文使用指南** 合集。按研究任务划分模块，逐步积累可复用的学术能力。

**仓库定位：这是学术技能总库；论文创新点探索只是其中的第一个模块。** 现已整理八个模块，覆盖文献、构思、实验、分析、写作、绘图、投稿回复和科研知识管理。

## 从这里开始

| 入口 | 内容 |
|---|---|
| [模块总索引](MODULE_INDEX.md) | 已收录模块与拟扩展方向，明确区分实际内容和规划。 |
| [创新点探索模块](modules/idea-discovery/README.md) | 当前第一个模块：5 个来源项目、6 份固定版本快照、18 个重点技能入口。 |
| [18 个技能中文索引](modules/idea-discovery/SKILL_INDEX.md) | 按任务选择文献梳理、头脑风暴、查新、假设生成和验证计划入口。 |
| [文献检索与综述模块](modules/literature-review/README.md) | 复用现有 4 个项目、5 份快照，整理 5 个核心技能、中文说明、模板和五篇论文示例。 |
| [实验设计与复现模块](modules/experiment-design/README.md) | 复用 2 个项目、2 份快照，整理 6 个核心技能、复现说明、模板和 CPU 教学示例。 |
| [数据分析与统计模块](modules/data-analysis/README.md) | 复用 3 个项目、4 份快照，整理 5 个核心技能、统计说明、模板及衔接实验输出的分析示例。 |
| [论文写作与润色](modules/paper-writing/README.md) | 6 个核心技能、12 个入口；大纲、章节、润色与证据核对。 |
| [学术绘图与可视化](modules/academic-figures/README.md) | 3 个核心技能、6 个入口；真实数据图、结构图与生成材料。 |
| [投稿与审稿回复](modules/submission-rebuttal/README.md) | 3 个核心技能、6 个入口；自查、逐条回复与实际修订示例。 |
| [科研知识管理](modules/research-knowledge/README.md) | 4 个核心技能、8 个入口；普通文件与知识库集成两条路线。 |
| [入门与任务选择](docs/GETTING_STARTED.md) | 根据已有材料选模块，核对依赖与使用范围。 |
| [连续教学案例](examples/research-workflow/README.md) | 同一合成实验贯通分析、图表、写作、模拟回复与知识记录。 |
| [运行状态](docs/RUNTIME_STATUS.md) | 区分文档、原创例子、上游组件及完整工作流。 |
| [仓库规划记录](docs/REPOSITORY_PLAN.md) | 仓库定位、目录约定、初始模块与后续扩展原则。 |

## 当前已收录模块

### 01 · 创新点探索 / Idea Discovery

围绕 **理解文献 → 发现问题 → 提出候选 → 对照已有工作 → 细化方法 → 设计最小验证**，保留官方技能及配套材料，并提供中文导览。

| 来源 | 本模块重点用途 | 本地说明 |
|---|---|---|
| ARIS | 将文献、构思、查新和实验规划串成探索流程 | [8 个重点入口](modules/idea-discovery/SKILL_INDEX.md) |
| Orchestra | 结构化研究头脑风暴与创造性思维 | [2 个重点技能](modules/idea-discovery/02_Orchestra/upstream/21-research-ideation/) |
| ResearchStudio-Idea | 论文检索、想法构思、已有工作重合检查 | [3 个主要技能及配套资料](modules/idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/README.md) |
| K-Dense | 科研头脑风暴、假设生成、文献综述、批判性思维 | [4 个重点技能](modules/idea-discovery/04_KDense/upstream/skills/) |
| ClaudeScholar | 从研究兴趣形成问题卡与证据计划 | [main / codex 两份适配快照](modules/idea-discovery/05_ClaudeScholar/) |

上述数量指创新点模块的整理范围，不是全库已安装的技能数，也不是运行测试成绩。完整快照可能包含其他技能。

### 02 · 文献检索与综述 / Literature Review

围绕 **确定范围 → 检索筛选 → 阅读记录 → 证据综合 → 引用核对 → 交接 idea**，复用原快照中的 ARIS、ResearchStudio-Idea、K-Dense 和 ClaudeScholar。5 个核心技能名称对应 8 个分支/宿主文件入口；源码保持原位，没有新增快照，跨模块复用不计为新的来源项目。

从 [技能中文索引](modules/literature-review/SKILL_INDEX.md) 和 [使用说明](modules/literature-review/USAGE.md) 开始；可参考 [五篇公开 RAG 论文的摘要级教学示例](modules/literature-review/examples/rag-literature-walkthrough.md) 与 [工作模板](modules/literature-review/templates/README.md)。最新 [实测报告](modules/literature-review/runtime-tests/2026-10-22/README.md) 已记录部分检索、记录处理、引用核验及宿主摘要综合可运行，也记录参数错配、静默失败、网络波动与缺依赖；完整流程尚未验证。

### 03 · 实验设计与复现 / Experiment Design & Reproduction

围绕 **明确主张 → 固定协议 → 基线复现 → 对照与消融 → 运行记录 → 审查与交接**，整理 ARIS 的 6 个核心技能、12 个主版本/Codex 入口，以及 ClaudeScholar main 的复现辅助规则。复用既有 2 个项目、2 份快照，没有新增上游版本。

从 [技能中文索引](modules/experiment-design/SKILL_INDEX.md)、[使用说明](modules/experiment-design/USAGE.md) 和 [工作模板](modules/experiment-design/templates/README.md) 开始。[原创 CPU 教学示例](modules/experiment-design/examples/README.md) 演示合成数据上的基线、变体、消融及独立复跑；其测试状态与上游技能分开记录。当前聚焦计算实验；[验证阶段快照](modules/experiment-design/runtime-tests/2026-10-22/README.md) 已记录部分原始队列组件测试、规划与合成日志判断，整轮复跑和审计仍待完成。

### 04 · 数据分析与统计 / Data Analysis & Statistics

围绕 **核对数据 → 确定分析单位 → 描述与比较 → 评估不确定性 → 审查主张 → 交接报告**，整理 ARIS、ClaudeScholar 与 K-Dense 的 5 个核心技能名称、9 个主版本/分支入口。复用既有 3 个项目、4 份快照，没有新增上游版本。

从 [技能中文索引](modules/data-analysis/SKILL_INDEX.md)、[使用说明](modules/data-analysis/USAGE.md) 和 [五类工作模板](modules/data-analysis/templates/README.md) 开始。[原创分析示例](modules/data-analysis/examples/README.md) 读取实验模块教学输出，演示描述统计、逐样本配对差值和固定划分下的 bootstrap 区间，明确条件性解释和事后分析边界。示例测试单独记录，上游运行验证仍为未测试。

### 05 · 论文写作与润色

复用 ARIS 与 ClaudeScholar 的 2 个项目、3 份快照，整理 6 个核心技能名称、12 个入口。提供中文索引、五类模板及已完成的 Methods/Results/Limitations 教学稿、中英润色和数字核对。进入 [模块首页](modules/paper-writing/README.md)。

### 06 · 学术绘图与可视化

复用 ARIS 一份快照，整理 3 个核心技能名称、6 个入口，区分数据图、结构图与流程图。原创 Matplotlib 示例已运行，FigureSpec 单文件渲染组件按限定范围实测，完整上游工作流仍未运行。进入 [模块首页](modules/academic-figures/README.md)。

### 07 · 投稿与审稿回复

复用 2 个项目、3 份快照，整理 3 个核心技能名称、6 个入口，另列可选重投流程。三条模拟意见对应证据、回复与实际修订，不代表真实审稿或投稿。进入 [模块首页](modules/submission-rebuttal/README.md)。

### 08 · 科研知识管理

复用 2 个项目、3 份快照，整理 4 个核心技能名称、8 个入口。提供普通文件与 Zotero/Obsidian 两条路线，完成一个可阅读的 Markdown 教学知识库；真实服务连接未测试。进入 [模块首页](modules/research-knowledge/README.md)。

## 目录结构

```text
academic-research-skills/
├── README.md / MODULE_INDEX.md / MODULES.json
├── AGENTS.md
├── modules/
│   ├── idea-discovery/        # 原始固定快照保存处
│   ├── literature-review/
│   ├── experiment-design/
│   ├── data-analysis/
│   ├── paper-writing/
│   ├── academic-figures/
│   ├── submission-rebuttal/
│   └── research-knowledge/
├── examples/research-workflow/ # 连续教学案例及运行/核验入口
├── docs/                     # 入门、交接、证据检查、状态与规划
├── templates/module-template/
├── scripts/verify_bundle.py
├── THIRD_PARTY_NOTICES.md / PUBLICATION_NOTES.md
└── CHANGELOG.md / PUBLISH_FILES.txt / SHA256SUMS.txt
```

## 共同使用与维护

本轮规划的八个模块与公共导航已落地。按 [研究流程](docs/RESEARCH_WORKFLOW.md) 交接输入输出，按 [证据检查指南](docs/EVIDENCE_CHECKS.md) 区分实现完整性、主张支持、稿件数字与引用核验；具体测试范围见 [运行状态](docs/RUNTIME_STATUS.md)。新增其他领域时继续遵循来源、许可与独立验证约定。

## 使用原则

先选择当前任务对应的模块，再阅读该模块的索引及所选上游 `SKILL.md`。本仓库不是统一 Agent 运行框架，也不自动注册技能。实际使用需要按各上游文档配置兼容宿主、模型与所需服务；不要把不同项目的全局设置直接互相覆盖。

上游代码作为资料保留，没有因收录而获得自动执行授权。运行前核对网络调用、文件读写、实验资源和 API 费用；未公开的论文、真实数据、密钥和个人配置留在本地。AI 生成的创新点及查新意见仍需对照原论文、实验和人工判断。

## 来源、许可和版本

本库是第三方资料的整理与导览，不冒充上游原创，不以统一许可证覆盖第三方内容。来源、固定提交和摘要位于各模块的 `SOURCE_MANIFEST.json`，许可证保留在对应上游目录。见 [第三方说明](THIRD_PARTY_NOTICES.md)。

最近整理日期：**2026-10-22**；上游快照仍为 2026-10-11 采集的固定版本，不代表自动追踪最新上游。

从本仓库根目录可运行 `python3 scripts/verify_bundle.py`（Windows 可用 `py -3.12 scripts/verify_bundle.py`）核对模块登记、复用来源、发布清单与摘要；它不会加载或运行上游技能。后续修改文件后，需要维护者审查并更新清单与摘要。详细记录见 [本地验证记录](docs/VALIDATION.md)。

首次上传见 [发布说明](docs/PUBLISH.md)。本地文件准备完成与远程发布成功是两个状态；是否已上传应以 GitHub 仓库及实际提交为准。

# 论文创新点 Skills 中文索引

本页以 `modules/idea-discovery/` 为相对路径基准，链接到已收录源码中的入口。技能用途依据对应上游说明整理；下面的“产出”指工作流设计目标，不表示本次已经运行或获得这些结果。来源与固定版本见 [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json)。

## 先按任务选择

| 你现在需要什么 | 优先入口 |
|---|---|
| 把一个宽泛方向推进为候选、查新和方法计划 | ARIS：`idea-discovery`，或按下表分步使用 |
| 先做一轮轻量头脑风暴，换角度找问题 | Orchestra：`brainstorming-research-ideas` + `creative-thinking-for-research` |
| 核对一个具体贡献有没有被已有论文覆盖 | ResearchStudio：`scoop-check`；先用 `paper-search` 补文献 |
| 把观察变成可证伪假设，并排除其他解释 | K-Dense：`hypothesis-generation` + `scientific-critical-thinking` |
| 从研究兴趣建立问题卡、证据需求与研究计划 | ClaudeScholar：`research-ideation` |

## 01 · ARIS：优先阅读的八个入口

**收录范围：**完整原仓库源码快照，包含下列主流程入口、其他技能、共享参考资料、工具与宿主适配。八个入口是本索引为创新点工作挑选的阅读顺序，不是上游全部技能数量。

上游说明：[中文 README](01_ARIS/upstream/README_CN.md) · [Codex 适配中文说明](01_ARIS/upstream/skills/skills-codex/README_CN.md)

| 技能入口 | 什么时候用 | 主要工作与预期产出 |
|---|---|---|
| [idea-discovery](01_ARIS/upstream/skills/idea-discovery/SKILL.md) | 希望把创新点探索串起来 | 编排文献、创意、查新、审阅与细化，形成候选报告、方案和实验计划。 |
| [research-lit](01_ARIS/upstream/skills/research-lit/SKILL.md) | 需要理解一个方向或几篇论文 | 检索、阅读、归纳相关工作，为判断问题与方法差异提供依据。 |
| [idea-creator](01_ARIS/upstream/skills/idea-creator/SKILL.md) | 有方向，缺少具体研究切入点 | 生成、比较和排序候选；其完整流程还可能调用查新与小规模实验。 |
| [novelty-check](01_ARIS/upstream/skills/novelty-check/SKILL.md) | 已有具体方法，准备查新 | 拆出核心技术主张，对照近期文献，寻找已有覆盖与可解释的差异。 |
| [research-review](01_ARIS/upstream/skills/research-review/SKILL.md) | 希望得到独立视角的批评 | 通过所配置的外部审阅后端检查研究论点、方法与证据。 |
| [research-refine](01_ARIS/upstream/skills/research-refine/SKILL.md) | 问题明确，技术路线仍模糊 | 锚定研究问题，细化主要机制、实现路径和最小验证。 |
| [experiment-plan](01_ARIS/upstream/skills/experiment-plan/SKILL.md) | 已选方向，需要规划验证 | 把论文主张对应到基线、实验、消融和资源安排。 |
| [research-refine-pipeline](01_ARIS/upstream/skills/research-refine-pipeline/SKILL.md) | 希望一次得到方法与实验路线 | 串联 `research-refine` 和 `experiment-plan`，整理最终方案与下一步。 |

**建议用法：**先 `research-lit` → `idea-creator` → `novelty-check`，人工选定一个候选后再细化。完整自动流程是否适合当前预算，要结合其具体步骤判断；文档包含的默认实验和审阅安排，不代表本次已执行。

**环境边界：**共享文件仍保留在原路径。跨模型审阅、联网检索及实验执行分别依赖所选宿主和后端。使用 Codex 时先看适配说明及其中的对应入口，不直接假定主版本的工具名适用于当前环境。

## 02 · Orchestra：两个轻量创意思考技能

**收录范围：**原仓库的整个 `21-research-ideation` 目录及根说明、许可，未收录其余科研分类。上游说明：[README](02_Orchestra/upstream/README.md)。

| 技能入口 | 主要用途 |
|---|---|
| [brainstorming-research-ideas](02_Orchestra/upstream/21-research-ideation/brainstorming-research-ideas/SKILL.md) | 从问题、矛盾、失败场景、约束变化等角度发散，再筛选并细化候选。 |
| [creative-thinking-for-research](02_Orchestra/upstream/21-research-ideation/creative-thinking-for-research/SKILL.md) | 通过问题重述、结构类比、约束操纵、反转和抽象层次变化寻找新角度。 |

**建议用法：**带入三至五篇参考论文、已有基线、算力上限和不想重复的路线，要求每个候选说明“为什么值得做、与哪篇工作最接近、最小实验是什么”。这里的轻量指思考流程较容易单独使用；实际调用仍需宿主能读取技能，外部文献也需要相应来源支持。

## 03 · ResearchStudio-Idea：检索、构思与重合检查

**收录范围：**整个 `ResearchStudio-Idea` 子树，以及根说明、许可等文档；ResearchStudio 的其他子项目不在本次范围。上游说明：[Idea 子项目 README](03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/README.md)。

| 技能入口 | 所需输入 | 主要工作与预期产出 |
|---|---|---|
| [paper-search](03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/paper_search/SKILL.md) | 关键词、年份范围，可加会议范围 | 汇总多学术来源的论文结果，为构思和查新建立文献基础。 |
| [idea-spark](03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/idea_spark/SKILL.md) | 研究问题或方向，可附论文与算力约束 | 细化研究动机和方法机制，组织为 idea card，并对照已有工作审查。 |
| [scoop-check](03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/scoop_check/SKILL.md) | 研究问题 + 所声称的创新点 | 查找最接近的工作，逐项判断重合程度，明确仍可成立的差异表述。 |

**建议用法：**已有候选时优先使用 `scoop-check`。输入应具体到机制，例如“记忆何时写入、如何筛选、何时检索”，只有“用记忆改善 Agent”这样的宽泛表述不足以精确查新。

**环境边界：**检索、论文抓取与解析依赖网络及脚本环境；API 凭据要求取决于来源，PDF 导出另有可选工具。部分上游说明链接指向外部站点，不保证离线可用。查新结果受检索覆盖、时间和对论文的理解限制；idea card 与模型评价都不是创新性或实验有效性的证明。

## 04 · K-Dense：四个科学思考与证据技能

**收录范围：**以下四个完整技能目录及根文档。上游说明：[README](04_KDense/upstream/README.md)。

| 技能入口 | 主要用途 | 使用时需注意 |
|---|---|---|
| [scientific-brainstorming](04_KDense/upstream/skills/scientific-brainstorming/SKILL.md) | 独立发散、整理假设、讨论评价和记录取舍 | 基础思考可由兼容宿主完成；可选本地工具另需 Python。 |
| [hypothesis-generation](04_KDense/upstream/skills/hypothesis-generation/SKILL.md) | 从观察提出候选与竞争解释，导出区分性预测和测量方案 | 适合把“可能有效”具体化为可支持、也可推翻的研究假设。 |
| [literature-review](04_KDense/upstream/skills/literature-review/SKILL.md) | 组织检索、筛选、证据综合与引用核对 | 网络检索、Python 工具和可选 PDF/绘图功能有不同依赖。 |
| [scientific-critical-thinking](04_KDense/upstream/skills/scientific-critical-thinking/SKILL.md) | 检查证据质量、实验设计、混杂因素与统计解释 | 可使用已提供的论文、实验表格和研究计划开展证据审查。 |

**建议用法：**如果 CV 方法只有一点指标提升，先列出数据划分、训练预算、增强策略等可能解释，再设计区分实验。若 Agent 策略提升效果，检查是否只是用了更多 token、调用次数或检索文档。这些是验证问题的示例，不预设原因或结论。

四个目录没有替代整个 K-Dense 技能库。上游提到的其他兄弟技能与外部服务，应在需要相应功能时按原文核对。

## 05 · ClaudeScholar：从兴趣到研究问题卡

**收录范围：**完整 `main` 和完整 `codex` 分支源码快照，分别保留，未互相覆盖。两个分支可能含不同宿主设置与配套文件。

| 分支 | 优先技能 | 配套说明 |
|---|---|---|
| `upstream_main` | [research-ideation](05_ClaudeScholar/upstream_main/skills/research-ideation/SKILL.md) | [中文 README](05_ClaudeScholar/upstream_main/README.zh-CN.md) · [MCP 配置说明](05_ClaudeScholar/upstream_main/MCP_SETUP.zh-CN.md) |
| `upstream_codex` | [research-ideation](05_ClaudeScholar/upstream_codex/skills/research-ideation/SKILL.md) | [中文 README](05_ClaudeScholar/upstream_codex/README.zh-CN.md) · [MCP 配置说明](05_ClaudeScholar/upstream_codex/MCP_SETUP.zh-CN.md) |

该技能通过 5W1H、文献与 gap 分析，把兴趣整理为研究问题卡，明确假设、现有证据、缺失证据、支持与反证条件、下一步。Zotero 等联动功能需要额外配置，并不因源码在目录中就已可用。其他开发、写作和知识库技能随原仓库一并保留，但不是本次创新点筛选的优先入口。

## 使用前的统一约定

先选一套完成一次有限任务，保留原文献、具体贡献、最近工作差异和验证计划，再决定是否扩展。多个技能的评价可以用于交叉检查，但不能替代对原论文和实验的核实。

本次提供源码入口与导览，没有自动注册技能、变更 Agent 全局配置或运行上游流程。实际接入方式、依赖和调用语法，以对应固定版本的上游文档为准。

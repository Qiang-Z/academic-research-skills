# 技能完整用法速查

[返回首页](../README.md) · [新手第一次使用](GETTING_STARTED.md) · [模块索引](../MODULE_INDEX.md) · [运行范围](RUNTIME_STATUS.md)

本页保留八个模块的全部 50 行重点/核心技能用法。跨模块存在同名复用，行数不是互不重复的技能数。第一次使用可先走新手路线，需要换技能或扩展任务时再来查。

链接优先使用 ARIS 的 Codex 适配和 ClaudeScholar 的 codex 分支；其他宿主请从模块中文索引选择主版本或 main。保留完整快照以便读取共享参考。任务目标与实际执行结果以记录区分。

将每行的材料、提问填入下列模板，输出放在自己的研究项目目录：

```text
请先阅读 modules/[模块ID]/SKILL_INDEX.md，
选择适合当前宿主的[来源/技能名]，读取其 SKILL.md 及必要参考。
任务：[下表提问]。
材料：[文件、版本与来源]；输出：[自己的项目目录]。
本轮范围：[只读审查 / 写文档 / 指定计算与资源上限]。
先核对缺失输入和依赖，记录实际产物、失败和未执行项。
```

## 按模块查看每个技能的用法

[文献检索与综述](#literature) · [论文创新点探索](#ideas) · [实验设计与复现](#experiments) · [数据分析与统计](#analysis) · [论文写作与润色](#writing) · [学术绘图与可视化](#figures) · [投稿与审稿回复](#submission) · [科研知识管理](#knowledge)

每个模块列出其中文索引内的全部重点/核心技能。同名技能可能跨模块复用，下面的行数不代表互不重复的新技能数量。展开表格后，把“材料”和“提问”填入上面的通用模板。

<a id="literature"></a>

### 文献检索与综述

先理解一个方向用 research-lit；扩充候选用 paper-search；已有材料需要综合时用 literature-review。

模块 ID：`literature-review` · [中文索引 / 其他宿主](../modules/literature-review/SKILL_INDEX.md) · [完整使用说明](../modules/literature-review/USAGE.md) · [示例](../modules/literature-review/examples/README.md)

<details>
<summary><strong>展开 5 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [research-lit](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/research-lit/SKILL.md)<br>ARIS | **材料：**研究问题、论文文件或检索范围。<br>**提问：**围绕[问题]阅读[材料]，记录版本和实际阅读范围，输出论文笔记、主题比较与待读问题。 | 论文笔记、相关工作、主题归纳 |
| [paper-search](../modules/idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/paper_search/SKILL.md)<br>ResearchStudio | **材料：**检索词、年份、来源、每源数量。<br>**提问：**按[检索词/年份/来源]收集候选，保留标识符、去重数、筛选理由与失败来源。 | 候选论文表、检索日志 |
| [literature-review](../modules/idea-discovery/04_KDense/upstream/skills/literature-review/SKILL.md)<br>K-Dense | **材料：**综述问题、纳排标准、检索记录、可读全文。<br>**提问：**按[纳排标准]综合[材料]，整理证据矩阵和专题综述，标出分歧与阅读范围。 | 筛选记录、证据矩阵、综述草稿 |
| [obsidian-literature-workflow](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/obsidian-literature-workflow/SKILL.md)<br>ClaudeScholar | **材料：**已绑定的项目知识库、论文笔记、证据记录。<br>**提问：**整理[项目]的论文笔记，按方法分类，将有证据的主张汇总为文献概览和写作材料。 | 分类概览、主张关联、写作交接 |
| [citation-verification](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/citation-verification/SKILL.md)<br>ClaudeScholar | **材料：**引用条目、拟支持的句子、DOI/arXiv ID 或原文。<br>**提问：**核对[引用清单]的身份、版本和元数据，再检查原文是否支持[句子]，保留待核验项。 | 引用核对表、原文定位、未决项 |

</details>

没有知识库时可用普通 Markdown/CSV 模板；需要 Zotero 导入时转到[知识管理](#knowledge)。摘要级阅读须保留阅读范围。部分路径已有[实际运行报告](../modules/literature-review/runtime-tests/2026-10-22/README.md)，其中记录了成功、缺陷和缺依赖。

<a id="ideas"></a>

### 论文创新点探索

轻量发散先选 Orchestra 或 scientific-brainstorming；已有具体贡献先查新，再细化方法与验证计划。

模块 ID：`idea-discovery` · [中文索引 / 其他宿主](../modules/idea-discovery/SKILL_INDEX.md) · [完整使用说明](../modules/idea-discovery/README_使用说明.md)

<details>
<summary><strong>展开 18 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [idea-discovery](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/idea-discovery/SKILL.md)<br>ARIS | **材料：**方向、参考论文、数据与资源限制。<br>**提问：**按 idea-discovery 推进[方向]，形成候选、查新记录、方案和验证计划；本轮执行范围与预算为[范围/预算]。 | 候选报告、方案、实验计划 |
| [research-lit](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/research-lit/SKILL.md)<br>ARIS | **材料：**研究问题、已有论文、检索范围。<br>**提问：**梳理[问题/论文]中的已有方法、证据差异和未解决问题，为下一步构思提供材料。 | 相关工作与问题清单 |
| [idea-creator](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/idea-creator/SKILL.md)<br>ARIS | **材料：**文献笔记、已有基线、资源上限。<br>**提问：**基于[材料]提出并排序研究候选，说明机制、最近工作和最小验证；本轮只生成候选。 | 候选排序、验证方向 |
| [novelty-check](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/novelty-check/SKILL.md)<br>ARIS | **材料：**具体方法、核心技术主张。<br>**提问：**对[技术主张]查新，逐项比较最接近工作，列出已覆盖内容、可辨差异和检索限制。 | 主张对照、近邻文献 |
| [research-review](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/research-review/SKILL.md)<br>ARIS | **材料：**方案或草稿、现有证据、已知限制。<br>**提问：**审阅[材料]的论点、方法与证据，按严重程度列问题和改进建议，并注明实际审阅方式。 | 审阅意见、修改优先级 |
| [research-refine](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/research-refine/SKILL.md)<br>ARIS | **材料：**已选问题、候选机制、约束。<br>**提问：**把[候选方法]细化为问题明确、机制可实现、能够被实验反驳的方案。 | 方法方案、最小验证 |
| [experiment-plan](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-plan/SKILL.md)<br>ARIS | **材料：**研究主张、基线、数据、预算。<br>**提问：**为[方案]设计基线、主实验和消融，将每项实验对应到主张并估算资源；本轮只规划。 | 实验计划、追踪表 |
| [research-refine-pipeline](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/research-refine-pipeline/SKILL.md)<br>ARIS | **材料：**候选方案、证据、资源预算。<br>**提问：**先细化[方法]，再为稳定后的方案安排实验，交付方案、审阅记录和下一步路线。 | 方法与实验规划包 |
| [brainstorming-research-ideas](../modules/idea-discovery/02_Orchestra/upstream/21-research-ideation/brainstorming-research-ideas/SKILL.md)<br>Orchestra | **材料：**参考论文、失败场景、资源约束。<br>**提问：**从矛盾、失败案例和约束变化出发，为[方向]发散候选，再筛选最值得验证的几个。 | 候选问题、筛选理由 |
| [creative-thinking-for-research](../modules/idea-discovery/02_Orchestra/upstream/21-research-ideation/creative-thinking-for-research/SKILL.md)<br>Orchestra | **材料：**卡住的问题、当前假设。<br>**提问：**对[问题]做重述、类比、反转和约束变化，给出不同思路及其可检验预测。 | 新视角、替代路线 |
| [paper-search](../modules/idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/paper_search/SKILL.md)<br>ResearchStudio | **材料：**关键词、年份、来源或会议范围。<br>**提问：**检索[关键词]在[年份范围]的论文，保留来源、标识符、去重和失败记录。 | 构思用文献清单 |
| [idea-spark](../modules/idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/idea_spark/SKILL.md)<br>ResearchStudio | **材料：**研究问题、参考文献、可用资源。<br>**提问：**将[问题]整理为 idea card，说明动机、方法机制、最近工作差异与验证办法。 | Idea card、机制与对照 |
| [scoop-check](../modules/idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/scoop_check/SKILL.md)<br>ResearchStudio | **材料：**研究问题、具体创新点。<br>**提问：**检查[机制/贡献]是否已被已有工作覆盖，给出重合证据和仍可成立的差异表述。 | 重合分析、贡献改写 |
| [scientific-brainstorming](../modules/idea-discovery/04_KDense/upstream/skills/scientific-brainstorming/SKILL.md)<br>K-Dense | **材料：**研究兴趣、已有发现、约束。<br>**提问：**围绕[现象]进行科学头脑风暴，整理候选问题、假设、评价方式和取舍。 | 候选、假设、取舍记录 |
| [hypothesis-generation](../modules/idea-discovery/04_KDense/upstream/skills/hypothesis-generation/SKILL.md)<br>K-Dense | **材料：**实际观察、已有解释、测量条件。<br>**提问：**为[观察]提出竞争假设，分别写出可区分预测、测量办法和反证条件。 | 可证伪假设、区分实验 |
| [literature-review](../modules/idea-discovery/04_KDense/upstream/skills/literature-review/SKILL.md)<br>K-Dense | **材料：**研究问题、纳排标准、论文材料。<br>**提问：**围绕[问题]整理检索和筛选记录，比较证据与分歧，寻找需要验证的空缺。 | 证据矩阵、问题依据 |
| [scientific-critical-thinking](../modules/idea-discovery/04_KDense/upstream/skills/scientific-critical-thinking/SKILL.md)<br>K-Dense | **材料：**论文或方案、实验设计、结果。<br>**提问：**检查[材料]的证据质量、混杂与过度推断，指出位置及可排除替代解释的验证。 | 疑点、替代解释、改进建议 |
| [research-ideation](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/research-ideation/SKILL.md)<br>ClaudeScholar | **材料：**研究兴趣、参考论文、已有资源。<br>**提问：**用 5W1H 和文献 gap 分析把[兴趣]变成问题卡，列出假设、证据缺口、支持与反证条件。 | 问题卡、证据需求、下一步 |

</details>

这是索引精选的 18 个入口。完整 idea-discovery 等流程可能安排实验与审阅，提问时写清范围和预算；查新结论受实际检索覆盖限制。

<a id="experiments"></a>

### 实验设计与复现

先做 experiment-plan，再按需要做消融、实现、运行和审计。当前主要面向计算实验。

模块 ID：`experiment-design` · [中文索引 / 其他宿主](../modules/experiment-design/SKILL_INDEX.md) · [完整使用说明](../modules/experiment-design/USAGE.md) · [示例](../modules/experiment-design/examples/README.md)

<details>
<summary><strong>展开 6 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [experiment-plan](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-plan/SKILL.md)<br>ARIS | **材料：**研究主张、目标设置、基线、数据、预算。<br>**提问：**把[研究主张]对应到基线、主实验、消融和反证条件，固定评价协议与资源估计；本轮只设计。 | 实验计划、主张—实验映射 |
| [ablation-planner](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/ablation-planner/SKILL.md)<br>ARIS | **材料：**方法组件、主张、已有结果、预算。<br>**提问：**为[组件]设计移除、简单替换及敏感性比较，说明控制变量、要区分的问题、优先级与成本。 | 消融矩阵、执行顺序 |
| [experiment-bridge](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-bridge/SKILL.md)<br>ARIS | **材料：**实验计划、已有代码、数据、目标环境。<br>**提问：**按[计划]复用已有代码准备实现和最小检查，设置 AUTO_DEPLOY=false，保存配置、命令与日志。 | 代码、配置、最小检查记录 |
| [run-experiment](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/run-experiment/SKILL.md)<br>ARIS | **材料：**可运行代码、配置、机器、资源与停止范围。<br>**提问：**在[指定环境]按[命令/配置]运行实验，预算[上限]，记录 Run ID、环境、日志、输出与实际状态。 | 真实运行记录、结果、失败记录 |
| [training-check](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/training-check/SKILL.md)<br>ARIS | **材料：**运行标识、指标日志、基线、停止范围。<br>**提问：**对[运行/日志]做一次检查，判断 CONTINUE、WAIT 或 STOP，列证据和理由；本轮只给建议。 | 指标快照、异常与行动建议 |
| [experiment-audit](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-audit/SKILL.md)<br>ARIS | **材料：**评价代码、标签来源、原始结果、配置、拟写主张。<br>**提问：**审计[文件路径]的真值来源、指标计算、结果存在性和表述范围，记录实际审阅身份与未解决问题。 | 实验审计报告与证据 |

</details>

可选 [monitor-experiment](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/monitor-experiment/SKILL.md)：提供任务与日志位置，要求“汇总当前状态、可用结果与缺失项”。复现规则见[辅助说明](../modules/experiment-design/SKILL_INDEX.md)。[本轮验证仍在进行](../modules/experiment-design/runtime-tests/2026-10-22/README.md)；已有 Windows 队列问题，使用前核对所选后端。

<a id="analysis"></a>

### 数据分析与统计

只想整理现有成绩先用 analyze-results；需要区间、检验或真实图表时使用 results-analysis。

模块 ID：`data-analysis` · [中文索引 / 其他宿主](../modules/data-analysis/SKILL_INDEX.md) · [完整使用说明](../modules/data-analysis/USAGE.md) · [示例](../modules/data-analysis/examples/README.md)

<details>
<summary><strong>展开 5 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [analyze-results](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/analyze-results/SKILL.md)<br>ARIS | **材料：**JSON/CSV、指标定义和方向、配置、基线。<br>**提问：**整理[结果目录]，核对覆盖与来源，报告原始指标、基线差值和异常；先做描述性比较。 | 结果表、描述比较、待查问题 |
| [results-analysis](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/results-analysis/SKILL.md)<br>ClaudeScholar | **材料：**原始记录、分析单位、配对/层级关系、协议。<br>**提问：**先核对[数据]的独立单位与可比性，再完成适用的效应量、区间和图表；前提不足时列缺口。 | 分析报告、统计附录、图表目录 |
| [result-to-claim](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/result-to-claim/SKILL.md)<br>ARIS | **材料：**拟写主张、数值来源、基线、限制与审计材料。<br>**提问：**将[主张清单]与[结果文件]逐项对照，判断支持程度，给出允许措辞和待补证据。 | 主张—证据表、措辞修订 |
| [results-report](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/results-report/SKILL.md)<br>ClaudeScholar | **材料：**已核对的分析报告、统计附录、图表目录。<br>**提问：**把[完整分析包]整理为内部实验报告，逐图解释，保留失败、限制、决策和产物索引。 | 内部总结、逐图解释、下一步 |
| [scientific-critical-thinking](../modules/idea-discovery/04_KDense/upstream/skills/scientific-critical-thinking/SKILL.md)<br>K-Dense | **材料：**研究设计、原始证据、结果与结论。<br>**提问：**检查[分析/结论]的选择偏差、混杂、依赖关系和外推，指出证据位置、影响与改进办法。 | 推断问题、剩余不确定性 |

</details>

只有汇总值时先做描述；区间和检验需要明确的分析单位与原始数据。results-report 接收已核对的分析包。可从[原创配对分析示例](../modules/data-analysis/examples/README.md)练习。

<a id="writing"></a>

### 论文写作与润色

组织全文先用 paper-plan；起草、重组中文材料、润色和数字核对分别选对应技能。

模块 ID：`paper-writing` · [中文索引 / 其他宿主](../modules/paper-writing/SKILL_INDEX.md) · [完整使用说明](../modules/paper-writing/USAGE.md) · [示例](../modules/paper-writing/examples/README.md)

<details>
<summary><strong>展开 6 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [paper-plan](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-plan/SKILL.md)<br>ARIS | **材料：**研究问题、主张证据表、结果、限制。<br>**提问：**依据[材料目录]制定大纲，将主张对应到结果、章节、图表和引用；缺证据处标为待补。 | PAPER_PLAN.md、章节与图表计划 |
| [paper-write](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-write/SKILL.md)<br>ARIS | **材料：**已定大纲、真实图表与结果、核验过的引用。<br>**提问：**依据[大纲]和[证据目录]起草[章节]的 LaTeX，保留来源与待补项，记录编译和审阅状态。 | 分节 LaTeX、引用文件、检查记录 |
| [ml-paper-writing](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/ml-paper-writing/SKILL.md)<br>ClaudeScholar | **材料：**ML/AI 项目材料、写作阶段、主张与引用。<br>**提问：**以[材料]起草[章节/稿件]，将主要陈述对应到证据记录，保留限制与尚未取得的证据。 | ML/AI 稿件、证据对应、缺项 |
| [nature-writing](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/nature-writing/SKILL.md)<br>ClaudeScholar | **材料：**中文研究笔记、目标章节、主张和证据。<br>**提问：**将[中文笔记]组织为[引言/方法/结果/讨论]，写清问题、观察、证据与边界。 | 结构化学术正文、缺失项 |
| [nature-polishing](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/nature-polishing/SKILL.md)<br>ClaudeScholar | **材料：**中英文原稿、术语、读者、修改范围。<br>**提问：**润色或翻译[段落]，保留数字、比较方向和限定词，返回原文、改文及修改理由。 | 润色/翻译稿、修改对照 |
| [paper-claim-audit](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-claim-audit/SKILL.md)<br>ARIS | **材料：**稿件源文件、原始结果、配置、图表。<br>**提问：**核对[稿件]与[原始产物]，逐条定位数字、分母、比较和范围，记录审阅方式与未解决项。 | 逐主张审计报告、状态记录 |

</details>

生成 LaTeX 后需要实际编译检查；证据不足时保留待补项。Nature 类技能提供写作方法参考，具体稿件要求仍按目标期刊确定。

<a id="figures"></a>

### 学术绘图与可视化

数值比较选 paper-figure；需要可编辑架构图选 figure-spec；流程和时序选 mermaid-diagram。

模块 ID：`academic-figures` · [中文索引 / 其他宿主](../modules/academic-figures/SKILL_INDEX.md) · [完整使用说明](../modules/academic-figures/USAGE.md) · [示例](../modules/academic-figures/examples/README.md)

<details>
<summary><strong>展开 3 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [paper-figure](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-figure/SKILL.md)<br>ARIS | **材料：**核对过的 CSV/JSON、指标单位、区间含义、图表计划。<br>**提问：**用[真实分析产物]绘制[对照/曲线/消融图]，保留全部条件与数据映射，交付脚本、矢量图、图注和核对记录。 | 绘图脚本、矢量图、比较表 |
| [figure-spec](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/figure-spec/SKILL.md)<br>ARIS | **材料：**实际组件、节点 ID、分组、连接关系和布局。<br>**提问：**将[组件及连接关系]转为 FigureSpec JSON 和可编辑 SVG，检查节点、箭头、文字与布局。 | JSON、可编辑 SVG、检查记录 |
| [mermaid-diagram](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/mermaid-diagram/SKILL.md)<br>ARIS | **材料：**真实流程、分支条件、时序或实体关系。<br>**提问：**把[实际流程]绘成[流程/时序]图，交付一致的 MMD 与 Markdown，记录实际渲染结果。 | MMD、Markdown、渲染预览 |

</details>

数据图从真实分析产物读取数值，误差线须有计算依据。可选 [paper-illustration](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-illustration/SKILL.md)：提供主题、概念关系和风格制作说明插图，并核对文字与关系。当前[有限测试](../modules/academic-figures/examples/VALIDATION.md)覆盖原创图表与 FigureSpec 渲染组件。

<a id="submission"></a>

### 投稿与审稿回复

投稿前用 paper-self-review；收到意见后用 review-response；多轮、严格限字回复用 rebuttal。

模块 ID：`submission-rebuttal` · [中文索引 / 其他宿主](../modules/submission-rebuttal/SKILL_INDEX.md) · [完整使用说明](../modules/submission-rebuttal/USAGE.md) · [示例](../modules/submission-rebuttal/examples/README.md)

<details>
<summary><strong>展开 3 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [paper-self-review](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/paper-self-review/SKILL.md)<br>ClaudeScholar | **材料：**完整稿件、结果证据、图表与引用。<br>**提问：**检查[稿件]的结构、主张、数字、引用和图表，指出位置，给出保留、削弱、修改或删除建议。 | 稿件自查、证据缺口、修改建议 |
| [review-response](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/review-response/SKILL.md)<br>ClaudeScholar | **材料：**原始意见、稿件版本、证据、已完成修改。<br>**提问：**拆解[审稿意见]，逐项给策略、证据位置与回复；未完成实验或修改保留待办状态。 | 意见分类、证据矩阵、逐条回复 |
| [rebuttal](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/rebuttal/SKILL.md)<br>ARIS | **材料：**多审稿人意见、当前轮次、已核实规则、稿件与结果。<br>**提问：**处理[意见与稿件]，遵循[本轮官方规则]，建立问题板、回复和承诺台账，检查每项意见的去向。 | 限字回复、问题板、修改与承诺记录 |

</details>

进阶 [resubmit-pipeline](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/resubmit-pipeline/SKILL.md)：提供旧稿、目标模板与规则，要求“在独立目录准备重投版本，仅修改[约定范围]并保留待办”。匿名、字数和附件要求需核对目标轮次；“已完成修改”应能定位到实际稿件。

<a id="knowledge"></a>

### 科研知识管理

暂未配置 Zotero/Obsidian 时，先用本模块模板保存普通 Markdown；已经有知识库时再选下面的集成入口。

模块 ID：`research-knowledge` · [中文索引 / 其他宿主](../modules/research-knowledge/SKILL_INDEX.md) · [完整使用说明](../modules/research-knowledge/USAGE.md) · [示例](../modules/research-knowledge/examples/README.md)

<details>
<summary><strong>展开 4 个技能的材料、提问与产物</strong></summary>

| 技能 / 来源 | 准备什么，怎样提问 | 预期产物 |
|---|---|---|
| [research-wiki](../modules/idea-discovery/01_ARIS/upstream/skills/skills-codex/research-wiki/SKILL.md)<br>ARIS | **材料：**项目目录、论文/idea/实验/主张材料、可用 helper。<br>**提问：**在[项目目录]整理[指定材料]，连接论文、idea、实验和主张，检查页面、关系、索引与变更日志。 | Wiki 页面、关系文件、索引与日志 |
| [obsidian-project-kb-core](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/obsidian-project-kb-core/SKILL.md)<br>ClaudeScholar | **材料：**已有 vault、项目标识、仓库绑定、写入范围。<br>**提问：**仅维护[指定项目]，检查绑定，建立 Hub、Plan、Index 和唯一注册表，报告链接与登记问题。 | 项目骨架、导航、注册表、健康检查 |
| [obsidian-source-ingestion](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/obsidian-source-ingestion/SKILL.md)<br>ClaudeScholar | **材料：**已建立的项目、原始来源、类型/版本、阅读状态。<br>**提问：**把[来源材料]登记到[项目]，保留身份、版本和阅读范围，更新注册表、Index 与 Daily。 | 来源笔记、索引与当日日志 |
| [zotero-obsidian-bridge](../modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/zotero-obsidian-bridge/SKILL.md)<br>ClaudeScholar | **材料：**可访问的 Zotero 条目、可读文献、已绑定项目。<br>**提问：**将[真实条目]导入[项目]，建立唯一论文笔记与证据记录，标明阅读范围，再整理可追溯的综合材料。 | 论文笔记、证据记录、综合与图谱 |

</details>

[普通 Markdown 模板](../modules/research-knowledge/templates/README.md)与[教学知识库](../modules/research-knowledge/examples/README.md)可用于入门；真实 Zotero/Obsidian 连接尚未验证。来源登记后仍需记录实际阅读范围；按各入口约定处理绑定路径和主张状态。

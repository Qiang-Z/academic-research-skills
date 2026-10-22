# 数据分析与统计 · 技能中文索引

[模块首页](README.md) · [使用说明](USAGE.md) · [示例目录](examples/README.md) · [来源清单](SOURCE_MANIFEST.json)

本模块整理 **5 个核心技能名称、9 个文件入口**，复用 **3 个来源项目、4 份固定快照**：ARIS 的主版本/Codex 入口、ClaudeScholar 的 main/codex 两份快照，以及 K-Dense 快照。所有上游文件仍位于 idea-discovery 原目录；本模块不复制、安装或更新这些技能。

主要面向计算与机器学习实验的结果整理、统计分析和证据解释。以下产出是技能设计目标，不代表本次已执行上游工作流，也不构成通用统计软件包。真实分析仍需原始材料、研究设计及相应运行环境。

## 先区分三个层次

| 层次 | 回答的问题 | 最低证据 | 不能直接推出什么 |
|---|---|---|---|
| 描述统计 | 已收集的结果是什么样 | 指标定义、实际结果、运行覆盖与来源 | 观察到差异不等于总体差异或显著性 |
| 统计推断 | 在指定抽样/随机机制及假设下，差异有多不确定 | 分析单位、可比较数据、依赖结构、预定比较和适用方法 | 小 p 值不等于大效应、实际价值或机制证实 |
| 结果到主张 | 这些证据允许怎样表述结论 | 数值、设计、适用范围、替代解释、缺失证据 | 模型审阅标签不能代替原始证据或独立复现 |

选择当前需要的一层；只有汇总均值时，先做可追溯的描述，不补造逐样本数据、置信区间或检验结果。

## 按任务选择入口

| 当前任务 | 优先入口 | 输入 | 预期交付 |
|---|---|---|---|
| 快速整理一批已存在的实验结果 | **analyze-results** | JSON/CSV、指标方向、基线、配置和运行记录 | 原始数据表、描述性比较、观察与后续问题 |
| 完成有统计依据的分析与真实图表 | **results-analysis** | 原始结果、分析单位、配对/层级关系、评价协议、主要比较 | analysis-report、stats-appendix、figure-catalog 与真实图表；材料不完整时只做审计 |
| 判断结果支持哪些研究主张 | **result-to-claim** | 拟写主张、数值与来源、基线、已知限制、审计材料 | 支持/部分支持/不支持、缺口、主张改写与下一步 |
| 从已完成分析整理内部实验报告 | **results-report** | 已核对的完整分析包、实验轮次与报告目的 | 内部总结、逐图解释、负结果、决策及产物索引 |
| 检查偏差、混杂及过度推断 | **scientific-critical-thinking** | 研究问题、设计、结果与来源 | 有证据位置的疑点、解释后果、剩余不确定性及改进方向 |

## 01 · analyze-results：轻量整理与描述

主版本：[analyze-results/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/analyze-results/SKILL.md) · Codex：[skills-codex/analyze-results/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/analyze-results/SKILL.md)

**用途：**定位 JSON/CSV 结果，按模型、超参数、数据配置及主要指标整理对照表；总结观察、可能解释、研究意义和下一步实验。多次运行时可报告适当的均值与标准差，记录趋势和可疑结果。

**版本与依赖：**两入口的工作流正文一致，主要区别是宿主 frontmatter。技能是工作指引，不是已附带并验证的完整统计分析程序；读取本地材料不必连接 W&B，实际计算工具按目标研究项目准备。

**本模块补充：**先核对每个 seed 控制的是数据划分、初始化还是采样；运行间散布与目标总体的不确定性分开。上游要求相对基线改进，应用时需注明指标方向、分母与单位；分母为零或相对比例无明确含义时记为不适用，改报原始差值。准确率的百分点差与相对百分比不可混写。

**适用边界：**此入口没有提供完整的抽样设计、配对/聚类处理或多重比较方案。整理出均值与标准差后，若要检验、区间或显著性主张，应进入 `results-analysis` 的证据核对流程。

## 02 · results-analysis：统计分析包与证据审计

main：[results-analysis/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/results-analysis/SKILL.md) · codex：[results-analysis/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/results-analysis/SKILL.md)

**用途：**先锁定主要问题、指标、比较单位和样本关系，再完成有依据的描述、效应量、区间、检验及图表解释。它特别要求核对缺失和失败、方法间可比性，不把 subject×task、fold、window、trial 或 seed 自动当作独立样本。

**输入输出：**输入可包括逐样本预测、逐次运行指标、日志与评价协议；完整模式预期产出 `analysis-report.md`、`stats-appendix.md`、`figure-catalog.md` 和 `figures/`。候选主张需附证据、允许措辞、禁止的更强措辞、不确定性及下一项检查。这些是分析材料，不是论文 Results 正文。

**版本与依赖：**两个快照的入口文件内容相同；各自的参考文件仍保留在所属分支，按需要读取。生成真实统计与图表需要实际数据、可用计算/绘图工具及明确输出位置；仓库收录不表示这些依赖已安装或运行通过。

**缺失输入时：**上游允许只读审计模式，交付可用统计、不可用统计、阻塞项和候选主张；不生成伪完整分析包。没有逐样本/逐运行材料、分析单位不清、配对缺失或比较不公平时，保留具体缺口，不为满足输出清单补造检验、图表或胜负结论。

**外围方法说明：**上游 [statistical-methods.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/results-analysis/references/statistical-methods.md) 保留了教学性简化，例如按正态性检验结果自动换方法、把未拒绝假设写成“接受”、固定推荐重复次数，以及不带条件的效应量阈值。它们不应作为通用执行规则；先按设计、目标量、依赖关系和分布特征判断。参考 [使用说明的方法选择表](USAGE.md#4-统计方法选择简表)。本模块不修改上游快照。

## 03 · result-to-claim：限定结论范围

主版本：[result-to-claim/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/result-to-claim/SKILL.md) · Codex：[skills-codex/result-to-claim/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/result-to-claim/SKILL.md)

**用途：**把实验结果与原先主张对照，分别记录实际支持什么、不支持什么、缺什么证据，以及是否收窄主张或补充实验。数据可来自本地结果/日志，或已经配置并获准使用的 W&B、远程日志；网络服务不是阅读本模块的前提。

**证据存在与主张支持分开：**上游 `evidence_check.py` 预检查关注来源文件和所引数值是否存在。它的 `verified` 只表示这一检查成功，不表示指标计算正确、比较有效或主张成立。辅助程序无法定位或未执行时，应保留跳过状态；`path_missing` / `value_not_found` 不得包装成已有证据。

**版本差异：**主版本通过外部 Codex MCP 审阅；Codex 基础版本由第二个 Codex agent 审阅，并标记 `review_independence: same-family`、`acceptance_status: provisional`。审阅不可用时保留 `REVIEW_UNAVAILABLE`；Codex 版另要求 `BLOCKED` 审阅记录。执行者不能补写一个 PASS 代替实际审阅。

**使用边界：**原流程还可能更新研究 Wiki、项目记录并转入补充实验；这些后续动作取决于目标项目和本次任务范围。只有新证据或分析修正才可能改变判断，不靠定时重复裁决获得更强支持。没有实验完整性审计时保留临时状态，模型的 yes/partial/no 不替代统计假设和结果可追溯性。

## 04 · results-report：分析之后的内部实验报告

main：[results-report/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/results-report/SKILL.md) · codex：[results-report/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/results-report/SKILL.md)

**用途：**把已核对的分析包整理为内部实验总结，说明研究问题、实际执行、主要结果、逐图解释、失败与限制、认知变化、下一步动作和产物索引。它不负责从零完成严格统计，也不直接等同于论文正文或投稿图表排版。

**前置条件：**完整报告需要 `analysis-report.md`、`stats-appendix.md`、`figure-catalog.md`，以及明确的来源与主要比较。条件不满足时先写缺口摘要，返回 `results-analysis`；不能将零散表格润色成结论已确定的报告。可先用本模块 [报告提纲](templates/report-outline.md) 记录材料状态，但不标为上游完整交付。

**版本与写入位置：**两入口主要流程相同，仅项目记忆路径分别为 `.claude/project-memory/` 与 `.codex/project-memory/`。已绑定 Obsidian 的项目可按其约定写入 `Results/Reports/` 等位置；未绑定时使用明确指定的本地输出目录，不假定知识库或连接已配置。

## 05 · scientific-critical-thinking：检查推断是否超出证据

入口：[K-Dense scientific-critical-thinking/SKILL.md](../idea-discovery/04_KDense/upstream/skills/scientific-critical-thinking/SKILL.md)

**用途：**区分描述、预测与因果问题，核对独立分析单位、抽样与选择偏差、混杂、测量、缺失、重复比较和外推范围。输出应指出证据位置、疑点影响、剩余不确定性及可采取的改进，而非只给抽象质量标签。

**依赖与范围：**核心批判性审阅可基于已有材料，不需要联网执行。上游可选的 scientific-schematics 绘图涉及额外工具、密钥和外部服务，不是本模块的默认依赖，也不因文档提及就视为已安装。涉及专门研究领域的评价框架时，需另行确认其适用性；本模块不扩展为临床或人类研究方案工具。

## 跨模块交接与验证状态

- 从 [实验设计与复现](../experiment-design/README.md) 及其 [结果交接模板](../experiment-design/templates/results-handoff.md) 接收计划、协议、数据版本、配置、成功与失败运行、指标来源和已知差异。
- 用本模块 [分析计划](templates/analysis-plan.md)、[数据核对表](templates/data-audit.md)、[分析结果表](templates/analysis-table.csv) 和 [主张—证据表](templates/claim-evidence.csv) 保留分析过程；未知、未做、失败和不适用要分别说明。
- 需要补实验时返回实验模块；需要补文献证据时返回 [文献检索与综述](../literature-review/README.md)。写作接收的是带限制的结论及来源，不是孤立的“显著/不显著”标签。
- [来源与许可](THIRD_PARTY_NOTICES.md) 和 [验证记录](VALIDATION.md) 分别记录来源和检查范围。自有教学示例检查与上游工作流执行分开，上游 `runtime_tested` 不因文档、链接或示例通过而变为 `true`。

# 论文写作与润色 · 技能中文索引

[模块首页](README.md) · [使用说明](USAGE.md) · [教学示例](examples/README.md)

以下 **6 个技能名称对应 12 个入口文件**，来自 2 个项目、3 份既有固定快照。预期产出依据本地上游说明整理，不表示本次已执行或安装。

## 按任务选择

| 当前任务 | 优先入口 | 必需材料 | 预期产出 |
|---|---|---|---|
| 证据已有，但不知如何组织文章 | ARIS `paper-plan` | 问题、主张、结果、限制 | 大纲、主张证据矩阵、章节/图表/引用计划。 |
| 大纲已定，需要逐节写 LaTeX | ARIS `paper-write` | 大纲、分析、图表和来源 | 分节草稿、参考文献及质量检查。 |
| 从 ML/AI 项目材料起草文章 | ClaudeScholar `ml-paper-writing` | 项目材料、操作模式、证据和引用 | 与证据台账对应的草稿及待补材料。 |
| 中文笔记需要重组为学术段落 | ClaudeScholar `nature-writing` | 章节任务、核心主张、证据与边界 | 结构化正文、假设和缺失项。 |
| 已有中文/英文稿，需要润色或翻译 | ClaudeScholar `nature-polishing` | 原稿、术语、论点与修改范围 | 修改文本和修改说明，或原文/修改/理由对照。 |
| 稿件已有，需要逐条核对数字 | ARIS `paper-claim-audit` | 论文源文件、原始结果和配置 | 数值、比较与范围的证据追溯，逐项审计报告。 |

## 01 · paper-plan：先组织证据，再组织章节

主版本：[SKILL.md](../idea-discovery/01_ARIS/upstream/skills/paper-plan/SKILL.md) · Codex：[SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-plan/SKILL.md)

接收研究叙事、实验结果和审阅材料，优先读取存在的 `CLAIMS_FROM_RESULTS.md`，形成 `PAPER_PLAN.md`、主张证据矩阵、章节安排、图表与引用计划。主张缺证据时标记缺口；没有完成主张裁决时，草稿模式保留未裁决状态，不能升级为投稿就绪。

主版本的大纲审阅使用外部 Codex MCP；Codex 适配由第二个 Codex agent 审阅。主版另有可选 `style-ref`、结构提取与 `GAP_REPORT.md` 机制，基础 Codex 文件没有同样完整的扩展，不能直接互换参数。文档中的页数、会场和匿名设置是固定版本默认值，实际使用应核对目标年份与稿件类型的官方要求。

## 02 · paper-write：依据大纲逐节写作

主版本：[SKILL.md](../idea-discovery/01_ARIS/upstream/skills/paper-write/SKILL.md) · Codex：[SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-write/SKILL.md)

接收 `PAPER_PLAN.md`、研究叙事、真实图表及现有文献文件，创建分节 LaTeX 草稿，完成引用、符号、段落结构与交叉审阅。没有大纲时先提供简要大纲，不让写作过程替代研究设计。

主版使用外部审阅；Codex 适配采用辅助 agent。各自的参考路径和可用工具需按当前宿主核对，主版另有可选风格提取和缺项机制。引用检索、样式文件获取、外部审阅及 PDF 编译是不同依赖，收录文件不代表全部已就绪。

**外围兼容说明：**主版示例把 `<!-- DATA_NEEDED -->` 写作 LaTeX 中的隐藏占位。HTML 注释不能直接当作 TeX 注释使用。若实际写入 `.tex`，应改用合法的 TeX 注释或显式待补标记，在自己的稿件中编译检查；不要改写本仓库原始快照。本模块教学稿为 Markdown，未验证 LaTeX 编译。

## 03 · ml-paper-writing：ML/AI 写作与引用纪律

main：[SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/ml-paper-writing/SKILL.md) · codex：[SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/ml-paper-writing/SKILL.md)

从项目、草稿或文献材料起草 ML/AI 文章，先选操作模式，再按主张台账将正文句子对应到 Claim Candidate 或 Evidence Record，保留允许与禁止的更强措辞。计划和文献动机不能作为自己的实验结果；无证据的陈述保留待补标记。

两份入口当前内容相同，配套材料仍属于各自快照。引用流程以其指定核验来源为准，不从记忆编 BibTeX；网络检索/API、相关 Python 包和目标模板需在实际使用时确认。仅修改已经提供的段落不必启用完整文献搜索或安装其推荐服务。文献核验复用 [文献模块](../literature-review/README.md)，提交前检查转入 [投稿模块](../submission-rebuttal/README.md)。

## 04 · nature-writing：中文材料到论证清楚的正文

main：[SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/nature-writing/SKILL.md) · codex：[SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/nature-writing/SKILL.md)

适合按章节重建标题、摘要、引言、方法、结果与讨论。先写清“在什么系统中，用何种方法观察到什么，由哪些证据支持，边界在哪里”，再决定段落顺序；材料不足时返回支架和缺项，不创造新颖性、机制或统计量。

两份入口当前相同。按需读取中文作者工作流、章节结构和段落参考；可选写作记忆不存在时仍可使用技能自身资料。Nature 风格仅是结构与语言参考，不保证适合所有学科或某个具体期刊，也不意味着达到发表要求。

## 05 · nature-polishing：保持含义的润色和翻译

main：[SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/nature-polishing/SKILL.md) · codex：[SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/nature-polishing/SKILL.md)

在作者提供论点和证据后，检查章节任务、段落逻辑、语法、清晰度和限定词。默认返回修改文本与简短修改说明，也可提供 `Original / Polished / Why changed`。两份入口当前相同。

结构调整与语言调整分别说明。将 “observed” 改成 “proved”、删去条件范围，或把百分点改成相对百分比，都可能改变科学含义，不能当作单纯润色。参考语料用于理解表达模式，不能复制他人独特措辞或借用其论点。

## 06 · paper-claim-audit：稿件到原始证据的忠实度

主版本：[SKILL.md](../idea-discovery/01_ARIS/upstream/skills/paper-claim-audit/SKILL.md) · Codex：[SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-claim-audit/SKILL.md)

检查数字、相对变化、最好/均值表述、配置匹配、图注和范围陈述。审阅只接收稿件和原始结果，不用作者总结替代数据，并要求新的审阅上下文。输出逐主张报告及机器可读状态，输入不足时保留 `BLOCKED` 等实际状态。

主版通过外部 Codex MCP 审阅。基础 Codex 版明确为 `review_independence: same-family`、`acceptance_status: provisional`；同家族新 agent 的 PASS 不等于跨模型接受，审阅不可用也不能由执行者补写 PASS。本模块的手工数字核对没有调用该技能，不能冒充这种审计报告。

它检查“论文是否如实报告结果”，不替代 [数据分析模块](../data-analysis/README.md) 对统计设计、估计对象和主张是否成立的判断，也不替代学术同行评议。

## 复用与状态

主版本/Codex 和 main/codex 按实际文件分别导航。12 个选定入口与 3 份根许可证构成 15 个来源引用，详见 [来源清单](SOURCE_MANIFEST.json)。关联参考仍由原快照保存，不构成新的独立来源项目。

全部上游工作流 `runtime_tested: false`。文档与教学稿核对见 [验证记录](VALIDATION.md)，不能把文件存在或语言流畅视为工作流已验证。

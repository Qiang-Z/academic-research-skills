# 文献检索与综述 · 技能中文索引

[模块首页](README.md) · [使用说明](USAGE.md) · [五篇论文示例](examples/rag-literature-walkthrough.md) · [来源清单](SOURCE_MANIFEST.json)

本模块复用仓库已有固定版本快照，整理 **5 个核心技能名称**；同一名称的宿主或分支版本不重复计数。链接均相对本模块目录，源码仍在 `../idea-discovery/` 下。下面区分上游设计能力与实测结果；最新 [运行报告](runtime-tests/2026-10-22/README.md) 已记录部分宿主流程和组件的成功、失败及缺陷，不表示全部入口已安装或通过。

## 先按任务选择

| 当前任务 | 建议入口 | 准备的材料 | 预期交付 |
|---|---|---|---|
| 初次了解方向，或阅读手头几篇论文 | **ARIS `research-lit`**，默认入门入口 | 具体问题、已有论文、年份范围、允许使用的来源 | 相关工作清单、论文摘要、主题归纳、待补读问题 |
| 围绕关键词、年份或会议扩充候选文献 | **ResearchStudio `paper-search`** | 检索词、起止年份、来源与数量限制 | 候选记录、来源与标识符、去重和筛选说明 |
| 对一批论文做专题综合，或准备系统综述方案 | **K-Dense `literature-review`** | 研究问题、纳排标准、检索记录、可获得的全文 | 检索与筛选记录、证据矩阵、主题综述与限制 |
| 将阅读结果积累到已有项目知识库 | **ClaudeScholar `obsidian-literature-workflow`** | 项目知识库、论文笔记及可定位的证据 | 文献概览、方法分类、主张图、写作交接材料 |
| 在笔记或综述中加入引用前核对来源 | **ClaudeScholar `citation-verification`** | 候选引用、拟支持的句子、标识符或原文 | 元数据核对、原文支持位置、待核验项 |

没有知识库时，从 `research-lit` 或 `literature-review` 开始，用本模块模板保存普通 Markdown/CSV 即可。知识库联动不是阅读论文的前置条件。

## 01 · ARIS：research-lit

| 版本 | 已保存入口 | 版本相关说明 |
|---|---|---|
| 主版本 | [research-lit/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/research-lit/SKILL.md) | [中文 README](../idea-discovery/01_ARIS/upstream/README_CN.md)；自定义论文库约定读取 `CLAUDE.md` |
| Codex 适配 | [skills-codex/research-lit/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/research-lit/SKILL.md) | [Codex 中文说明](../idea-discovery/01_ARIS/upstream/skills/skills-codex/README_CN.md)；自定义论文库约定读取 `AGENTS.md` |

**用途：**从已有 PDF、参考管理器或联网来源整理相关工作，为精读和研究问题细化建立起点。

**范围与依赖：**本地阅读需要宿主能够访问所指定文件并读取 PDF；网络检索需要实际可用的搜索或辅助工具。Zotero、Obsidian 联动依赖各自连接。Semantic Scholar、DeepXiv、Exa、Gemini、OpenAlex 属于另外选择的来源，可能需要脚本环境、CLI、SDK、服务凭据或其他配置。两版本的 `sources: all` 都不等于调用全部可选服务。

**阅读边界：**上游的本地初筛默认扫描每篇前 3 页，最多 20 篇；该结果只能证明初筛阅读范围，不能写成“已全文精读”。需要方法、数据或数值结论时，应继续读取相应章节并记录位置。

**分支差异：**Codex 入口有可选综述交叉核对的后端约定；对于用户明确要求但没有配置的 Zotero/Obsidian，它要求显式报告缺失。应按所选入口核对工具，不混用两个版本的安装记录或配置路径。本文的自然语言示例不自动启用审阅后端或修改全局配置。

## 02 · ResearchStudio-Idea：paper-search

入口：[paper_search/SKILL.md](../idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/paper_search/SKILL.md) · [子项目 README](../idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/README.md)

**用途：**按主题、年份和会议等条件检索 arXiv、DBLP、OpenAlex、OpenReview、Semantic Scholar、Crossref，整理候选论文及来源。其脚本设计包括跨来源去重、排序和 JSON 原始结果；相关性判断仍需要读取摘要。

**输入与输出：**显式给出研究问题、检索词、年份、来源、每源上限；保留标识符、原标题、来源、检索日期、失败来源、去重数以及筛选理由。检索命中数不等于纳入研究数。

**依赖与宿主：**这是带 Python 检索脚本的入口，网络 API 必须可达，OpenReview 额外依赖 `openreview-py`。上游示例使用 `CLAUDE_PROJECT_DIR` 定位脚本，本模块没有注册该变量或制作独立 Codex 移植版。后续确需运行时，要根据已保存目录定位脚本并检查依赖；不能把示例变量当作已经存在。

**本模块整理约定：**上游另有 `model_knowledge`（模型记忆）来源。它只能产生待核验线索，不能当作实际检索命中、已核验引用或系统综述证据。保留未筛选原始记录及排除理由，不把排序分数、引用次数或“未找到”直接当作质量、新颖性或研究空白结论。上游的默认联网、自动执行和报告写入约定不是本仓库收录行为的执行授权。

## 03 · K-Dense：literature-review

入口：[literature-review/SKILL.md](../idea-discovery/04_KDense/upstream/skills/literature-review/SKILL.md) · [完整流程参考](../idea-discovery/04_KDense/upstream/skills/literature-review/references/core_workflow.md) · [上游综述模板](../idea-discovery/04_KDense/upstream/skills/literature-review/assets/review_template.md)

**用途：**按问题界定、检索、筛选、提取、证据评价、综合和引用核对组织综述。适合把论文清单推进为主题比较，而不是逐篇摘要的堆叠。

**最低输入：**研究问题、综述类型、检索范围、纳排标准、可获得的论文材料。正式综合需要注明阅读范围及证据位置；只有摘要的记录保留为待精读材料。

**依赖分层：**阅读工作流和填写模板不等于运行脚本。其 Python 工具要求 Python 3.10+，其中 DOI 核对还需 `requests` 和网络；本地记录处理可用标准库。可选 `parallel-cli` 需额外安装与认证；PDF 导出需要 Pandoc、XeLaTeX；AI 示意图另需服务凭据。本轮已测试记录处理、引用检查及 PDF 缺依赖路径，具体成功范围见 [K-Dense 报告](runtime-tests/2026-10-22/kdense-report.md)。

**能力边界：**上游脚本主要处理标准化记录、检查 DOI 注册和导出文档，不会自动完成完整系统综述。其文档提到的 `citation-management`、领域数据库、绘图库等兄弟技能不因此视为本地已收录或已安装。该入口支持 Meta 分析规划，**不提供 Meta 分析统计引擎**。系统综述还需适合问题的检索方案、完整筛选记录、全文评价及相应方法学流程。

## 04 · ClaudeScholar：obsidian-literature-workflow

| 分支 | 已保存入口 | 配套说明 |
|---|---|---|
| main | [obsidian-literature-workflow/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/obsidian-literature-workflow/SKILL.md) | [main 中文 README](../idea-discovery/05_ClaudeScholar/upstream_main/README.zh-CN.md) |
| codex | [obsidian-literature-workflow/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/obsidian-literature-workflow/SKILL.md) | [codex 中文 README](../idea-discovery/05_ClaudeScholar/upstream_codex/README.zh-CN.md) |

**用途：**组织项目内的 `Sources/Papers/ → Knowledge/ → Writing/` 文献流程，按需形成文献图谱。两分支目前所列主要流程相同，链接与周边配置仍分开保留。

**输入与产出：**已有论文笔记、项目问题和证据记录；产出方法分类、文献概览、证据支撑的研究缺口及写作交接。没有项目知识库时，可先使用本模块模板，不必预先配置 Obsidian。

**证据要求：**笔记需区分作者主张、项目解释和实际证据。进入知识综合或写作的主张需带 Evidence Record ID、来源类型、强度及允许表述。摘要记录、网页占位或未获取全文条目可更新待读清单，不能直接升级为已证实的综合结论。

**可选关联材料：**已有 Zotero 与项目知识库时可参考 main 分支的 [zotero-obsidian-bridge](../idea-discovery/05_ClaudeScholar/upstream_main/skills/zotero-obsidian-bridge/SKILL.md)。它不计入本模块 5 个核心名称；实际联动仍需连接配置、正确的项目目录与可访问材料，不从 main 自动推定 codex 有相同入口。

## 05 · ClaudeScholar：citation-verification

| 分支 | 已保存入口 | 本次核对到的区别 |
|---|---|---|
| main | [citation-verification/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/citation-verification/SKILL.md) | 原则列有权威元数据来源，部分旧示例仍偏向 Google Scholar |
| codex | [citation-verification/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/citation-verification/SKILL.md) | 示例更明确优先 DOI、arXiv、出版方及学术元数据来源 |

**定位：**这是引用核验指南，快照同时保存参考脚本，不能等同于已部署的一键服务。本轮执行了宿主官方来源核对和脚本检查，发现参考实现与文档存在差异，见 [ClaudeScholar 报告](runtime-tests/2026-10-22/claudescholar-report.md)。联网核对仍依赖宿主可用的检索或数据连接；核查具体表述需要明确原文位置。

**输入与输出：**输入引用条目和拟支持的句子；逐项记录文献身份、作者、年份、版本、标识符、原文支持位置及核对状态。文献真实存在与“支持这句话”必须分别核查。

**本模块整理约定：**优先按所引用版本的官方论文页或出版方元数据核对；预印本和正式版有年份差异时分别记录，不以“相差一年”机械放行。上游中残留的固定 AI 引用错误率没有在本次建立证据来源，因此不在中文指南中作为统计事实引用。原始快照保持不变，这些处理属于外围导览约定。

## 接到 idea 模块

完成文献记录、证据矩阵和限制说明后，用 [idea 交接模板](templates/idea-handoff.md) 整理研究问题、最接近的工作、尚未解决的证据问题与下一步检索，再进入 [创新点探索索引](../idea-discovery/SKILL_INDEX.md)。文献中的“未覆盖”和模型提出的候选差异，仍须在具体范围内查新与验证。

# 学术技能补充检索与筛选记录

检索日期：2026-10-22。目标是找出能改善本仓库实际任务的组件与交接方法，尤其是新手从一个问题走到一份有证据的小报告的路径。

**结论：有值得补充的具体能力，但本轮没有证据证明某个新仓库整体优于现有五个项目。** 建议继续使用已保存的技能；优先吸收小批量检索、引用身份核对、数据来源契约和证据交接，再按实际需求评估新增组件。

## 检索范围与证据边界

通过公开网页搜索、中英文 GitHub 定向搜索发现候选，再读取项目自己的 README、具体技能正文、许可证和 GitHub API 返回的提交及文件树。检索词包括：

- `GitHub academic research skills scientific skills agent literature review`
- `GitHub research pipeline skills scientific discovery experiment paper`
- `site:github.com academic research skills pipeline literature review SKILL.md`
- `site:github.com science skills Scientific Research skills agent`
- `site:github.com academic pipeline research skills provenance experiment`
- `site:github.com 科研 skill 文献 检索 实验 复现 pipeline`

候选名称发现后另做名称定向搜索。下方六项经过具体技能文件阅读；Zsun79/LitReviewSkill 另作为暂缓项检查。其他搜索命中的排行榜、聚合列表及社交平台只用于发现线索，不作为能力或质量结论的依据。这是有限搜索，不能证明覆盖全网，也不是系统综述。

本轮完成的是**来源与接口静态审阅**：未安装、未执行这些新增候选的上游代码，未运行它们的测试集或付费服务。仓库自述的有效性、兼容平台数或测试覆盖不等于本仓库复测结论。GitHub API 曾出现一次 TLS 连接错误，重试后获得 Kalaris 元数据；一个许可文件读取失败，已采用同提交许可范围说明和具体技能许可核对，未把请求失败当作文件不存在。

## 与现有内容比较

现有 [来源清单](../../../modules/idea-discovery/SOURCE_MANIFEST.json) 保存 ARIS、Orchestra、ResearchStudio、K-Dense、ClaudeScholar，共五项目六快照。其中 K-Dense 只保存 brainstorming、hypothesis-generation、literature-review 和 critical-thinking 四个技能；Orchestra 只保存 ideation 子树。新增候选并不意味着需要再引入一套完整科研平台。

| 当前任务 | 已有可用入口 | 本轮发现的增量 | 建议 |
|---|---|---|---|
| 找到少量可读论文 | ARIS research-lit、ResearchStudio paper-search | GDM 的来源专用 CLI、明确限量和空结果处理 | 先完善来源状态记录；需要替换某个失败来源时再验证 CLI |
| 核对参考文献 | ClaudeScholar citation-verification、K-Dense 文献工具 | Kalaris 的标题/第一作者/年份交叉核对 | 增加“标识符真实但文献错配”的验收用例 |
| 从计划推进到实测 | ARIS experiment-plan/bridge/audit | ai4s 的数据契约与统一结果来源 | 保留真实运行证据，缺环境时停在计划 |
| 防止设计层面错误 | ARIS 计算实验计划 | yigityildiz0 的实验单位、重复层级、随机化与区组 | 作为领域扩展；不把生物实验设计生搬到所有计算任务 |
| 让新手只给自然语言 | 现有三张任务卡与模块路由 | xcl2005 的最小能力选择、缺证据回退 | 提取成一条轻量流程，隐藏不必要的技能选择 |
| 输出前检查引用 | 现有证据检查 | jkitchin 的按标识符分流 | 保留不确定性，修正“请求错误即无效”的规则冲突 |

## 六个重点候选

### 1. Google DeepMind Science Skills：适合补充来源专用检索

- 固定版本：[`99f3085bcb40514cdba7833205b3dedbf473b26d`](https://github.com/google-deepmind/science-skills/tree/99f3085bcb40514cdba7833205b3dedbf473b26d)，提交时间 2026-10-15；Apache-2.0（GitHub 许可元数据）。
- 入口：[arXiv](https://github.com/google-deepmind/science-skills/blob/99f3085bcb40514cdba7833205b3dedbf473b26d/skills/literature_search_arxiv/SKILL.md)、[OpenAlex](https://github.com/google-deepmind/science-skills/blob/99f3085bcb40514cdba7833205b3dedbf473b26d/skills/literature_search_openalex/SKILL.md)。输入查询或标识符，输出文献元数据；全文下载为后续步骤。
- 依赖：`uv`、Python 脚本和可达的数据库服务；不同来源的凭据、额度与论文许可须另核对。OpenAlex README 与技能正文对密钥要求的表述并不完全一致，不能承诺无密钥可用。
- 值得提取：每批少量结果、标识符解析、返回来源链接、空结果如实报告、下载后验证文件。
- 限制：它解决数据访问，不自动完成相关性判断、综述或研究有效性评价。对新手应由流程隐藏 CLI 选择。

### 2. Kalaris Labs Research Agent Skills：优先评估引用元数据核验

- 固定版本：[`f73da6a491e3cc3417cfe88e1130469e763b1b33`](https://github.com/KalarisLabs/research-agent-skills/tree/f73da6a491e3cc3417cfe88e1130469e763b1b33)，提交时间 2026-10-21。
- 入口：[citation-verification](https://github.com/KalarisLabs/research-agent-skills/blob/f73da6a491e3cc3417cfe88e1130469e763b1b33/skills/citation-verification/SKILL.md)。输入 BibTeX 或 DOI，输出逐条状态报告；文档声明 Python 3.9+ 标准库，联网访问 Crossref、OpenAlex、arXiv。
- 许可：GitHub 自动识别为 `NOASSERTION`，但已直接读取 [LICENSE](https://github.com/KalarisLabs/research-agent-skills/blob/f73da6a491e3cc3417cfe88e1130469e763b1b33/LICENSE)，正文为 MIT，另有第三方许可说明；不能只靠 API 标签判断。
- 值得提取：DOI 能解析还不够，标题、作者和年份必须匹配；引用身份与是否支持某一句话分开检查。
- 限制：技能正文要求的语义核验仍依赖读原文，脚本未在本轮运行。`not-found` 不应直接作为虚构定论；灰色文献、索引覆盖、版本差异和网络故障需分别处理。

### 3. xcl2005 Academic Paper Writing Skill：适合借鉴单入口与交接

- 固定版本：[`33ddc61ee5aaa1932210894ac62d4d7ac909c936`](https://github.com/xcl2005/academic-paper-writing-skill/tree/33ddc61ee5aaa1932210894ac62d4d7ac909c936)，提交时间 2026-09-02；[MIT](https://github.com/xcl2005/academic-paper-writing-skill/blob/33ddc61ee5aaa1932210894ac62d4d7ac909c936/LICENSE)。
- 入口：[根 SKILL.md](https://github.com/xcl2005/academic-paper-writing-skill/blob/33ddc61ee5aaa1932210894ac62d4d7ac909c936/SKILL.md)。输入自然语言任务、现有材料和边界，按需选最小能力集合；输出阶段材料及证据状态。
- 值得提取：主张对应证据 ID 与准确位置，缺输入保持未知，能力不可用时显式回退，不要求新手先安装所有外部技能。
- 依赖与限制：文档路由较轻；完整项目初始化、阶段门禁和导出有 Python、配置及所选工具依赖。完整门禁还要求记录人类审阅，不能由助手代签。其检查证明记录一致性，不证明科学结论正确；本轮未测试脚本。

### 4. ai4s Research Skills：适合借鉴实验数据与结果交接

- 固定版本：[`744ab2049a7b52ae726c43313468fd518b330980`](https://github.com/ai4s-research/ai4s-skills/tree/744ab2049a7b52ae726c43313468fd518b330980)，提交时间 2026-07-27；MIT（GitHub 许可元数据）。
- 入口：[experiment-suite](https://github.com/ai4s-research/ai4s-skills/blob/744ab2049a7b52ae726c43313468fd518b330980/skills/experiment-suite/SKILL.md)、[结果协议](https://github.com/ai4s-research/ai4s-skills/blob/744ab2049a7b52ae726c43313468fd518b330980/skills/experiment-suite/references/03-results-protocol.md)。输入问题、数据和预算，输出设计、代码、结果、图和报告。
- 值得提取：数据来源和划分单独记录，结果声明 measured/simulated/mixed、执行来源、种子及局限，供下游写作复用。
- 依赖与限制：流程靠宿主实施，实际执行取决于生成代码所用环境；“无独立运行时”不等于没有 Python 或训练依赖。其默认 simulated 和长文/大量引用配额不适合本库新手主线。应采用真实小实验或待执行状态，绝不填占位数字冒充结果。

### 5. yigityildiz0 Scientific Agent Skills：实验设计的领域扩展

- 固定版本：[`5996deb3a2c7bb260b3d7aae4ab3e087077afb11`](https://github.com/yigityildiz0/scientific-agent-skills/tree/5996deb3a2c7bb260b3d7aae4ab3e087077afb11)，提交时间 2026-10-14。
- 入口：[experimental-design](https://github.com/yigityildiz0/scientific-agent-skills/blob/5996deb3a2c7bb260b3d7aae4ab3e087077afb11/skills/common/experimental-design/SKILL.md)。输入问题、实验单位、因素及约束，形成设计与分配计划；脚本依赖 NumPy、pandas、pyDOE3。
- 值得提取：先决定独立重复单位，检查伪重复、批次混淆，再决定分析；固定随机种子并保存分配计划。
- 许可与来源：这是混合来源集合，[许可范围说明](https://github.com/yigityildiz0/scientific-agent-skills/blob/5996deb3a2c7bb260b3d7aae4ab3e087077afb11/docs/LICENSE-SCOPE.md)明确不能整体重标许可。本项 [LICENSE.txt](https://github.com/yigityildiz0/scientific-agent-skills/blob/5996deb3a2c7bb260b3d7aae4ab3e087077afb11/skills/common/experimental-design/LICENSE.txt)为 K-Dense Inc. MIT，属于已知上游的范围扩展，不能计作独立方法验证。
- 限制：湿实验/组学倾向明显；本轮未验证随机化脚本，也不据此升级本库对临床或硬件实验的支持状态。

### 6. jkitchin Skillz：可借鉴标识符分流，不原样采用判定规则

- 固定版本：[`776a4bc8dc151d82798cdf7e029b94be693791c7`](https://github.com/jkitchin/skillz/tree/776a4bc8dc151d82798cdf7e029b94be693791c7)，提交时间 2026-10-20；MIT（GitHub 许可元数据）。
- 入口：[citation-verifier](https://github.com/jkitchin/skillz/blob/776a4bc8dc151d82798cdf7e029b94be693791c7/skills/citation-verifier/SKILL.md)。输入 Markdown、BibTeX、Org 或文本，提取 DOI/arXiv/PMID/ISBN 等并分类核对；依赖宿主读取与联网工具。
- 值得提取：去重、按标识符选择权威来源、逐项交付状态与修复建议。
- 静态发现的问题：其 DOI 步骤把 Crossref `404 or error` 标作 INVALID，而后文又要求区分无法核验与确定无效。网络错误和单一索引缺失不能支持“虚构”结论。不得原样采用该规则，也不能将 DOI 身份核对称为主张支持验证。
- 新手适配：后台组件候选；目前建议继续用本库已有核验指南，并补充故障状态验收。

## 暂缓项与没有采用的默认行为

[Zsun79/LitReviewSkill](https://github.com/Zsun79/LitReviewSkill/tree/a53cd419352e4dd05958f67340fde3642d84abc3)（提交 2026-06-08）将检索、双向引文扩展、筛选日志和最终引用集合边界组织得较清楚。但本轮文件树未发现许可文件，GitHub 许可字段为空；README 的克隆示例还指向 `LitReviewAI`，与当前仓库名不一致。因此只作为流程设计参考，不复制代码、不推荐照抄安装命令。其全文层使用 CORE，检索层使用 OpenAlex，另有图表与 PDF 导出工具链；这些均未实跑。

所有候选都需要区分“文档描述”“静态核对”“本地脚本测试”“在线来源测试”和“全流程完成”。不采用自动安装全部技能、默认模拟成绩、引用数量硬配额、把请求失败当文献虚构、或替作者填写审批记录等做法。

## 可提取的轻量流程

建议组合为 **问题 → 检索与筛选 → 最小实验 → 分析 → 有证据的短报告**。新用户只提供问题和已有材料；助手按阶段选择已有技能。

每步只保留四件事：输入及来源、实际做了什么、输出及检查、未解决项。检索保存真实命中和失败来源；实验保存数据版本、划分和实际命令；分析从原始结果重算；写作将每个重要结论连到文献位置或运行产物。缺材料就停在相应阶段并说明下一步，不生成完整论文来填补证据空白。

此流程建议是本仓库对多项来源的原创综合，不是安装或调用上述六套系统的声明。新增来源尚未进入既有固定快照计数。验证应使用小规模案例，并额外检查无输入、来源失败、文献错配、缺结果和过强结论；即使这些检查通过，也只能证明这条限定流程的相应路径。

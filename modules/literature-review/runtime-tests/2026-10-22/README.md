# 文献检索与综述：实际运行验证

日期：2026-10-22（Asia/Shanghai）。**结论：部分路径可以实际运行，但不能将整个模块视为已验证的一键综述工具。** 本次既执行原始脚本，也让当前宿主按固定技能完成了有限检索、摘要综合和引用核对；成功、受阻和缺陷分别保留。

[模块首页](../../README.md) · [使用说明](../../USAGE.md) · [运行状态总表](../../../../docs/RUNTIME_STATUS.md)

## 五类技能的结果

| 技能与测试版本 | 已实际完成 | 存在的问题 / 未覆盖 | 证据 |
|---|---|---|---|
| ARIS `research-lit`，Codex 入口 | 宿主网页检索得到 9 张候选卡，去重后 9 条；筛选 3 篇官方指定版本页，形成摘要级比较与综合。原辅助程序可启动，解析组件可处理实际 Atom 数据 | Python arXiv 直连出现 TLS EOF；curl 诊断可成功。辅助程序去掉 `vN` 版本号。全文、全部来源及知识库联动未测 | [报告](aris-report.md) · [过程数据](aris-results.json) · [候选](search-records.json) · [实际综述](synthesis.md) |
| ResearchStudio `paper-search` | 补 requests 后，原聚合 CLI 的 OpenAlex 检索返回 2 条；worker 的 arXiv、OpenAlex、Crossref 各返回 2 条。原自检最终为 15/15 与 16/16 | 文档要求的 `--json` 不存在；DBLP 解析失败、Semantic Scholar 429、OpenReview 缺库；来源失败仍可能退出 0。完整语义筛选和报告链未测 | [报告](researchstudio-report.md) · [过程数据](researchstudio-results.json) |
| K-Dense `literature-review` | 本地规范化记录去重/年份过滤/排序及 Markdown/BibTeX 导出；补 requests 后两个 DOI 注册核验、DPR 的 Crossref 元数据查询成功 | 本地处理器不是联网搜索。首轮网络失败；arXiv DOI 的 Crossref 元数据 404。PDF 缺 Pandoc/XeLaTeX；完整综述与全文评价未测 | [报告](kdense-report.md) · [19 项记录及输入](kdense-results.json) |
| ClaudeScholar `citation-verification`，codex | 宿主官方来源核对两条正确引用并识别一条标题/ID 错配；补兼容依赖后原脚本的两条 API 查询成功 | 新版 arxiv SDK 与代码不兼容；独立格式检查 CLI 没有执行入口；主脚本格式检查报告与退出状态不能充分表达错误。定量主张支持未测 | [报告](claudescholar-report.md) · [官方来源核对](claudescholar-citation-results.json) · [组件记录](claudescholar-component-results.json) |
| ClaudeScholar `obsidian-literature-workflow`，codex | 标准库 canvas 组件在临时合成项目生成 2 个论文节点、1 条边 | 关系路径前缀和混合自定义分类可静默丢边/丢节点；codex 绑定提示与真实读取路径不一致。未接入真实 Obsidian/Zotero | [报告](claudescholar-report.md) · [组件记录](claudescholar-component-results.json) |

## 所需环境

本次宿主：Codex 会话，Windows 11，CPython 3.12.10。测试时使用仓库外临时目录；没有把包、配置、真实知识库或论文全文放进仓库，没有改上游文件或全局 Python 安装。

| 用途 | 本次实际准备或检测到的条件 | 后续使用方式 |
|---|---|---|
| 阅读技能并联网核对 | 宿主的搜索服务与官方页面读取成功；另一 Web 工具发生传输失败 | 先确认当前宿主实际可用能力，保留失败和降级来源 |
| ARIS arXiv helper；K-Dense 本地记录处理；canvas JSON | Python 标准库即可启动 | 使用明确路径，不假定上游 Bash 命令或环境变量在 Windows 已配置 |
| ResearchStudio 与 K-Dense DOI 组件 | 隔离依赖 requests 2.34.2；附属包版本见各报告 | 独立项目环境准备，不依赖这次临时目录；真实网络仍需单独测试 |
| ClaudeScholar 引用参考脚本 | 本次兼容组合为 bibtexparser 1.4.3、arxiv 2.1.3、requests 2.32.5；另测新版组合并保留失败 | 按 ClaudeScholar 报告准备该组合；不要把其他来源所用 requests 版本直接混装进此组合 |
| OpenReview | 缺少 `openreview-py` | 本次未验证；准备依赖后仍要测试网络与具体接口 |
| PDF 导出 | 未找到 Pandoc、XeLaTeX；实际导出失败 | 单独准备并测试，不能用其他导出器的成功代替原组件验证 |
| 其他集成 | 没有可用的 Zotero/Obsidian 专用连接；未启用 Parallel、AI 图像及外部审阅服务 | 仅在需要相应能力时另建有限测试，不计入本次通过范围 |

本次依赖准备遇到 TLS 错误；有限重试及复用已准备的隔离包后继续。没有关闭证书校验，没有向测试提供服务密钥。每份报告保留环境隔离方式、原命令、版本与输入要求；临时绝对路径已替换为通用占位符。

## 使用与问题处理顺序

1. **先用已验证的有限路径。** 选择 ARIS Codex 的 `sources: web`，以少量公开文献完成元数据和摘要级比较；引用用指定版本官方页核对。需要原始结构化候选时，参考 ResearchStudio 已成功的来源和 worker JSON 路线。
2. **把业务结果作为成功条件。** 检查来源的 `errors`、实际条数、摘要缺失、引用匹配和图谱节点/边数量。退出 0、文件存在或 DOI 能解析都不能替代这些检查。
3. **优先处理固定代码缺陷。** `--json` 文档/接口不一致、版本号丢失、格式检查入口/报告问题，以及 canvas 静默遗漏已有复现证据。后续若修复，应放在外围适配层并单独测试，或评估新上游版本；本次保持原快照原样。
4. **再处理外部环境缺口。** 对限流、响应解析失败、网络波动、OpenReview 缺库和 PDF 工具缺失分别复验。不要把失败来源当零命中，也不要因网页可访问就推定 Python API 连通。

## 状态如何登记

`runtime_status: partially-tested`；`host_workflow_tested: true`、`component_runtime_tested: true`、`upstream_code_executed: true`。这些字段表示有真实执行记录，具体是否通过取决于上表与日志。完整 `runtime_tested: false` 保持不变；main/codex 的未测分支、全部来源组合、全文系统综述及真实服务集成没有通过证据。

早期 [五篇论文教学示例](../../examples/rag-literature-walkthrough.md) 不改成运行成果。本次三篇网页综合、检索 worker 返回记录、K-Dense 合成后处理输入和临时 canvas fixture 各有自己的范围与计数，不互相拼接成一次完整系统综述。

# ClaudeScholar：引用核验与文献知识库实测

日期：2026-10-22（Asia/Shanghai）。测试入口为已保存的 **codex 分支**，提交 `b672e80951a2348dd6136316d096603bf2dc5b83`；main 分支仅做文档对比，未据此宣称 main 运行通过。

## 结论

当前宿主可以按 `citation-verification` 指南完成少量公开论文的规范元数据和摘要范围核验：两条正确引用通过，一条故意构造的标题—标识符错配被拒绝。它是模型配合 Web 工具实际执行的有限步骤，不是引用脚本自动验证或全文主张审查通过。

另行实测的原 `verify-citations.py` 在 **`arxiv 2.1.3` 兼容组合**下，也通过两条正确引用并拒绝同一错配负例；在 `arxiv 4.0.1` 组合下失败。该脚本只验证元数据匹配，不自动核对原文论点，且格式检查路径存在独立缺陷。

`obsidian-literature-workflow` 的原始 canvas 构建组件在临时合成项目可启动并生成 JSON，但发现关系目标和分类导致的静默遗漏。当前没有发现可用的 Zotero/Obsidian 专用连接工具，也未使用真实 vault。完整文献知识库工作流不具备本轮通过证据。

## 依赖与范围

| 路径 | 所需条件 | 实际状态 |
|---|---|---|
| 当前宿主按引用指南执行 | 能读取指南的宿主、可访问官方论文页的 Web 工具 | 本次通过，无需安装 Python 包 |
| 原 `verify-citations.py` 参考脚本 | Python、`bibtexparser`、`requests`；可选 `arxiv`、`semanticscholar` | CPython 3.12.10 原环境缺包；临时补齐后已测试格式路径与公开论文 API 路径，仍有返回码、报告与 SDK 兼容问题，见下文 |
| 原 `format-checker.py` 参考脚本 | Python、`bibtexparser` | 临时安装后函数级规则可运行，但文件没有 main 调用，文档中的直接命令不会执行检查 |
| 原 `build_literature_canvas.py` | Python 标准库、原位兄弟文件 `obsidian-project-kb-core/scripts/kb_common.py`、项目绑定、论文笔记目录 | 标准库组件实测；JSON 形式的临时绑定无需 PyYAML。此解释器未发现 PyYAML，因此未测试 YAML 格式绑定 |
| 真实项目文献工作流 | 真实项目绑定、完整来源笔记和证据门槛；需要界面或同步时还须对应宿主能力 | 未连接、未测试；不能由生成 canvas 文件推定 Obsidian 渲染或 Zotero 同步通过 |

在新建临时目标目录安装 `bibtexparser 1.4.3`、`requests 2.34.2`、`arxiv 4.0.1`、`semanticscholar 0.12.0` 及传递依赖；再在第二临时目标目录准备 `arxiv 2.1.3`、`requests 2.32.5`、`feedparser 6.0.14` 等兼容组合，并在该组测试中放在 Python 导入路径前面。两组完整已解析版本分别见组件日志的 `dependency_retry` 与 `compatibility_retry`，不混写为同一次安装结果。没有修改全局 site-packages。Python 运行加 `-B -X utf8`，输出仅在临时目录；仓库保留本报告及脱敏结果，不保留依赖包、临时知识库或主机配置。

## 官方来源与引用结果

| 用例 | 实际核对结果 | 可支持范围 |
|---|---|---|
| RAG，`2005.11401v4` | 标题和 Patrick Lewis 等 12 位作者匹配；首次提交 2020-05-22，v4 为 2021-04-12；页面注明 NeurIPS 2020 | 摘要描述了参数化生成器与非参数检索记忆结合，并比较序列级与 token 级检索条件。这里只记录摘要描述，不验证实验效果或方法细节。[官方版本页](https://arxiv.org/abs/2005.11401v4) |
| Self-RAG，`2310.11511v1` | 标题和 Akari Asai 等 5 位作者匹配；该版本日期 2023-10-17；该版本页未声明正式会议，不补填会议 | 摘要描述按需检索及 reflection tokens。没有根据摘要声称任意任务均有效。[官方版本页](https://arxiv.org/abs/2310.11511v1) |
| 故意负例：Self-RAG 标题 + `2005.11401v4` | **拒绝**：标识符实际指向 RAG，标题、第一作者和版本年份与输入不符 | 不生成已验证书目条目；待使用正确标识符重新核验 |

两个版本页本次确实通过 Web 工具打开；读取范围为元数据、版本历史与摘要。未下载 PDF、核对全文页码、取得可解析 BibTeX 或对外写入 bibliography。因此“官方文献存在”和“全文支持某一结论”仍分别记录。网页访问成功不证明当前 Python 解释器能访问对应 API。

## 初轮六次进程检查

精确命令、退出码、脱敏输出、源程序摘要和 fixture 参数见 [组件日志](claudescholar-component-results.json)。

| 检查 | 结果 | 含义 |
|---|---|---|
| `verify-citations.py --help` | 退出 1：缺 `bibtexparser` | 原参考脚本当前不可直接启动 |
| `build_literature_canvas.py --help` | 退出 0 | 命令入口可加载，不能单独视为功能通过 |
| 无项目绑定 | 退出 1，报告未注册项目 | 预期阻塞，未写图谱 |
| 两篇合成笔记，均为 `other`，关系目标 `Papers/b` | 退出 0，2 个文件节点、1 条边，端点有效 | 基本 JSON 生成路径可运行 |
| 同样两篇笔记，关系目标改为 `Sources/Papers/b` | 退出 0，2 个文件节点、**0 条边** | 规范目录前缀与内部节点键不一致，关系静默丢失 |
| 一篇 `other`、一篇自定义 `rag` 分类 | 退出 0，仅 **1 个文件节点**；日志仍报告读取 2 篇 | 混合分类会漏掉不在固定枚举中的论文，退出码不能代表图谱完整 |

合成笔记正文明确声明仅为解析测试，不含科研主张；没有借摘要材料生成 `Knowledge/` 或 `Writing/` 科研结论。上述只检查 JSON 数据结构与计数，未在 Obsidian 界面查看布局。

## 补依赖后的引用组件测试

| 检查 | 实际结果 |
|---|---|
| 直接运行 `format-checker.py valid.bib --strict` 与错误 fixture | 两次均退出 0、无输出；文件只有函数定义，没有 main 入口，不能视为正确或错误引用都通过 |
| 导入同一原模块，调用加载、结构、字段和重复键检查函数 | 正例无错误；负例识别 6 个问题，包含缺作者/标题/期刊、坏年份、坏 DOI 与重复键。属于函数级调用，未伪称原 CLI 已修复 |
| `verify-citations.py ... --format-only --verbose --output ...` 正负例 | 均退出 0；负例的格式错误在 verbose 输出出现，但 Markdown 报告不含这些错误。`format_checked` 没纳入失败计数/报告分组，不能依退出码放行 |
| 两条已知真实论文的 `--api-only --verbose`，各设 35 秒外层限制 | 在 `arxiv 4.0.1` 中先报 `Search` 无 `results` 属性，然后进入 Semantic Scholar fallback，两次均超时终止；未得到有效核验结论 |
| 切换 `arxiv 2.1.3` + `requests 2.32.5`，其余依赖从第一临时目录读取 | 两条正确引用各退出 0、arxiv 来源匹配分数 1.00；错配负例退出 1、分数 0.13。三次均在各自 35 秒限时内完成；保留弃用警告 |
| 同一兼容组合，隔离凭据环境再跑上述三例 | 只继承 Windows 必需进程变量，用户目录/配置路径指向新空目录，NETRC 指向不存在的临时文件，不传 API key 环境变量；正例仍各退出 0，错配仍退出 1 |

API 用例的 BibTeX 由本次官方元数据构造，是明确的测试输入，不是从规范来源导出的 BibTeX。原脚本还会把全部 API 失败概括为“论文不存在”；连接错误和工具失败不能支持该结论。本次超时记录为无法判定，而不是文献不存在。

日志共 20 项记录：18 次进程检查、2 次函数级检查，不含安装步骤和前面的宿主网页核验。早期进程继承普通进程环境，未对网络库可能的自动凭据查找做追踪；最终三次使用明确隔离环境，并未读取私人凭据。兼容版本的成功仅覆盖这三个输入和此次环境；`Search.results()` 已有弃用警告，不能推定新 SDK 或未来网络环境长期兼容。

## 复跑引用组件

选择已经准备好的独立项目 Python 环境，按上述兼容组合安装依赖；不要直接复用这次临时目录，也不要把未固定的最新 arxiv 包视为兼容。下列 `<项目Python>`、`<测试目录>` 需替换为自己的路径，从仓库根目录调用：

```text
<项目Python> -m pip install bibtexparser==1.4.3 arxiv==2.1.3 requests==2.32.5
<项目Python> -B -X utf8 modules/idea-discovery/05_ClaudeScholar/upstream_codex/skills/citation-verification/scripts/verify-citations.py <测试目录>/rag.bib --api-only --verbose --output <测试目录>/rag-report.md
```

本次还安装了 `semanticscholar 0.12.0` 以观察 fallback；成功的最终三例实际来自 arxiv，不证明 Semantic Scholar 路线可用。依赖解析和完整版本以组件日志为准。联网进程应加外围总时限，本次为每次 35 秒；失败时检查具体来源错误，不采信脚本将所有 API 失败归为“论文不存在”的概括。

正例测试输入可由 [已核对元数据](claudescholar-citation-results.json) 构造，保留 title、author、year、eprint 及 archivePrefix；它是测试 fixture，不是官方导出的 BibTeX。负例把 Self-RAG 的 eprint 故意改为 RAG ID，运行后应拒绝。格式检查的两份完整输入在组件日志 `dependency_retry.fixtures` 中；当前独立格式 CLI 无实际检查入口，不能把它作为质量门槛。

## 发现的问题与使用建议

1. **引用说明存在版本内冲突。** codex `SKILL.md` 优先 DOI/arXiv 等规范源，但 `scripts/README.md` 仍把 Google Scholar 写为主要核验路径，同时明确脚本只是参考实现。此次按 codex 主入口使用官方版本页，不将参考脚本依赖视为阅读指南的必需条件。
2. **固定年份容差不可机械使用。** 技能允许约一年的差异，本次把首次提交、所引版本日期及会议年份分别记录，没有以容差放行错配。
3. **未建立来源的固定“40%”说法。** codex 指南仍在 Best Practices 留有该表述；此次不把它作为经验证事实。
4. **codex 绑定路径提示不一致。** `kb_common.py` 实际读取 `.claude/project-memory/registry.yaml`，无绑定错误却提示 `.codex/project-memory/registry.yaml`。本次仅在临时目录按代码真实路径准备 JSON fixture，未修改用户主机配置。不能照错误提示配置后就声称已绑定。
5. **图谱不是完整性验证器。** 使用该固定组件前应核对预期论文数、实际文件节点数及关系数。需要处理正式项目的 `Sources/Papers/` 链接或自定义分类时，应先做外围修复和回归验证；当前原组件不宜直接用于宣称完整的文献图谱。
6. **原引用命令暂不适合作为自动放行门槛。** `format-checker.py` 缺命令入口，`verify-citations.py --format-only` 不能通过退出码反映格式失败。其“Content Validation”实际为元数据匹配评分，没有执行原文支持性核对；即便输出 verified，也不能证明引用支持具体论点。
7. **必须记录 SDK 版本及请求错误。** 未固定依赖时安装得到的 `arxiv 4.0.1` 已移除原脚本使用的 `Search.results()`。这是实测兼容失败；Semantic Scholar 的默认重试还可能让命令长时间不返回。需使用外围总时限并把超时保留为未判定。

上游快照保持不变；本报告未修复这些源代码问题。主版本 `obsidian-literature-workflow/SKILL.md` 与 codex 字节相同，但不因此推定其周边脚本或环境已经测试。完整技能运行状态保持未验证，有限宿主步骤与单组件结果应单独登记。

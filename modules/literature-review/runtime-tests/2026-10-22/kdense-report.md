# K-Dense 文献综述组件实测

测试日期：2026-10-22；Windows / CPython 3.12.10。来源为已保存的 K-Dense 固定提交 `92ace75ac21efe19a620434e0ca4e356081fe807`；上游原文件没有修改。逐项退出码、输入和脱敏输出见 [kdense-results.json](kdense-results.json)。

**结论：本地文献记录处理可以运行；补齐隔离依赖后，DOI 注册及单条 Crossref 元数据查询可以运行，但有网络波动。PDF 导出因缺少 Pandoc 和 XeLaTeX 未成功。完整文献综述工作流未执行。**

## 实际依赖

| 能力 | 上游要求 | 本次环境与结果 |
|---|---|---|
| `search_databases.py` 记录处理 | Python 3.10+ 标准库；输入为规范化 JSON 数组 | CPython 3.12.10 直接运行成功；脚本不访问文献数据库 |
| `verify_citations.py` DOI 检查 | Python、`requests`、可访问 DOI Handle 与 Crossref 的网络 | 初始缺 requests，连 `--help` 也报 `ModuleNotFoundError`；临时隔离安装 requests 2.34.2 后运行 |
| `generate_pdf.py` PDF 导出 | Pandoc、XeLaTeX；按需另备本地参考文献、CSL、模板和 TeX 包 | 两个命令均未找到；实际 `--check-deps` 和一次导出均失败，没有生成 PDF |
| `parallel-cli` 辅助发现 | 可选 CLI 及 Parallel 认证 | 当前命令路径未找到；未配置或执行 |
| AI 示意图 | 可选 OpenRouter 凭据、联网服务、图像与审阅接口 | 未探查凭据、未运行；普通文字综述不依赖此功能 |
| 全文提取、证据综合、系统综述 | 实际检索来源、纳排标准、全文、评价流程、人工判断 | 本次仅测试组件，不据此宣称已完成这些环节 |

隔离安装实际使用：

```powershell
py -3.12 -m pip install --disable-pip-version-check --no-input --only-binary=:all: --target <临时目录>/deps requests==2.34.2
```

运行子进程的 `PYTHONPATH` 指向该临时依赖目录，启用 UTF-8 并禁止生成字节码。没有更改全局安装或主机配置。实际依赖版本：requests 2.34.2、certifi 2026.10.19、charset-normalizer 3.5.2、idna 3.20、urllib3 2.8.0。安装时发生 SSL EOF 重试，随后通过当前 pip 配置的缓存/下载 wheel 成功安装；没有读取私人 pip 配置，也不推定本次下载一定直接来自某个指定镜像。

没有为了 PDF 测试安装大型 TeX 发行版。Pandoc 与 XeLaTeX 均可用后，仍须真实导出并检查 TeX 包、字体、引用和版面；仅 `--version` 成功不足以证明 PDF 工作流通过。

## 运行结果

共记录 **19 项检查/尝试**，不是“19 个完整工作流全部通过”。离线预期拒绝、依赖阻塞和真实网络失败均保留在日志中。

| 项目 | 真实结果 | 解释 |
|---|---|---|
| 8 条合成记录：去重、2019–2024 年过滤、引用数排序 | 成功；去重后 6 条，过滤后 4 条，排序与独立预期一致 | DOI 规范化去重；同标题但不同 DOI 保留；无 DOI 的标题只与其他无 DOI 记录比较 |
| Markdown 与 BibTeX 输出 | 成功；各输出 4 条记录，重复作者年份键变为 `Doe2020` / `Doe2020_2` | 仅检查此小样本的文本内容和键，不等于验证任意元数据都能形成标准参考文献 |
| 原始 API 外壳、颠倒年份、未知参数、损坏 JSON | 均以非零退出码拒绝 | `search_databases.py` 接收规范化数组，不能把 API 原始响应直接当输入 |
| DOI 提取去重与括号处理；非法 DOI 语法 | 进程内检查符合预期；非法语法不联网 | 合成 DOI 只用于处理逻辑测试，不作为真实引用 |
| 没有 DOI 的文档 | 退出码 0，明确警告没有 DOI，报告 `total_dois: 0` | 退出码 0 本身不表示任何引用已被核验 |
| 报告输出覆盖输入 | 被拒绝，退出码 2 | 本例输入保持不变 |
| ACL DPR DOI 首轮 | 注册成功；Crossref 连接重置，元数据不可用；退出码 0 | DOI 存在与元数据完整性是两件事 |
| ACL DPR DOI 有限复验 | 注册和 Crossref 元数据均成功；返回标题与 2020 年份 | 核对的是 `10.18653/v1/2020.emnlp-main.550`；不是全文或具体主张支持核查 |
| arXiv RAG DOI 首轮 | 连接重置；`inconclusive`，退出码 1 | 不能据此判断论文或 DOI 不存在 |
| arXiv RAG DOI 有限复验 | 注册成功；Crossref HTTP 404，`metadata_unavailable`；退出码 0 | 核对的是 `10.48550/arXiv.2005.11401`；Crossref 不覆盖该条元数据时应另查官方记录 |
| PDF 依赖检查与实际导出 | 两次均退出 1，没有 PDF 文件 | 原因是缺 Pandoc 与 XeLaTeX；不是已经通过导出测试 |

联网范围仅为上述两个公开 DOI，各做一次初测和一次有限复验；保留上游自己的有界重试行为，没有进行大规模检索或上传研究资料。DPR 元数据返回题名为 “Dense Passage Retrieval for Open-Domain Question Answering”。报告只保存必要字段，不保存论文全文。文献身份/年份仍需按实际引用版本人工确认。

## 可复跑方式

从仓库根目录确定脚本位置；在自己的临时测试目录准备输入和输出。`kdense-results.json` 的 `fixtures` 保存本次 8 条合成记录、两个公开 DOI 文本、空引用文本及错误输入，`checks` 保存原始参数。将 `fixtures.normalized_records` 另存为 UTF-8 无 BOM 的 `records.json`，文本字段分别保存为 `review.md`、`rag-doi.md`、`doi-none.md`。

下列命令中的 `python` 指向已准备好 requests 的项目环境，路径占位符需替换；不要在上游保存目录中写运行产物。

```text
python -B -X utf8 <脚本目录>/search_databases.py <测试目录>/records.json --deduplicate --year-start 2019 --year-end 2024 --rank citations --format json --summary --output <测试目录>/normalized.json
python -B -X utf8 <脚本目录>/search_databases.py <测试目录>/normalized.json --format markdown --output <测试目录>/records.md
python -B -X utf8 <脚本目录>/search_databases.py <测试目录>/normalized.json --format bibtex --output <测试目录>/records.bib
python -B -X utf8 <脚本目录>/verify_citations.py <测试目录>/review.md -o <测试目录>/dpr-report.json
python -B -X utf8 <脚本目录>/verify_citations.py <测试目录>/rag-doi.md -o <测试目录>/rag-report.json
python -B -X utf8 <脚本目录>/generate_pdf.py --check-deps
```

脚本目录相对仓库根目录为 `modules/idea-discovery/04_KDense/upstream/skills/literature-review/scripts/`。测试脚本及其原始 SHA-256 在结果 JSON 中逐一记录；该目录仍属于完整固定快照。

## 使用时需处理的问题

1. **不要按文件名推断能力。** `search_databases.py` 是本地后处理器，实际查询由其他来源工具承担；本次合成记录不是实际检索命中。
2. **不要只看退出码。** 引用核验在“零 DOI”和“注册成功但 Crossref 元数据缺失”时都可能返回 0。应检查 `total_dois`、`failed`、`inconclusive`、`metadata_unavailable` 和每条元数据，另核对引用身份及原文支持。
3. **年份未知的记录会保留。** 本次 `year: unknown` 留在 2019–2024 过滤结果中。它应进入人工待核对队列，不能直接算作满足纳入年份。
4. **去重不等于研究合并。** DOI 重复保留第一条，其他来源信息不会自动合并；应保留原始记录。不同论文是否来自同一研究仍要独立判断。
5. **网络失败需保留。** 本次连接重置后有限复验成功，证明存在环境/网络波动；不可将 `inconclusive` 批量删除或写成“假文献”。
6. **PDF 仍需补环境。** 现有失败已记录。没有用其他导出工具替换后冒充上游 `generate_pdf.py` 成功。

这轮测试没有改写原脚本，也没有自动安装整套技能。完整七阶段综述、系统综述方法学、全文阅读、偏倚评价、证据综合、PDF 版面、跨平台效果与 AI 服务均不在通过范围内。

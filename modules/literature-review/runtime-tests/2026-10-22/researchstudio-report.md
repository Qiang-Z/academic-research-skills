# ResearchStudio paper-search 实际运行记录

日期：2026-10-22。固定来源提交：`063f10088af49909e1a4a7ea8d29efe19633f34e`。入口见 [原技能说明](../../../idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/skills/paper_search/SKILL.md)，逐项命令、退出码、脱敏输出和源码摘要见 [测试证据](researchstudio-results.json)。

**结论：部分检索组件可运行，但不能把原技能说明原样照抄为已跑通的完整流程。** 补齐 requests 后，原聚合命令通过 OpenAlex 返回两条真实结果；原 worker 通过 arXiv、OpenAlex、Crossref 各获得两条记录。另外三个来源分别受响应解析、限流或缺依赖影响。原文档要求的 `--json` 参数在这份固定脚本中不存在，已实际复现失败。

## 环境与依赖

| 项目 | 实际状态 |
|---|---|
| Python | Windows / CPython 3.12.10；已有解释器，无新增全局安装 |
| 必需网络库 | 初始缺少 requests，连原 CLI 的 `--help` 都以 `ModuleNotFoundError` 失败 |
| 实测依赖版本 | requests 2.34.2、urllib3 2.8.0、certifi 2026.10.19、charset-normalizer 3.5.2、idna 3.20 |
| 依赖准备 | 本子任务两次从官方 PyPI 临时安装均遇 TLS EOF；随后只读复用同轮 K-Dense 测试已准备的隔离依赖目录，实际导入及联网成功；没有关闭证书校验 |
| OpenReview | 未安装 `openreview-py`；该来源停在依赖错误，未验证 OpenReview 服务或登录 |
| API 凭据 | 本次未提供 API key、账号或密码；三个成功来源在这次匿名小范围请求中返回结果，不据此推定长期无认证可用 |
| HTTP 限额 | 连接超时 8 秒、读空闲超时 15 秒、最多 1 次尝试；每来源最多返回 2 条，非全库抓取 |

原 `_env.py` 会向脚本祖先目录寻找 `.env`。本次在仓库外建立字节一致的脚本副本，并放置已知空 `.env`，防止向上读取用户配置；子进程只继承基本系统变量，`NETRC` 指向受控空文件。13 份实际执行或导入的上游 Python 文件与原文件摘要一致。原始快照未修改，依赖、原始 JSON 和临时配置没有加入仓库。

## 实际结果

统一联网输入：`retrieval augmented generation`，年份范围 2020–2026，每来源 2 条。年份筛选不是精确到测试日的日期筛选。本次只检查连接、结构和输出，不声称检索覆盖完整或候选已经纳入综述。

| 测试 | 结果 | 解释 |
|---|---|---|
| 原后处理自检 | 15/15 通过 | 去重、标识符归一、词法排序、综述标记和显式阈值过滤；不验证真实语义相关性 |
| 原运行自检，默认环境 | 16/16 通过 | 本地/模拟的超时、重试、worker 隔离、错误保留和 schema；不是六个远端服务全部连通 |
| 原聚合 CLI，OpenAlex | 退出 0，2 条结果，stderr 为空 | 成功执行检索、去重和排序；显示 0 条跨来源重复，因为此命令仅选择一个来源 |
| 原 worker，arXiv | 2 条，errors 为空 | API 请求与结果解析成功，返回两篇 2025 年候选 |
| 原 worker，OpenAlex | 2 条，errors 为空 | 返回 2020 年 RAG 论文和 2023 年 RAG Survey；摘要字段均非空 |
| 原 worker，Crossref | 2 条，errors 为空 | 返回两个 2026 年章节 DOI；摘要字段为空，不能直接做摘要语义筛选 |
| 原 worker，DBLP | 0 条，有 JSONDecodeError | 响应未能解析为 JSON；不能解释为“没有相关论文” |
| 原 worker，Semantic Scholar | 0 条，有 HTTP 429 | 本次被限流；未盲目重试、未验证带 key 路径 |
| 原 worker，OpenReview | 0 条，有 RuntimeError | `openreview not installed. pip install openreview-py`；属于本地依赖缺口 |
| 原 CLI 的文档 `--json` 示例 | 退出 2 | `unrecognized arguments: --json ...`；没有生成所要求 JSON |
| 原聚合 CLI，仅选择缺库的 OpenReview | 退出 0，但 stderr 报错且 0 条结果 | 进程成功结束不能作为检索成功判据 |

共保存 14 次测试进程记录，另保留两次依赖安装失败记录。运行自检最初沿用了联网测试的短超时设置，因此 15/16 通过：OpenReview 模拟测试断言的是默认 `(15, 300)`，而测试环境传入了 `(8, 15)`。清除这些覆盖后，原文件 16/16 通过；两次结果均保留，未把初轮失败隐藏或误报为实际登录故障。Windows 的本地超时模拟另打印 `ConnectionAbortedError: [WinError 10053]`，不影响对应断言通过。

成功返回的 6 条原始候选未进行完整筛选：arXiv 命中含图像生成和认知增强方向；Crossref 返回的是章节记录且没有摘要。记录类型、相关性和阅读范围仍需逐项审查，不能将 6 条命中数直接写为纳入的 6 项研究。仓库证据只保留元数据、摘要长度/摘要哈希与日志，完整摘要及原始响应留在临时测试目录。

## 可复用的运行方式

先准备独立项目环境中的 Python 与 requests，并阅读上游脚本；下例在与原脚本字节一致的受控工作副本中运行，`scripts/` 指向该副本。真实项目如需凭据应由使用者配置，不能为测试自动读取未知 `.env`。

```powershell
# 已激活准备好 requests 的项目环境；本次使用这些有限超时
$env:PAPER_SEARCH_CONNECT_TIMEOUT_SECONDS = '8'
$env:PAPER_SEARCH_TIMEOUT_SECONDS = '15'
$env:PAPER_SEARCH_MAX_ATTEMPTS = '1'
python -B scripts/search_papers.py --query "retrieval augmented generation" --start-year 2020 --end-year 2026 --max-papers 2 --sources open_alex

# 固定版本没有 --json；原 worker 的 --out 可以保存单来源 JSON
# 用参数列表传递 JSON，避免不同 PowerShell 版本的内层引号处理差异
@'
import json, subprocess, sys
subprocess.run([
    sys.executable, "-B", "scripts/source_worker.py",
    "--source", "open_alex", "--queries-json",
    json.dumps(["retrieval augmented generation"]),
    "--start-year", "2020", "--end-year", "2026",
    "--max-results", "2", "--out", "openalex-results.json",
], check=True)
'@ | python -
```

这是在现存组件上绕开文档/CLI 不一致的方式，没有修补或重新打包上游脚本。多来源时需分别保留每个 worker 的 JSON 和错误，再调用已审查的原 `postprocess` 函数去重/排序；本轮没有据此实现新的完整自动流程。

运行离线自检时不要继承上述短超时覆盖，原测试中的默认值断言依赖默认环境：

```powershell
Remove-Item Env:PAPER_SEARCH_CONNECT_TIMEOUT_SECONDS -ErrorAction SilentlyContinue
Remove-Item Env:PAPER_SEARCH_TIMEOUT_SECONDS -ErrorAction SilentlyContinue
Remove-Item Env:PAPER_SEARCH_MAX_ATTEMPTS -ErrorAction SilentlyContinue
python -B scripts/selftest_postprocess.py
python -B scripts/selftest_runtime.py
```

结束后同时检查 stderr、worker JSON 的 `errors`、实际条数和摘要缺失情况。`source_worker.py` 在来源失败时仍会正常写出错误信封并退出 0，聚合器也可能以 0 结束；自动化不能只检查退出码。

## 当前问题与待补范围

1. **固定文档与 CLI 不一致。** 若需要原技能承诺的完整未筛选 JSON，当前可用 worker JSON 路线；后续可在外围增加明确版本的适配器，或单独评估新版上游，不能直接改动固定快照。
2. **失败与零命中需要分开。** 保留逐来源错误；429、JSON 解析错误和缺库不能推断研究空白。
3. **依赖/网络不能假定已有。** 记录 Python、requests、OpenReview 库及证书/网络结果。这里记录的是本机本次结果，未检验别的平台或长期稳定性。
4. **完整技能交付未验证。** 没有完成原技能要求的所有候选摘要语义筛选、完整主题报告、`allinone.md` 交付及模型记忆补充。OpenReview 服务、凭据路径、全文获取与系统综述流程也未验证。因此此处只登记上游组件实测及部分来源成功，不能把整个 `paper-search` 或文献模块标为全部通过。

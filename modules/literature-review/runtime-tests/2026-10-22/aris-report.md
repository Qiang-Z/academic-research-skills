# ARIS research-lit：限定宿主流程与原始组件测试

日期：2026-10-22，Asia/Shanghai。宿主为本次 Codex 会话；Python 3.12.10 / Windows 11。使用固定快照的 [Codex 入口](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/research-lit/SKILL.md)；未注册斜杠命令，未安装全部 ARIS。

## 实际任务与结果

测试问题：少量基础 RAG 工作如何描述外部知识与证据利用？选择 `sources: web`、2020—2023 年基础工作、最多三篇摘要级材料；不启用 PDF 下载、知识库或外部审阅。实际保留了 [候选及筛选记录](search-records.json) 和 [综述输出](synthesis.md)，由当前宿主读取技能后执行，不是自动生成的脚本综述。

| 步骤 | 观察到的结果 | 判断 |
|---|---|---|
| 原始 `arxiv_fetch.py --help` | 退出 0，命令可加载；只需标准库 | 启动通过 |
| 原始脚本关键词检索，最多 3 条 | 退出 1，`SSL: UNEXPECTED_EOF_WHILE_READING`；原重试结束后无结果 | 此次直连失败，不是零命中 |
| 宿主 `web__run` | 传输失败 | 此工具本次不可用 |
| 宿主搜索服务替代入口 | 两个精确标题检索词合并返回 9 张结果卡；按 arXiv ID 去重仍为 9；选 3 篇、排除本次测试外 6 篇 | 公开网页检索可用；按技能允许的 WebSearch 降级继续 |
| 打开三篇官方指定版本页 | 核对标题、作者、版本日期与摘要；完成结构表和三段综合 | 有限宿主流程完成，阅读范围为摘要与页面元数据 |
| 同一 API 地址的 curl 诊断 | 两次请求退出 0；后一次响应为有效 Atom，原始解析组件提取 3 条记录 | API 并非全面不可达；成功来自替代客户端，不覆盖原脚本失败 |
| 版本参数组件检查 | `id:2005.11401v4`、`2005.11401v4`、`id:2310.11511v1` 均被转换为不含版本号的 `id_list` | 固定版本被去掉，不能以此证明读到请求的版本 |

脱敏过程数据、准确查询及 SHA-256 见 [aris-results.json](aris-results.json)。curl 取得的另外三条记录只用于传输/解析诊断，不混入本次三篇网页综述的筛选数量。没有把缓存网页访问日期当作论文发表日期或完整实时索引证明。

## 所需依赖与复跑

- 宿主流程需要可用的网页搜索/打开能力及文档写入能力；这些工具属于宿主，不是安装一个 Python 包即可获得。
- 原始 arXiv 辅助程序只需 Python 标准库与 HTTPS API；其 curl 回退只针对 HTTP 406，本次 TLS EOF 不会触发该路径。
- Windows 需把上游 Bash 的路径定位改为显式路径；以下从总仓库根目录运行。不修改全局 `ARIS_REPO` 或宿主配置。

```powershell
py -3.12 -B -X utf8 modules/idea-discovery/01_ARIS/upstream/tools/arxiv_fetch.py --help
py -3.12 -B -X utf8 modules/idea-discovery/01_ARIS/upstream/tools/arxiv_fetch.py search 'ti:"Retrieval-Augmented Generation" AND submittedDate:[202001010000 TO 202312312359]' --max 3
```

本次子进程移除了可选 `ARIS_VERIFY_EMAIL`，未发送个人联系信息。临时日志在发布时去掉本机路径。没有关闭 TLS 校验。

若直连失败，保留错误，再让宿主按同一研究范围查找官方页面；保存实际使用的工具、检索词和版本链接。不要将网页降级或 curl 诊断写成原脚本检索成功。指定版本应直接核对带 `vN` 的官方页；本轮没有修补上游的去版本行为。

## 未覆盖

未测试 main 入口、全部来源组合、全文/PDF 读取、下载、Zotero/Obsidian、DeepXiv/Exa/Gemini、知识库更新或跨模型审阅。没有将原技能在这一有限输入上的宿主执行等同于所有入口和集成都已通过。`host_workflow_tested: true` 仅表示本页限定路径确已执行；模块完整 `runtime_tested` 保持 false。

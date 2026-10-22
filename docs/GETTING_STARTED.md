# 从这里开始使用学术技能库

[总首页](../README.md) · [模块总索引](../MODULE_INDEX.md) · [研究流程](RESEARCH_WORKFLOW.md) · [运行状态](RUNTIME_STATUS.md)

先根据手头材料选择模块，再阅读该模块中文索引，只加载当前任务需要的技能。仓库保存的是固定版本技能、中文指南和教学材料；文件已经收录不等于自动安装或整套流程已经运行通过。

## 按手头材料选择入口

| 你已经有什么 | 当前想完成什么 | 建议入口 |
|---|---|---|
| 研究方向、关键词或几篇论文 | 确定检索范围、筛选与证据综合 | [文献检索与综述](../modules/literature-review/README.md) |
| 文献证据、观察或未解决的问题 | 形成候选想法、查新与可检验问题 | [创新点探索](../modules/idea-discovery/README.md) |
| 明确问题、候选方法和资源范围 | 固定协议、基线、消融和复现记录 | [实验设计与复现](../modules/experiment-design/README.md) |
| 原始结果、预测、日志与评价协议 | 核对数据、比较结果、判断推断范围 | [数据分析与统计](../modules/data-analysis/README.md) |
| 方法、分析包与有证据的主张 | 大纲、正文、翻译润色与数字核对 | [论文写作与润色](../modules/paper-writing/README.md) |
| 已核对数值或实际方法结构 | 可追溯数据图、结构图与图注 | [学术绘图与可视化](../modules/academic-figures/README.md) |
| 已成形稿件或真实审稿意见 | 自查、逐条回复、修订与条件核对 | [投稿与审稿回复](../modules/submission-rebuttal/README.md) |
| 分散的来源、实验、分析与决策 | 建立项目导航、证据记录和交接 | [科研知识管理](../modules/research-knowledge/README.md) |

不必从第一个模块顺序重做。例如已经有实验结果，可以直接进入分析；只有一张汇总截图时先登记材料缺口，而不是让写作技能补出完整研究。

文献模块已有 [实际运行报告](../modules/literature-review/runtime-tests/2026-10-22/README.md)。先按其中的依赖和分项状态选路径；部分原脚本会在失败时仍退出 0，不能只凭命令结束判断成功。

实验模块的 [验证阶段快照](../modules/experiment-design/runtime-tests/2026-10-22/README.md) 已记录 Python 标准库可测路径及 Windows 队列问题；当前复跑与审计仍待完成，远程训练依赖须单独准备和验证。

## 最小使用步骤

1. **确定一次有限任务。** 写清问题、已有材料、输出目的，以及本次只读、写文档或需要运行代码的范围。
2. **选择一个入口。** 先看模块 `SKILL_INDEX.md`，再读所选主版本或 Codex 入口；不要一次加载全部快照。
3. **准备真实输入。** 在自己的研究目录放协议、原始结果、来源和版本，按模块模板登记未知项、失败与限制。公开仓库模板保持空白。
4. **核对依赖与输出位置。** 明确哪些步骤只需材料，哪些需要计算环境、网络、审阅后端或知识库连接。没有相应能力时保留未执行状态。
5. **完成有限交付并核验。** 每个数字、引用和主张能回到证据；把材料缺口交回相应模块。检查方法见 [证据检查指南](EVIDENCE_CHECKS.md)。

可使用这样的自然语言开头：

```text
请先读取本仓库中 [模块名] 的中文索引，选择适合当前宿主的必要入口。
我的任务是：[具体任务]。
已有材料与版本：[位置]；输出到：[自己的项目目录]。
本次允许的工作范围：[只读审计 / 写文档 / 指定计算]。
先列明输入缺口，再完成证据允许的交付；没有执行的步骤和无法确认的结论请明确保留。
```

这是任务描述，不要求斜杠命令已安装。技能文档提到的全局配置、外部服务和自动后续步骤，应按实际环境和本次任务范围处理。

## 先走通教学案例

[连续教学案例](../examples/research-workflow/README.md) 使用同一份原创合成 1NN 实验材料，贯通实验、分析、图表、写作、模拟回复和普通文件知识库。它不代表真实论文复现或投稿。

默认运行器只执行本库原创实验、分析和绘图代码；绘图需要已配置的 Matplotlib，具体版本和输入要求以案例说明为准。让 python 指向已准备好绘图库的项目环境，在仓库根目录的 PowerShell 中使用以下形式；每个输出目录必须尚不存在：

```powershell
python -B examples/research-workflow/run_workflow.py --output "$env:TEMP/ars-workflow-demo-01"
python -B examples/research-workflow/verify_workflow.py --input "$env:TEMP/ars-workflow-demo-01"
```

可选的 ARIS 结构图单组件需显式启用，并使用另一新目录：

```powershell
python -B examples/research-workflow/run_workflow.py --output "$env:TEMP/ars-workflow-renderer-01" --include-renderer
python -B examples/research-workflow/verify_workflow.py --input "$env:TEMP/ars-workflow-renderer-01"
```

可选组件成功也不表示 ARIS 完整绘图技能、外部审阅或全部上游流程已验证。运行状态分层见 [运行状态说明](RUNTIME_STATUS.md)。

文献模块的 [公开 RAG 论文示例](../modules/literature-review/examples/rag-literature-walkthrough.md) 是另一项摘要级阅读练习；它与合成 1NN 案例不属于同一研究，不能把 RAG 文献当作 1NN 结论的证据。

# 连续教学案例：从实验到研究记录

[入门指南](../../docs/GETTING_STARTED.md) · [模块索引](../../MODULE_INDEX.md) · [验证记录](VALIDATION.md)

本例让同一份合成 1-NN 实验依次进入分析、图表、写作、模拟审稿回复和普通知识库。前三步有原创可执行程序，后三步是已写完并核对的教学文档。运行器重新计算数据并核对默认分析摘要，再登记这些文档的版本；它不调用模型自动写论文、产生真实审稿或连接知识库。

| 阶段 | 实际输入与交付 | 阅读入口 |
|---|---|---|
| 实验 | 固定协议 → 三个划分、三个条件、完整预测 | [实验例子](../../modules/experiment-design/examples/README.md) |
| 分析 | 原始产物 → 描述统计及固定 split 11 配对区间 | [分析例子](../../modules/data-analysis/examples/README.md) |
| 绘图 | 已验证分析 → 9 个图点、配对区间、图注与来源 | [绘图例子](../../modules/academic-figures/examples/README.md) |
| 写作 | 相同数值与范围 → Methods/Results/Limitations、中英润色 | [完成的小稿](../../modules/paper-writing/examples/manuscript-walkthrough.md) |
| 回复 | 三条明确模拟意见 → 证据、回复与 M1–M3 修订 | [完成的回复示例](../../modules/submission-rebuttal/examples/mock-review-walkthrough.md) |
| 知识管理 | 实验、来源、主张及决定 → 普通文件知识库 | [项目导航](../../modules/research-knowledge/examples/plain-files/index.md) |

文献模块的 RAG 示例是另一项阅读练习，不能作为此 1-NN 例子的文献依据。此处不提出新颖性或可投稿性主张；协议形成于既有结果之后，固定划分区间不覆盖训练/选模/跨划分不确定性。

## 复跑

先按 [绘图环境说明](../../modules/academic-figures/examples/README.md) 在自己的项目环境准备 Python 与 requirements.txt 中的依赖。下面的 python 应指向该环境。输出必须是仓库外尚不存在的目录，脚本拒绝已有输出与仓库内运行产物。

```powershell
# 在本仓库根目录执行
python -B examples/research-workflow/run_workflow.py --output "$env:TEMP/ars-chain-a"
python -B examples/research-workflow/verify_workflow.py --input "$env:TEMP/ars-chain-a"
# 可选：另外验证并调用固定 ARIS 单文件 SVG 组件
python -B examples/research-workflow/run_workflow.py --output "$env:TEMP/ars-chain-b" --include-renderer
python -B examples/research-workflow/verify_workflow.py --input "$env:TEMP/ars-chain-b"
```

默认执行原创实验、分析、绘图和产物核验。可选参数才调用已审阅的上游渲染组件，先检查其固定摘要；没有启用外部模型、Mermaid 下载或知识库配置。运行失败时保留日志与部分输出，换新目录重试，不把部分结果称为完整交付。

## 输出与交接

输出含 experiment/、analysis/、figures/、run-log.json、handoff.json；可选增加 pipeline.svg。handoff 记录三个阶段 manifest、运行器、案例映射、八份已完成文档的摘要及组件是否执行。文档留在仓库原路径，定位见 [case-map.json](case-map.json)，不复制成引用失效的副本。

用核验器检查数据、阶段来源、图表数据和文档版本对应。它不重新生成手工文本，不自动证明每句话正确；稿件数值、证据链与模拟修订已另作人工/独立复核。若分析摘要或手工文档改变，应审查整条交接链再复跑，不能只修改摘要绕过检查。

最终阅读顺序：实验协议 → 分析限制 → 实际图表和图注 → 教学稿 → 模拟回复 → 知识库决定。共有的缺证据处理方式见 [证据检查指南](../../docs/EVIDENCE_CHECKS.md)。

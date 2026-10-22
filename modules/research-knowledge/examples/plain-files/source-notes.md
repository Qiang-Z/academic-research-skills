# 来源与证据记录

[项目导航](index.md) · [实验与分析笔记](experiment-analysis.md) · [主张与决策](claims-decisions.md)

以下两个来源是本仓库的原创教学项目文档。读取验证记录可以核对它报告了什么；要独立核验原始运行，需要依其说明生成产物。这里没有把记录类型改写成论文或原始数据。

## SRC-TOY-EXPERIMENT-DOC

- Source ID：`SRC-TOY-EXPERIMENT-DOC`。
- 标题：原创 CPU 教学实验的说明、协议与本地验证记录。
- 来源类型：项目文档；包含教学源码与固定协议链接。
- 责任方：本仓库原创教学材料。
- 记录版本：文档日期 2026-10-22；代码与协议以实际文件及仓库摘要为准。
- DOI / arXiv / Zotero ID：不适用，本记录不是论文条目。
- 已读范围：[实验说明](../../../experiment-design/examples/toy-reproducibility/README.md)、[协议](../../../experiment-design/examples/toy-reproducibility/protocol.json)、[验证记录](../../../experiment-design/examples/toy-reproducibility/VALIDATION.md)。
- 原始代码：[run_demo.py](../../../experiment-design/examples/toy-reproducibility/run_demo.py)；此链接存在不代表本知识库步骤已执行它。
- 原始产物：前模块说明运行时生成 `protocol.json`、`dataset.json`、`runs.json`、`manifest.json`；本目录没有保存该运行输出。

### ER-20261022-toy-exp-01

- Source ID：`SRC-TOY-EXPERIMENT-DOC`。
- 定位：实验说明的默认协议与结果、验证记录中的实际检查。
- 归纳：记录描述 240 个合成样本，划分 seed 为 11、23、47；每次训练/验证/测试为 144/48/48。条件包括原始 1-NN、训练集范围缩放的 1-NN，以及去掉 x0 的缩放消融。
- 支持：下游笔记可以如实说明该教学协议和验证记录报告的条件。
- 不能支持：本知识库刚独立运行过实验、已经复现某篇论文、方法适用于真实任务。
- 已知限制：三次划分复用同一数据集，不是三项独立研究；实际运行版本应以产物 manifest 核验。
- 核对方式：阅读上述文档与协议，未在本步骤读取原始临时运行目录。

## SRC-TOY-ANALYSIS-DOC

- Source ID：`SRC-TOY-ANALYSIS-DOC`。
- 标题：原创配对分析的说明、协议与本地验证记录。
- 来源类型：项目文档；包含分析源码与固定协议链接。
- 责任方：本仓库原创教学材料。
- 记录版本：文档日期 2026-10-22。
- DOI / arXiv / Zotero ID：不适用。
- 已读范围：[分析说明](../../../data-analysis/examples/paired-analysis/README.md)、[分析协议](../../../data-analysis/examples/paired-analysis/analysis_protocol.json)、[验证记录](../../../data-analysis/examples/paired-analysis/VALIDATION.md)。
- 原始代码：[analyze_demo.py](../../../data-analysis/examples/paired-analysis/analyze_demo.py)；本步骤未执行。
- 原始产物：应由读者生成并保存四份分析输出，本目录只记录文档中的默认结果。

### ER-20261022-toy-analysis-01

- Source ID：`SRC-TOY-ANALYSIS-DOC`。
- 定位：分析说明的“输出、实际数值和解释”及验证记录的“已记录的结果”。
- 转录值：seed 11 测试集基线 27/48、变体 43/48，配对增益 18、损失 2；差值 +33.3333 个百分点。默认 5,000 次配对 bootstrap 的教学区间为 [18.7500, 47.9167] 个百分点。
- 配置：固定 seed 11 的测试样本对，bootstrap seed 20261022，95% percentile-linear；分析协议已知是事后教学分析。
- 支持：描述验证文档所报告的该设置结果与计算限制。
- 不支持：正式显著性、总体优越性、训练随机性或跨划分不确定性已被覆盖。
- 限制：区间条件于固定模型/划分及 IID 测试样本假设；只有文档转录，不能以此替代独立检查原始产物。
- 原记录所报 `analysis.json` SHA-256：`b2fa4ed155337da6e8e337bfde23186d842c80efda2b1a5db5b214bed3c7d8c0`。这是便于复跑核对的文档记录值，不是本目录持有该产物的证明。
- 核对方式：与已保存分析说明和验证记录交叉核对数值与措辞。

本文 Evidence ID 在 [实验笔记](experiment-analysis.md) 与 [主张台账](claims-decisions.md) 中继续沿用。新增自己的运行产物属于新的证据来源，应记录新 manifest 和具体位置，再决定是否更新主张。

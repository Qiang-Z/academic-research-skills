# 对原创实验结果做一次配对分析

[示例目录](../README.md) · [使用说明](../../USAGE.md) · [验证记录](VALIDATION.md) · [前序实验](../../../experiment-design/examples/toy-reproducibility/README.md)

本例使用 Python 标准库，读取前序 CPU 实验的完整输出，列出全部种子与条件的结果，并演示固定划分下的配对 bootstrap。无需安装包、联网或执行任何上游技能。本例不是通用数据导入器：任意 CSV、真实研究数据或不符合已知格式的 JSON 都不能直接作为输入。

## 1. 先说明分析是在什么条件下做的

前序实验已经公开过结果，因此这份 [analysis_protocol.json](analysis_protocol.json) 是**事后教学分析协议，不是预注册或确认性分析**。协议记录基线 `raw_1nn`、比较条件 `scaled_1nn`、固定测试划分种子 `11`、5,000 次重采样、随机种子 `20261022`、95% percentile 区间。保存协议便于复跑，不会使事后选择变成事前设定。

固定 seed 11 用于展示计算，不通过比较三个 seed 的效果来自动择优。原始的 `11/23/47` 三个划分、三个条件、验证集和测试集统计都保留；变差的消融条件也保留。三个划分复用同一份 240 个样本的数据，不把它们当作独立研究做总体 t 检验或跨种子置信区间，也不把三个测试集简单合计为 144 个独立样本。

## 2. 从已有实验输出开始

在仓库根目录的 PowerShell 中运行。每个输出路径必须尚不存在；如已存在，换新名字。下例使用本轮实际检查过的 Python 3.12，其他可用环境的命令形式可自行替换，但本轮没有验证其他 Python 版本或平台。

```powershell
py -3.12 -B modules/experiment-design/examples/toy-reproducibility/run_demo.py --output "$env:TEMP/ars-stat-input"
py -3.12 -B modules/data-analysis/examples/paired-analysis/analyze_demo.py --input "$env:TEMP/ars-stat-input" --output "$env:TEMP/ars-stat-a"
py -3.12 -B modules/data-analysis/examples/paired-analysis/analyze_demo.py --input "$env:TEMP/ars-stat-input" --output "$env:TEMP/ars-stat-b"
py -3.12 -B modules/data-analysis/examples/paired-analysis/verify_analysis.py --input "$env:TEMP/ars-stat-input" --output "$env:TEMP/ars-stat-a" --compare "$env:TEMP/ars-stat-b"
```

如果已有前序实验输出，跳过第一行并把 `--input` 指向它。输入目录只能包含 `protocol.json`、`dataset.json`、`runs.json`、`manifest.json`。程序先检查文件集合、JSON 重复键/非有限数字、已知字段和类型，再复用前序原创 `verify_demo.py` 检查产物与代码摘要、数据生成、划分、训练集缩放、全部条件、预测和指标；未知格式或篡改后不一致的输入会报错。输入必须包含 seed 11。

`--input`、`--output` 都必须显式提供；已有输出和输入目录下的输出路径会被拒绝，避免改变输入集合。程序在通过输入和协议检查之后才创建输出目录。可选 `--protocol` 可以指定另存的协议，允许更换分析标识、重采样随机种子和 100–50,000 之间的重采样次数；本教学版本固定比较条件、seed 11 和区间方法，修改它们会被拒绝。调整次数或随机种子可能改变区间，须使用新输出目录如实保存，不应反复尝试直到获得想要的结果。

## 3. 配对和区间怎样计算

先用 `sample_id` 对齐同一个测试样本在两个条件下的预测，检查 ID 唯一、集合相同、真实标签一致。每一对记录基线正确性 `aᵢ`、变体正确性 `bᵢ`，两者均为 0 或 1。差值 `dᵢ = bᵢ − aᵢ` 只能是 −1、0、1；平均差乘以 100 得到 **accuracy 的百分点差**。例如 56.25% 到 89.58% 是约增加 33.33 个百分点，不是增加 33.33%。

一次 bootstrap 从 48 个配对样本的索引中有放回抽取 48 次，两条件使用同一组索引。这等价于对 48 个 `dᵢ` 重采样后取均值；不能分别打乱或独立重采样两个条件。重复 5,000 次得到百分点差分布，取 2.5% 与 97.5% 分位点。具体采用线性插值：排序后的位置为 `q × (B − 1)`，在相邻值间插值。

[SciPy 官方 bootstrap 文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) 说明了 percentile 区间与配对输入使用相同重采样索引的原则（查阅日期：2026-10-22）。本例按这些原则用标准库写成，没有调用 SciPy，也不承诺与 NumPy/SciPy 的随机数序列一致。采用 percentile 是为了展示计算过程，并不意味着它在小样本或离散指标下总有理想覆盖率。

这里需要把测试样本视为目标测试分布的独立同分布观察。区间**只描述给定这一次划分和已经拟合好的两个模型时，测试样本抽样造成的不确定性**；没有重训模型，也没有覆盖训练集变化、模型选择或跨划分变化。若有重复被试、聚类、时间依赖或相关样本，本例的逐样本 bootstrap 假设就不适用。它也不是针对这固定 48 个样本的“真值误差条”：固定样本上的正确数是已知的。

## 4. 输出、实际数值和解释

| 输出文件 | 内容 |
|---|---|
| `analysis_protocol.json` | 本次分析使用的协议原始字节。 |
| `input_manifest.json` | 输入实验的 manifest 原始字节，含输入环境和原始代码摘要。 |
| `analysis.json` | 全部描述统计、固定配对记录、bootstrap 区间、重采样差值分布计数和解释限制。 |
| `manifest.json` | 三个分析产物摘要、全部四个输入文件摘要、前序两份代码摘要、本例两份代码摘要，以及本次 Python/平台记录。 |

`analysis.json.descriptive_rows` 有 18 行，即 3 个 seed × 3 个条件 × 验证/测试两部分。每行保存 `split_seed`、`evaluation_split`、`condition`、`n`、`correct`、`accuracy`、`baseline`、`difference_vs_baseline_pp`、`gained_vs_baseline`、`lost_vs_baseline`；最后两项分别是基线错而本条件对、基线对而本条件错的样本数。基线相对自身的差值为零，不生成一个虚假的独立比较。

`paired_bootstrap` 保存固定比较的 48 个 `pairs`、点估计、区间、随机种子、重采样次数和 `resample_sum_counts`。分布计数记录每种“48 个配对差之和”出现的次数，总计 5,000，足以还原本次统计量分布；没有保存每次抽到的索引序列。输入目录需另行保留，分析输出不会复制全部原始数据。

2026-10-22 本地实测结果如下（展示测试集，验证集结果同样保留在输出中）：

| 划分 seed | 基线正确数 | 变体正确数 | 变体 − 基线（百分点） | 消融正确数 | 消融 − 基线（百分点） |
|---|---:|---:|---:|---:|---:|
| 11 | 27 / 48 | 43 / 48 | +33.3333 | 22 / 48 | −10.4167 |
| 23 | 33 / 48 | 44 / 48 | +22.9167 | 26 / 48 | −14.5833 |
| 47 | 34 / 48 | 42 / 48 | +16.6667 | 27 / 48 | −14.5833 |

seed 11 中，变体相对基线有 18 个样本由错变对、2 个由对变错，其余 28 个正确性相同。因此点估计为 `(18 − 2) / 48 × 100 = 33.3333` 个百分点，教学用 95% percentile 区间为 **[18.7500, 47.9167] 个百分点**。这个结果不能被改写为正式显著性结论、真实任务效果或对所有训练划分的保证；本例不输出 p 值或显著/不显著判断。

可用于教学交接的表述是：“在指定合成数据、固定 seed 11 划分及已拟合模型下，变体测试 accuracy 比基线高 33.3333 个百分点；逐测试样本配对 bootstrap 给出上述受条件限制的区间。全部其他划分及条件结果已保留，未进行总体效果或显著性判断。”

## 5. 验证范围

[verify_analysis.py](verify_analysis.py) 重新检查输入、输出摘要与代码版本，读取保存的分析协议并重算统计；`--compare` 要求不同目录，逐字节比较两个输出中的协议、输入 manifest 快照和分析结果。环境记录保留在各自 manifest 中，不要求相同，因此比较成功不等于跨平台验证。

验证器复用了本例的分析函数，不能独立证明统计方法或实现完全正确；本轮另做了手算配对、分位点和小样本重采样边界检查，详见 [VALIDATION.md](VALIDATION.md)。摘要用于发现版本错配或变化，不是真实性签名。代码摘要不匹配时应保留原版本重跑，不能只手改摘要冒充原来的分析。

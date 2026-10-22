# 特征尺度与 1-NN：从实验记录到教学报告

[示例目录](README.md) · [数字核对](claim-check.md) · [验证记录](VALIDATION.md)

这是基于现有合成数据产物的**事后教学写作**。目的在于展示证据、章节和措辞之间的对应，不提出新方法、新颖性或真实任务效果，也不把小稿称为可投稿论文。

## 1. 已填写的写作任务

| 项目 | 本例内容 |
|---|---|
| 读者 | 正在学习实验记录、数据分析和论文结果表达的研究者。 |
| 任务 | 先写中文 Methods、Results、Limitations，再对一个英文结果段落做保留含义的修改。 |
| 核心观察 | 在固定合成数据的三个划分中，使用训练集极差缩放的 1-NN 测试正确数均高于原始距离基线；去掉 `x0` 的消融正确数均低于基线。 |
| 证据 | 前模块原创 `protocol.json`、`runs.json` 与 `analysis.json`；具体选择字段见核对表。 |
| 不能声称 | 缩放普遍更好、机制得到真实世界验证、确认性显著性结果、正式预注册或任何论文创新性。 |
| 交付范围 | 三个中文章节、一个英文修改对照、数值与范围核对；无论文全文、图稿、引用列表或 LaTeX 编译。 |

本例不需要把前序文献模块的 RAG 论文加入参考文献：它们与当前合成实验没有建立证据关系。真实研究若要论述相关工作、算法来源或创新性，需另做有出处的文献核对。

## 2. 写作大纲与证据分工

| 章节 | 段落任务 | 证据与限制 |
|---|---|---|
| Methods | 说明合成样本、划分、三个条件、评价和事后分析 | 原始实验协议和实现；不能把教学协议写成正式预注册。 |
| Results | 展示全部测试条件与划分，再解释 seed 11 的配对差 | 原始正确数和分析产物；不能挑最好种子作为总体效果。 |
| Limitations | 说明构造任务、共享数据与区间覆盖范围 | 协议、数据依赖和分析假设；不添加未经测试的外推。 |

以下三段是可阅读的完成内容，不是待填模板。

## 3. 中文 Methods

本教学实验生成了 240 个带有两个整数特征的二分类样本，数据生成种子为 1729。特征 `x0` 的符号决定翻转前的标签，`x1` 为数值尺度更大的随机特征；每个标签通过固定随机过程以十分之一的概率翻转，实际翻转比例不要求恰为 10%。我们使用划分种子 11、23 和 47，分别将同一批样本分为 144 个训练样本、48 个验证样本和 48 个测试样本。不同划分共享原始数据，各划分内部的训练、验证和测试集合互不重叠。

比较条件为原始平方欧氏距离的 1-NN 基线 `raw_1nn`、按训练集各特征极差缩放距离的变体 `scaled_1nn`，以及从缩放距离中移除 `x0` 项的消融 `scaled_1nn_without_x0`。三个条件在每个划分中使用相同训练样本和评价样本。缩放参数仅由训练集计算，距离相同时按固定样本 ID 选择邻居；实现通过等价整数运算比较缩放距离。条件和划分在评价前由教学协议固定，没有进行梯度训练、超参数搜索或模型选择。验证集只作诊断，测试集不用于拟合缩放参数或选择条件。评价指标为正确预测数除以对应评价样本数。

在结果已经可见之后，我们增加了一个事后教学分析：固定使用 seed 11 测试集，通过样本 ID 对齐基线和缩放变体的正确性，计算变体减基线的百分点差。使用随机种子 20261022，对 48 个配对样本有放回重采样 5,000 次，每次保留两条件的同一样本对应关系，并使用线性插值的 2.5% 和 97.5% 分位数构造教学用 95% percentile 区间。该区间仅在测试样本可视为独立同分布观察的假设下，条件于当前划分和已经确定的模型；本次没有进行显著性检验或跨划分总体推断。

## 4. 中文 Results

表 1 列出三个划分的全部测试条件。缩放变体的正确数分别为 43/48、44/48 和 42/48，相对基线的差值分别为 33.33、22.92 和 16.67 个百分点。移除 `x0` 的消融在三个划分中均低于基线，其较差结果也保留在表中。这里的“均”仅指所列三个划分，不能外推到未评价的任务或数据。

| 划分种子 | 基线正确数 | 缩放变体正确数 | 变体减基线（百分点） | 消融正确数 | 消融减基线（百分点） |
|---|---:|---:|---:|---:|---:|
| 11 | 27/48 | 43/48 | +33.33 | 22/48 | −10.42 |
| 23 | 33/48 | 44/48 | +22.92 | 26/48 | −14.58 |
| 47 | 34/48 | 42/48 | +16.67 | 27/48 | −14.58 |

表 1：同一合成数据在三个固定划分上的测试正确数与条件差值。每个分母均为该划分的 48 个测试样本；差值按未舍入的正确数计算后保留两位小数。三个划分不是三个独立研究，表中没有跨划分平均的置信区间。验证集统计保留在原始产物中，本表仅展示测试结果。

在用于配对演示的 seed 11 中，基线与缩放变体的 accuracy 分别为 56.25% 和 89.58%，差值为 33.33 个百分点。18 个样本由基线预测错误变为变体预测正确，2 个样本变化相反，其余 28 个样本的正确性相同。配对 bootstrap 给出的教学用 95% percentile 区间为 [18.75, 47.92] 个百分点。这个区间保留上述固定划分、固定模型和独立同分布测试样本的条件，不代表重新训练或换划分后的效果范围。

## 5. 中文 Limitations

这些观察来自按特定信号与尺度机制构造的合成数据，目的是练习记录和解释，不能据此宣称缩放在真实数据上普遍有效。消融结果与本例的生成机制相符，但本例没有排除真实应用中的其他解释，也没有开展计算效率、更多数据集或跨任务泛化比较。

三个划分复用同一批原始样本，测试样本可能跨划分重复出现，因此不能将其合并为 144 个独立测试样本，或将三个种子当作三个独立研究进行推断。seed 11 的区间只覆盖所述条件下的测试样本不确定性，不包含训练集变化、模型选择或跨划分变化；其百分位方法在小样本和离散指标下也不保证理想覆盖率。分析与写作均为已知结果之后的教学活动，不是确认性研究、正式预注册或论文复现。

## 6. 英文润色前后与理由

下面的 Original 是本次为教学编写、含义已经受证据约束的粗稿，不是第三方原文。Polished 只调整结构和表达，不新增统计结果。

### Original

On the synthetic test split with seed 11, the raw 1-NN made 27 correct predictions out of 48, and the scaled 1-NN made 43 out of 48. The difference from raw to scaled was 33.33 percentage points. There were 18 wrong-to-correct changes and 2 correct-to-wrong changes. A paired bootstrap with 5,000 resamples gave a 95% percentile interval of 18.75 to 47.92 percentage points. This calculation assumes IID test observations and is for the fixed split and the fitted models. It does not include training, model-selection or across-split uncertainty. It is a post-hoc teaching analysis and there is no significance decision.

### Polished

On the synthetic test split defined by seed 11, the scaled 1-NN correctly classified 43 of 48 samples, compared with 27 of 48 for the raw-distance baseline, an observed difference of 33.33 percentage points. The paired predictions included 18 wrong-to-correct changes and two correct-to-wrong changes. A paired bootstrap using 5,000 resamples yielded a teaching-only 95% percentile interval of [18.75, 47.92] percentage points. Assuming independent and identically distributed test observations, this interval is conditional on the fixed split and fitted models; it excludes uncertainty from training, model selection and changes in the split. No confirmatory significance claim is made from this post-hoc analysis.

### 修改理由

| 修改 | 理由 | 含义核对 |
|---|---|---|
| 将两个正确数合并为一个比较句 | 读者先看到比较对象、分母和差值 | 保留 43/48、27/48 和变体减基线方向。 |
| 加入 observed 并明确 raw-distance baseline | 明确是在当前条件下的观察 | 不改写为 proved、universally better 或 causal effect。 |
| 展开 IID 的首次出现 | 减少缩写对读者的要求 | 不省略独立同分布假设。 |
| 将固定条件与排除的不确定性放在同一句 | 更容易辨认区间回答的范围 | 保留训练、选模和跨划分均不覆盖。 |
| 明确 teaching-only 与 post-hoc | 避免从流畅英文推断为确认性论文结果 | 未增加 p 值、显著性判断或创新性。 |

没有在润色中增加引用、作者、资助、期刊或统计检验。上述英文只对应中文 Results 的 seed 11 子段；完整报告仍须保留全部划分的结果和方法、限制，不能把此段单独截取为普遍效果证明。

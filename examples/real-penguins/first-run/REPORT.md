# 已知物种能否改善企鹅体重预测？

真实公开数据教学比较。鳍长是翅膀状鳍肢的长度；MAE是预测体重与实测体重的平均绝对差，越小越好。

## 方法

主比较用2007–2008年223条观测训练，2009年119条观测测试。预定补充比较用2007年109条训练、2008年114条测试。年份表示简化CSV的季节标签。
三条件为训练体重均值、鳍长普通最小二乘回归、鳍长加物种截距回归（共享斜率）。全部参数只在训练集拟合，x=(鳍长mm−200)/10是固定单位换算。没有调参或依据结果选择条件。
均值条件回答“只知道平均体重怎样”；鳍长条件增加测量信息；物种条件还要求知道物种。详细方案见protocol.json，原始预测在results/predictions.csv。

## 主要结果

- 官方数据共344条，按本题所需两列筛选后保留342条；主划分训练223条、测试119条。
- 2009年留出记录上，mean_baseline的MAE为710.5克，RMSE为819.5克（n=119）。
- 2009年留出记录上，flipper_ols的MAE为325.7克，RMSE为398.9克（n=119）。
- 2009年留出记录上，flipper_species_ols的MAE为297.1克，RMSE为372.7克（n=119）。
- 在本次2009年留出记录上，加入物种后MAE比仅用鳍长降低28.7克；这是固定划分上的描述性差异。
- Horst等2022年论文已讨论鳍长与体重的关系以及加入物种的回归示例；本例是增加时间留出评价的教学延伸。

| 划分 | 条件 | 测试记录 | MAE（克） | RMSE（克） |
|---|---|---:|---:|---:|
| primary | mean_baseline | 119 | 710.5 | 819.5 |
| primary | flipper_ols | 119 | 325.7 | 398.9 |
| primary | flipper_species_ols | 119 | 297.1 | 372.7 |
| secondary | mean_baseline | 114 | 655.7 | 798.7 |
| secondary | flipper_ols | 114 | 306.2 | 385.6 |
| secondary | flipper_species_ols | 114 | 307.7 | 379.6 |

补充划分按原计划保留，无论它是否呈现与主划分相同的方向。下面按物种展开，以免总体均值遮住组内结果。

| 划分 | 物种 | 条件 | 测试记录 | MAE（克） | RMSE（克） |
|---|---|---|---:|---:|---:|
| primary | Adelie | mean_baseline | 52 | 614.0 | 710.5 |
| primary | Chinstrap | mean_baseline | 24 | 501.8 | 572.2 |
| primary | Gentoo | mean_baseline | 43 | 943.5 | 1032.2 |
| primary | Adelie | flipper_ols | 52 | 373.2 | 438.2 |
| primary | Chinstrap | flipper_ols | 24 | 400.7 | 448.5 |
| primary | Gentoo | flipper_ols | 43 | 226.5 | 309.8 |
| primary | Adelie | flipper_species_ols | 52 | 385.0 | 453.3 |
| primary | Chinstrap | flipper_species_ols | 24 | 225.6 | 278.9 |
| primary | Gentoo | flipper_species_ols | 43 | 230.6 | 304.0 |
| secondary | Adelie | mean_baseline | 50 | 481.7 | 591.2 |
| secondary | Chinstrap | mean_baseline | 18 | 508.1 | 600.0 |
| secondary | Gentoo | mean_baseline | 46 | 902.6 | 1029.7 |
| secondary | Adelie | flipper_ols | 50 | 309.9 | 382.6 |
| secondary | Chinstrap | flipper_ols | 18 | 373.8 | 495.7 |
| secondary | Gentoo | flipper_ols | 46 | 275.7 | 336.5 |
| secondary | Adelie | flipper_species_ols | 50 | 321.9 | 394.1 |
| secondary | Chinstrap | flipper_species_ols | 18 | 285.0 | 362.4 |
| secondary | Gentoo | flipper_species_ols | 46 | 301.1 | 369.9 |

## 解释和限制

这些误差描述本次固定留出样本。群间差异可能提供预测信息，但没有分离性别、岛屿、年份等作用；不作因果解释。

- 这是三个物种、三个岛屿、三个繁殖季的公开观测数据，不能推广到所有企鹅、地区或未来季节。
- 原采样包含同巢成对成鸟；简化CSV缺少巢ID，跨年个体重复情况未确认。时间留出不保证个体独立或完全隔离。
- 物种模型要求预测时已知物种；物种与岛屿等因素相关，本比较不证明物种的因果作用。
- 两个时间划分共享观测；不合并为独立重复，不报告p值或置信区间，也不声称统计显著或稳定胜出。
- 排除2条鳍长或体重缺失记录；未建模缺失机制。性别未作预测变量，9条仅缺性别的可用记录仍保留。
- 论文按来源表指定章节阅读；三个EDI原始数据门户本轮未能读取，实际计算使用固定版本的官方公开CSV。
- 已有论文关系和基准知识在设计时已知；本地方案先于本次指标计算，但不是外部预注册或Gorman原文完整复现。
- 流程核验只证明交接结构与引用摘要一致；另行的独立程序复算仅覆盖本固定案例的数值，不等于同行评审。

## 来源与核验

本次evidence.mode=new；replay命令一律复用历史阅读记录，不会重新联网阅读。原始阅读范围和失败网址保留在evidence.json。
- P1（read）：https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081；Publisher HTML: abstract; Materials and Methods / Field methods; Statistical methods; Data management. Selected paragraphs only; supplements, all results and discussion were not fully read.
- P2（read）：https://journal.r-project.org/articles/RJ-2022-020/；Publisher HTML: introductory summary; Data source; The palmerpenguins R package; Data structure and sample size; linear-relationships paragraphs/Figure 4 caption; Penguins data processing; Conclusion. Did not execute supplementary R code or independently reproduce its figures.
- D1（read）：https://raw.githubusercontent.com/allisonhorst/palmerpenguins/8957207b78d6ccd1b4654a9dd9c9041b657478ab/inst/extdata/penguins.csv；Official GitHub API resolved main to the pinned commit. Read DESCRIPTION, README License/Additional data use information/Data citations, and man/penguins.Rd. Downloaded CSV bytes into memory for SHA256 and inspected header/sample rows; full data audit is a separate execution artifact.
- E1（unavailable）：https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.219.5；Package identity read in P2/D1 references only; direct EDI page request returned an internal retrieval error with no usable page content.
- E2（unavailable）：https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.220.5；Package identity read in P2/D1 references only; direct EDI page request returned HTTP 403.
- E3（unavailable）：https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.221.6；Package identity read in P2/D1 references only; direct EDI page request returned HTTP 403.
- L1（read）：https://creativecommons.org/publicdomain/zero/1.0/；Official deed: No Copyright, Other Information and Notice; not a substitute for a dataset-specific license declaration.
- L2（read）：https://lternet.edu/data-access-policy/；Data types, metadata, and Data Use Agreements paragraphs; read online policy text.

公开数据：Palmer Penguins / PAL-LTER，固定官方快照，CC0 1.0；保留来源作者与数据引用。
独立数值检查见logs/numeric.stdout.txt；阶段记录见state.json/events.jsonl；报告主张定位见claims.json。
这是结果模板和受限教学研究，不是可直接投稿的论文。下一步可在另一独立数据来源按新协议检验泛化；不能把本轮测试集继续用于挑模型。

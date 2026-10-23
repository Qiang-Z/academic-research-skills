# 本案例使用的公开数据

[penguins.csv](penguins.csv)是作者官方`palmerpenguins`仓库的固定版本，原始字节保持不变。它是真实公开观测数据，不是合成数据；下载核对记录见[audit.json](audit.json)，论文、检索、许可及访问失败见[来源记录](../SOURCES.md)。

| 项目 | 内容 |
|---|---|
| 官方文件 | [固定版本CSV](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/8957207b78d6ccd1b4654a9dd9c9041b657478ab/inst/extdata/penguins.csv) |
| 上游提交 | `8957207b78d6ccd1b4654a9dd9c9041b657478ab` |
| 获取日期 | 2026-10-23 |
| 文件大小 | 15,241字节 |
| SHA256 | `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93` |
| 原始规模 | 344条观测，8个字段 |
| 数据许可 | CC0 1.0；官方[DESCRIPTION](https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/DESCRIPTION)与[README许可说明](https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/README.md#license)明确声明 |

## 一行和一列分别表示什么

一行是一条成鸟观测。PLOS原研究在同巢采样配对成鸟；简化CSV没有个体/巢ID，不能由此证明344条记录彼此独立，也没有核实跨年个体是否重复。

| 字段 | 新手读法 | 本题用途 |
|---|---|---|
| `species` | Adelie、Chinstrap、Gentoo三类物种 | 第三个模型额外使用；假定预测时已知 |
| `island` | Biscoe、Dream、Torgersen三座岛屿 | 保留背景，不作为本题预测量 |
| `bill_length_mm` | 喙长，毫米 | 保留，本题不用 |
| `bill_depth_mm` | 喙深，毫米 | 保留，本题不用 |
| `flipper_length_mm` | 鳍长，毫米 | 预测量 |
| `body_mass_g` | 体重，克 | 要预测的数值 |
| `sex` | 性别，部分未知 | 保留，本题不用 |
| `year` | 2007、2008、2009的研究季节标签 | 时间划分，不作为模型特征 |

`year`提取自产卵记录，分别对应原论文描述的2007/08、2008/09、2009/10南半球繁殖季，不表示整年连续监测。物种和岛屿分布不平衡，不能把物种系数解释为纯粹因果效应。

## 缺失处理与计数

只排除鳍长或体重为`NA`的两条记录：原始CSV数据记录序号 **4、272**（从1开始，不含表头）。原始文件不删行；执行时按协议筛选。

| 研究年份 | 原始记录 | 本题可用记录 |
|---|---:|---:|
| 2007 | 110 | 109 |
| 2008 | 114 | 114 |
| 2009 | 120 | 119 |
| 合计 | 344 | 342 |

342条可用记录中还有9条性别为`NA`，因本题不使用性别而保留。不要对所有列统一删缺失，否则会悄悄改变实验样本。

公开数据可按[CC0说明](https://creativecommons.org/publicdomain/zero/1.0/)再分发。本案例保留Kristen Gorman、Palmer Station LTER、Allison Horst、Alison Hill及原论文/数据包引用；源头为PAL-LTER→EDI→palmerpenguins。EDI三个网页本轮读取失败，不能把本地CSV可读取说成原始门户完整核验成功。数据作者没有为本案例提供背书。

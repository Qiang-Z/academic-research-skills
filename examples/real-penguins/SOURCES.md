# Palmer Penguins：真实来源与阅读记录

核对日期：2026-10-23。机器可读交接：[sources.json](sources.json)。这是4条实际检索、8个证据条目的定向阅读；范围是两篇论文、官方数据及许可，不是系统综述。使用仓库已有 ARIS `research-lit` 的 web-only 路线与 ClaudeScholar `citation-verification` 的身份/主张分离规则；没有运行上游检索脚本或安装新技能。

## 实际检索（Chinese / English）

| 查询 | 实际结果与选择 |
|---|---|
| `Palmer penguins Horst Hill Gorman 2022 R Journal data 2007 2009 CC0` | 找到论文、包说明；优先读期刊和作者官方来源。 |
| `Gorman Williams Fraser 2014 Ecological Sexual Dimorphism Environmental Variability Penguins 90081 repeated individuals` | 找到PLOS原文；已读段落不能排除跨季节重复个体。 |
| `Palmer Penguins 企鹅 数据 鳍长 体重 2007 2009 原始 数据` | 精度较低；教程、转载和无关企鹅材料未作为证据。 |
| `site.allisonhorst.github.io/palmerpenguins "individual" "year"` | 未解决跨年身份问题；进一步直接查看官方包文档。 |

检索返回的候选并非全部纳入。没有使用镜像CSV替代官方固定版本，也没有把搜索摘要当作论文全文。

## 论文身份与实际阅读范围

| ID / 文献 | 阅读位置 | 对本题的用途与边界 |
|---|---|---|
| **P1**：Gorman KB, Williams TD, Fraser WR. 2014. *Ecological Sexual Dimorphism and Environmental Variability within a Community of Antarctic Penguins (Genus Pygoscelis).* PLoS ONE 9(3):e90081. [期刊原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081) | 摘要、Field methods、Statistical methods、Data management；未通读全部结果/讨论或补充材料。期刊身份与Crossref元数据相符。 | 核对观测来源、测量单位及成对采样。本例不复现原文的生态/性别研究。 |
| **P2**：Horst AM, Hill AP, Gorman KB. 2022. *Palmer Archipelago Penguins Data in the palmerpenguins R Package - An Alternative to Anderson's Irises.* The R Journal 14(1):244–254. [期刊原文](https://journal.r-project.org/articles/RJ-2022-020/) · [DOI](https://doi.org/10.32614/RJ-2022-020) | Data source、变量清单、Data structure、线性关系段落/Fig.4图注、Penguins data processing、Conclusion；未执行论文R附件。期刊身份与Crossref相符。 | 原文已提出加入/省略物种的回归教学比较，本例增加2009留出流程；不得包装为新发现。 |

两篇论文HTML均读取成功。以上是**指定段落阅读**，不是“全文精读成功”。P2的辛普森悖论例子是喙长/喙深，不应把这个标签直接贴到鳍长/体重结果上。

## 数据固定与可再分发性

实际使用 **D1**：[作者官方CSV固定版本](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/8957207b78d6ccd1b4654a9dd9c9041b657478ab/inst/extdata/penguins.csv)。本轮只读获取字节并计算摘要；行数、缺失和划分检查由案例执行记录另行给出。

```text
commit: 8957207b78d6ccd1b4654a9dd9c9041b657478ab
commit date: 2024-09-19T22:17:00Z
package version: 0.1.1
retrieved: 2026-10-23
bytes: 15241
SHA256: f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93
```

[固定版本DESCRIPTION](https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/DESCRIPTION)声明CC0，[README许可段](https://github.com/allisonhorst/palmerpenguins/blob/8957207b78d6ccd1b4654a9dd9c9041b657478ab/README.md#license)和P2相互印证。结合 **L1** [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)，该CSV可以随教学仓库公开再分发。本仓库保留Gorman、Palmer Station LTER、Horst/Hill/Gorman及EDI引用，不暗示其认可案例结论。论文与数据许可应分别看待，不能把文章许可替代数据许可。

**L2** [LTER政策](https://lternet.edu/data-access-policy/)要求看具体数据许可并恰当引用；官方包也建议正式发表研究者联系数据作者讨论成果。本次发布的是教学工作流，没有联系作者，不声称得到其背书。

实际下载路径为官方整理CSV。上游来源链是 **PAL-LTER → EDI → palmerpenguins**，本轮没有证据把Dryad写为数据来源。三个EDI条目保留在交接中：

| ID | 官方数据包 / DOI | 本轮状态 |
|---|---|---|
| E1 | [Adélie 219.5](https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.219.5) · [DOI](https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f) | 直接页面获取内部错误；身份仅从P2/D1引用核对。 |
| E2 | [Gentoo 220.5](https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.220.5) · [DOI](https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689) | HTTP 403；未读EDI正文。 |
| E3 | [Chinstrap 221.6](https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.221.6) · [DOI](https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e) | HTTP 403；未读EDI正文。 |

另外，固定提交下的顶层`LICENSE`请求返回404，应引用实际存在的DESCRIPTION/README；官方首页CC0旧链接本次转到2008年草案讨论页，已改读L1正式说明。失败没有改写为成功。

## 进入实验前应保留的限制

单行代表一条成鸟观测，不能仅凭行数推定相互独立。P1按巢采成对成鸟；简化CSV没有巢/个体ID，跨季节身份是否重叠尚未核实。按年留出解决的是本例时间划分，不能宣称个体或地点完全隔离。

`flipper_length_mm`是鳍长（毫米），`body_mass_g`是体重（克），`species`是三类物种。`year`取自产卵记录；2007/2008/2009对应P1描述的2007/08、2008/09、2009/10南半球繁殖季起始年，不能解释成全年持续监测。三个物种的岛屿分布也不平衡。使用物种作为预测量须假定预测时物种已知；模型改进不表示物种的因果效应，单一留出季节也不能证明区域外泛化。

这些是来源边界和设计限制，不能靠结构检查消除。后续性能数字必须来自本仓库实际执行产物；当前来源文件不预填或推测模型结论。

# 公开数据来源与署名

[案例首页](../README.md) · [取得记录与 SHA-256](../DATA_SOURCE.json)

本目录保存从 UCI 官方 ZIP 解出的 `wine.data` 和 `wine.names`，**均保持原始字节**。2026-10-23 实际下载并核对行列、类别、有限数值及重复特征；没有添加表头或改写旧说明。

- 引用：Aeberhard, S. & Forina, M. (1992). *Wine* [Dataset]. UCI Machine Learning Repository. [DOI: 10.24432/C5PC7J](https://doi.org/10.24432/C5PC7J)。
- [官方数据页](https://archive.ics.uci.edu/dataset/109/wine) · [原始 ZIP](https://archive.ics.uci.edu/static/public/109/wine.zip)。
- 许可：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。署名与来源保留如上；UCI 和原作者未对本库代码或结论背书。
- `wine.data`：178 行，无表头；首列为类别 1/2/3，其余 13 列为化学指标。类别数为 59/71/48。
- 标签表示同一区域酒样的三种栽培品种，**不表示质量评分**。此数据与 Wine Quality 不能混用。
- 特征顺序：Alcohol、Malic acid、Ash、Alcalinity of ash、Magnesium、Total phenols、Flavanoids、Nonflavanoid phenols、Proanthocyanins、Color intensity、Hue、OD280/OD315 of diluted wines、Proline。
- 数据页捐赠日期为 1991，推荐数据引用年份为 1992，旧说明另有 1998 更新记录；不将它们混作论文发表年份。

直接下载有问题时优先使用本目录已核对快照。需要重新取得时只取官方 ZIP 的这两个确切文件，并与 `DATA_SOURCE.json` 的摘要比较；不把检索网页保存成 CSV，不用未经确认的同名镜像代替。

数据说明中的历史分类成绩采用不同方法和评价协议，不能直接与本例固定 5-NN 留出集成绩比较。论文只保存链接、元数据与原创阅读说明，不附论文全文。

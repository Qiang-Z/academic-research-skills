# 文献工作模板

[模块首页](../README.md) · [使用说明](../USAGE.md) · [教学示例](../examples/rag-literature-walkthrough.md)

复制模板到自己的研究项目中填写。占位内容和空字段都不是实际研究记录；未执行的检索、未阅读的全文、未核对的引用分别保留“未执行”“未读”“未核对”。不要将个人研究材料回填到公开仓库模板。

| 模板 | 何时填写 | 交付给下一步的内容 |
|---|---|---|
| [检索日志](search-log.md) | 检索前定范围，检索后填实际结果 | 可复现的查询、来源、失败记录和纳排决定。 |
| [论文笔记](paper-note.md) | 每篇材料阅读时 | 元数据、实际阅读范围、支持与反证及定位。 |
| [证据矩阵 CSV](evidence-matrix.csv) | 跨论文比较时 | 一行一个有来源定位的证据项；同篇论文可多行。 |
| [综述提纲](review-outline.md) | 归纳主题和撰写时 | 与证据项对应的段落、边界和待核验项。 |
| [idea 交接卡](idea-handoff.md) | 进入创新点探索前 | 已知事实、候选问题、最近工作与验证计划。 |

CSV 仅提供字段表头，不含虚构样本。`evidence_id` 与笔记和提纲中的证据编号保持一致；`read_scope` 可填 `metadata-only`、`abstract-only`、`selected-sections` 或 `full-text`；后两种需在 `locator` 记录实际阅读定位。`claim_status` 可填“作者摘要报告”“原文结果已定位”“相互矛盾”“尚待核验”；这些标签不代表人工已读或结论已被独立复现。

`source_type` 记录实际拿到的材料类型，不能把预印本摘要页写成已取得预印本全文；`claim_type` 区分作者报告、策展者归纳、候选假设和独立复现；`claim_strength` 记录判断及理由，未判断则写“待判定”，不由文献身份或阅读范围自动推定。进入 ClaudeScholar 前须按所选分支的 Evidence Record schema 补全和转换，并检查其升级条件。填写这些通用模板不等于通过知识或写作的证据审核。

`supports` / `contradicts` 应写证据对具体问题的关系，`limitation` 记录适用条件，`allowed_wording` 与 `forbidden_stronger_wording` 用于避免综述或 idea 交接时增强结论。空值表示未填写，不表示没有局限或没有反证。

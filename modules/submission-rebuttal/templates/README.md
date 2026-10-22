# 投稿与回复工作模板

[模块首页](../README.md) · [使用说明](../USAGE.md)

复制到自己的研究项目填写。真实稿件、审稿意见和个人投稿信息不要写回公开空白模板。

| 模板 | 用途 |
|---|---|
| [投稿前自查](pre-submission-check.md) | 记录结构、证据、图表和引用问题及待办。 |
| [意见与证据矩阵](reviewer-evidence.csv) | 一行对应一个原子意见，保留证据、回复、修改和未决事项的对应。 |
| [逐条回复](response-template.md) | 从直接回答写到证据、实际修改和仍未解决的问题。 |
| [修改记录](revision-log.csv) | 追踪旧稿、新稿位置、执行状态和核验。 |
| [投稿条件核对](submission-conditions.md) | 记录当前官方规则及核对方式，避免沿用旧例子。 |

两份 CSV 仅有表头，没有虚构的审稿或修改数据。意见表有 15 个字段，修改表有 12 个字段。`issue_id` 为稳定标识；一项意见对应多处修改时在修改表拆成多行，不覆盖原始意见。一个改动涉及多个意见时可在 `issue_ids` 用分号分隔。

`evidence_status` 可写 `available_verified`、`available_unchecked`、`missing`、`planned` 或 `not_applicable`；“verified”须说明实际核对范围，不意味着外部审阅或研究结论成立。`issue_status` 可写 `open`、`answered`、`deferred_intentionally`、`needs_input`；已回答仍可能缺证据，在 `next_action` 保留后续需求。

`commitment_status` 可写 `already_done`、`approved_for_rebuttal`、`future_work_only`、`unconfirmed`、`not_applicable`。已确认的计划仍不是已完成结果；不确定的承诺不能写进确定性回复。`verification_status` 记录检查了哪些修改及证据，未检查写 `unchecked`，不要用空白表示通过。

空字段表示尚未记录；未执行、未确定、不适用需明确说明。通用模板不自动满足上游完整流程的全部产物契约，也不代表符合任何真实投稿场所规则。

# 科研知识管理工作模板

[模块首页](../README.md) · [使用说明](../USAGE.md) · [已填写示例](../examples/README.md)

以下五类模板用于普通文件项目笔记，复制到自己的项目填写。它们是本库通用记录格式，不是 ARIS Wiki 或 ClaudeScholar Obsidian helper 的输入 schema；真正接入时按选定上游契约转换并保留映射。

| 模板 | 用途 |
|---|---|
| [项目导航](project-index.md) | 说明问题、阶段、资料入口、当前决定及下一项动作。 |
| [来源与证据摘录](source-evidence.md) | 区分来源身份与具体证据，记录版本、已读范围、支持/冲突和限制。 |
| [实验与分析日志](experiment-analysis-log.md) | 连接协议、原始产物、分析设置、结果与验证范围。 |
| [主张与决策台账](claim-decision-log.md) | 保存允许措辞、证据状态、反证、取舍理由及版本变更。 |
| [维护与交接](maintenance-handoff.md) | 检查身份、链接、过期记录和未完成项，形成交接摘要。 |

项目 ID、来源 ID、Evidence ID、运行 ID、分析 ID 和主张 ID 分别使用；标题更改不应改变身份。Evidence ID 可采用 `ER-日期-主题-序号`，同一条证据在下游继续使用原编号。空白表示未记录，`not_available` 表示材料当前不可获得，不能把两者当作已验证或数值为零。

本模板的 `evidence_state` 可用 `hypothesis`、`documented`、`artifact_checked`、`needs_review`、`superseded`；每个状态都需文字说明范围。它不是 ARIS 的证明轴或 Scholar 的 claim strength，也不表示证据自动足以支持某项研究结论。

# 实验与复现工作模板

[模块首页](../README.md) · [使用说明](../USAGE.md) · [教学示例](../examples/README.md)

复制到自己的研究项目后填写。空白字段表示尚未记录，不能当作“无问题”；计划与实际结果分开保存。未公开代码、数据及服务器信息留在自己的项目中，不回填到公开仓库。

| 模板 | 用途 | 关键交付 |
|---|---|---|
| [实验计划](experiment-plan.md) | 将研究主张转成测试并冻结协议 | 假设、指标、基线、数据划分、资源上限与停止规则。 |
| [复现检查单](reproduction-checklist.md) | 核对原文、环境、配置与实际结果 | 逐项证据、未决项、差异及复现判断的范围。 |
| [消融矩阵](ablation-matrix.csv) | 描述各条件的变化与不变项 | 条件 ID、比较对象、单一变化、混杂因素及种子计划。 |
| [运行日志](run-log.csv) | 记录每次实际运行 | 运行 ID、协议与数据标识、指标位置、失败和重试关系。 |
| [结果交接](results-handoff.md) | 交接分析及证据审查 | 原始输出、完整条件覆盖、偏离记录与允许的结论。 |

两个 CSV 仅含表头，没有伪造运行行。`ablation-matrix.csv` 的 `status` 使用 `planned`、`implemented`、`not_run` 等计划状态；`run-log.csv` 只在实际启动运行后填写，`status` 使用 `running`、`succeeded`、`failed`、`interrupted`。未运行的条件留在消融矩阵，不虚构开始时间或退出码。

`seed_set` 使用例如 `11;23;37` 的文本；`protocol_id`、`condition_id` 和种子须可关联到实际配置。`code_ref` 可是固定提交或源文件摘要，`data_manifest_sha256` 与 `split_manifest_sha256` 对应实际保存的文件；没有记录就标为未知，不能填示意哈希冒充证据。

`metrics_path` 指向逐次或逐样本结果，`artifacts_manifest_path` 指向输出及摘要清单。发生失败、资源耗尽或重试时保留原运行行，以 `retry_of` 关联新尝试。只有指标文件落盘并完成基本检查后，才标为 `succeeded`；完成运行与研究假设成立是两个不同判断。

这些是通用交付字段，不要求上游工具输出相同列名。接收其 JSON/CSV、日志或 manifest 时保留原文件，另建立字段对应说明。原创教学示例的文件结构以其 README 为准。

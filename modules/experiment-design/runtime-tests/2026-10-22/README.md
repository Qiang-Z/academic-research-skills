# 实验设计与复现：运行验证阶段快照

日期：2026-10-22。**状态：部分测试已有记录，整轮验证仍在进行。** 本页随当前版本同步保存；不能据此将完整上游工作流标为通过。

[模块首页](../../README.md) · [使用说明](../../USAGE.md) · [运行状态](../../../../docs/RUNTIME_STATUS.md)

## 已取得的记录

| 范围 | 当前实际状态 | 证据 |
|---|---|---|
| experiment-plan / ablation-planner | 已按固定技能生成工程实验计划、消融候选与初始追踪表；本轮 CPU 复跑与新上下文审阅待完成 | [规划记录](planning-report.md)、[实验计划](EXPERIMENT_PLAN.md)、[消融计划](ABLATION_PLAN.md)、[追踪表](EXPERIMENT_TRACKER.md) |
| experiment-bridge / run-experiment 相关队列组件 | 原始清单生成器与队列状态函数完成 27 个隔离用例；9 项功能通过、3 项预期拒绝、5 项输入校验缺口、1 项缺依赖受阻、5 项能力边界、2 项平台失败、2 项部署失败 | [组件结果及完整复跑输入](bridge-components-results.json) |
| training-check / monitor-experiment | 已读取 5 个合成日志场景，作一次宿主判断；另完成一份本地合成结果快照的读取比较。只记录建议，没有停止进程或建立调度 | [监控记录](monitor-audit-report.md)、[输入和结果](monitor-audit-results.json) |
| experiment-audit | 已盘点依赖及检查规则；真实 CPU 产物的 fresh reviewer 审计待完成。留痕辅助脚本启动因缺 Bash 受阻 | [监控与审计范围](monitor-audit-report.md) |
| 原创 CPU 示例 | 此前示例测试继续有效；本轮新复跑尚未完成，未产生新成绩 | [既有示例验证](../../examples/toy-reproducibility/VALIDATION.md) |

`run_validation.py` 是本库新增的外围验证入口，当前快照中尚未执行验证。它只运行原创 CPU 示例及错误输入检查；不能替代 ARIS 部署或训练。冻结计划和审阅完成后才按计划执行，并保留实际结果。

## 依赖和已发现问题

本机为 Windows / CPython 3.12.10。JSON 清单处理、队列纯状态测试和原创 CPU 示例只需 Python 标准库；YAML 输入另需 PyYAML，本次未安装。原队列执行路径依赖 Linux/SSH、GPU、screen 及相应环境，当前没有实际启动训练任务。Bash、screen、rsync、conda、nvidia-smi 等未发现，具体检测以组件记录为准。外部审阅、云平台和通知路径尚未测试。

实测发现 Windows 下队列第二次保存状态会失败，重复 job id 可静默合并任务，结果路径存在即可被当作完成；单独复制旧 tools 入口也会因缺少规范实现而失败。其他输入校验缺口、已披露的调度边界、命令和异常保留在 JSON 中。使用时应保留完整快照，手工核对任务编号、输出文件内容与状态持久化，不能只依赖退出码或路径存在。

本次没有改写上游文件。组件执行记录与完整工作流验证分别登记；`runtime_tested: false` 保持不变。后续仍需完成冻结计划审阅、本轮 CPU 双次运行与独立指标核算、真实产物审计及最终综合验收，才能关闭本轮验证。

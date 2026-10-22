# 规划技能受限宿主试用记录

日期：2026-10-22。记录范围：实际阅读仓库原有规划技能，并以本仓库原创教学例为输入形成可执行计划和消融候选表。此记录创建时未执行实验、未填写本轮新成绩，也尚未取得新上下文审阅结果。

## 使用的材料与产物

| 材料 | 本次用途 |
|---|---|
| [实验模块中文索引](../../SKILL_INDEX.md) | 确认入口、分支、复用方式和运行边界 |
| [ARIS Codex experiment-plan](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-plan/SKILL.md) | 采用最多两个主张、证据表、实验块、阶段、资源与停止条件结构 |
| [ARIS Codex ablation-planner](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/ablation-planner/SKILL.md) | 采用 reviewer 问题、组件移除、方向性预期、覆盖评估、预算和可行性结构 |
| [输出版本约定](../../../idea-discovery/01_ARIS/upstream/skills/shared-references/output-versioning.md)、[输出清单约定](../../../idea-discovery/01_ARIS/upstream/skills/shared-references/output-manifest.md)、[语言约定](../../../idea-discovery/01_ARIS/upstream/skills/shared-references/output-language.md) | 明确中文输出、版本留痕与清单阈值；本次新建四文件，无覆写既有规划产物 |
| [ClaudeScholar main 复现规则](../../../idea-discovery/05_ClaudeScholar/upstream_main/rules/experiment-reproducibility.md) | 复用固定随机种子、配置保存、环境记录和数据摘要原则；不执行文中安装或深度学习示例 |
| [原创示例说明](../../examples/toy-reproducibility/README.md)、[协议](../../examples/toy-reproducibility/protocol.json)、[入口](../../examples/toy-reproducibility/run_demo.py)、[验证器](../../examples/toy-reproducibility/verify_demo.py) | 确定输入数据生成机制、固定条件、支持的命令、输出结构和验证器局限 |

本阶段输出：[EXPERIMENT_PLAN.md](EXPERIMENT_PLAN.md)、[EXPERIMENT_TRACKER.md](EXPERIMENT_TRACKER.md)、[ABLATION_PLAN.md](ABLATION_PLAN.md) 以及本记录。产物位于模块的日期目录，不写入上游源码目录。未创建 `MANIFEST.md`：共享约定要求超过 15 个产物时才创建，此规划阶段只有四个文件。

## 已完成与待完成

| 工作项 | 规划阶段实际状态 | 可据此作出的结论 |
|---|---|---|
| 理解并实例化实验规划结构 | 完成：两项工程主张、五个实验块、两次完整复跑、六类负例及核算已固定 | 指令可在当前宿主中用于生成受限工程计划 |
| 实例化消融结构 | 完成候选设计：一个组件移除、基线比较、方向性预期、覆盖与资源说明 | 既有例子能映射到消融框架；不等于审阅或执行完成 |
| 宿主执行者可行性核对 | 根据源码完成静态核对：已有入口一次性生成三个条件，无需改码和新增依赖 | 计划命令与本例接口对应；实际运行仍待测 |
| 新上下文审阅 | 待完成，`[pending external review]` | 不能宣称已完成 reviewer 主导的完整流程；同模型家族复核应标明临时性内部审阅 |
| 两次复跑、原验证器、独立核算、负例 | 待执行 | 本记录不提供新的运行成功证据或成绩 |
| 上游完整规划到部署/训练/审计链 | 未执行 | 不得把计划文档生成标记成完整上游运行通过 |

本次规划子任务不执行任何实验代码。计划与消融表的 SHA-256 在移交执行者时计算并提交；执行者应将冻结摘要写入运行记录。初始 tracker 保持 TODO，随后更新是正常记录行为，不应把更新后的摘要冒充初始冻结值。

## 依赖与输入缺口

本例实际执行所需依赖为已有 Python 解释器、标准库、CPU 和可写临时目录；解释器是否存在及其具体版本必须由执行阶段实测。代码不依赖 NumPy、PyTorch、CUDA、Hydra、DVC、W&B、联网检索、模型服务或密钥，不需要从规则样例引入这些工具。ClaudeScholar 规则中的 GPU 确定性、深度学习 checkpoint、优化器与调度器状态在此例不适用。

本次具备协议、可读源码、合成数据定义、完整固定条件和历史公开结果；不缺少执行该教学例的研究输入。缺少真实论文版本、真实数据授权/切分、原论文目标与容差、研究合同、真实计算预算、`result-to-claim` 产物及领域专家审阅。这些是开展真实研究或完整上游链的缺口，不能以此教学输入补齐或伪造。本轮只使用用户任务给定的有限目标，不制造“已支持论文主张”的前提。

## 适配与发现的问题

1. **已有结果公开，不能作为盲测预注册。** 计划冻结发生在当前复跑前，但不是历史结果出现前；明确只验证工程重复性、可追踪性和指定错误检测。
2. **技能为论文证据链设计，本任务为仓库可运行性核查。** `experiment-plan` 中的论文表格、创新性与前沿必要性条目在此改为有限工程主张，明确无这些科学主张；这是宿主适配，不是按原目标完成整套论文工作流。
3. **消融技能的 reviewer 阶段尚未完成。** 先交付候选表供新上下文审阅；审阅身份、模型家族和处置必须另行记录。不可把同一代理自查称为外部审阅。
4. **原验证器复用原算法函数。** 一致性检查可能重复原实现缺陷，所以计划另外要求不导入原函数的独立核算，并加入更新摘要后的语义篡改负例；这仍不等于全面正确性证明。
5. **固定入口不是通用训练运行器。** 一次调用包含全部条件和种子，无 GPU、SSH、队列、训练 checkpoint 或远程监控；不能推广为 ARIS `run-experiment` / `training-check` 已验证。
6. **输出目录和文件名为模块维护约定。** 四文件保存于当前日期目录而非技能默认的 `refine-logs/`；最终运行记录承担上游 `EXPERIMENT_LOG.md` / `findings.md` 的结果记录作用。属于显式路径适配，未修改上游源文件。
7. **成绩与完整性分开判断。** 工程通过条件是完整、可核算、一致及正确拒绝预设错误；不以缩放必胜作为通过门槛。三个种子共享同一合成数据，不作显著性或可推广效果主张。

## 移交要求

执行者先保存新上下文审阅与冻结摘要，再按固定顺序完成计划。记录实际依赖、两次独立运行的日志和完整产物、正向与负向结果、异常及原文件完整性；对未通过或未执行项如实标记。最终模块状态必须分别报告“规划文档生成”“原创样例执行”“受限宿主工作流”“上游组件测试”“完整上游工作流”，不能合并成一个无边界的 verified。

# 文档、示例、宿主流程、组件与完整工作流状态

[入门指南](GETTING_STARTED.md) · [模块总索引](../MODULE_INDEX.md) · [仓库验证记录](VALIDATION.md)

当前八个模块的完整上游工作流均保持 **`runtime_tested: false`**。文献模块现为 **部分可运行、已做限定实测**：当前宿主完成了三篇公开论文的摘要级检索/综合及引用核对，也执行了多项原始组件并记录失败与缺陷。实验模块已保存部分组件测试和规划/监控演练，当前整轮验证仍在进行；此前原创实验、分析、绘图示例及 FigureSpec 组件的测试继续有效。各项范围独立，不合并表述为全部技能已实测可用。

## 原创自动化编排

新增[自动化科研 pipeline](../workflows/automated-research/README.md)，实际验证范围见[运行记录](../workflows/automated-research/VALIDATION.md)。默认 Wine 适配器复用历史论文阅读与固定协议，重新执行实验和数值核验，生成本次模板报告。自定义课题按结构、摘要和引用关系推进，实际科研执行和语义判断由宿主完成。最新外部热门仓库的检索比较属于静态选型，并未安装或验证这些候选的完整工作流。

## 五类状态分别记录

| 层次 | 检查的对象 | 通过意味着什么 | 不意味着什么 |
|---|---|---|---|
| 文档与静态核对 | 来源记录、路径、摘要、索引、字段与教学数值 | 所声明的文档和来源检查完成 | 技能已安装、代码已执行或研究结论有效 |
| 原创教学示例 | 本库新编实验、分析或绘图代码 | 该例子在记录的环境和用例下运行符合预期 | 上游同名技能、真实论文复现或跨平台兼容已通过 |
| 限定宿主流程 | 宿主按固定技能在明确材料/来源范围内执行 | 所记录路径实际产生并检查了产物 | 所有来源、分支、全文或外部集成都通过 |
| 上游组件 | 一份明确路径的原始程序及指定功能 | 只有标为通过的测试支持所测路径有效；其他可失败或受阻 | 执行过程序、退出 0 或生成文件不自动表示功能正确 |
| 完整上游工作流 | 所选技能及依赖、实际审阅/接入和产物契约 | 只有完整执行并核验后才能记录相应测试 | 不能由前四类检查推定这一类通过 |

`example_runtime_tested` 只描述原创代码示例的运行状态；手工写好的示例文档可完成内容核对，同时保持该字段为 false。`host_workflow_tested` 表示有限宿主路线实际执行，`component_runtime_tested` 表示有组件运行记录；成功、失败及阻塞必须查看分项结果。`upstream_code_executed` 记录是否执行原始程序，不能据此把完整 `runtime_tested` 改为 true。

## 入门组合流程的单独验证

[六步流程记录](discovery/2026-10-22/README.md)覆盖同题三个公开来源的限定阅读、既有合成计算链复跑、新短报告，以及 864 条预测独立计数和两项损坏输入拒绝。另对新发现 Research Hound 的一个离线审计组件做五个合成用例，发现两项漏检；它不属于既有固定快照，不能升级任何模块整体状态。六个主要候选只完成静态审阅，其他在线集成没有测试。之前实验模块的部署/完整审计等未完成项继续独立保留。

## 真实数据案例 · 2026-10-23

[UCI Wine六步案例](../examples/real-wine/README.md)已完成两篇论文的限定阅读、官方公开数据取得与许可核对、首次指标运行前固定方案、实际CPU比较、分析和有边界的中文报告。实际产物为178个样本、六个划分、三个条件、810条预测；另写校验程序与540条NumPy交叉预测一致。九项检查含重复运行、改错预测、全数据拟合、错误数据、覆盖与缺产物的拒绝，详见[验证记录](../examples/real-wine/VALIDATION.md)。

这是本库原创真实数据案例和限定宿主组合流程；没有执行完整上游实验/写作/审稿链，没有新增外部审阅或真人新手研究。原有实验模块未完成的整轮验证保持原状态，不能用本例通过来关闭它。数据快照属于另记许可的公开数据，不改变既有技能来源快照计数。

## 各模块当前范围

| 模块 | 文档与示例材料 | 原创代码示例 | 上游单组件 | 完整上游工作流 |
|---|---|---|---|---|
| [创新点探索](../modules/idea-discovery/README.md) | 来源和中文导航 | 本轮没有独立原创运行示例 | 未执行 | 未运行 |
| [文献检索与综述](../modules/literature-review/runtime-tests/2026-10-22/README.md) | 原教学例子；新增三篇真实宿主摘要综合及引用核对 | 无独立原创研究实验 | 检索、去重/导出、引用和临时构图等已分项测试；存在缺陷及受阻路径 | 部分路径已执行，完整验证未通过 |
| [实验设计与复现](../modules/experiment-design/runtime-tests/2026-10-22/README.md) | 已生成受限规划与单轮合成日志判断；整轮仍在进行 | 既有例子已测试；本轮新复跑待完成 | 队列组件 27 项记录，含通过、缺口、失败与受阻 | 未完成；部署和真实产物审计待测 |
| [数据分析与统计](../modules/data-analysis/VALIDATION.md) | 设计、单位、配对及受限区间说明 | 已测试；CPython 3.12.10 / Windows，详见记录 | 未执行 | 未运行 |
| [论文写作与润色](../modules/paper-writing/VALIDATION.md) | 已填写手工教学稿、润色和数字核对 | 无；文档完成不作软件实测 | 未执行 | 未运行 |
| [学术绘图与可视化](../modules/academic-figures/VALIDATION.md) | 数据映射、结构说明、图注和检查材料 | 已测试；CPython 3.12.10 / Matplotlib 3.11.2，见绘图记录 | ARIS `figure_renderer.py` 的指定校验/渲染路径已测试 | 未运行 |
| [投稿与审稿回复](../modules/submission-rebuttal/VALIDATION.md) | 三条手工模拟意见、回复及实际文字修订 | 无；没有真实投稿或外部审稿执行 | 未执行 | 未运行 |
| [科研知识管理](../modules/research-knowledge/VALIDATION.md) | 普通 Markdown 教学知识库与证据记录 | 无；文档材料不是上游兼容数据库 | 未执行 | 未运行 |

固定来源、文件路径和许可证以各模块 `SOURCE_MANIFEST.json` 为准：[创新点](../modules/idea-discovery/SOURCE_MANIFEST.json)、[文献](../modules/literature-review/SOURCE_MANIFEST.json)、[实验](../modules/experiment-design/SOURCE_MANIFEST.json)、[分析](../modules/data-analysis/SOURCE_MANIFEST.json)、[写作](../modules/paper-writing/SOURCE_MANIFEST.json)、[绘图](../modules/academic-figures/SOURCE_MANIFEST.json)、[投稿](../modules/submission-rebuttal/SOURCE_MANIFEST.json)、[知识管理](../modules/research-knowledge/SOURCE_MANIFEST.json)。

## 已执行上游组件的明确边界

绘图模块此前执行了 [ARIS figure_renderer.py](../modules/idea-discovery/01_ARIS/upstream/skills/figure-spec/scripts/figure_renderer.py)，检查结构 JSON 的 `validate`、两次 SVG 渲染一致性，以及重复节点 ID、指向未知节点的边被拒绝。

这不覆盖 `figure-spec` 完整 agent 工作流、模型审阅、PNG/PDF 转换或所有异常输入。完整组件记录与图表例子的实际环境以 [绘图示例验证记录](../modules/academic-figures/examples/VALIDATION.md) 为准。不能把本轮概括为“没有执行任何上游代码”，也不能概括为“ARIS 已验证”。

文献模块本次执行的原始文件、依赖版本、命令、失败和有限产物见 [文献运行报告](../modules/literature-review/runtime-tests/2026-10-22/README.md)。HTTPS 失败不等于零命中；Crossref 未提供元数据不等于 DOI 虚假；临时合成绑定生成画布不等于真实 Obsidian 联动。原始快照保持不变，发现的问题写在外围说明中。

## 仍未验证的集成

三张新手任务卡的 [限定宿主走查](onboarding-tests/2026-10-22/README.md) 单独保存输入、回答与卡片版本，覆盖材料解读、想法梳理和段落修改。它们是提供材料范围内的文字任务，缺输入/需澄清与完整交付分别记录；无仓库分支是能力限制模拟。该记录不代表代码组件、真实网页版、所有论文文件或完整上游工作流通过，也没有执行新的科研实验。

尚未验证上游科研技能的外部审阅后端、Mermaid CLI、AI 学术绘图接口或真实 Zotero/Obsidian 连接。首页导航配图已通过内置 ImageGen 生成，仓库也已同步到 GitHub；这些事实不代表对应上游集成工作流通过。没有向投稿平台提交稿件。

[连续教学案例](../examples/research-workflow/README.md) 默认仅串联原创实验、分析和绘图；上游渲染器通过 `--include-renderer` 单独启用。运行器或核验脚本的结果只覆盖其明确检查的产物，实际命令、环境、失败路径和未验证范围应以对应验证记录为准。

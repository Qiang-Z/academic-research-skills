# 剩余规划完成核对

日期：2026-10-22。本页保留“剩余模块整理完成”阶段的验收快照；同日后续文献运行测试另见 [当前运行状态](RUNTIME_STATUS.md)，下文“本轮”不包含该后续阶段。整个仓库现有八个整理模块，机器登记见 [MODULES.json](../MODULES.json)。

## 四个新增模块

每个模块均有中文首页、技能索引、使用说明、来源清单、验证记录，以及五类工作模板和已填写的教学示例。上游源码仍保存在原创新点模块中，通过相对路径引用。

| 规划项 | 可直接阅读和使用的交付 | 本轮核对范围 |
|---|---|---|
| [论文写作与润色](../modules/paper-writing/README.md) | 6 个核心技能、12 个分支入口；大纲、章节、润色、主张核对与交接模板；已完成的 Methods / Results / Limitations、中英润色与数字核对 | [示例核对](../modules/paper-writing/examples/VALIDATION.md)：与同一合成实验的实际分析结果对应；不代表执行过上游写作工作流 |
| [学术绘图与可视化](../modules/academic-figures/README.md) | 3 个核心技能、6 个入口；数据图、结构图、图注和交接材料；原创绘图脚本、核验器及三份展示图 | [运行与视觉检查](../modules/academic-figures/examples/VALIDATION.md)：实际数据图输出、独立数值检查、两次产物一致、图像预览；限定 FigureSpec 组件测试 |
| [投稿与审稿回复](../modules/submission-rebuttal/README.md) | 3 个核心技能、6 个入口；投稿自查、意见拆解、证据矩阵、回复和修订清单；三条模拟意见对应回复及实际文字修订 | [模块核对](../modules/submission-rebuttal/VALIDATION.md)：回复能指向已存在证据，新增实验明确列为未执行；没有真实审稿或投稿 |
| [科研知识管理](../modules/research-knowledge/README.md) | 4 个核心技能、8 个入口；普通文件与 Zotero / Obsidian 集成两条路线；完成的索引、来源笔记、实验分析、主张决策及维护记录 | [模块核对](../modules/research-knowledge/VALIDATION.md)：来源—证据—主张指向本例实际材料；没有真实服务同步 |

新增模块合计 16 个核心技能名称、32 个入口文件，全部复用既有快照。核心入口之外的可选入口、辅助程序与许可证分别登记，不混入核心技能数量。

## 公共使用方式与连续案例

| 规划项 | 交付 | 验收依据 |
|---|---|---|
| 统一入门 | [入门指南](GETTING_STARTED.md) | 按已有材料选模块，说明环境准备、示例入口和测试范围 |
| 跨模块流程 | [研究流程与交接](RESEARCH_WORKFLOW.md) | 各阶段的输入、输出、回退条件与交接字段可追溯 |
| 公共证据核验 | [证据检查](EVIDENCE_CHECKS.md) | 区分文件完整性、计算正确性、科学解释、引用和真实投稿状态 |
| 运行状态 | [状态表](RUNTIME_STATUS.md) | 分开记录文档、原创示例、上游组件与完整上游工作流 |
| 同一数据贯通 | [连续教学案例](../examples/research-workflow/README.md) | 实验→分析→绘图实际运行；与八份完成的写作、回复和知识材料绑定版本；[运行记录](../examples/research-workflow/VALIDATION.md)记载默认及可选组件路径 |

连续案例没有将不同题材强行合并：前面的 RAG 文献阅读案例仍是独立摘要级示范；此处使用合成 1-NN 教学实验，不是 RAG 实验或论文复现。后半段文稿与知识记录是完成的手工材料，运行器核对其文件版本，不自动撰写或审阅论文。

## 仓库维护交付

- [总首页](../README.md)、[模块总索引](../MODULE_INDEX.md)、[机器登记](../MODULES.json)与[更新记录](../CHANGELOG.md)已同步八个模块，当前登记没有剩余 planned 条目。
- 每个新模块都有来源清单及原许可证引用；[总来源说明](../THIRD_PARTY_NOTICES.md)保留项目、分支及许可归属。原始上游文件的完整性由 [整包核验器](../scripts/verify_bundle.py)检查。
- [发布说明](../PUBLICATION_NOTES.md)、[发布清单](../PUBLISH_FILES.txt)和[校验和](../SHA256SUMS.txt)纳入本轮交付。临时依赖、原始运行目录、字体与本地同步标记不进入发布清单。
- 最新整包数量、实际核验结果与历史阶段区别见 [仓库验证记录](VALIDATION.md)。

## 完成边界

本轮完成的是约定模块的整理、示例交付和已记录的测试。八个模块的完整上游工作流均保持 `runtime_tested: false`。已实测的上游代码仅为 ARIS `figure_renderer.py` 的指定 validate/render 路径；没有据此宣称 ARIS、写作、审稿或知识库集成全部可运行。未进行真实论文投稿或 GitHub 发布。

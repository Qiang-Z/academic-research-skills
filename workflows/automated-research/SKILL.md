---
name: automated-research
description: Coordinate a bounded research project from question and sources to a frozen protocol, actual experiment, analysis, and traceable report using this repository. Use for a connected research pipeline or resuming a research run; single-paper reading and paragraph polishing use the beginner task cards.
---

# 自动化科研流程

本技能属于整个仓库，不能只复制这个文件单独安装。按相对位置找到仓库根目录，并读取 [使用入口](README.md)。它编排现有技能与本库原创程序；没有注册统一斜杠命令，也没有后台常驻服务。

## 先选最短路径

- 用户想先体验、没有自己的数据：运行根目录 `scripts/research_pipeline.py doctor`，然后 `demo --output <仓库外新目录>`。读取本次 `REPORT.md` 和 `state.json`。前三步是复用既有研究材料，实验和数值核验是本次实际执行；报告是根据本次产物生成的模板报告。
- 用户已有课题：`init --topic <用户题目> --output <仓库外新目录>`，按 `NEXT.md` 补齐当前阶段，再调用 `advance --run <该目录>`。初始化只登记题目，不把未知资源写成已具备。不要替用户填科学判断或结果。
- 用户要继续：先 `status --run`，再 `advance --run`；若完成材料或代码摘要改变，另开一个版本，不编辑历史状态来强行恢复。

新手只需说题目、提供材料和可用资源；JSON、路径和命令由助手维护。能从文件确定的信息直接读取，不反复让用户选择技能。缺少决定性信息时只问一项，并继续不依赖它的工作。

## 每次只加载当前阶段

[skill-routing.json](skill-routing.json) 保存六个阶段的本地入口与摘要。先读取 `module_index`，再读 `primary.path`；仅在对应需求出现时加载 `supplemental`。这些路径相对仓库根目录。`external_candidates` 是固定版本的候选链接，未安装、未作为默认运行依赖；无法读取时明确说明，不假装已执行。

1. **question**：由现有材料收窄成一个可检验问题，记录范围、资源和停止条件。K-Dense 的假设/预测/证据区分用于避免把解释当结论。
2. **evidence**：ARIS 做小批量检索和阅读，ClaudeScholar 核对来源身份及支持位置。综述扩大时才读取 K-Dense 的综述流程。每条来源保留版本、阅读范围、日期、支持与不支持的内容；失败条目保留未获取状态。旧笔记是 `reused`，不能重标为本轮新搜索。
3. **protocol**：ARIS 把问题转为基线、全部条件、样本/独立单位、划分、预处理拟合范围、指标和停止条件。数据要有身份、许可与摘要；明确以前是否见过结果。收集到的是固定方案，不自动称为预注册。
4. **experiment**：默认白名单只执行本库 Wine 适配器。自定义研究由宿主在用户已授权的环境中准备并运行相应代码，写入真实命令、环境、失败和产物摘要；编排器不会执行 `command` 文本。不能将此接口描述为任意 CSV 自动建模。上游的远程部署、付费资源、安装指令不随路由启用。
5. **analysis**：用 ARIS 整理完整结果，以 ClaudeScholar 检查单位、配对、缺失和允许措辞。比例、百分点、相对提升分开；重复划分不算独立研究。Wine 有数值重算；自定义接口仅自动核对结构、摘要和引用，宿主仍需实施适合任务的数值验证。
6. **report**：根据当前分析写报告及 `claims.json`。句子对应来源或结果定位，保留限制和未决项。用 ARIS 大纲/主张检查作适用范围内的参考；没有真实外部审阅就写明未审阅。结构通过、模板生成或同模型复读都不等于投稿就绪。

字段与通过条件见 [CONTRACTS.md](CONTRACTS.md)，只有填当前阶段时才读相应部分。不要一次加载整套上游技能。

## 有边界地继续

默认自定义任务首轮最多四个检索请求、八条来源记录；这是宿主需要遵守并记录的工作预算，不是脚本能控制的 API 计费器。已有更大任务范围或用户预算时，初始化用 `--max-searches` / `--max-sources` 设置合适上限；不要事后改状态。证据不足时解释缺口，在用户已有授权范围内另开清楚限定的下一轮；不能据此声称系统综述已经完整。

数值执行有超时和有限重试，失败产物留在独立尝试目录。不要循环到结果为正，也不要让审阅器自动放宽标准。只在材料确实缺失、校验失败或授权范围不涵盖下一动作时暂停。换方案、数据或代码需新运行目录，并说明与旧版本的关系。

结束时交付本次报告位置、实际完成的阶段、证据范围、问题和最有价值的下一步。需要绘图时按学术绘图模块读取已验证数据，图表是可选扩展，核心流程不要求 Matplotlib 或外部生成服务。

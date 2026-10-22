# 实验设计与复现 · 技能中文索引

[模块首页](README.md) · [使用说明](USAGE.md) · [示例目录](examples/README.md) · [来源清单](SOURCE_MANIFEST.json)

本模块整理 **6 个核心技能名称、12 个主版本/Codex 文件入口**，均来自已保存的 ARIS 快照。另引用 `monitor-experiment` 的两个版本及 ClaudeScholar main 分支的复现规则作为辅助材料；它们不计入核心技能数。源码仍保留在原目录，没有新增安装、更新上游版本或合并不同宿主版本。

适用范围是计算与机器学习实验：方法验证、基线复现、对照与消融、运行记录和证据检查。真实实验还需研究方案、数据与可用环境；本模块没有验证硬件实验、临床试验或人类参与者研究流程。下面的产出是上游设计目标；当前已完成和仍待测试的范围见 [运行验证阶段快照](runtime-tests/2026-10-22/README.md)。

## 先按任务选择

| 当前任务 | 优先入口 | 需要什么 | 预期交付 |
|---|---|---|---|
| 把研究主张转为实验计划 | **experiment-plan**，默认入门 | 方法说明、目标主张、数据与预算约束 | 主张—证据对应、基线、评价协议、运行顺序和追踪表 |
| 检查某组件是否有贡献 | **ablation-planner** | 组件说明、已有结果或明确标为待验证的假设 | 消融矩阵、替代解释、优先级和资源估计 |
| 从已有计划准备实现 | **experiment-bridge** | 实验计划、实现上下文、目标环境 | 实验代码、检查记录；部署和结果收集另有实际执行前提 |
| 启动已准备好的实验 | **run-experiment** | 明确代码版本、命令、数据、目标机器和资源范围 | 启动记录、任务标识、日志和结果位置 |
| 判断正在训练的任务是否异常 | **training-check** | 已有任务、指标/日志、基线与停止范围 | 有证据的 CONTINUE / WAIT / STOP 判断 |
| 在形成结论前检查实验材料 | **experiment-audit** | 原始结果、评价代码、真实标签来源、配置及拟写主张 | 问题清单与审计记录，含审阅独立性及不可用状态 |

“代码生成完成”“进程退出成功”“指标可重算”“主张得到支持”是不同状态。先选能完成当前阶段的入口，不把设计任务自动扩展为远程部署或付费运行。

## 01 · experiment-plan：先定义要取得什么证据

主版本：[experiment-plan/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/experiment-plan/SKILL.md) · Codex：[skills-codex/experiment-plan/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-plan/SKILL.md)

**用途：**把已细化方法转为主要主张、待排除解释、最小可信证据和分阶段运行计划。两版本的主要规划流程相同，默认优先少量主张与强基线，区分必须做和可选实验。

**输入输出：**可读取已有 `FINAL_PROPOSAL.md`、审阅摘要或用户提供的方法说明；上游预期生成 `refine-logs/EXPERIMENT_PLAN.md` 和 `EXPERIMENT_TRACKER.md`。本模块也提供 [实验计划模板](templates/experiment-plan.md)。

**依赖与边界：**整理已有材料可作为文档任务完成；查找新基线或核对数据需要相应来源。上游默认的种子数只是可调整起点，不能当作所有研究都足够的重复次数。计划中的预期效果、资源估计和成功判据须与实测值分开；不生成虚构结果。

## 02 · ablation-planner：让对照回答具体问题

主版本：[ablation-planner/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/ablation-planner/SKILL.md) · Codex：[skills-codex/ablation-planner/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/ablation-planner/SKILL.md)

**用途：**规划移除组件、替换简单方案、超参数敏感性等比较，说明每项改变检验什么、其他条件如何保持一致。主要入口围绕已有主结果后的消融，也支持用户明确要求的消融规划。

**输入输出：**需要组件、主张、现有结果和资源；没有结果时明确“前瞻计划”，不能伪造 `claim_supported` 或填入未执行指标。产出实验矩阵、预期观察、优先级、运行顺序和成本估计。

**版本差异：**主版本使用外部 Codex MCP 审阅设计；Codex 版本使用第二个 Codex reviewer，委派不可用时允许本地规划但须保留 `[pending external review]`。本地自行写出的方案不能冒充独立审阅。实现与启动属于后续动作，不能由消融列表存在就推定已完成。

## 03 · experiment-bridge：从计划到实现的桥接

主版本：[experiment-bridge/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/experiment-bridge/SKILL.md) · Codex：[skills-codex/experiment-bridge/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-bridge/SKILL.md)

**用途：**读取实验计划，准备代码、日志和评价接口，先做最小运行检查，再进入基线、主方法和消融。其完整流程包含部署与结果收集，不能等同于“只写实现方案”。

**默认行为：**两个入口都包含 `AUTO_DEPLOY = true` 和代码审阅约定。仅设计或准备代码时，应在任务中明确停在该阶段；如实际按入口参数执行，可指定 `AUTO_DEPLOY = false`，并以本次任务范围为准。源码中存在默认值不是已获得机器、账号、网络或预算授权。

**版本差异：**主版本通过外部审阅后端检查实现；Codex 版本的 fresh-agent 审阅属于同模型家族的临时结论，委派不可用时要求标为 `[local-only]`。Codex 版本另有失败后诊断路径，不能为了获得成功结果而悄悄更改数据、评价定义或原假设。

**最低记录：**代码提交或文件摘要、完整配置、数据版本、实际命令、最小检查结果和失败日志。小样本检查通过只能说明有限的执行路径可用，不能替代完整实验或论文复现。

## 04 · run-experiment：在明确目标上执行

主版本：[run-experiment/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/run-experiment/SKILL.md) · Codex：[skills-codex/run-experiment/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/run-experiment/SKILL.md)

**用途：**在指定环境启动已准备的实验，保留运行标识、命令、日志、输出位置及资源信息。主版本读取项目 `CLAUDE.md`，Codex 版本读取项目 `AGENTS.md`；这些是目标研究项目的环境说明，不应把本收录仓库的维护文件改写为私人机器配置。

**依赖：**按所选后端可能涉及本地 CUDA/MPS、SSH、环境管理、代码同步、Vast.ai 或 Modal；W&B 是另行启用的指标来源。上游的环境契约还要求实际执行核验，不能用“包可以导入”替代运行准备完成。

**本模块整理约定：**目标机器、同步范围、资源上限与结束方式应写进计划。上游展示的 Git 提交/推送、远端安装、云实例租用、日志上传和清理步骤各有实际影响，只在当前任务已授权的范围内使用；没有后端时记录缺口，不默默换成另一种付费或远程执行方式。

## 05 · training-check：运行中检查，不替代结论分析

主版本：[training-check/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/training-check/SKILL.md) · Codex：[skills-codex/training-check/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/training-check/SKILL.md)

**用途：**读取已有训练的损失、评价指标、NaN/Inf、学习率和可用梯度记录，判断继续、等待或停止。W&B 不可用时可根据已配置日志降级；两者都不可读时，状态应是证据不足，不是实验失败。

**版本差异：**主版本使用周期调度，间隔由约 10 分钟逐渐增加到 60 分钟，并可对不确定情形调用外部审阅；Codex 版本是当前会话内的交互式监控，默认约 30 分钟。不能把两种行为混为“装上后一直后台监控”。

**操作边界：**两版本的 STOP 都可能停止任务。使用前应明确实际任务标识和可采取的停止动作；保存指标、日志片段及原因。模块收录本身不创建计划任务、不长期轮询，也不授权结束不属于当前任务的进程。监控异常与科研主张是否成立分别记录。

## 06 · experiment-audit：检查结果与证据是否对应

主版本：[experiment-audit/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/experiment-audit/SKILL.md) · Codex：[skills-codex/experiment-audit/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-audit/SKILL.md)

**用途：**从评价代码、结果、标签来源、配置及拟写主张检查虚假真值、不当指标变换、无来源结果和评价范围夸大等问题。主要交付是 `EXPERIMENT_AUDIT.md` / `.json` 及对应证据。

**版本差异：**主版本强调执行者收集路径、外部 reviewer 独立读取并判断；Codex 基础版本明确记录 `review_independence: same-family`、`acceptance_status: provisional`。审阅调用不可用时应报告不可用或阻塞状态，不能写成 PASS。本次模块整理没有执行这种审计。

**解释边界：**上游审计具有建议性质，保留 WARN/FAIL 标签并不保证自动停止后续流程；“流程继续”不能解释为问题已解决。报告的完整性问题须在结果交接中保留，不能靠模型判语替代原始数据、评价代码或独立复现。对同一材料反复审阅直至得到满意标签也不是新的实验证据。

## 辅助资料与衔接

- **任务状态与产物收集：**[monitor-experiment 主版本](../idea-discovery/01_ARIS/upstream/skills/monitor-experiment/SKILL.md) · [Codex 版本](../idea-discovery/01_ARIS/upstream/skills/skills-codex/monitor-experiment/SKILL.md)。它关注正在运行的任务与产物位置，可补充 training-check；不是第七个核心技能。
- **复现记录规则：**[ClaudeScholar main：experiment-reproducibility.md](../idea-discovery/05_ClaudeScholar/upstream_main/rules/experiment-reproducibility.md)，涉及种子、配置、环境、检查点及数据版本。它是规则参考，不是可调用的独立 SKILL；本次未发现 codex 快照中的对应规则，因此不建立虚构分支入口。示例中的 PyTorch、NumPy、Hydra、DVC 等不是本模块自有 CPU 示例的依赖，也不因源码存在而自动安装。
- **来源与范围：**[固定来源与许可](THIRD_PARTY_NOTICES.md) · [验证状态](VALIDATION.md)。本模块依赖完整仓库中的原快照目录，不能单独复制导览目录后宣称可安装运行。

上一步可从 [文献模块](../literature-review/README.md) 或 [idea 模块](../idea-discovery/SKILL_INDEX.md) 带入问题、证据及方法计划；下一步用 [结果交接模板](templates/results-handoff.md) 传递真实产物、失败记录和可比较条件。更完整的统计分析与论文论证属于后续任务。

# 投稿与审稿回复 · 技能中文索引

[模块首页](README.md) · [使用说明](USAGE.md) · [模板](templates/README.md)

核心范围是 **3 个技能名称、6 个文件入口**；另有 1 个进阶技能名称、2 个入口。以下描述是固定快照的设计用途，不代表本库已经安装或运行，也不保证提高录用率。

## 先按当前任务选择

| 当前任务 | 优先入口 | 输入 | 预期交付 |
|---|---|---|---|
| 稿件已成形，需要检查完整性和过度主张 | `paper-self-review` | 稿件、证据材料、图表与引用 | 结构和主张问题，保留/削弱/修改/删除建议，具体缺口。 |
| 收到审稿意见，需要整理策略和逐条回复 | `review-response` | 原始意见、稿件、分析证据、实际修改范围 | 分类后的意见、证据锚点、回复策略和专业表述。 |
| 需要管理严格限字回复及后续轮次 | `rebuttal` | 稿件、原始意见、明确投稿规则和轮次 | 问题板、策略、受限回复、修改计划、承诺和覆盖检查。 |
| 已完成论文要迁移到另一投稿场所 | `resubmit-pipeline`（进阶） | 旧稿、目标模板、既有审稿、限定修改范围 | 隔离的新版本、格式检查、微调及审阅记录；不默认新增实验或文献。 |

## 01 · paper-self-review：稿件自查

main：[paper-self-review/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/paper-self-review/SKILL.md) · codex：[paper-self-review/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/paper-self-review/SKILL.md)

两个入口内容相同。技能检查论文结构、逻辑、引用、图表、语言和研究主张。对每条重要主张，可记录 `keep / weaken / revise / remove`、证据、缺失项及建议措辞。适合初稿完成后、交给合作者前，以及修订后复核。

它检查“稿件如何使用已有证据”，不替代重新统计、核实原始结果或验证书目信息。上游将缺少显著性检验列为常见问题，这不意味着所有研究都应补一个 p 值；应按 [数据分析模块](../data-analysis/README.md) 的设计与分析单位判断适用性。引用完整、文字通顺和检查表打勾都不能证明结论有效。

基础自查可基于已有本地材料；需要验证引用真实性、当前会议信息或外部事实时，再查相应原始来源。不得把上游关于录用率的表述当成效果已验证。

## 02 · review-response：意见分类与有依据的回复

main：[review-response/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/review-response/SKILL.md) · codex：[review-response/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/review-response/SKILL.md)

将原始意见按内容和优先级拆解，选择接受修改、依据证据解释、澄清或补实验等策略。每项回复必须指向稿件位置、结果表/图/分析产物、引用/证据记录、带状态的计划，或明确的 `unresolved`。一条意见包含多个问题时要拆分，不用泛泛感谢替代逐项回应。

两个分支主要流程一致，区别是可选写作记忆位于 `.claude` 或 `.codex` 的已安装技能目录。没有对应记忆时可以使用技能自带参考，不能假定用户已有 Zotero、Obsidian 或历史写作库。

“建议补实验”不等于“实验已经完成”；回答“我们已增加”必须附产物和修改位置。仅提出下一步时写清范围、状态与是否已确认，不替作者承诺截止日期、资源或一定取得正结果。

## 03 · rebuttal：管理回复、证据和承诺

主版本：[rebuttal/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/rebuttal/SKILL.md) · Codex：[skills-codex/rebuttal/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/rebuttal/SKILL.md)

此入口适合多审稿人、严格字数/字符限制及后续回复。核心约束是每个事实有来源、每个承诺有状态、每个意见有去向。轻量 `QUICK_MODE` 在问题拆解与策略阶段结束，形成 `ISSUE_BOARD.md` 和 `STRATEGY_PLAN.md`；完整模式进一步生成回复草稿、纯文本版本、修改计划、检查和压力测试记录。

| 版本差异 | 主版本 | Codex 快照 |
|---|---|---|
| 回复布局 | 明确区分共享单文档和逐审稿人独立回复 | 主要按文本回复和每位审稿人组织；不能推定具有相同的模式参数 |
| 审阅方式 | 配置的外部 Codex MCP 或其他受支持后端；手工后端不可用时有停止要求 | 压力测试步骤使用 `spawn_agent`；部分常量和后续文字仍保留 MCP 描述，应以实际适配工具核对 |
| 压力测试轮次 | 有基础轮次与关键意见追加安排及上限 | 保存的基本流程是一轮压力测试 |
| HTML 辅助视图 | 按主版本渲染与审阅约定处理 | 标明渲染失败非阻塞，原始文本和详细草稿仍是正式产物 |

两个版本的 `AUTO_EXPERIMENT` 默认都是 false，但开启时会转向实验流程；读取技能不构成补实验、连接远端或使用算力的授权。默认会议和示例字符数都只是上游参数，真正使用前必须核对具体场所、届次和投稿界面的计数方式。

模型压力测试与真实外部审稿分开记录。未调用审阅时写“未执行”，后端不可用时保留失败/不可用状态；不能因为草稿写好了就声称通过独立审阅。此技能准备回复材料，不自动向 OpenReview、CMT 或 HotCRP 提交。

## 进阶 · resubmit-pipeline：受限范围的重投准备

主版本：[resubmit-pipeline/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/resubmit-pipeline/SKILL.md) · Codex：[skills-codex/resubmit-pipeline/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/resubmit-pipeline/SKILL.md)

适用于已有成熟论文、目标格式文件和既有审稿意见，只进行有限文字修改与格式迁移的场景。它要求保留此前投稿目录，并把新版本放到独立位置；不是通用写作、补实验或重构理论的入口。超出微调范围时应转回写作或实验模块。

主版本与 Codex 适配分别涉及外部审阅或 agent 调用，以及排版工具、审计辅助程序；可选同步还需要目标平台配置。运行前核对实际依赖、文件复制和编译规则，而不是直接执行快照中的示例命令。本模块仅列为进阶导航，没有运行或验证重投流水线，也不把保存的新目录视为远程投稿成功。

## 检查状态与下一步

上游入口均为 `runtime_tested: false`。整理和教学示例的核对范围见 [验证记录](VALIDATION.md)，版本与许可见 [来源说明](THIRD_PARTY_NOTICES.md)。具体填写方法见 [使用说明](USAGE.md)。

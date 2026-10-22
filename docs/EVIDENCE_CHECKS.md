# 跨模块证据检查指南

[研究流程](RESEARCH_WORKFLOW.md) · [运行状态](RUNTIME_STATUS.md) · [模块总索引](../MODULE_INDEX.md)

以下四类检查回答不同问题。保留各自输入、检查范围、实际执行方式和缺口，不把某一层通过当成整项研究已经验证。入口引用用于跨模块导航，不增加核心技能计数，也不授权执行上游脚本或调用外部服务。

## 四类检查的分工

| 检查 | 回答的问题 | 需要的主要输入 | 不能替代什么 |
|---|---|---|---|
| [experiment-audit](../modules/idea-discovery/01_ARIS/upstream/skills/experiment-audit/SKILL.md) | 实验实现和评价是否存在完整性问题 | 实验代码、配置、数据处理和评价定义、执行证据 | 代码未发现问题不说明结果支持目标主张，也不是统计有效性保证 |
| [result-to-claim](../modules/idea-discovery/01_ARIS/upstream/skills/result-to-claim/SKILL.md) | 现有结果在科学上支持什么主张 | 结果、设计、基线、分析、限制和候选主张 | 不自动保证稿件每个数字抄录正确或引用语境正确 |
| [paper-claim-audit](../modules/idea-discovery/01_ARIS/upstream/skills/paper-claim-audit/SKILL.md) | 稿件数字、比较和范围是否忠实对应原始证据 | 实际稿件源文件、原始结果与配置；按所选入口提供新的审阅上下文 | 对照一致不说明研究设计充分、创新成立或因果关系成立 |
| [citation-audit](../modules/idea-discovery/01_ARIS/upstream/skills/citation-audit/SKILL.md) | 引用是否存在、元数据正确并支持所在语境 | 稿件引用上下文、参考文献和可核对的原始来源 | 文献存在不等于支持当前句子，书目校对不等于全文证据审阅 |

需要 Codex 适配时，应从对应模块索引选择，避免把主版本工具名直接套入另一宿主：[实验索引](../modules/experiment-design/SKILL_INDEX.md)、[分析索引](../modules/data-analysis/SKILL_INDEX.md)、[写作索引](../modules/paper-writing/SKILL_INDEX.md)、[文献索引](../modules/literature-review/SKILL_INDEX.md)。

## 一项检查至少留下什么

- 被检查的输入、版本或摘要以及范围；改变材料后注明旧记录是否仍适用。
- 逐条发现及原始位置，区分事实错误、证据不足、方法限制和文字歧义。
- 已做的核对、使用的工具或真实审阅方式，及没有执行的部分。
- 每个结论允许和禁止的措辞、仍需补充的证据及下一步。

缺原始结果时，不能把数值主张审计写成 PASS；没有真实外部来源核对时，不能称引用真实性已验证；审阅后端不可用时，记录不可用或阻塞，不由执行者补写一个通过结论。

## 容易混淆的状态

| 看到的状态 | 最多能说明什么 | 不能自动推出什么 |
|---|---|---|
| 文件存在、路径或摘要匹配 | 文件在对应版本可定位，或与记录字节一致 | 数据真实、计算正确或结论成立 |
| `evidence_check` 的 `verified` | 上游预检查在声明范围内找到文件或所引数值 | 科学主张得到支持、统计设计正确 |
| 自查完成 | 当前自查范围已处理并记录问题 | 已完成独立同行评审或外部审阅 |
| Codex 基础审阅的 `same-family / provisional` | 同系列模型的新审阅及其临时状态 | 独立模型接受、作者之外的真实同行评审 |
| 引用元数据匹配 | 指定来源的作者、题名等记录相符 | 引用的全文结论支持当前具体陈述 |
| 回复覆盖所有意见 | 每个问题都有回复或明确去向 | 所有证据缺口已补齐或审稿人已认可 |

具体状态名以实际所选技能为准，不能在未执行时生成它的正式通过记录。不存在适用检验时保留描述和原因，不为了自查清单补造 p 值、置信区间或独立样本数。

## 检查随证据变化更新

实验代码或评价协议变化后，复核相应实验检查；分析或主张变化后，重新核对结果到主张；稿件或引用变化后，核对受影响的数字与引用。应由材料变化和具体缺口驱动检查，不通过反复裁决直到出现有利结论。

[投稿模块](../modules/submission-rebuttal/README.md) 使用这些记录准备自查与回复；[知识管理模块](../modules/research-knowledge/README.md) 保存来源、状态和决定。知识库中的重复摘要、连线或“已整理”标签不能提升证据强度。

## 当前未执行的进阶取证

ARIS 已保存的 [integrity-forensics](../modules/idea-discovery/01_ARIS/upstream/skills/integrity-forensics/SKILL.md) 是外部 Anti-Autoresearch 的薄启动器，涉及另一个固定仓库、其验证程序和审阅后端。本库保存入口不等于已经收录或运行其完整依赖。本轮未执行该流程；它不作为现有四层检查已通过的依据。

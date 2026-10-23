# 组合依据与接入边界

[立即使用](README.md) · [热门仓库实查](../../docs/discovery/2026-10-23/README.md) · [机器路由](skill-routing.json)

本轮优化的重点是让现有技能交出一致的材料，使计算结果能继续进入分析和报告。不是把热门仓库全部安装到一起：技能库、检索服务、自动实验框架承担的职责不同，同时启动会重复检索、重复审阅，甚至混淆实验状态。

## 调研如何影响本次实现

2026-10-23 通过公开网络检索及官方 GitHub API 核对候选的星标、默认分支、提交和许可。星标是查询时的累计数量，不代表近期增长、效果排名或全网穷尽结果；同项目宿主变体不重复作为独立方法。原始时间与数据见[调研目录](../../docs/discovery/2026-10-23/README.md)。

| 来源与本轮星标快照 | 适合借鉴/复用的能力 | 本库实际接入方式 |
|---|---|---|
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)，53,960 | 假设/证据区分、专题综述、按需科学方法 | 复用本地已固定的 `hypothesis-generation` 和 `literature-review`；统计专门技能仅列为扩展，不假装已收录全部技能 |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)，17,937 | 问题到实验计划、执行记录、结果与写作衔接 | 六步主干引用已有固定入口；不更新或重写上游原件 |
| [ARS](https://github.com/Imbad0202/academic-research-skills)，53,509 | 研究、写作、审查、修改分阶段；阅读与引用记录 | 借鉴交付物与审阅状态的区分；当前 CC BY-NC 4.0，未复制成默认依赖，也未调用其完整流程 |
| [Google DeepMind Science Skills](https://github.com/google-deepmind/science-skills)，3,317 | 具体科学数据库的查询说明与来源定位 | 固定提交的来源适配候选；默认继续使用宿主实际可用检索，接入时单测，不把数据库说明当成通用综述器 |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch)，98,418 | 固定评价边界、资源上限、记录每次实验 | 本库原创协议摘要、限定执行与尝试记录；未复制代码，未启动持续自改训练循环 |
| [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw)，14,743 | 分阶段推进、检查与恢复 | 原创 `state.json`、事件日志、阶段检查和恢复入口；未安装其整套服务 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher)，30,250 | 多来源检索与报告编排 | 有模型/检索提供方配置成本，作为需要服务化检索时的候选；本轮不作为默认新手依赖 |

[AI-Scientist](https://github.com/SakanaAI/AI-Scientist)、[AI-Researcher](https://github.com/HKUDS/AI-Researcher) 等也纳入比较，具体许可、依赖和暂不采用原因见调研记录。更少星标但有特定功能的候选会单列，不包装为热门榜前列。

**既有 ClaudeScholar 继续负责引用和统计边界。** 它已在本库保存固定版本，与 ARIS 的文件布局相容；这项选择基于功能和现有验证，不根据星标做质量推断。`citation-verification` 检查身份及支持位置，`results-analysis` 检查单位、配对及允许措辞。本次只组合所需部分，不把两家的内部状态名称直接混用。

## 六步的默认选择

| 阶段 | 默认本地技能 | 按需补充 | 原创执行层负责什么 |
|---|---|---|---|
| 定问题 | K-Dense `hypothesis-generation` | 用户已有材料与想法任务卡 | 保存题目、范围、资源、停止条件 |
| 找证据 | ARIS `research-lit` | ClaudeScholar `citation-verification`；范围扩大时 K-Dense `literature-review` | 统一来源 ID、阅读状态、版本/日期，保留失败 |
| 定方案 | ARIS `experiment-plan` | 有组件归因问题时再进入消融技能 | 固定协议和数据摘要，分开旧结果与新运行 |
| 真运行 | 内置 Wine 原创适配器；自定义任务参考 ARIS `run-experiment` | 用户实际环境中的已审查程序 | 超时、有限尝试、产物与日志、失败恢复 |
| 做分析 | ARIS `analyze-results` | ClaudeScholar `results-analysis` | Wine 独立数值重算；通用接口做结构、摘要和引用检查 |
| 写报告 | ARIS `paper-plan` | 需要时另做 `paper-claim-audit` | 本次结果模板报告或宿主稿件、主张映射、限制 |

上游 ARIS 的“始终计算相对提升”在本组合中按指标含义处理：基线为零或比例差更易解释时采用合适度量，不强行报相对百分比。报告阶段采用草稿范围，不继承上游默认投稿场所、页数或外部审阅承诺。

## 接入分三档

1. **默认可执行：**本库原创标准库编排器及已存在 Wine 程序。自动执行范围有实测记录。
2. **宿主按需读取：**十个现有技能文件的路径和 SHA256 已进入路由。宿主据当前步骤阅读；脚本只核对路径/摘要，不会“运行 Markdown”。
3. **外部候选：**本轮官方提交链接、能力、依赖与许可记录。需专门功能时再决定是否引入；目前没有安装，也没有完整运行验证。

这种分层让“收录”“读过说明”“实际执行”“科学审阅”各自可追踪。热门仓库的最新提交与本库原固定快照是两个版本：调研最新能力不意味着已更新本库快照。

## 后续扩展优先级

先扩展一个有真实需求的适配器：公开数据下载/身份核对，或指定领域的论文检索。每次扩展都应接到已有阶段文件，保存输入、真实响应和故障，不另造一套状态。其次才是其他数据集的实验适配器与可选绘图。只有明确需要长时间模型实验时，才评估 GPU、服务凭据和更完整的实验循环。

本轮没有自动安装、全局配置变更、后台计划任务或自动投稿。未知许可、服务凭据或依赖缺口只影响对应候选接入，不阻碍默认本地流程。

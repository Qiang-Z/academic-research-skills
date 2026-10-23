# 热门学术技能与自动化框架：本轮组合依据

[首页](../../../README.md) · [新的自动化入口](../../../workflows/automated-research/README.md) · [现有六步流程](../../../workflows/research-starter/README.md) · [上轮功能比较](../2026-10-22/README.md)

检索日期：**2026-10-23**。本轮建议是：保留现有 ARIS 与 K-Dense 技能主干，用本库自己的执行器连接阶段和证据；从热门项目吸收按需检索、固定评估、运行预算、检查点恢复及写作证据检查。需要联网、付费模型或 GPU 的组件单独接入。

## 热度如何核对

先用公开网页搜索发现仓库，再调用 GitHub 官方仓库、提交和文件树 API。另对以下三组 GitHub 查询按 stars 降序各取前 15 条；完整响应摘要见 [search-evidence.json](search-evidence.json)。

- `academic skills in:name,description archived:false`
- `scientific skills in:name,description archived:false`
- `autonomous research in:name,description stars:>1000 archived:false`

排除金融专用代理、自动驾驶模拟器、安全测试工具、纯链接合集和重复移植，保留与“论文—实验—分析—报告”直接相关的候选。定向补查 autoresearch 和 AI-Scientist，因为这些名称不一定匹配上面三个查询。

下表是**本次检索范围内的高关注候选**，不是全网穷尽排名。stars 是 2026-10-23 05:16–05:20 UTC 的累计快照，不是近期增长、独立使用人数或科研效果。`updated_at` 会受收藏等活动影响；维护情况另看默认分支提交日期。原始元数据、查询时间和提交见 [metadata.json](metadata.json)。

| 项目 | Stars | 类型 / 默认分支提交日期 | 在本库的建议位置 |
|---|---:|---|---|
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 98,418 | 有限单次训练、持续迭代的实验代理约定；2026-03-26 | 借鉴固定评估、先跑基线、记录失败；给迭代加总预算和停止条件 |
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 53,960 | 专业技能库；2026-10-19 | 复用本地已有四项技能；统计/绘图等额外技能按需评估 |
| [Imbad0202 academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 53,509 | 研究、写作、审阅技能套件；2026-10-21 | 参考主张与证据对应、阅读范围及阶段交接；作为外部可选套件 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | 30,250 | 网络/本地检索与报告框架；2026-10-10 | 需要深度检索时的可选后端，不承担实验复现 |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 17,937 | 研究与实验技能库；2026-10-22 | 现有主干：问题、文献、实验计划和运行交接 |
| [Sakana AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 14,776 | 模板实验与论文生成框架；2025-12-19 | 高资源路线参考，暂不加入新手默认安装 |
| [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | 14,743 | 多阶段科研自动化框架；2026-08-19 | 参考阶段状态、检查点恢复、预算和失败留痕 |
| [HKUDS AI-Researcher](https://github.com/HKUDS/AI-Researcher) | 5,834 | 容器化研究执行框架；2025-10-16 | 完整平台候选，当前不加入默认链 |
| [zLanqing 中文科研技能](https://github.com/zLanqing/codex-claude-academic-skills) | 5,208 | 写作、Office、科学计算三个入口；2026-05-14 | 参考按交付物路由；Office/MATLAB 任务再考虑扩展 |
| [Google DeepMind Science Skills](https://github.com/google-deepmind/science-skills) | 3,317 | 来源专用科学工具技能；2026-10-15 | 参考 arXiv/OpenAlex 分源检索、限量结果和可追溯元数据 |

ARS 的 [Codex 变体](https://github.com/Imbad0202/academic-research-skills-codex) 有 13,371 stars，作为同一家族的宿主适配记录，不能当作第二份独立方法验证。上轮 Kalaris（53 stars）和 xcl2005（22 stars）有相关功能，但本轮不把它们包装为热门仓库。

## 真正值得组合的部分

| 六步 | 主干与增量来源 | 应交接的可检查产物 |
|---|---|---|
| 1. 明确问题 | 本地 ARIS / K-Dense 问题与假设技能 | 问题、已有材料、可执行范围、未知项 |
| 2. 找到并读懂证据 | 本地文献技能；GDM 的来源专用检索思路 | 真实 URL/标识符、版本、阅读位置、失败来源、候选与已读区分 |
| 3. 固定实验设计 | 本地 ARIS；autoresearch 的固定评估约定 | 数据身份与许可、基线、划分、指标、训练集拟合范围、预算 |
| 4. 执行和记录 | 本库已验证的 Wine 执行器；AutoResearchClaw 的检查点思路 | 真实命令、退出码、每阶段状态、输入/代码摘要、可恢复记录 |
| 5. 复算与分析 | 本库独立复算器；K-Dense 方法选择指引 | 原始预测、数值重算、配对关系、不确定性、失败检查 |
| 6. 形成有证据的报告 | 本地写作/审阅技能；ARS 主张追溯思路 | 每项结论对应来源或结果、局限、待确认项、可复跑说明 |

这是原创整合约定。自动化执行、提示词路由和外部后端是不同接入层：给出技能链接不等于运行了该技能，把已有来源记录导入本轮也不等于重新检索或阅读全文。新题目需要先形成真实材料和协议；不能把 Wine 示例参数直接套到所有课题。

## 固定版本入口、依赖和取舍

完整机器可读映射见 [candidates.json](candidates.json)。下列链接固定在本次检查的提交，避免未来默认分支变化后无法复核。

- **ARIS**：[experiment-plan](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/23745b69a14880b5716d1773e5d20f5f1e6ab1d6/skills/experiment-plan/SKILL.md)、[experiment-bridge](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/23745b69a14880b5716d1773e5d20f5f1e6ab1d6/skills/experiment-bridge/SKILL.md)。Markdown 依赖宿主实施，实际训练依赖课题环境；远程执行和多模型审阅另有配置。MIT。本库继续用既有 `26b95cfa…` 快照，**没有自动升级为本轮上游提交**。不继承其中默认自动部署行为。
- **K-Dense**：[statistical-analysis](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/statistical-analysis/SKILL.md)、[research-lookup](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/research-lookup/SKILL.md)。MIT。前者要求 Python 3.12+ 及独立统计环境；后者要求 Python 3.10+、Parallel 工具/API，OpenRouter 是可选后端。不能把整库宣传成无密钥、无依赖。本地已有快照仍为 `92ace75a…`，只含四项技能。旧名 `claude-scientific-skills` 已改为 `scientific-agent-skills`，新入口目录为 `skills/`。
- **GDM**：[arXiv](https://github.com/google-deepmind/science-skills/blob/99f3085bcb40514cdba7833205b3dedbf473b26d/skills/literature_search_arxiv/SKILL.md)、[OpenAlex](https://github.com/google-deepmind/science-skills/blob/99f3085bcb40514cdba7833205b3dedbf473b26d/skills/literature_search_openalex/SKILL.md)。Apache-2.0，数据和论文许可另计。具体搜索脚本要求 Python 3.10+、`polite-http`，OpenAlex 另用 `python-dotenv`，示例以 `uv run` 调用。OpenAlex 技能正文把密钥写成可选，而项目 README 的介绍更严格；服务可用性和额度须实际查询，不能承诺无密钥可用。本轮未执行这些脚本。
- **AutoResearchClaw**：[runner](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/pipeline/runner.py)、[stages](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/researchclaw/pipeline/stages.py)。MIT。Python 3.11+，核心依赖 PyYAML/rich/arxiv/NumPy；完整运行还需所选 LLM 后端、检索服务和具体实验环境，Docker/LaTeX 按路线需要。静态看到了恢复函数和预算检查，不代表其全流程可靠性已由本库验证。
- **autoresearch**：[program.md](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md)、[依赖](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/pyproject.toml)。原版使用单 GPU、PyTorch/CUDA 训练，评估指标针对语言模型；不是通用论文流水线。本次完整文件树未发现许可证，API 许可字段为空。因此只参考设计，不复制代码或提示词；本库也不采用无限循环和自动回退 Git 的行为。
- **ARS / ARS-Codex**：[写作入口](https://github.com/Imbad0202/academic-research-skills/blob/3224a27a2571cefef0fddfd437004cb006f2b0cb/academic-paper/SKILL.md)、[主张登记契约](https://github.com/Imbad0202/academic-research-skills/blob/3224a27a2571cefef0fddfd437004cb006f2b0cb/shared/contracts/evidence/claim_registry.schema.json)、[Codex 入口](https://github.com/Imbad0202/academic-research-skills-codex/blob/71528d9349bcdacfbe94111f06d9e2d82215a44d/skills/academic-research-suite/SKILL.md)。根许可明确为 **CC BY-NC 4.0**，不是 MIT；本轮只给外部引用和原创概念综合。部分登记脚本需 PyYAML/jsonschema；全文检索、PDF 处理、多模型调用各有条件。覆盖检查不能证明所有语义主张正确，也不代替作者的阅读声明。
- **GPT Researcher**：[开发技能入口](https://github.com/assafelovic/gpt-researcher/blob/3582a6841fe7dc801e2a34e34ee408641aea9bce/.claude/SKILL.md)、[依赖](https://github.com/assafelovic/gpt-researcher/blob/3582a6841fe7dc801e2a34e34ee408641aea9bce/pyproject.toml)。Python 3.12+ 及较多网页/模型依赖；调用模型和搜索服务取决于配置。根 LICENSE 为 Apache-2.0，但同提交 pyproject 标 MIT，存在声明冲突。本轮只做链接候选，未复制或安装。其 Codex SKILL 是简短 MCP 指引，不是完整离线实现。
- **zLanqing**：[科学计算入口](https://github.com/zLanqing/codex-claude-academic-skills/blob/7ed6377f0efb6a38951b48ef03b19d996e454b1f/scientific-toolkit-skill/SKILL.md)、[写作入口](https://github.com/zLanqing/codex-claude-academic-skills/blob/7ed6377f0efb6a38951b48ef03b19d996e454b1f/research-writing-skill/SKILL.md)。根 MIT，内含第三方参考需保留来源。以交付物分流很适合中文新手，但与本库已有覆盖重叠；涉及 Office、MATLAB 或具体科学包时才增加相应环境。
- **AI-Scientist / AI-Researcher**：[前者许可](https://github.com/SakanaAI/AI-Scientist/blob/1de1dbc1f4ee2c5f61e9c94348d55eb51d7fa2eb/LICENSE)、[后者说明](https://github.com/HKUDS/AI-Researcher/blob/f9a6f8480860c193afff600eeffe3defcee8a978/README.md)。前者当前为定制 AI Scientist Source Code License，依赖 LLM 接口和模板计算环境；后者采用 Docker/模型服务，本次根目录未见许可声明。二者都不适合直接拼入无配置的新手路径。

## 本轮没有证实的事情

本轮完成的是官方元数据核对和选定正文的静态阅读，未安装或执行以上候选的新上游代码，未测试其模型效果、全套依赖或科学结论。40 份已读取文件的摘要和阅读位置记录在 [file-evidence.json](file-evidence.json)，文件树摘要在 [tree-evidence.json](tree-evidence.json)；没有收录上游源码全文。

本轮 API 请求和选定原始文件读取均成功。网页检索曾命中同名分叉或较旧介绍，因此以官方 `full_name` 和固定提交确认身份；这不表示所有候选的网络服务都能运行。现有八模块的完整 `runtime_tested` 状态不因本次调研而升级，旧实验模块未完成项继续保留。实际自动化入口的测试应以该入口自己的验证记录为准。

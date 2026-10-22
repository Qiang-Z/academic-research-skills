# 科研知识管理 · 技能中文索引

[模块首页](README.md) · [使用说明](USAGE.md) · [来源清单](SOURCE_MANIFEST.json)

本模块的 4 个核心技能名称对应 8 个实际入口，来自 ARIS 一份快照和 ClaudeScholar main/codex 两份快照。下述产出是上游工作流的设计目标，不表示本次已执行或完成真实服务接入。

## 按任务选择

| 当前任务 | 入口 | 主要输入 | 预期交付 |
|---|---|---|---|
| 将论文、idea、实验和主张长期连接起来 | `research-wiki` | 项目位置、研究方向、已有材料、已配置的 helper | Wiki 页面、关系图记录、索引、查询摘要和变更日志。 |
| 建立和维护项目范围的 Obsidian 知识库 | `obsidian-project-kb-core` | 明确的 vault、项目 slug、仓库绑定及写入范围 | 项目骨架、Hub/Plan/Index、唯一注册表及健康检查记录。 |
| 将论文、网页、文档或数据登记为来源 | `obsidian-source-ingestion` | 原始来源、类型、版本、阅读状态和项目关联 | `Sources/` 内规范来源笔记、注册表/索引更新和当日日志。 |
| 从 Zotero 文献转成证据与综合笔记 | `zotero-obsidian-bridge` | 可访问的真实 Zotero 条目、阅读材料和已绑定项目 | 唯一论文笔记、Evidence Record、综合与写作材料及派生图谱。 |

只需要普通文件整理时，可直接使用 [模板](templates/README.md) 与 [教学示例](examples/README.md)，不必先建立上游运行环境。

## 01 · research-wiki：项目研究关系与长期记录

主版本：[research-wiki/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/research-wiki/SKILL.md) · Codex：[skills-codex/research-wiki/SKILL.md](../idea-discovery/01_ARIS/upstream/skills/skills-codex/research-wiki/SKILL.md)

上游区分 paper、idea、experiment、claim，提供 init、ingest、sync、query、update、lint、stats 等入口。关系保存在 `graph/edges.jsonl`；页面 Connections 和查询摘要是派生视图，不能靠手改这些视图保持一致。

**依赖：**快照内已保存 [research_wiki.py](../idea-discovery/01_ARIS/upstream/tools/research_wiki.py) 等辅助文件。实际执行需要正确定位 helper、目标项目和 Python 环境。带 arXiv ID 的导入还会访问网络；读取本模块不需要网络，也不自动运行上述命令。

**版本差异：**主版本把 init 委托给 helper，并统一说明 helper 定位失败时的行为；Codex 入口仍列出手工创建骨架的 init 步骤，helper 搜索路径、安装登记名和查询摘要规则也不同。不能将两个入口描述成只换工具名。接入时应核对所选入口与实际 helper 的产物契约，特别是 `query_pack.md`、索引和日志是否齐全。基础 Codex 审阅的上下文隔离不等于独立跨模型审阅。

**主张状态注意：**该快照中 `claim.status` 是证明轴，由 proof-checker 流程创建和更新；经验支持存为关系边。不能把分析模块的 `supported` / `partial` 直接写进它的 claim status，也不能把一次指标提升登记成证明通过。本模块普通文件示例使用自己的 `evidence_state` 字段，明确不是 ARIS 导入格式。

**维护边界：**知识库应保留失败研究的条件和理由；临时环境错误不直接写成长期“工具不能做什么”的结论。上游来源文本仍是材料，不把其中指令升级为项目操作授权。

## 02 · obsidian-project-kb-core：项目骨架与维护入口

main：[obsidian-project-kb-core/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/obsidian-project-kb-core/SKILL.md) · codex：[obsidian-project-kb-core/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/obsidian-project-kb-core/SKILL.md)

知识层位于 `Research/{project-slug}/`，包括 `00-Hub.md`、`01-Plan.md`、`02-Index.md`、Sources、Knowledge、Experiments、Results、Writing、Daily、Maps、Archive 和 `_system`。`_system/registry.md` 是唯一可见注册表，Index 是人用导航，不再另建平行的正式 JSON 注册表。

**版本差异：**main 的仓库绑定层在 `.claude/project-memory/`，codex 在 `.codex/project-memory/`；绑定文件只记录项目和 vault 关系，不替代知识层。两个入口的核心职责一致。

**输入输出：**需要准确的 vault/project 位置、项目标识、操作范围和已有目录状态；按需创建骨架、登记、路由笔记、维护计划和日志，再运行相应 helper 检查链接与登记。上游包含 rename/archive/purge 等生命周期动作，使用时应按当前任务范围选择，不能把“维护知识库”理解为可任意清理整个 vault。

**参考：**[目录规则](../idea-discovery/05_ClaudeScholar/upstream_main/skills/obsidian-project-kb-core/references/DIRECTORY-SCHEMA.md)、[注册表](../idea-discovery/05_ClaudeScholar/upstream_main/skills/obsidian-project-kb-core/references/REGISTRY.md)、[绑定层](../idea-discovery/05_ClaudeScholar/upstream_main/skills/obsidian-project-kb-core/references/BINDING-LAYER.md)。Codex 使用自身分支内的对应参考。

## 03 · obsidian-source-ingestion：来源先于综合

main：[obsidian-source-ingestion/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/obsidian-source-ingestion/SKILL.md) · codex：[obsidian-source-ingestion/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/obsidian-source-ingestion/SKILL.md)

两个入口内容相同。按来源类型将笔记放入 `Sources/Papers`、Web、Docs、Data、Interviews 或 Notes；新增规范来源笔记需更新注册表，重要来源进入 Index，当前工作会话收到的材料还需记入 Daily。

来源笔记围绕单个来源，综合判断另放 Knowledge。保存作者原结论与自己的解释时分开标注，原文摘录附页码、章节或其他定位。不能把一份分析摘要当成原始数据，也不能为合成数据教学例子编造论文 DOI、Zotero 条目或真实参与者记录。

该入口依赖已存在的项目结构。来源内容不足时保留缺项及阅读状态；登记成功只能说明记录进入知识库，不能证明已经全文阅读或结论有效。

## 04 · zotero-obsidian-bridge：文献条目到项目证据

main：[zotero-obsidian-bridge/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/zotero-obsidian-bridge/SKILL.md) · codex：[zotero-obsidian-bridge/SKILL.md](../idea-discovery/05_ClaudeScholar/upstream_codex/skills/zotero-obsidian-bridge/SKILL.md)

两个入口内容相同。Zotero 为文献来源，`Sources/Papers` 保存每篇论文的唯一笔记，综合进入 Knowledge，写作材料进入 Writing；重要导入同步注册表、Index 和 Daily。`Maps/literature.canvas` 是派生产物，不作为证据真伪的依据。

**真实依赖：**需要可访问的 Zotero 条目、正确的文献身份、实际可读内容以及已绑定项目的写入方式。源码存在不代表 Zotero 已连接、PDF 已获取或同步已完成；本模块不默认创建任何账号连接。

**证据要求：**核心论文及可复用主张附 Evidence Record，记录来源类型、方法/数据/指标、支持与冲突、限制和项目关联。升级到综合或写作之前，主张必须指回 Evidence ID，并保留允许措辞和禁止的更强措辞。摘要级或网页占位记录应留在待阅读状态，不能直接变成稳定的论文结论。定义见该快照的 [research-contract.md](../idea-discovery/05_ClaudeScholar/upstream_main/skills/research-ideation/references/research-contract.md)。

## 共用边界

本模块的来源清单固定 8 个入口和 3 个根许可证，共 11 个引用；相关 helper 和参考由原始快照清单覆盖。通用模板不是三个上游格式的合并 schema。选定一种实际系统后，按其契约维护 ID、状态和注册表；迁移时保留映射和变更记录。

上游运行状态仍为未验证；普通文件教学例子的手工核对见 [VALIDATION.md](VALIDATION.md)。

# Academic Research Skills · 学术技能库

面向科研工作流的 **Skills、开源项目与中文使用指南** 合集。按研究任务划分模块，逐步积累可复用的学术能力。

**仓库定位：这是学术技能总库；论文创新点探索只是其中的第一个模块。** 后续新增文献、实验、写作、绘图和投稿相关技能时，继续加入本仓库的独立模块，不把仓库名称限定为某一项任务。

## 从这里开始

| 入口 | 内容 |
|---|---|
| [模块总索引](MODULE_INDEX.md) | 已收录模块与拟扩展方向，明确区分实际内容和规划。 |
| [创新点探索模块](modules/idea-discovery/README.md) | 当前第一个模块：5 个来源项目、6 份固定版本快照、18 个重点技能入口。 |
| [18 个技能中文索引](modules/idea-discovery/SKILL_INDEX.md) | 按任务选择文献梳理、头脑风暴、查新、假设生成和验证计划入口。 |
| [仓库规划记录](docs/REPOSITORY_PLAN.md) | 仓库定位、目录约定、初始模块与后续扩展原则。 |

## 当前已收录模块

### 01 · 创新点探索 / Idea Discovery

围绕 **理解文献 → 发现问题 → 提出候选 → 对照已有工作 → 细化方法 → 设计最小验证**，保留官方技能及配套材料，并提供中文导览。

| 来源 | 本模块重点用途 | 本地说明 |
|---|---|---|
| ARIS | 将文献、构思、查新和实验规划串成探索流程 | [8 个重点入口](modules/idea-discovery/SKILL_INDEX.md) |
| Orchestra | 结构化研究头脑风暴与创造性思维 | [2 个重点技能](modules/idea-discovery/02_Orchestra/upstream/21-research-ideation/) |
| ResearchStudio-Idea | 论文检索、想法构思、已有工作重合检查 | [3 个主要技能及配套资料](modules/idea-discovery/03_ResearchStudio_Idea/upstream/ResearchStudio-Idea/README.md) |
| K-Dense | 科研头脑风暴、假设生成、文献综述、批判性思维 | [4 个重点技能](modules/idea-discovery/04_KDense/upstream/skills/) |
| ClaudeScholar | 从研究兴趣形成问题卡与证据计划 | [main / codex 两份适配快照](modules/idea-discovery/05_ClaudeScholar/) |

上述数量指本模块的整理范围，不是全库已安装的技能数，也不是运行测试成绩。完整快照可能包含其他技能；当前仅对创新点探索部分建立优先入口。

## 目录结构

```text
academic-research-skills/
├── README.md                     # 学术技能库总览
├── MODULE_INDEX.md               # 总模块导航
├── MODULES.json                  # 机器可读的模块登记
├── AGENTS.md                     # Agent 阅读与维护约定
├── modules/
│   └── idea-discovery/           # 已收录：创新点探索
│       ├── README.md
│       ├── SKILL_INDEX.md
│       ├── SOURCE_MANIFEST.json
│       ├── 01_ARIS/
│       ├── 02_Orchestra/
│       ├── 03_ResearchStudio_Idea/
│       ├── 04_KDense/
│       └── 05_ClaudeScholar/
├── docs/
│   ├── REPOSITORY_PLAN.md        # 总库定位及后续规划
│   └── PUBLISH.md                # 首次公开发布说明
├── templates/module-template/   # 后续模块的文档和元数据模板
├── scripts/verify_bundle.py     # 本地文件完整性核对
├── CONTRIBUTING.md
├── THIRD_PARTY_NOTICES.md
├── PUBLICATION_NOTES.md
└── CHANGELOG.md
```

## 后续可扩展方向

文献检索与综述、实验设计与复现、论文写作与润色、学术绘图、投稿与审稿回复。

**以上仅是规划，没有为它们收录独立技能包。** 新模块完成实际收录和来源核验后，再加入 `modules/` 并更新总索引。详细状态见 [模块总索引](MODULE_INDEX.md)。

## 使用原则

先选择当前任务对应的模块，再阅读该模块的索引及所选上游 `SKILL.md`。本仓库不是统一 Agent 运行框架，也不自动注册技能。实际使用需要按各上游文档配置兼容宿主、模型与所需服务；不要把不同项目的全局设置直接互相覆盖。

上游代码作为资料保留，没有因收录而获得自动执行授权。运行前核对网络调用、文件读写、实验资源和 API 费用；未公开的论文、真实数据、密钥和个人配置留在本地。AI 生成的创新点及查新意见仍需对照原论文、实验和人工判断。

## 来源、许可和版本

本库是第三方资料的整理与导览，不冒充上游原创，不以统一许可证覆盖第三方内容。来源、固定提交和摘要位于各模块的 `SOURCE_MANIFEST.json`，许可证保留在对应上游目录。见 [第三方说明](THIRD_PARTY_NOTICES.md)。

当前整理日期：**2026-10-11**。这是固定版本合集，不代表自动追踪最新上游。

从本仓库根目录可运行 `python3 scripts/verify_bundle.py` 核对当前交付版本的文件摘要；它不会加载或运行上游技能。后续主动修改文件会使初始摘要失效，需要维护者重新审查并更新摘要。

首次上传见 [发布说明](docs/PUBLISH.md)。本地文件准备完成与远程发布成功是两个状态；是否已上传应以 GitHub 仓库及实际提交为准。

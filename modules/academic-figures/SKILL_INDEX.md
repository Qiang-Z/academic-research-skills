# 学术绘图 · 技能中文索引

[模块首页](README.md) · [使用说明](USAGE.md) · [来源清单](SOURCE_MANIFEST.json)

3 个核心名称对应 6 个入口，均来自 ARIS 一份 main 快照；Codex 适配保存在同一快照内。以下是技能设计目标，不表示本次执行了完整工作流。

| 任务 | 技能 | 输入与预期输出 |
|---|---|---|
| 实验数据可比较 | paper-figure | 核对后的数据及图表计划 → 脚本、矢量图、比较表。 |
| 精确表达组件关系 | figure-spec | 节点、坐标、边、分组 JSON → 可编辑 SVG。 |
| 简洁流程与时序 | mermaid-diagram | 实际步骤与关系 → 一致的 MMD/Markdown 源码及渲染预览。 |

## paper-figure：实验图与比较表

[主版本](../idea-discovery/01_ARIS/upstream/skills/paper-figure/SKILL.md) · [Codex](../idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-figure/SKILL.md)

输入通常为 PAPER_PLAN.md 图表计划及 JSON/CSV。适合曲线、散点、消融、方法对照、热图和多面板图；保留脚本、样式、PDF 与表格片段。数值从实际产物读取，不能为预期结论编造分数。

实际绘图依赖 Python、Matplotlib 等；主版本通过 Codex MCP 审阅，Codex 入口改用另一个 agent。实际审阅与独立性据实记录。本模块原创脚本不等于运行过该技能。

上游正文把数据图与架构图分开，但输出目录示意仍出现架构图脚本名称，不能据此推定其自动架构图能力。会议风格、图宽及字号是版本内建议，实际投稿要求另行核对。

## figure-spec：可编辑结构图

[主版本](../idea-discovery/01_ARIS/upstream/skills/figure-spec/SKILL.md) · [Codex](../idea-discovery/01_ARIS/upstream/skills/skills-codex/figure-spec/SKILL.md) · [渲染器](../idea-discovery/01_ARIS/upstream/skills/figure-spec/scripts/figure_renderer.py)

使用节点 ID、中心坐标、形状、边与分组描述结构；JSON 与 SVG 一起保留。每个箭头对应实际关系，修改 JSON 后重新渲染。title 只作元数据，不自动显示。

两个入口解析工具位置的方式不同，均应定位实际 skills/figure-spec/scripts/figure_renderer.py。SVG 基础路径只需标准库；PNG/PDF 转换另需工具。主版可选审阅使用 Codex MCP，基础 Codex 适配明确同系列审阅和临时接受状态。

渲染器可以覆盖同名输出，示例使用新目录；validate 成功不能替代视觉检查或完整输入安全验证。单组件实测见 [示例验证](examples/VALIDATION.md)。

## mermaid-diagram：流程与时序

[主版本](../idea-discovery/01_ARIS/upstream/skills/mermaid-diagram/SKILL.md) · [Codex](../idea-discovery/01_ARIS/upstream/skills/skills-codex/mermaid-diagram/SKILL.md)

按关系选择图型，保存内容一致的 .mmd 与 .md。两入口要求语法和视觉核对，Codex 正文明确调用 Mermaid CLI。上游包含缺少 mmdc 时用 npx 获取最新版的命令，阅读不触发该操作；实际接入应记录选定版本及环境。只有手工源码检查时不能标为渲染成功。

## 可选：AI 示意插图

[paper-illustration 主版本](../idea-discovery/01_ARIS/upstream/skills/paper-illustration/SKILL.md) · [Codex](../idea-discovery/01_ARIS/upstream/skills/skills-codex/paper-illustration/SKILL.md)

依赖外部图像服务、密钥和审阅，不计为核心技能。主版可选 style-ref 段落在基础 Codex 版没有相同完整内容。固定版本的模型名、接口与所谓会议风格不能作为当前服务可用性或官方投稿规范。生成图需逐字、逐箭头复核；不当作真实实验样本。名称相近的 figure-description 面向专利附图，未纳入核心范围。

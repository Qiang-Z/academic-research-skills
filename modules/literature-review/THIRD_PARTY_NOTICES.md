# 来源、许可与复用边界

[模块首页](README.md) · [机器可读来源清单](SOURCE_MANIFEST.json)

本模块的技能来自以下既有固定快照。中文指南、模板和教学示例属于外围整理；没有将第三方技能改写为本仓库原创，也没有重新授权第三方文件。

| 来源 | 分支与固定提交 | 原许可证 |
|---|---|---|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | main · `26b95cfa0d8747078e9e43b42e20952709e561b8`，其中包含 Codex 适配目录 | [MIT](../idea-discovery/01_ARIS/upstream/LICENSE) |
| [ResearchStudio](https://github.com/microsoft/ResearchStudio) | main · `063f10088af49909e1a4a7ea8d29efe19633f34e` | [MIT](../idea-discovery/03_ResearchStudio_Idea/upstream/LICENSE) |
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | main · `92ace75ac21efe19a620434e0ca4e356081fe807` | [MIT](../idea-discovery/04_KDense/upstream/LICENSE.md) |
| [ClaudeScholar](https://github.com/Galaxy-Dawn/claude-scholar) | main · `903787345d6aec134086afa2b97715a78fbde519` | [MIT](../idea-discovery/05_ClaudeScholar/upstream_main/LICENSE) |
| ClaudeScholar | codex · `b672e80951a2348dd6136316d096603bf2dc5b83` | [MIT](../idea-discovery/05_ClaudeScholar/upstream_codex/LICENSE) |

这些版本沿用 2026-10-11 的采集记录。本模块整理日期为 2026-10-22，不代表重新拉取或追踪最新分支。根许可证不取代文件及子目录中的独立声明，完整说明见 [原模块第三方说明](../idea-discovery/THIRD_PARTY_NOTICES.md)。

## 相对路径与依赖

本模块的 `SOURCE_MANIFEST.json` 以其所在目录为路径基准。每项 `bundle_relative_path` 指向 `../idea-discovery/` 内的原快照；`reused_from_manifest` 和 `reused_source_id` 指回原清单。`files` 保留 8 个核心入口、1 个可选关联入口、5 个根许可证，以及本次实际执行/导入的辅助文件原始摘要。辅助文件列在 `supporting_files`，不增加核心技能数；主版本与 Codex 分支不合并覆盖。

`files` 是本模块选定文件的核验范围，不是独立安装所需依赖清单。共享参考、脚本和其他已保存文件由 [原始完整来源清单](../idea-discovery/SOURCE_MANIFEST.json) 记录，仍保留在原相对目录；外部连接、服务、数据库或未收录的兄弟技能不会因为引用而自动可用。

## 教学示例与新整理材料

示例链接五篇公开论文的官方摘要页，采用简短中文归纳，没有复制论文全文、图片或附件。论文作者、标题、版本及实际核对范围见 [示例](examples/rag-literature-walkthrough.md)。模型推断、候选问题与作者报告分别标注。

本轮未为新增整理材料指定额外统一许可证；原作者署名和许可保持原状。

实际运行记录另保存必要的公开文献元数据、简短中文综合和自建测试输入。原脚本有的在原位运行，有的在受控临时副本执行，字节与原清单一致。没有把临时依赖包、全文、用户知识库或凭据复制到本模块。执行范围见 [运行报告](runtime-tests/2026-10-22/README.md)。

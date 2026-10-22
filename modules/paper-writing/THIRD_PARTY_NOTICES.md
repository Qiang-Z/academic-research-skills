# 来源、许可与复用边界

[模块首页](README.md) · [来源清单](SOURCE_MANIFEST.json)

本模块通过相对路径引用既有快照，不复制源码、不更新版本，也不以统一许可证替代原许可。

| 来源 | 固定分支与提交 | 引用范围 | 许可 |
|---|---|---|---|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | main · `26b95cfa0d8747078e9e43b42e20952709e561b8` | paper-plan、paper-write、paper-claim-audit 及快照内 Codex 适配，共 6 个入口 | [MIT](../idea-discovery/01_ARIS/upstream/LICENSE) |
| [ClaudeScholar](https://github.com/Galaxy-Dawn/claude-scholar) | main · `903787345d6aec134086afa2b97715a78fbde519` | ml-paper-writing、nature-writing、nature-polishing，共 3 个入口 | [MIT](../idea-discovery/05_ClaudeScholar/upstream_main/LICENSE) |
| [ClaudeScholar](https://github.com/Galaxy-Dawn/claude-scholar) | codex · `b672e80951a2348dd6136316d096603bf2dc5b83` | 同名 3 个入口，独立保留分支 | [MIT](../idea-discovery/05_ClaudeScholar/upstream_codex/LICENSE) |

清单以本目录为路径基准，保留 **12 个核心入口 + 3 份根许可证 = 15 个固定文件引用**。`bundle_relative_path`、`reused_from_manifest` 和 `reused_source_id` 指向 `../idea-discovery/` 的原快照和来源记录；选定文件记录直接保留原摘要和元数据。采集日期仍为 2026-10-11，本模块整理日期为 2026-10-22。

配套写作参考、模板、脚本及原作者署名留在原路径，由 [完整来源清单](../idea-discovery/SOURCE_MANIFEST.json) 覆盖。子目录和材料的独立许可声明仍有效；模块根许可证不能覆盖第三方参考中的独立权利。更完整的来源边界见 [原模块第三方说明](../idea-discovery/THIRD_PARTY_NOTICES.md)。

中文导览、空白工作模板、合成数据教学稿和英文修改对照为本次外围整理。它们基于本仓库原创实验与分析例子，不复制第三方论文正文、数据集、图片或作者贡献；教学稿没有虚构外部引用。上游写作参考中的兼容性问题在外围说明，未改写快照。

本轮未为新增整理材料指定额外统一许可证。文档中的外部服务、引用 API 或编译工具不因收录而可用，未执行上游工作流。

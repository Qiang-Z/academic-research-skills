# 来源、许可与复用边界

[模块首页](README.md) · [来源清单](SOURCE_MANIFEST.json)

本模块的第三方内容来自以下既有快照。技能、辅助规则与本仓库新编教学材料分别注明，不以统一许可证替代上游许可。

| 来源 | 固定分支与提交 | 本模块引用范围 | 原许可证 |
|---|---|---|---|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | main · `26b95cfa0d8747078e9e43b42e20952709e561b8` | 6 个核心技能及快照内 Codex 适配；可选 monitor-experiment 的两个入口 | [MIT](../idea-discovery/01_ARIS/upstream/LICENSE) |
| [ClaudeScholar](https://github.com/Galaxy-Dawn/claude-scholar) | main · `903787345d6aec134086afa2b97715a78fbde519` | `rules/experiment-reproducibility.md` 辅助规则；不是独立技能 | [MIT](../idea-discovery/05_ClaudeScholar/upstream_main/LICENSE) |

主版本与 Codex 适配分别导航，未互相覆盖。ClaudeScholar 已保存的 codex 快照中没有同名复现规则，本模块不为它创建推定入口，也不将其计入来源快照数。

## 清单与依赖

来源采集日期仍为 2026-10-11，本模块整理日期为 2026-10-22。`SOURCE_MANIFEST.json` 以本目录为路径基准，通过 `bundle_relative_path`、`reused_from_manifest` 和 `reused_source_id` 指向 `../idea-discovery/` 下的原始快照和清单。

初始清单保留 **12 个核心入口 + 2 个可选监控入口 + 1 个辅助规则 + 2 个根许可证 = 17 个文件引用**；本轮另登记组件执行和监控盘点涉及的辅助文件，具体数量及原始摘要以来源清单为准。它不是独立运行依赖清单；其他共享参考、工具、脚本及文件仍位于原快照，并由 [原始完整来源清单](../idea-discovery/SOURCE_MANIFEST.json) 覆盖。上游文档中的外部审阅服务、SSH、GPU 或队列依赖不因收录而可用。

所有原作者署名、上游许可证及子目录独立声明保持不变，另见 [原模块第三方说明](../idea-discovery/THIRD_PARTY_NOTICES.md)。上游原始字节保持不变；本轮已执行原始队列组件，具体成功、失败与未测范围见 [运行验证阶段快照](runtime-tests/2026-10-22/README.md)。

## 原创教学材料

中文导览、空白模板及 [CPU 教学示例](examples/README.md) 为本次外围整理。示例使用自行生成的合成数据和新编标准库代码，没有复制第三方数据、模型权重或论文结果，也不声称复现任何具体论文。示例测试与上游运行验证分开记录。

本轮未为新增整理材料指定额外统一许可证；第三方内容继续适用各自原许可。

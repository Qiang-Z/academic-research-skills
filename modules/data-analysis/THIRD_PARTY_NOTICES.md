# 来源、许可与复用边界

[模块首页](README.md) · [来源清单](SOURCE_MANIFEST.json)

本模块引用以下已保存快照；不复制源码、不更新版本、不以统一许可证覆盖各原作者许可。

| 来源 | 固定分支与提交 | 本模块引用范围 | 原许可证 |
|---|---|---|---|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | main · `26b95cfa0d8747078e9e43b42e20952709e561b8` | analyze-results、result-to-claim 及快照内 Codex 适配，共 4 个入口 | [MIT](../idea-discovery/01_ARIS/upstream/LICENSE) |
| [K-Dense](https://github.com/K-Dense-AI/scientific-agent-skills) | main · `92ace75ac21efe19a620434e0ca4e356081fe807` | scientific-critical-thinking，共 1 个入口 | [MIT](../idea-discovery/04_KDense/upstream/LICENSE.md) |
| [ClaudeScholar](https://github.com/Galaxy-Dawn/claude-scholar) | main · `903787345d6aec134086afa2b97715a78fbde519` | results-analysis、results-report，共 2 个入口 | [MIT](../idea-discovery/05_ClaudeScholar/upstream_main/LICENSE) |
| [ClaudeScholar](https://github.com/Galaxy-Dawn/claude-scholar) | codex · `b672e80951a2348dd6136316d096603bf2dc5b83` | 同名分析和报告技能，共 2 个入口 | [MIT](../idea-discovery/05_ClaudeScholar/upstream_codex/LICENSE) |

## 清单与依赖

来源采集日期仍为 2026-10-11，本模块整理日期为 2026-10-22。`SOURCE_MANIFEST.json` 以本目录为路径基准，通过 `bundle_relative_path`、`reused_from_manifest` 和 `reused_source_id` 指向原快照和清单。3 个项目的 4 份快照对应 **9 个核心入口 + 4 个根许可证 = 13 个固定文件引用**，不是新增的独立上游文件。

技能内部引用的统计参考、脚本、共享配置仍保留原路径，并由 [原始完整来源清单](../idea-discovery/SOURCE_MANIFEST.json) 覆盖。此处选定文件清单不是可独立安装的运行依赖清单；文档提及的外部统计包、兄弟技能或审阅服务不因此可用。

保留原署名、许可和分支差异；更完整的收录边界见 [原模块第三方说明](../idea-discovery/THIRD_PARTY_NOTICES.md)。上游统计参考中的简化表述通过外围中文说明提示适用限制，没有改写快照文件。

## 原创教学材料

中文导览、空白模板和 [配对分析示例](examples/README.md) 是本次外围整理。示例使用新编标准库代码，读取 [实验模块原创示例](../experiment-design/examples/README.md) 生成的合成数据与预测，不复制第三方数据集、模型权重或研究结果。NIST、SciPy 等官方资料通过链接注明来源，仅用于说明方法与假设。

示例测试与上游技能运行验证分别记录。本轮未为新增整理材料指定额外统一许可证；第三方内容继续适用各自原许可。

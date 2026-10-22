# 第三方来源与许可

本仓库是学术技能的整理和导航合集，不冒充第三方原创，也不以一个总库许可证替代各上游许可。

当前来源均位于 [创新点探索模块](modules/idea-discovery/README.md)。各来源的许可证、子目录独立声明和收录边界见 [模块第三方说明](modules/idea-discovery/THIRD_PARTY_NOTICES.md)；固定提交、原始路径和摘要见 [SOURCE_MANIFEST.json](modules/idea-discovery/SOURCE_MANIFEST.json)。

2026-10-22 新增的 [文献检索与综述模块](modules/literature-review/README.md) 引用上述既有快照，未引入新的上游版本或重新授权。其 4 个来源项目、分支与许可链接见 [文献模块第三方说明](modules/literature-review/THIRD_PARTY_NOTICES.md)，所选入口的固定来源见 [文献模块来源清单](modules/literature-review/SOURCE_MANIFEST.json)。教学示例仅链接公开论文并作简短归纳，没有收录论文全文或图稿。

同日后续文献运行测试将实际执行/导入的原始辅助文件加入模块引用登记，仍保持原始字节；测试报告、公开元数据及合成输入另存。临时安装的 requests、arxiv 等依赖没有随仓库分发；各脚本的运行状态和依赖版本见模块实测报告。

同日新增的 [实验设计与复现模块](modules/experiment-design/README.md) 复用 ARIS 和 ClaudeScholar main，固定来源、辅助规则及许可见 [实验模块第三方说明](modules/experiment-design/THIRD_PARTY_NOTICES.md)。其中 CPU 教学代码和合成数据生成规则是新编材料，不是第三方论文或数据集的复制。

同日新增的 [数据分析与统计模块](modules/data-analysis/README.md) 复用 ARIS、K-Dense 和 ClaudeScholar main/codex，固定来源与许可见 [分析模块第三方说明](modules/data-analysis/THIRD_PARTY_NOTICES.md)。原创分析代码读取前一模块的合成数据教学产物；统计资料只链接官方说明并作必要归纳，没有复制外部数据集。

后续完成的 [写作模块](modules/paper-writing/THIRD_PARTY_NOTICES.md)、[绘图模块](modules/academic-figures/THIRD_PARTY_NOTICES.md)、[投稿模块](modules/submission-rebuttal/THIRD_PARTY_NOTICES.md) 与 [知识管理模块](modules/research-knowledge/THIRD_PARTY_NOTICES.md) 继续引用既有 ARIS 与 ClaudeScholar 快照。四模块分别固定 15、10、11、11 个文件引用，不新增上游快照。原创图表使用 Matplotlib，依赖只放在临时环境；结构 SVG 由保存的 ARIS 渲染器产生。图稿来源与执行范围已分别注明，不收录字体文件、私有数据或真实审稿记录。

初始整理将原有材料搬入模块目录；文献模块整理时按固定摘要恢复了两份原本缺失文件，后续实验和数据分析模块继续保持上游原始字节。新增的总览、目录登记、维护约定与发布辅助材料不构成对第三方内容的重新授权。本次没有为新整理材料指定额外统一许可证。

实验模块本轮有限测试执行了原始队列组件，监控及审计依赖检查另行记录；已涉及的辅助文件加入模块来源引用。原始快照保持不变，测试产物及本库外围验证入口不替代原许可证。整轮运行验证仍在进行，详见 [阶段快照](modules/experiment-design/runtime-tests/2026-10-22/README.md)。

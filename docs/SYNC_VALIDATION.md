# 当前版本同步前核验

日期：2026-10-22。目标：[Qiang-Z/academic-research-skills](https://github.com/Qiang-Z/academic-research-skills)，默认分支 `main`。同步准备时读取到远程基点为 `05faa0c8c41b5b521e202a2df3fdf12b175fa596`。

本次版本包含八模块整理、文献运行测试，以及 [实验验证的进行中快照](../modules/experiment-design/runtime-tests/2026-10-22/README.md)。实验 CPU 新复跑和真实结果审计尚未完成，完整工作流保持未验证。新增外围验证入口仅做语法检查，不能记作运行通过。

同步通过独立临时 Git 检出目录准备，保留原远程历史。发布范围以 [PUBLISH_FILES.txt](../PUBLISH_FILES.txt) 为准，上游原始文件以固定来源摘要核对；本地同步标记和依赖包不发布。整包核验及本地链接检查在暂存前执行，远程推送结果以本次会话最终核验为准。

同步前实际检查：22 份维护 JSON 解析通过，新增外围 Python 入口语法检查通过，127 份维护 Markdown 中的 995 个本地链接无缺失；本轮实验记录未检出本机用户目录路径。发布范围为 2,199 个文件、2,198 个摘要；原始上游 2,022 个文件及跨模块 125 个引用交由整包验证器逐项核对。

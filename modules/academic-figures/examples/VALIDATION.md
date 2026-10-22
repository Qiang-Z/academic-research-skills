# 绘图示例与单组件验证记录

[示例说明](README.md) · [模块验证](../VALIDATION.md)

日期：2026-10-22。CPython 3.12.10 / Windows；Matplotlib 3.11.2、NumPy 2.5.4。全部运行产物位于临时目录；仓库只保留经过检查的三份展示图，未复制依赖包或字体。完整依赖版本见 requirements.txt。

## 原创数据图

已生成两套实际图，SVG/PDF/PNG、绘图数据和图注五个产物在同环境下字节一致。输入经前序原创验证器核对；9 个测试点独立用有理数算式检查，与三个 seed 的正确数 27/43/22、33/44/26、34/42/27（各除以 48）一致。固定配对差为 100/3 个百分点，区间直接绘制两端点，无跨 seed 池化。

已查看实际 PNG：9 个点、单位、完整条件图例、零参考线与配对区间清晰，无标注裁切或覆盖；配色以点形辅助。未将 Python 的一位小数显示当作原始数值精度。图注保留各 seed 样本数与区间限制。

初轮命令检查包含输入生成、分析生成、两次绘图、拒绝覆盖、拒绝把输出放入输入目录。之后新增图注样本数及验证器，在连续案例的默认/可选路径重新生成、核验和逐字节比较；图表损坏被拒绝，详见 [连续案例验证](../../../examples/research-workflow/VALIDATION.md)。

verify_figures 检查来源、产物摘要、绘图数据与分析一致、SVG 根及 PDF/PNG 格式签名；不能单独验证所有图面数值位置、图注语义或完整渲染兼容性。实际图像和代码另作上述复核。没有重新实施统计检验。

## ARIS 单组件

实际执行的是原位 skills/figure-spec/scripts/figure_renderer.py，未改写源码。已通过教学 JSON validate、两次 render 字节一致；重复节点 ID 与指向未知节点的边被拒绝且未生成输出。组件基础路径仅用标准库，没有使用 preview 选项、外部审阅或 PNG/PDF 转换。

流程图的 4 个节点、3 个箭头、中心坐标与边界经检查；用已有 sharp 将 SVG 转成临时 PNG 并查看，标签未裁切，方向为 data → experiment → analysis → writing。原组件的原始字节摘要记录在模块来源清单；仅这些有限路径得到运行验证，不代表所有输入、完整工作流或跨平台效果。

登记：原创 `example_runtime_tested: true`；上游 `component_runtime_tested: true`、`upstream_code_executed: true`；完整技能 `runtime_tested: false`。未执行 Mermaid CLI、图像服务或外部模型审阅，没有上传或投稿。

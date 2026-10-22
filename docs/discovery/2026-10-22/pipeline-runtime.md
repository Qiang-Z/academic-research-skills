# 入门 pipeline：原创计算主干实跑记录

日期：2026-10-22（Asia/Shanghai）。本次实际执行了仓库现有的原创合成实验、配对分析、绘图及交接核验，随后独立复算指标，并验证损坏输入会被拒绝。新检索证据与本轮短报告由同目录其他材料分别记录；本页不将它们算作运行器自动生成内容。

## 环境与命令

CPython 3.12.10 / Windows；Matplotlib 3.11.2、NumPy 2.5.4。系统默认 Python 没有 Matplotlib，本次通过仅当前进程有效的 `PYTHONPATH` 复用先前准备的隔离绘图依赖。没有新安装依赖或改变全局环境。依赖版本清单见 [requirements.txt](../../../modules/academic-figures/examples/requirements.txt)。其他用户需在自己的环境准备这些依赖，不能直接使用本机临时目录。

在仓库根目录执行下列命令；`python` 指向上述环境，`$RUN_DIR` 表示仓库外一个尚不存在的目录，本次逻辑名为 `ars-starter-pipeline-20261022-1ca876a0`。复跑时另取新目录。

```text
python -B -X utf8 examples/research-workflow/run_workflow.py --output $RUN_DIR
python -B -X utf8 examples/research-workflow/verify_workflow.py --input $RUN_DIR
```

两条命令均退出 0。运行器的 experiment、analysis、figures、figure verification 四步分别完成；核验器检查了数据、阶段来源、图表数据及预写文档版本。未使用 `--include-renderer`，本次没有执行上游组件。实际标准输出见 [运行日志](pipeline-run-log.json)，命令、环境、源文件与全部产物 SHA-256 见 [结构化结果](pipeline-runtime.json)。

## 独立逐样本复算

将本轮 `experiment/runs.json` 中全部预测序列化到临时 CSV，再仅用标准库 `csv` 读回。复算程序没有导入数据生成器、预测函数或分析函数。864 条预测分成 18 组（3 划分 × 3 条件 × 验证/测试），每组样本 ID 唯一且有 48 条；重新计数与原始运行和分析结果逐项一致。准确率列仅作显示，完整精度在 JSON。

| 划分 | 评价集 | 条件 | 正确数/样本数 | 准确率 |
|---|---|---|---:|---:|
| 11 | test | raw_1nn | 27/48 | 0.562500 |
| 11 | validation | raw_1nn | 30/48 | 0.625000 |
| 11 | test | scaled_1nn | 43/48 | 0.895833 |
| 11 | validation | scaled_1nn | 39/48 | 0.812500 |
| 11 | test | scaled_1nn_without_x0 | 22/48 | 0.458333 |
| 11 | validation | scaled_1nn_without_x0 | 25/48 | 0.520833 |
| 23 | test | raw_1nn | 33/48 | 0.687500 |
| 23 | validation | raw_1nn | 27/48 | 0.562500 |
| 23 | test | scaled_1nn | 44/48 | 0.916667 |
| 23 | validation | scaled_1nn | 41/48 | 0.854167 |
| 23 | test | scaled_1nn_without_x0 | 26/48 | 0.541667 |
| 23 | validation | scaled_1nn_without_x0 | 25/48 | 0.520833 |
| 47 | test | raw_1nn | 34/48 | 0.708333 |
| 47 | validation | raw_1nn | 31/48 | 0.645833 |
| 47 | test | scaled_1nn | 42/48 | 0.875000 |
| 47 | validation | scaled_1nn | 41/48 | 0.854167 |
| 47 | test | scaled_1nn_without_x0 | 27/48 | 0.562500 |
| 47 | validation | scaled_1nn_without_x0 | 25/48 | 0.520833 |

固定 split 11 的测试样本按 ID 配对，真实标签一致；基线错误而变体正确 18 个，基线正确而变体错误 2 个，两者都正确 25 个、都错误 3 个。独立净差为 `(18-2)/48 × 100 = 33.3333` 个百分点，与分析产物一致。复算程序全文及其 SHA-256 保存在结构化结果的 `independent_recount` 中，CSV 仅作本轮临时中间文件，未收录。

[实际分析产物](pipeline-analysis.json) 同时保留全部 18 行、48 个配对样本、5,000 次重采样的分布计数及限制。其 95% percentile 区间为 `[18.7500, 47.9167]` 个百分点；此区间由现有分析器产生、既有验证器复核，本次独立 CSV 复算没有重新实现区间算法。

## 损坏输入是否会被发现

仅复制本轮 `experiment/` 到新的临时目录，然后翻转 seed 11、`raw_1nn` 测试集第一条记录的预测。原始产物未修改。用下列命令检查副本：

```text
python -B -X utf8 modules/experiment-design/examples/toy-reproducibility/verify_demo.py $TAMPERED_COPY
```

| 输入 | 实际退出码 | 实际错误 | 判断 |
|---|---:|---|---|
| 改一条预测，保留原摘要 | 1 | `Artifact hash mismatch: runs.json` | 按预期拒绝字节变化 |
| 同一损坏副本，仅更新该副本的 runs.json 摘要 | 1 | `Prediction differs from recorded method` | 越过摘要检查后，仍按预期拒绝错误预测 |

第二项专门检查语义校验，并非修复真实产物。前后逐个比较真实运行目录所有文件 SHA-256，完全相同。具体改动位置、前后值、命令及失败日志均在结构化结果。

## 验证结论与边界

通过的是本次环境下的原创计算主干、逐样本计数交接与两个负例。运行器只为既有写作、模拟回复和知识库教学文档登记摘要，没有自动写论文、产生外部审稿或完成真实投稿。图片视觉检查另行记录，产物核验本身不能替代看图。

案例为已有结果之后的合成教学复跑，不能称预注册、查新贡献或真实论文复现。三个划分共享同一数据，不是独立研究；区间只条件于固定 split 11 与拟合模型，并依赖测试观察 IID 假设，不涵盖训练、选模或跨划分不确定性。CSV 独立复算证明记录计数对应，不能独立证明最近邻实现、统计方法或科学结论正确。完整上游工作流状态仍为 `runtime_tested: false`。

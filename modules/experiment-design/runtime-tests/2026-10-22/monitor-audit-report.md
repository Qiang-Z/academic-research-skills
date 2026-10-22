# training-check、monitor-experiment 与 experiment-audit 限定验证

日期：2026-10-22（Asia/Shanghai）。上游：ARIS 固定快照 `26b95cfa0d8747078e9e43b42e20952709e561b8`。

本记录完成了 **5 个合成日志的单轮宿主判断、1 个本地结果快照的读取比较**。直接相关的 `save_trace.sh` 实际启动被缺少 Bash 阻断。这里没有给实验完整性审计签发 PASS，也没有验证完整上游监控或审计流程。CPU 教学复跑产物的 fresh 审阅另行记录。

## 验证层级与入口

| 入口 | 类型 | 本次实际执行 | 结果 |
|---|---|---|---|
| [training-check](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/training-check/SKILL.md) | Markdown 宿主工作流 | 读取新临时目录中的 4 个日志及 1 个不存在的日志路径，再按说明作单轮判断 | 限定演练完成；只有建议 |
| [monitor-experiment](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/monitor-experiment/SKILL.md) | Markdown 宿主工作流 | 读取 1 份合成 JSON，比较两项同配置准确率，保留缺失指标的运行中条目 | 本地快照读取完成 |
| [experiment-audit](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/experiment-audit/SKILL.md) | 需要 fresh reviewer 的语义审计 | 盘点审阅与留痕依赖，检查引用关系 | 此报告未执行真实结果审计；无 verdict |
| [save_trace.sh](../../../idea-discovery/01_ARIS/upstream/tools/save_trace.sh) | Bash 留痕辅助程序 | 在临时工作目录尝试启动原脚本，参数明确标记为合成留痕测试 | 启动失败：`FileNotFoundError / WinError 2`，Bash 未找到 |
| [verify_paper_audits.sh](../../../idea-discovery/01_ARIS/upstream/tools/verify_paper_audits.sh) | 论文审计汇总校验器 | 只读检查 | 不覆盖 `EXPERIMENT_AUDIT.json`，未把它当作实验审计器运行 |
| `review_gate.py` | auto-review-loop 状态转换组件 | 检查用途 | 不作为实验完整性校验器运行 |

没有执行 SSH、W&B API、云平台、通知发送、定时轮询或真实进程停止。没有安装依赖、访问私有数据或修改上游快照。

## 环境和依赖

本次使用 Windows、PowerShell、CPython **3.12.10**。合成输入的生成、读取、JSON 提取和哈希计算只使用 Python 标准库；这些辅助操作不是上游自带的监控分类程序。

| 依赖 | 用途 | 当前情况 |
|---|---|---|
| 支持读文件及推理的 Codex 宿主 | 按 training-check / monitor-experiment 说明解释日志 | 本次可用 |
| 可创建 fresh reviewer 的宿主 | experiment-audit 的独立阅读步骤 | 本报告未调用；需单独记录真实审阅身份和产物 |
| Bash 与 `date/find/wc/tr/cat/mkdir` 等 POSIX 工具 | 原始 save_trace.sh | Bash 不在命令搜索路径，标准 Git 安装位置也未发现 |
| Bash 可调用的 `python3` | save_trace.sh 中的 JSON 与模型族元数据处理 | 未验证；Windows 中发现的是 WindowsApps 命令别名，没有调用该别名 |
| W&B SDK/API、认证、SSH 或云运行后端 | 相应可选在线分支 | 本次未接入或测试 |

留痕脚本的进程没有成功启动，因而没有脚本退出码。外围输入生成脚本退出 0，仅表示它生成并读取输入、捕获了预期的缺文件和缺 Bash 错误，不能解释为留痕成功。

## 单轮日志结果

输入由本次验证作者构造，不是 CPU 教学脚本的训练日志，也不是真实训练观测。实际文件读取内容、SHA-256、时间、精确命令与宿主判断保存在 [monitor-audit-results.json](monitor-audit-results.json)。

| 场景 | 实际读到的证据 | 宿主建议 | 解释 |
|---|---|---|---|
| healthy | loss：0.82 → 0.61 → 0.44；accuracy：0.68 → 0.72 → 0.76；梯度范数有限且下降 | CONTINUE | 当前三条记录方向正常 |
| transient_noise | 第二条 loss 升至 0.89、accuracy 降至 0.66；第三条恢复为 0.59 / 0.72 | CONTINUE | 普通短暂波动不构成明确失败 |
| nan_failure | 连续两条 `train_loss=nan`、`grad_norm=nan` | STOP | 明确数值失败；仅建议 |
| inf_failure | 连续两条 `train_loss=inf`、`grad_norm=inf` | STOP | 明确数值失败；仅建议 |
| unreachable | 读取不存在的 `missing.log` 得到 FileNotFoundError，且本次没有接入 W&B | WAIT | 缺少观测，不能据此认定训练失败 |

每条结果都记录了数据来源、证据、理由、`action_taken=recommendation_only` 和 `next_check=null`。这次测试没有真实训练进程，故未测试 STOP 的实际执行、停止范围或停止命令安全性；也没有等待下一轮或创建调度。

这些结果属于 **一次宿主按说明执行的演练**。上游没有为这些输入提供独立自动分类器；它们不是该分类器的单元测试，也不能证明未来所有日志、噪声水平、训练阶段或平台都会得到正确判断。

## 本地结果快照

从实际写入并重新读取的 JSON 提取：

| 条目 | accuracy | 相对 baseline | 状态 |
|---|---:|---:|---|
| baseline | 0.70 | 0 | 可读 |
| current | 0.76 | +0.06（6 个百分点） | 可读 |
| pending | 未提供 | 无法计算 | running |

两项可比较记录均声明 `dataset=synthetic`、`split=test`、`config=toy-v1`、`evaluation_type=simulation_only`。这里仅检查声明字段一致并计算差值，未证明真实数据或运行来源，也未计算显著性。缺失指标保留为 null，没有填成 0、伪造完成或推断提升。

## 问题和使用边界

1. **缺少 Bash 阻断原始留痕脚本。** 本次没有安装替代品。真正调用 reviewer 后，应按 [review-tracing.md](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/shared-references/review-tracing.md) 和 [integration-contract.md](../../../idea-discovery/01_ARIS/upstream/skills/skills-codex/shared-references/integration-contract.md) 的 Policy C 直接写规范留痕，不能把缺少辅助程序解释为可以跳过。此处属于信息收集及监控演练，没有 reviewer 调用，因此未伪造审阅 trace。
2. **留痕元数据存在静态约定差异。** review-tracing 例子含 `review_independence`、`acceptance_status`；本次检查的 save_trace.sh 输出的是 `family_relation`、`independence_verified` 等字段。脚本未能运行；此项是源文件检查结果，不是已复现的运行异常。审计产物或宿主适配应显式保留审阅独立性与 provisional/accepted 状态，不能默认字段完全一致。
3. **实验审计不是论文审计校验器的同义入口。** verify_paper_audits.sh 的四类必需文件是 PROOF_AUDIT、PAPER_CLAIM_AUDIT、CITATION_AUDIT 和 KILL_ARGUMENT；其通过不能证明实验审计通过。未发现本入口直接引用、覆盖 A–F 科研检查的确定性实验审计程序。
4. **版本专属审阅保证需要明确。** 通用 experiment-integrity 引用要求不同模型族；当前 Codex experiment-audit 的基础路径明确是 fresh agent、same-family、provisional。应保留当前变体的 provisional 限制，不能标成 cross-family accepted。
5. **停止建议、可选联网和完整周期仍未验证。** 真实使用时先明确目标运行、日志/指标来源、基线与停止授权，再按实际证据作判断。本次只证明本地输入能被读取并形成一次有证据的建议。

## 复现和证据

[结果 JSON](monitor-audit-results.json) 的 `fixture_creation_and_probe_command.command` 保存完整 PowerShell 命令，内含传给 Python 的原始脚本；`trace_helper_attempt.command` 保存实际尝试启动的 argv。重跑会创建新的临时目录，写入合成日志并捕获缺 Bash 的启动错误。测试没有在上游目录产生输出。

结果 JSON 还保存全部输入行、比较 JSON 内容、各自 SHA-256、9 个相关源文件的仓库相对路径与 SHA-256。本机路径已规范化为 `<REPO>`、`<TEMP>` 和 `<PYTHON>`；保存的启动 argv 保持原参数结构，使用这些占位符代替本机绝对路径。哈希在此次探测后采集，用于精确定位版本；仓库范围的前后完整性校验由本轮总报告记录，不能把这组事后哈希单独当作前后未改动证明。

此次执行前另对原创教学示例的 [run_demo.py](../../examples/toy-reproducibility/run_demo.py)、[verify_demo.py](../../examples/toy-reproducibility/verify_demo.py) 与 [protocol.json](../../examples/toy-reproducibility/protocol.json) 做了只读风险审查：仅标准库、无网络或子进程、只写新输出目录，固定 240 个合成样本和 3 seeds × 3 个 1-NN 条件。验证器复用生成器与预测函数，属于一致性重算，不是完全独立算法验证；实际复跑和 fresh 审计结论须看相应独立记录。

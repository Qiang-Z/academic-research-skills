# 外部组件小测：Research Hound 的主张—证据结构审计

[返回候选检索](candidate-search.md) · [完整输入与原始输出](component-probe.json)

测试日期：2026-10-22。结论：这个组件能帮助发现证据编号断链和未登记的数字句，依赖很轻；**它不能证明正文数字与登记值一致，也不能证明所有结论都有依据**。因此适合作为流程末尾的一项辅助检查，不能用它的 `pass` 代替研究判断或引用核验。

## 来源与复现范围

- 项目：[AlveeeRahman/research-hound](https://github.com/AlveeeRahman/research-hound)。本次通过官方 GitHub 页面及 GitHub API 核对仓库、树与版本。
- 固定提交：`abf4bb77bfa9935977d7ed6ee6e277623a21ad2d`；[技能入口](https://github.com/AlveeeRahman/research-hound/blob/abf4bb77bfa9935977d7ed6ee6e277623a21ad2d/SKILL.md) 的版本为 `1.2.0`。
- 许可：[MIT LICENSE](https://github.com/AlveeeRahman/research-hound/blob/abf4bb77bfa9935977d7ed6ee6e277623a21ad2d/LICENSE)，保留了 MrPirate 与 K-Dense AI 的版权声明。
- 被测文件：[scripts/writing/audit_claims.py](https://github.com/AlveeeRahman/research-hound/blob/abf4bb77bfa9935977d7ed6ee6e277623a21ad2d/scripts/writing/audit_claims.py)，并读取 `scripts/writing/_common.py`、`scripts/_shared/safe_io.py` 两个共享依赖。
- 环境：Windows、CPython 3.12.10，只使用 Python 标准库；未安装包、未修改宿主配置。

执行前已完整阅读三个程序文件。被测入口读取指定 Markdown、CSV、JSON 文件并向标准输出写 JSON；本次运行没有网络调用。为核对使用契约，还阅读了技能入口、证据流程、两个模板和许可说明。下载使用固定提交的 `raw.githubusercontent.com` 地址，执行文件保持原样，仅位于临时目录，没有加入本库的上游快照或个人技能目录。九个取得文件的 SHA-256 均记录在 JSON 中。

本次的所有稿件和数字都是**原创测试夹具**，不是论文结果。输入中的 `verified` 与 `source_opened: true` 仅用于测试程序要求的状态分支；JSON 明确标明 `fixture_only: true`、`human_verification_performed: false`，并未冒充任何真人读过来源。上游[证据流程](https://github.com/AlveeeRahman/research-hound/blob/abf4bb77bfa9935977d7ed6ee6e277623a21ad2d/references/writing/evidence_workflow.md) 要求真实使用时由负责的人打开来源并记录核验，不能把本次合成状态移植到真实稿件。

## 五个实际输入及输出

基础句子是一个教学夹具：“In this authored fixture, 43 of 48 synthetic predictions were correct.” 登记表保存这句话的 SHA-256，主张编号为 `C001`，来源编号为 `E001`。测试分别启动独立 Python 进程；每次均检查返回码和完整 JSON 内容。

| 用例 | 修改的输入 | 真实返回 | 判断 |
|---|---|---|---|
| `valid_registered_claim` | 主张编号、来源编号和登记表均匹配 | exit 0；`pass`；0 errors、0 warnings | 正确结构可通过；不是科学结论认证 |
| `unknown_evidence` | 正文与登记表都改用不存在的 `E999` | exit 1；`UNKNOWN_CITATION_MARKER`、`UNKNOWN_CLAIM_EVIDENCE` | 成功识别证据编号断链 |
| `untagged_numeric` | 数字句删除全部主张/证据标记 | exit 1；`UNTAGGED_NUMERIC_CONTENT`，另有未使用主张警告 | 成功识别本例未登记数字句 |
| `changed_number_same_hash` | 正文把 `43 of 48` 改成 `48 of 48`，登记哈希仍是原句 | exit 0；`pass`；0 issues | **未检出正文与登记哈希不一致** |
| `unregistered_nonnumeric_claim` | 追加未标记的 “The method works better on every real task.” | exit 0；`pass`；0 issues | **未检出无数字的普遍性结论** |

上述最后两项是有意构造的漏检反例，不能计作完整性审计成功。源代码只验证 `claim_text_sha256` 是否为 64 位十六进制字符串，没有重新计算正文片段的哈希；未登记句子的启发式检查以数字模式为触发条件。这与实际输出一致。程序也没有读取来源原文、重新计算实验结果或判断一条证据是否支持结论。

## 如何复跑

先把固定提交的三个运行文件按原目录结构放到一个单独目录：

```text
scripts/
  writing/audit_claims.py
  writing/_common.py
  _shared/safe_io.py
```

从本页 JSON 取每个用例的 `input_manuscript` 写入 UTF-8 `manuscript.md`，用 `claim_registry_row` 的键作 CSV 列名、值作唯一一行，取顶层 `source_manifest_fixture` 写入 `sources.json`。运行：

```text
python -B scripts/writing/audit_claims.py manuscript.md claims.csv sources.json
```

Windows 的本次等价命令为 `py -3.12 -B scripts/writing/audit_claims.py manuscript.md claims.csv sources.json`；需从上述临时目录执行，或改用文件绝对路径。不得把未下载的脚本路径直接当成本库可运行命令。JSON 保存了全部五组具体输入、返回码、标准错误和解析后的标准输出，复跑时应对照具体问题代码，而不只看退出状态。

## 对本库 pipeline 的取舍

可以提取其“来源编号 → 主张编号 → 同行可检查的定位”方法，给每条最终结论保留输入、数字、单位和适用范围；本库已有证据表可继续使用，不必强迫新手填写一套新表格。若选择接入该组件，应明确称为**结构检查**。

正文数字还须与本次运行产物逐项核对，编辑后须重新绑定确切文本；“所有任务均有效”等没有数字的外推，仍需人工或宿主逐句检查。建议保留本页的两个漏检用例作为提醒，不能把结构审计绿色结果包装为论文正确。

没有测试完整 Research Hound 工作流、联网 DOI 解析、全文检索、其他 CLI、真实稿件、真实人工验证、其他系统或不同 Python 版本。本次没有把这个外部项目收录为第六份来源项目，也没有改变已有模块的完整运行状态。

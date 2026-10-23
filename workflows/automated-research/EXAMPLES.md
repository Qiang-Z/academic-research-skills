# 通用新手入口：三个可复制示例

[开始自己的课题](START_HERE.md) · [六步流程](README.md) · [验证范围](VALIDATION.md)

下面展示材料检查阶段应得到什么。示例命令在仓库根目录的Windows PowerShell中运行，只需要可用的Python 3.12；不会执行研究模型或重新检索论文。助手可以替你运行命令，维护交接文件。

## 1．已有本地阅读笔记与真实公开数据

直接发给助手：

```text
请按 workflows/automated-research/SKILL.md 开始一个自定义研究项目。
研究问题：已知物种是否有助于用企鹅鳍长预测体重？
论文材料：examples/real-penguins/SOURCES.md。这是历史论文阅读笔记，不是论文全文。
数据：examples/real-penguins/data/penguins.csv。
请先用新手入口检查材料，说明已有内容和下一步；不要把历史笔记标成这次阅读全文。
```

自己运行时，可复制整段：

```powershell
$runOut = Join-Path $env:TEMP ('ars-intake-local-' + [guid]::NewGuid().ToString('N'))
py -3.12 -B -X utf8 scripts/start_research.py start --question "已知物种是否有助于用企鹅鳍长预测体重？" --paper "examples/real-penguins/SOURCES.md" --data "examples/real-penguins/data/penguins.csv" --output "$runOut"
if ($LASTEXITCODE -notin @(0, 2)) { throw '检查调用失败，请先处理报错。' }
Get-Content -LiteralPath (Join-Path $runOut 'START_HERE.md') -Encoding UTF8
```

应看到笔记可接收、CSV结构预览，以及阅读和定题的下一步。数据有344条原始观测；检查器保留全部记录，不执行企鹅实验中的筛选或模型。它不会把材料齐全写成六步已完成，也不会根据CSV最后一列猜测研究目标。

这份笔记涉及两篇真实论文，但这里只复用历史记录；需要新阅读时由助手另行读取原文并记录范围。若只是想复跑已经验证的固定企鹅实验，使用[企鹅案例的完整复跑入口](../../examples/real-penguins/README.md)，不必重新设计一个课题。

## 2．只有研究问题，材料还没准备好

直接发给助手：

```text
请按 workflows/automated-research/SKILL.md 帮我开始研究：
同样的肥料会改变不同品种植物的生长吗？
论文暂缺，数据也暂缺。我希望先明确一个适合新手的小问题。
请建立材料检查记录，告诉我先准备什么；不要替我编造数据或实验结果。
```

也可先只登记问题：

```powershell
$runOut = Join-Path $env:TEMP ('ars-intake-question-' + [guid]::NewGuid().ToString('N'))
py -3.12 -B -X utf8 scripts/start_research.py start --question "同样的肥料会改变不同品种植物的生长吗？" --output "$runOut"
if ($LASTEXITCODE -notin @(0, 2)) { throw '检查调用失败，请先处理报错。' }
Get-Content -LiteralPath (Join-Path $runOut 'START_HERE.md') -Encoding UTF8
```

此时预期返回 `2`，但项目已创建。检查页会指出尚缺论文和数据，并让助手先收窄研究范围。接下来可以讨论植物种类、生长指标与可获得的材料，不需要立即购买工具或开展实验。

准备好材料后告诉助手文件位置即可。助手可在同一项目中用 `check --run` 加上实际 `--paper`、`--data` 路径补登记。若已经接受研究协议，或原有材料已改写，则另开新运行保存新版。

## 3．有论文网址与本地数据，尚未获取原文

这两条网址来自既有企鹅案例的来源记录，本页没有重新读取论文：

- [Horst等：Palmer Penguins教学数据论文](https://journal.r-project.org/articles/RJ-2022-020/)
- [Gorman等：原始企鹅研究](https://doi.org/10.1371/journal.pone.0090081)

复制给助手：

```text
请按 workflows/automated-research/SKILL.md 开始我的课题：已知物种是否有助于用企鹅鳍长预测体重？
论文：https://journal.r-project.org/articles/RJ-2022-020/ 和 https://doi.org/10.1371/journal.pone.0090081 。
数据：examples/real-penguins/data/penguins.csv。
先检查材料，再实际读取可获得的论文部分并记录范围；打不开的来源保留失败状态。
```

只运行离线材料检查：

```powershell
$runOut = Join-Path $env:TEMP ('ars-intake-links-' + [guid]::NewGuid().ToString('N'))
py -3.12 -B -X utf8 scripts/start_research.py start --question "已知物种是否有助于用企鹅鳍长预测体重？" --paper "https://journal.r-project.org/articles/RJ-2022-020/" --paper "https://doi.org/10.1371/journal.pone.0090081" --data "examples/real-penguins/data/penguins.csv" --output "$runOut"
if ($LASTEXITCODE -notin @(0, 2)) { throw '检查调用失败，请先处理报错。' }
Get-Content -LiteralPath (Join-Path $runOut 'START_HERE.md') -Encoding UTF8
```

预期返回 `2`：CSV可预览，两个网址标为“已登记、待获取”。这不表示论文不可用，只表示检查器没有联网。助手需另外完成获取和阅读；URL格式正确、标题匹配与论文支持某个句子是不同检查。

数据也只有网址时，用 `--data "公开数据网址"` 登记，同样保持待获取。不要把数据页面存在当成数据已下载或许可已核对。

## 重新检查与依赖提示

在上述同一PowerShell会话中可运行：

```powershell
py -3.12 -B -X utf8 scripts/start_research.py check --run "$runOut"
if ($LASTEXITCODE -notin @(0, 2)) { throw '重查未完成，请阅读报错。' }
```

每次检查都追加历史，并更新项目的中文检查页；不会改写已接受的研究阶段。文件副本与原件发生变化会被提示，不能用修改摘要的方式掩盖。

提供PDF或XLSX后，检查页会说明实际尚未读取的内容，并检查相关解析包的安装元数据。若某项研究代码确实需要特定包，助手可在协议接受前使用 `--require 包名` 或 `--require 包名==确切版本` 登记。这个参数不安装或导入包；包存在、版本满足和功能实测通过要分别记录。

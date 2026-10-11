# 首次公开发布

本次默认目标为 `Qiang-Z/academic-research-skills`。它是学术技能总库，创新点探索在 `modules/idea-discovery/` 下。

交付 ZIP 的外层提供 `publish_to_github.command`，与本仓库目录同级。完整解压后运行该新版脚本；不要再使用旧包中指向单独创新点仓库的脚本。发布脚本不作为上游技能安装。

需要 Git、GitHub CLI 和 shasum；未登录时会通过浏览器授权，并确认当前账号是 Qiang-Z。脚本只上传文件清单中的内容，使用 GitHub noreply 提交邮箱，不写入私人邮箱。

目标不存在时创建 Public 仓库并推送总库目录。已存在但没有任何引用的公开仓库可完成首次提交；已存在且有提交的仓库、私有仓库或归档仓库均停止，不进行覆盖或权限变更。

首次发布完成后的日常维护，使用正常 Git 提交和推送流程；本脚本不负责自动合并更新。同名仓库非空时，不要通过删除仓库或强制推送绕过保护，应先核对已有内容。

本地目录准备和脚本模拟测试不等于远程上传成功。脚本在真实推送后核对提交与 Public 状态才报告成功。

## 官方命令依据

- [GitHub CLI：创建仓库](https://cli.github.com/manual/gh_repo_create)
- [GitHub CLI：浏览器登录](https://cli.github.com/manual/gh_auth_login)
- [GitHub CLI：安装](https://github.com/cli/cli#installation)

此处记录发布方式，不声称目标仓库当前已经存在。

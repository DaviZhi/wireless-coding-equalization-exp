# 无线通信技术作业实时跟踪表

本目录用于在 GitHub 仓库中跟踪学生作业状态，名单来自 `无线通信技术课程名单.pdf`。

## 文件说明

- `students.csv`：课程学生名单。教师需要在 `GitHub用户名` 列补充每位学生的 GitHub 账号。
- `homework_tracking.csv`：作业跟踪表 CSV，字段覆盖是否提交代码、PR 数量、提交次数、最新 PR、评分结果和最近提交时间。
- `HOMEWORK_TRACKING.md`：自动生成的 GitHub Markdown 看板，可同步写入 Actions Summary 和指定 Issue 评论。
- `grading/update_homework_tracking.py`：自动汇总脚本，可读取 GitHub PR、评论中的自动评分结果并生成最新跟踪表。
- `.github/workflows/homework-tracker.yml`：实时跟踪工作流，在 PR 提交/更新、手动触发和定时任务时运行。

## 使用步骤

1. 在 `students.csv` 的 `GitHub用户名` 列填写学生 GitHub 登录名，例如 `octocat`，不要加 `@`。
2. 在 GitHub 仓库中新建一个 Issue，标题建议为“无线通信技术作业实时跟踪表”。
3. 在仓库 `Settings → Secrets and variables → Actions → Variables` 中新增变量：
   - `TRACKING_ISSUE_NUMBER`：上一步 Issue 的编号，例如 `1`。
4. 要求学生的 PR 标题包含姓名或学号，例如 `实验02-张桂嘉-2022040399`。
5. 学生通过 Pull Request 提交作业后，`作业情况实时跟踪` 工作流会自动刷新该 Issue 下的跟踪评论。
6. 教师也可以在 `Actions → 作业情况实时跟踪 → Run workflow` 手动刷新。

## 跟踪字段

| 字段 | 含义 |
| --- | --- |
| 是否提交代码 | 是否已匹配到该学生的 Pull Request |
| PR数量 | 该学生在仓库中创建的 PR 数量 |
| 提交次数 | 最新 PR 的 commit 数，作为代码提交次数统计 |
| 最新PR | 最新一次 PR 的编号与链接 |
| 最新PR状态 | open、closed 或 merged |
| 最新评分 | 从自动评分 PR 评论中解析的 `总分: x/100` |
| 评分状态 | 已评分、未评分或待提交 |
| 最近提交时间 | 最新 PR 更新时间 |

## 匹配规则

自动脚本优先用 `students.csv` 中的 `GitHub用户名` 匹配 PR 作者。如果某位学生暂未填写 GitHub 用户名，脚本会按以下顺序兜底匹配：

1. PR 分支名中的学号，例如 `2024080705-exp2`。
2. PR 标题中的学号，例如 `实验02-2024080705`。
3. PR 标题中的姓名，例如 `实验02-张桂嘉`。

建议教师在发布实验时明确要求学生 PR 标题同时包含姓名和学号，减少同名或误写导致的匹配错误。

## 当前初始化状态

当前跟踪表已按 30 名学生初始化；在填写 GitHub 用户名并推送到 GitHub 后，即可通过 Actions 实时更新。
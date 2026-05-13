# 教师使用说明：信道编码与信道均衡实验

## 1. 实验定位

本实验对应《无线通信技术》第6章“信道编码”和第7章“均衡”。建议安排 2 学时课堂实验，学生课后补充实验报告。

## 2. 课堂安排建议

### 第一阶段：教师讲解与演示（30~45 分钟）

1. 信道编码背景：噪声、误码、冗余与可靠性。
2. Hamming(7,4)：生成矩阵、校验矩阵、伴随式纠错。
3. 均衡背景：多径、ISI、差错平底。
4. ZF 与 LMS：迫零思想、自适应迭代、MSE 曲线。
5. GitHub 流程演示：Fork/Clone/PR/自动评分。

### 第二阶段：学生实现（60~75 分钟）

1. 完成 Hamming 编码与译码。
2. 完成 ZF 和 LMS 均衡。
3. 运行脚本生成结果图。
4. 提交 PR 查看自动评分。

## 3. 发布前检查

```bash
pip install -r requirements.txt
python src/test_environment.py
python -m pytest grading/ -v
python grading/calculate_grade.py
```

还需要创建测试 PR，确认：

- GitHub Actions 成功运行。
- PR 评论正常，或至少 Summary/Artifacts 可见。
- `actions/upload-artifact` 使用 v4。
- 评分脚本没有 `0/1` 解析错误。

## 4. GitHub 仓库设置

远程仓库：<https://github.com/jwentong/wireless-coding-equalization-exp>

建议设置：

- Template repository：开启。
- Actions Workflow permissions：Read and write permissions。
- Allow GitHub Actions to create and approve pull requests：开启。

## 5. 自动评分说明

| 项目 | 分值 |
|---|---:|
| 环境配置 | 5 |
| Part 1 信道编码 | 35 |
| Part 2 信道均衡 | 35 |
| 实验报告 | 15 |
| 代码质量 | -10~+5 |
| 选做加分 | +10 |

最终分数封顶 100 分，最低 0 分。

## 6. 已知风险与处理

- PR 评论失败：查看 Actions Summary 和 Artifacts。
- 旧 workflow 重跑失败：关闭再打开 PR，或让学生 push 新提交。
- 依赖缺失：确认 `requirements.txt` 完整。
- 学生代码雷同：结合报告和现场提问人工复核。

## 7. 课件对应关系

- `course_materials/06章-信道编码-v2.pdf`
  - 线性分组码
  - Hamming 码
  - 卷积码与 Viterbi
- `course_materials/07章-均衡.pdf`
  - ISI
  - ZF 均衡
  - LMS/MMSE 均衡
  - DFE 与 MLSE 简介

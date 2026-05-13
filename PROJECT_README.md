# 项目总览：无线通信技术实验 02

本项目是《无线通信技术》课程第二次实验平台，主题为“信道编码与信道均衡”。

## 实验组织

- Part 1：信道编码
  - Hamming(7,4) 编码
  - 伴随式译码
  - 单比特纠错
  - 编码前后 BER 对比
- Part 2：信道均衡
  - 多径信道与 ISI
  - ZF 均衡
  - LMS 自适应均衡
  - 均衡前后波形/眼图/MSE 对比

## 技术栈

- Python
- NumPy
- SciPy
- Matplotlib
- pytest
- GitHub Actions

## 目录说明

```text
src/          学生代码区
grading/      自动评分脚本
docs/         理论文档
materials/    教师 Word/PPT 授课材料
examples/     示例生成脚本
results/      学生实验输出
course_materials/ 原始课件 PDF
```

## 自动评分

自动评分由 `.github/workflows/grading.yml` 触发，主要检查：

1. Python 环境
2. Part 1 函数正确性与结果图
3. Part 2 函数正确性与结果图
4. 实验报告完整性
5. 代码质量
6. 选做任务

评分结果会写入 PR 评论、Actions Summary 和 Artifacts。

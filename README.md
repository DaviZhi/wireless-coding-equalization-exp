# 无线通信技术实验：信道编码与信道均衡

本实验用于《无线通信技术》课程本周实验课，围绕课件第6章“信道编码”和第7章“均衡”设计。实验分为两个部分，放在同一个 GitHub 仓库中：

- **Part 1：信道编码** —— 实现 Hamming(7,4) 线性分组码，理解冗余、伴随式、单比特纠错；选做卷积码与 Viterbi 硬判决译码。
- **Part 2：信道均衡** —— 实现迫零 ZF 均衡和 LMS 自适应均衡，观察多径信道下 ISI 的抑制效果。

远程仓库：<https://github.com/jwentong/wireless-coding-equalization-exp>

---

## 实验目标

1. 理解信道编码通过冗余提升可靠性的基本思想。
2. 掌握 Hamming(7,4) 编码、伴随式检测与单比特纠错。
3. 理解多径信道导致的符号间干扰（ISI）。
4. 掌握 ZF 与 LMS 均衡的基本实现流程。
5. 学会使用 GitHub PR 和自动评分系统提交实验。

---

## 评分标准

| 项目 | 分值 | 说明 |
|---|---:|---|
| 环境配置 | 5 | `src/test_environment.py` 通过 |
| Part 1：Hamming(7,4) 信道编码 | 35 | 编码 12 + 伴随式/纠错 13 + 性能图 10 |
| Part 2：信道均衡 | 35 | ZF 12 + LMS 13 + 均衡效果图 10 |
| 实验报告 | 15 | 章节完整、结果图、分析讨论 |
| 代码质量 | -10~+5 | pylint 评分，优秀加分，较差扣分 |
| 选做加分 | +10 | 卷积码/Viterbi 或 BER 对比扩展 |

最终总分限制在 0~100 分。

---

## 快速开始

```bash
pip install -r requirements.txt
python src/test_environment.py
```

完成 Part 1：

```bash
python src/part1_channel_coding.py
```

完成 Part 2：

```bash
python src/part2_equalization.py
```

本地检查评分：

```bash
python grading/calculate_grade.py
```

---

## 需要完成的代码

### Part 1：信道编码

打开 `src/part1_channel_coding.py`，完成：

- `hamming74_encode(bits)`
- `hamming74_syndrome(codewords)`
- `hamming74_decode(received)`

选做：

- `convolutional_encode(bits)`
- `viterbi_decode_hard(received_bits)`

### Part 2：信道均衡

打开 `src/part2_equalization.py`，完成：

- `estimate_zf_equalizer(channel, num_taps)`
- `apply_fir_filter(signal, taps)`
- `lms_equalizer(rx_train, tx_train, num_taps, step_size)`

---

## 实验结果要求

运行脚本后，`results/` 至少应生成：

- `coding_ber_curve.png`
- `equalization_eye_comparison.png`
- `equalization_mse_curve.png`

---

## 提交流程

1. Fork 或使用模板创建自己的仓库。
2. Clone 到本地并安装依赖。
3. 完成 `src/` 中的 TODO。
4. 运行两个实验脚本生成结果图。
5. 根据 `REPORT_TEMPLATE.md` 编写 `REPORT.md`。
6. Commit & Push。
7. 在教师仓库创建 Pull Request。
8. 查看 PR 评论、Actions Summary 和 Artifacts 中的评分结果。

---

## AI 助手使用要求

可以使用 Copilot 或其他 AI 助手辅助理解、编码与调试，但必须：

- 能解释自己提交的每个核心函数。
- 在实验报告中说明 AI 辅助的内容。
- 不要提交未理解、未运行、未验证的代码。

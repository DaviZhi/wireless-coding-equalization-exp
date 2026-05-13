# 无线通信技术实验指导手册

## 实验名称

信道编码与信道均衡综合实验

## 课程与学时

- 课程：无线通信技术
- 学时：2 学时课堂实验 + 课后报告
- 仓库：<https://github.com/jwentong/wireless-coding-equalization-exp>

## 一、实验目标

1. 掌握 Hamming(7,4) 信道编码与伴随式译码。
2. 理解编码冗余、码率和纠错能力之间的关系。
3. 掌握多径信道下 ISI 的形成机制。
4. 实现 ZF 与 LMS 均衡器并比较均衡效果。
5. 熟悉 GitHub PR 自动评分流程。

## 二、实验环境

```bash
pip install -r requirements.txt
python src/test_environment.py
```

要求：

- Python 3.9+
- VS Code
- Git
- GitHub 账号
- 可选：GitHub Copilot

## 三、课前准备

请阅读：

- `course_materials/06章-信道编码-v2.pdf`
- `course_materials/07章-均衡.pdf`
- `docs/theory_channel_coding.md`
- `docs/theory_equalization.md`

## 四、实验任务

### Part 1：信道编码

完成：

- `hamming74_encode(bits)`
- `hamming74_syndrome(codewords)`
- `hamming74_decode(received)`

运行：

```bash
python src/part1_channel_coding.py
```

应生成：

```text
results/coding_ber_curve.png
```

### Part 2：信道均衡

完成：

- `estimate_zf_equalizer(channel, num_taps)`
- `apply_fir_filter(signal, taps)`
- `lms_equalizer(rx_train, tx_train, num_taps, step_size)`

运行：

```bash
python src/part2_equalization.py
```

应生成：

```text
results/equalization_eye_comparison.png
results/equalization_mse_curve.png
```

## 五、评分标准

| 项目 | 分值 |
|---|---:|
| 环境配置 | 5 |
| Part 1 信道编码 | 35 |
| Part 2 信道均衡 | 35 |
| 实验报告 | 15 |
| 代码质量 | -10~+5 |
| 选做任务 | +10 |

## 六、提交方式

```bash
git add .
git commit -m "Complete coding and equalization experiment"
git push origin main
```

然后在 GitHub 创建 Pull Request。

## 七、自动评分查看

评分结果可能出现在：

1. PR 评论
2. Actions Summary
3. Actions Artifacts

如果 PR 评论没有出现，请先查看 Actions Summary，不要重复提交无关代码。

## 八、常见问题

### 1. `ModuleNotFoundError`

运行：

```bash
pip install -r requirements.txt
```

### 2. 结果图没有生成

确认已经运行：

```bash
python src/part1_channel_coding.py
python src/part2_equalization.py
```

### 3. LMS 不收敛

检查：

- 步长是否过大
- 抽头数是否合理
- 训练序列长度是否足够
- 输入向量和期望符号是否对齐

### 4. GitHub Actions 失败

优先查看 Summary 和 Artifacts。不要直接 re-run 旧 workflow，建议 push 新提交或关闭再重新打开 PR。

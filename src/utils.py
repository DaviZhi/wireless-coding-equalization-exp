"""
实验工具函数：随机比特、信道、绘图和 BER 计算。
这些函数已由教师提供，学生通常不需要修改。
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def setup_chinese_font():
    """配置 Matplotlib 中文字体。"""
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False


def ensure_results_dir():
    """确保 results 目录存在。"""
    os.makedirs('results', exist_ok=True)


def generate_bits(num_bits, seed=None):
    """生成随机 0/1 比特。"""
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, num_bits, dtype=int)


def bpsk_modulate(bits):
    """BPSK 映射：0 -> +1, 1 -> -1。"""
    bits = np.asarray(bits, dtype=int)
    return 1.0 - 2.0 * bits


def bpsk_demodulate(symbols):
    """BPSK 硬判决。"""
    return (np.asarray(symbols) < 0).astype(int)


def add_awgn(signal, snr_db, seed=None):
    """添加实 AWGN 噪声。"""
    rng = np.random.default_rng(seed)
    signal = np.asarray(signal, dtype=float)
    power = np.mean(signal ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = power / snr_linear
    noise = rng.normal(0, np.sqrt(noise_power), size=signal.shape)
    return signal + noise


def binary_symmetric_channel(bits, error_probability, seed=None):
    """二元对称信道：以给定概率翻转比特。"""
    rng = np.random.default_rng(seed)
    bits = np.asarray(bits, dtype=int)
    flips = rng.random(bits.shape) < error_probability
    return np.bitwise_xor(bits, flips.astype(int))


def multipath_channel(symbols, channel, noise_std=0.0, seed=None):
    """通过多径 FIR 信道并可选添加噪声。"""
    rng = np.random.default_rng(seed)
    symbols = np.asarray(symbols, dtype=float)
    channel = np.asarray(channel, dtype=float)
    received = np.convolve(symbols, channel, mode='full')[: len(symbols)]
    if noise_std > 0:
        received = received + rng.normal(0, noise_std, size=received.shape)
    return received


def calculate_ber(bits_tx, bits_rx):
    """计算误比特率。"""
    bits_tx = np.asarray(bits_tx, dtype=int)
    bits_rx = np.asarray(bits_rx, dtype=int)
    length = min(len(bits_tx), len(bits_rx))
    if length == 0:
        raise ValueError('比特序列不能为空')
    return float(np.mean(bits_tx[:length] != bits_rx[:length]))


def plot_ber_curve(x_values, curves, title, filename):
    """绘制 BER 曲线。"""
    setup_chinese_font()
    ensure_results_dir()
    plt.figure(figsize=(8, 5))
    for label, values in curves.items():
        plt.semilogy(x_values, values, marker='o', linewidth=2, label=label)
    plt.xlabel('信道误码概率 / SNR')
    plt.ylabel('BER')
    plt.title(title)
    plt.grid(True, which='both', alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename), dpi=300)
    plt.close()


def plot_equalization_results(original, received, equalized, filename):
    """绘制均衡前后波形对比。"""
    setup_chinese_font()
    ensure_results_dir()
    length = min(120, len(original), len(received), len(equalized))
    plt.figure(figsize=(10, 6))
    plt.plot(original[:length], label='发送符号', linewidth=1.5)
    plt.plot(received[:length], label='多径接收', alpha=0.8)
    plt.plot(equalized[:length], label='均衡输出', alpha=0.8)
    plt.xlabel('符号序号')
    plt.ylabel('幅度')
    plt.title('均衡前后波形对比')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename), dpi=300)
    plt.close()


def plot_mse_curve(errors, filename):
    """绘制 LMS 训练误差曲线。"""
    setup_chinese_font()
    ensure_results_dir()
    errors = np.asarray(errors, dtype=float)
    plt.figure(figsize=(8, 5))
    plt.semilogy(np.maximum(errors ** 2, 1e-12), linewidth=1.5)
    plt.xlabel('迭代次数')
    plt.ylabel('瞬时平方误差')
    plt.title('LMS 均衡器训练误差曲线')
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename), dpi=300)
    plt.close()

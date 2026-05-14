"""
Part 1：信道编码实验

学生需要完成 Hamming(7,4) 编码、伴随式计算和单比特纠错译码。
选做内容包括卷积码编码和 Viterbi 硬判决译码。
"""

import numpy as np
from utils import (
    binary_symmetric_channel,
    calculate_ber,
    generate_bits,
    plot_ber_curve,
)

HAMMING_G = np.array([
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
], dtype=int)

HAMMING_H = np.array([
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1],
], dtype=int)


def hamming74_encode(bits):
    """
    Hamming(7,4) 系统码编码。

    参数:
        bits: 一维 0/1 数组，长度必须是 4 的倍数。

    返回:
        encoded: 一维 0/1 编码比特数组，长度为输入的 7/4 倍。

    要求:
        使用课件中的生成矩阵 G，按 GF(2) 进行矩阵乘法。
    """
    bits = np.asarray(bits, dtype=int)
    if bits.ndim != 1:
        raise ValueError('bits 必须是一维数组')
    if len(bits) % 4 != 0:
        raise ValueError('Hamming(7,4) 要求输入长度为 4 的倍数')
    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError('bits 只能包含 0 或 1')

    blocks = bits.reshape(-1, 4)
    encoded = (blocks @ HAMMING_G) % 2
    return encoded.reshape(-1)


def hamming74_syndrome(codewords):
    """
    计算 Hamming(7,4) 码字的伴随式。

    参数:
        codewords: 一维或二维 0/1 数组。若为一维，长度必须是 7 的倍数。

    返回:
        syndromes: 形状为 (N, 3) 的伴随式数组。
    """
    codewords = np.asarray(codewords, dtype=int)
    if codewords.ndim == 1:
        if len(codewords) % 7 != 0:
            raise ValueError('码字长度必须是 7 的倍数')
        codewords = codewords.reshape(-1, 7)
    if codewords.shape[1] != 7:
        raise ValueError('每个 Hamming(7,4) 码字长度必须为 7')

    return (codewords @ HAMMING_H.T) % 2


def hamming74_decode(received):
    """
    Hamming(7,4) 单比特纠错译码。

    参数:
        received: 一维 0/1 接收序列，长度必须是 7 的倍数。

    返回:
        decoded_bits: 纠错后提取出的信息比特序列。

    提示:
        1. 计算每个码字的伴随式。
        2. 若伴随式非零，将其与 H 的各列比较，定位错误比特。
        3. 翻转对应错误位。
        4. 系统码的信息位为前 4 位。
    """
    received = np.asarray(received, dtype=int)
    if received.ndim != 1 or len(received) % 7 != 0:
        raise ValueError('received 必须是一维数组，长度为 7 的倍数')

    corrected = received.reshape(-1, 7).copy()
    syndromes = hamming74_syndrome(corrected)
    for index, syndrome in enumerate(syndromes):
        if np.any(syndrome != 0):
            for position in range(7):
                if np.array_equal(syndrome, HAMMING_H[:, position]):
                    corrected[index, position] ^= 1
                    break
    return corrected[:, :4].reshape(-1)


def _convolutional_outputs_and_next_state(state, input_bit):
    """(2,1,3) 一步：状态为 (u_{n-2}, u_{n-1})，输入 u_n，返回 (c1,c2) 与下一状态编码 0..3。"""
    x0 = state // 2
    x1 = state % 2
    u = int(input_bit) & 1
    c1 = u ^ x1 ^ x0
    c2 = u ^ x0
    next_state = 2 * x1 + u
    return c1, c2, next_state


def convolutional_encode(bits):
    """
    选做：实现 (2,1,3) 卷积码编码，生成多项式为 g1=111, g2=101。

    默认在末尾添加 2 个 0 作为尾比特，使状态回到全零。
    """
    bits = np.asarray(bits, dtype=int)
    if bits.ndim != 1:
        raise ValueError('bits 必须是一维数组')
    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError('bits 只能包含 0 或 1')

    padded = np.concatenate([bits, np.zeros(2, dtype=int)])
    state = 0
    output = []
    for u in padded:
        c1, c2, state = _convolutional_outputs_and_next_state(state, u)
        output.extend([c1, c2])
    return np.asarray(output, dtype=int)


def viterbi_decode_hard(received_bits):
    """
    选做：实现 (2,1,3) 卷积码硬判决 Viterbi 译码。
    """
    received_bits = np.asarray(received_bits, dtype=int)
    if received_bits.ndim != 1:
        raise ValueError('received_bits 必须是一维数组')
    if len(received_bits) % 2 != 0:
        raise ValueError('卷积码接收序列长度必须是 2 的倍数')
    if not np.all((received_bits == 0) | (received_bits == 1)):
        raise ValueError('received_bits 只能包含 0 或 1')

    num_steps = len(received_bits) // 2
    if num_steps == 0:
        return np.zeros(0, dtype=int)

    large = 1e18
    cost = np.full(4, large, dtype=float)
    cost[0] = 0.0
    survivor_prev = np.zeros((num_steps, 4), dtype=int)
    survivor_bit = np.zeros((num_steps, 4), dtype=int)

    for step in range(num_steps):
        r0 = int(received_bits[2 * step])
        r1 = int(received_bits[2 * step + 1])
        new_cost = np.full(4, large, dtype=float)
        for prev_state in range(4):
            path = cost[prev_state]
            if path >= large:
                continue
            x0 = prev_state // 2
            x1 = prev_state % 2
            for u in (0, 1):
                c1 = u ^ x1 ^ x0
                c2 = u ^ x0
                next_state = 2 * x1 + u
                branch = int(r0 != c1) + int(r1 != c2)
                candidate = path + branch
                if candidate < new_cost[next_state]:
                    new_cost[next_state] = candidate
                    survivor_prev[step, next_state] = prev_state
                    survivor_bit[step, next_state] = u
        cost = new_cost

    end_state = int(np.argmin(cost))
    decoded_rev = []
    state = end_state
    for step in range(num_steps - 1, -1, -1):
        decoded_rev.append(int(survivor_bit[step, state]))
        state = int(survivor_prev[step, state])

    with_tail = np.asarray(decoded_rev[::-1], dtype=int)
    if len(with_tail) < 2:
        return with_tail
    return with_tail[:-2]


def run_coding_demo():
    """运行 Part 1 演示并生成 BER 曲线。"""
    print('=' * 60)
    print('Part 1：信道编码实验')
    print('=' * 60)

    error_probabilities = np.array([0.001, 0.003, 0.01, 0.03, 0.06, 0.1])
    uncoded_ber = []
    coded_ber = []

    try:
        bits = generate_bits(4000, seed=2026)
        bits = bits[: len(bits) // 4 * 4]
        encoded = hamming74_encode(bits)

        for index, probability in enumerate(error_probabilities):
            uncoded_rx = binary_symmetric_channel(bits, probability, seed=100 + index)
            encoded_rx = binary_symmetric_channel(encoded, probability, seed=200 + index)
            decoded = hamming74_decode(encoded_rx)
            uncoded_ber.append(calculate_ber(bits, uncoded_rx))
            coded_ber.append(calculate_ber(bits, decoded))

        plot_ber_curve(
            error_probabilities,
            {'未编码': uncoded_ber, 'Hamming(7,4)': coded_ber},
            'Hamming(7,4) 编码前后 BER 对比',
            'coding_ber_curve.png',
        )
        print('✅ 已生成 results/coding_ber_curve.png')
    except NotImplementedError as error:
        print(f'⏸️ 尚未完成核心函数：{error}')
    except Exception as error:
        print(f'❌ Part 1 运行失败：{error}')


if __name__ == '__main__':
    run_coding_demo()

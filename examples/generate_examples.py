"""生成教师示例结果图，不依赖学生 TODO 实现。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
from utils import (  # type: ignore[import-not-found]
    binary_symmetric_channel,
    bpsk_demodulate,
    bpsk_modulate,
    calculate_ber,
    generate_bits,
    multipath_channel,
    plot_ber_curve,
    plot_equalization_results,
    plot_mse_curve,
)

G = np.array([
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
], dtype=int)
H = np.array([
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1],
], dtype=int)


def encode(bits):
    return (bits.reshape(-1, 4) @ G % 2).astype(int).reshape(-1)


def decode(received):
    words = received.reshape(-1, 7).copy()
    syndromes = words @ H.T % 2
    for i, syndrome in enumerate(syndromes):
        for position in range(7):
            if np.array_equal(syndrome, H[:, position]):
                words[i, position] ^= 1
                break
    return words[:, :4].reshape(-1)


def zf(channel, taps):
    rows = len(channel) + taps - 1
    matrix = np.zeros((rows, taps))
    for column in range(taps):
        matrix[column: column + len(channel), column] = channel
    desired = np.zeros(rows)
    desired[len(channel) // 2 + taps // 2] = 1
    return np.linalg.lstsq(matrix, desired, rcond=None)[0]


def apply(signal, taps):
    return np.convolve(signal, taps, mode='full')[: len(signal)]


def lms(rx, tx, taps=7, mu=0.01):
    weights = np.zeros(taps)
    weights[taps // 2] = 1
    padded = np.pad(rx, (taps - 1, 0))
    errors = []
    for n in range(len(tx)):
        vector = padded[n:n + taps][::-1]
        y = float(np.dot(weights, vector))
        error = tx[n] - y
        weights += mu * error * vector
        errors.append(error)
    return weights, np.array(errors)


def main():
    bits = generate_bits(4000, seed=1)
    bits = bits[: len(bits) // 4 * 4]
    coded = encode(bits)
    probabilities = np.array([0.001, 0.003, 0.01, 0.03, 0.06, 0.1])
    uncoded_ber = []
    coded_ber = []
    for index, probability in enumerate(probabilities):
        uncoded = binary_symmetric_channel(bits, probability, seed=index)
        coded_rx = binary_symmetric_channel(coded, probability, seed=100 + index)
        uncoded_ber.append(calculate_ber(bits, uncoded))
        coded_ber.append(calculate_ber(bits, decode(coded_rx)))
    plot_ber_curve(probabilities, {'未编码': uncoded_ber, 'Hamming(7,4)': coded_ber}, '编码前后BER示例', 'coding_ber_curve.png')

    eq_bits = generate_bits(2000, seed=2)
    symbols = bpsk_modulate(eq_bits)
    channel = np.array([0.9, 0.35, -0.25])
    rx = multipath_channel(symbols, channel, noise_std=0.12, seed=3)
    weights, errors = lms(rx[:800], symbols[:800])
    output = apply(rx, weights)
    print('raw BER', calculate_ber(eq_bits, bpsk_demodulate(rx[: len(eq_bits)])))
    print('eq BER', calculate_ber(eq_bits, bpsk_demodulate(output[: len(eq_bits)])))
    plot_equalization_results(symbols, rx, output, 'equalization_eye_comparison.png')
    plot_mse_curve(errors, 'equalization_mse_curve.png')


if __name__ == '__main__':
    main()

"""Part 1 信道编码自动测试。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from part1_channel_coding import (  # type: ignore[import-not-found]
    HAMMING_H,
    hamming74_decode,
    hamming74_encode,
    hamming74_syndrome,
)


class TestHamming74:
    def test_known_encoding(self):
        bits = np.array([1, 0, 1, 1])
        encoded = hamming74_encode(bits)
        expected = np.array([1, 0, 1, 1, 0, 1, 0])
        np.testing.assert_array_equal(encoded, expected)

    def test_multiple_blocks_length(self):
        bits = np.array([1, 0, 1, 1, 0, 1, 0, 0])
        encoded = hamming74_encode(bits)
        assert len(encoded) == 14

    def test_codewords_have_zero_syndrome(self):
        bits = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1])
        encoded = hamming74_encode(bits)
        syndromes = hamming74_syndrome(encoded)
        assert np.all(syndromes == 0)

    def test_single_error_syndrome_matches_column(self):
        bits = np.array([1, 0, 1, 1])
        encoded = hamming74_encode(bits)
        received = encoded.copy()
        received[2] ^= 1
        syndrome = hamming74_syndrome(received)[0]
        np.testing.assert_array_equal(syndrome, HAMMING_H[:, 2])

    def test_decode_without_error(self):
        bits = np.array([1, 0, 1, 1, 0, 1, 0, 0])
        decoded = hamming74_decode(hamming74_encode(bits))
        np.testing.assert_array_equal(decoded, bits)

    def test_decode_all_single_bit_errors(self):
        bits = np.array([1, 0, 1, 1])
        encoded = hamming74_encode(bits)
        for position in range(7):
            received = encoded.copy()
            received[position] ^= 1
            decoded = hamming74_decode(received)
            np.testing.assert_array_equal(decoded, bits)

    def test_invalid_input_length(self):
        with pytest.raises(ValueError):
            hamming74_encode(np.array([1, 0, 1]))
        with pytest.raises(ValueError):
            hamming74_decode(np.array([1, 0, 1]))


def test_coding_result_file_exists():
    path = os.path.join('results', 'coding_ber_curve.png')
    if not os.path.exists(path):
        pytest.skip('尚未生成 coding_ber_curve.png')
    assert os.path.getsize(path) > 1000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

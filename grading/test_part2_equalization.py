"""Part 2 信道均衡自动测试。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from part2_equalization import apply_fir_filter, estimate_zf_equalizer, lms_equalizer  # type: ignore[import-not-found]
from utils import bpsk_modulate, generate_bits, multipath_channel  # type: ignore[import-not-found]


class TestEqualization:
    def test_apply_fir_filter_identity(self):
        signal = np.array([1.0, -1.0, 2.0, 0.5])
        taps = np.array([1.0])
        filtered = apply_fir_filter(signal, taps)
        np.testing.assert_allclose(filtered, signal)

    def test_apply_fir_filter_matches_convolution(self):
        signal = np.array([1.0, 2.0, 3.0])
        taps = np.array([0.5, 0.5])
        filtered = apply_fir_filter(signal, taps)
        expected = np.convolve(signal, taps, mode='full')[: len(signal)]
        np.testing.assert_allclose(filtered, expected)

    def test_zf_equalizer_length(self):
        channel = np.array([0.9, 0.3, -0.2])
        taps = estimate_zf_equalizer(channel, num_taps=7)
        assert len(taps) == 7
        assert np.all(np.isfinite(taps))

    def test_zf_equalizer_reduces_isi_near_center(self):
        channel = np.array([0.9, 0.3, -0.2])
        taps = estimate_zf_equalizer(channel, num_taps=7)
        combined = np.convolve(channel, taps)
        peak_index = int(np.argmax(np.abs(combined)))
        peak = abs(combined[peak_index])
        side_energy = np.sum(combined ** 2) - combined[peak_index] ** 2
        assert peak > 0.7
        assert side_energy < 0.35

    def test_lms_equalizer_shapes(self):
        bits = generate_bits(200, seed=1)
        symbols = bpsk_modulate(bits)
        channel = np.array([0.9, 0.3, -0.2])
        rx = multipath_channel(symbols, channel, noise_std=0.0)
        taps, errors = lms_equalizer(rx, symbols, num_taps=5, step_size=0.01)
        assert len(taps) == 5
        assert len(errors) > 50
        assert np.all(np.isfinite(taps))

    def test_lms_error_decreases_on_training(self):
        bits = generate_bits(600, seed=2)
        symbols = bpsk_modulate(bits)
        channel = np.array([0.9, 0.35, -0.25])
        rx = multipath_channel(symbols, channel, noise_std=0.0)
        _, errors = lms_equalizer(rx, symbols, num_taps=7, step_size=0.01)
        first = np.mean(errors[:100] ** 2)
        last = np.mean(errors[-100:] ** 2)
        assert last < first

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            estimate_zf_equalizer(np.array([]), 3)
        with pytest.raises(ValueError):
            lms_equalizer(np.array([1, 2]), np.array([1]), 3)


def test_equalization_result_files_exist():
    files = ['equalization_eye_comparison.png', 'equalization_mse_curve.png']
    missing = [name for name in files if not os.path.exists(os.path.join('results', name))]
    if missing:
        pytest.skip(f'尚未生成均衡结果图: {missing}')
    for name in files:
        assert os.path.getsize(os.path.join('results', name)) > 1000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

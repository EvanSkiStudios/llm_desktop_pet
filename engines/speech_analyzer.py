import librosa
import numpy as np
from scipy.ndimage import gaussian_filter1d


def extract_amplitude(path):
    y, sr = librosa.load(path)

    frame_length = 2048
    hop_length = 512

    amp = np.array([
        np.max(np.abs(y[i:i+frame_length]))
        for i in range(0, len(y), hop_length)
    ])

    amp = amp / np.max(amp)
    amp = gaussian_filter1d(amp, sigma=2)

    seconds_per_step = hop_length / sr

    return amp, seconds_per_step

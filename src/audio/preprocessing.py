from __future__ import annotations

from typing import Tuple

import librosa
import numpy as np


def load_audio(file_path: str, target_sr: int = 22050) -> Tuple[int, np.ndarray]:
    """Load mono audio from disk and return (sample_rate, samples)."""
    samples, sample_rate = librosa.load(file_path, sr=target_sr, mono=True)
    return sample_rate, samples.astype(np.float32)


def normalize_audio(audio_data: np.ndarray) -> np.ndarray:
    """Peak-normalize waveform to the range [-1, 1]."""
    max_val = float(np.max(np.abs(audio_data))) if audio_data.size else 0.0
    if max_val <= 0:
        return audio_data
    return (audio_data / max_val).astype(np.float32)


def reduce_noise(audio_data: np.ndarray) -> np.ndarray:
    """Apply a lightweight median filter to reduce impulsive noise."""
    if audio_data.size < 5:
        return audio_data

    padded = np.pad(audio_data, (2, 2), mode="edge")
    denoised = np.array(
        [np.median(padded[index : index + 5]) for index in range(audio_data.size)],
        dtype=np.float32,
    )
    return denoised


def preprocess_audio(file_path: str, target_sr: int = 22050) -> Tuple[int, np.ndarray]:
    """Load and preprocess an audio file for downstream pitch tracking."""
    sample_rate, audio_data = load_audio(file_path, target_sr=target_sr)
    audio_data = normalize_audio(audio_data)
    audio_data = reduce_noise(audio_data)
    return sample_rate, audio_data
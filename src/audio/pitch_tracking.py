from __future__ import annotations

from typing import Dict, List

import librosa
import numpy as np

PITCH_CLASS_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def track_pitch(
    audio_data: np.ndarray,
    sr: int = 22050,
    frame_length: int = 2048,
    hop_length: int = 256,
) -> List[float]:
    """Return dominant pitch per frame in Hz."""
    pitches, magnitudes = librosa.piptrack(
        y=audio_data,
        sr=sr,
        n_fft=frame_length,
        hop_length=hop_length,
        fmin=220.0,
        fmax=1400.0,
    )

    pitch_values: List[float] = []
    for frame in range(pitches.shape[1]):
        peak_index = int(np.argmax(magnitudes[:, frame]))
        peak_magnitude = magnitudes[peak_index, frame]
        peak_pitch = pitches[peak_index, frame]
        if peak_magnitude > 0 and peak_pitch > 0:
            pitch_values.append(float(peak_pitch))

    return pitch_values


def pitch_to_class(pitch_hz: float) -> int:
    """Convert frequency in Hz to pitch class (0=C ... 11=B)."""
    midi_number = int(round(librosa.hz_to_midi(pitch_hz)))
    return midi_number % 12


def build_pitch_class_histogram(pitch_values: List[float]) -> np.ndarray:
    """Create a normalized 12-bin pitch-class histogram."""
    histogram = np.zeros(12, dtype=np.float32)
    for pitch in pitch_values:
        if pitch > 0:
            histogram[pitch_to_class(pitch)] += 1

    total = float(np.sum(histogram))
    if total > 0:
        histogram /= total
    return histogram


def identify_scale(pitch_values: List[float]) -> Dict[str, object]:
    """Infer most likely major or natural minor scale from pitch values."""
    from models.scale_classifier import ScaleClassifier

    classifier = ScaleClassifier()
    histogram = build_pitch_class_histogram(pitch_values)
    return classifier.predict(audio_features=histogram)
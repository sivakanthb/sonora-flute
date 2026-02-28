from typing import List

import numpy as np


def _covered_hole_estimate(frame: np.ndarray, bins: int = 6) -> int:
    """Estimate covered holes from darkness in horizontal regions."""
    if frame.ndim == 3:
        gray = np.mean(frame, axis=2)
    else:
        gray = frame

    width = gray.shape[1]
    step = max(1, width // bins)
    covered = 0
    for index in range(bins):
        x0 = index * step
        x1 = width if index == bins - 1 else (index + 1) * step
        segment = gray[:, x0:x1]
        if segment.size == 0:
            continue
        if float(np.mean(segment)) < 0.45:
            covered += 1
    return covered


def _covered_to_pitch_class(covered_count: int) -> int:
    mapping = {
        0: 0,
        1: 2,
        2: 4,
        3: 5,
        4: 7,
        5: 9,
        6: 11,
    }
    return mapping.get(max(0, min(6, covered_count)), 0)


def detect_fingering(frames: List[np.ndarray]) -> np.ndarray:
    """Return a 12-bin pseudo pitch-class histogram from flute fingering video."""
    histogram = np.zeros(12, dtype=np.float32)
    for frame in frames:
        covered = _covered_hole_estimate(frame)
        pitch_class = _covered_to_pitch_class(covered)
        histogram[pitch_class] += 1

    total = float(np.sum(histogram))
    if total > 0:
        histogram /= total
    return histogram
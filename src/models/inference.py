from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from audio.pitch_tracking import build_pitch_class_histogram, track_pitch
from models.scale_classifier import ScaleClassifier


def run_inference(
    model: Optional[ScaleClassifier] = None,
    audio_features: Optional[np.ndarray] = None,
    video_features: Optional[np.ndarray] = None,
) -> Dict[str, object]:
    classifier = model or ScaleClassifier()
    return classifier.predict(audio_features=audio_features, video_features=video_features)


def infer_scale_from_audio(audio_data: np.ndarray, sample_rate: int) -> Dict[str, object]:
    pitch_values = track_pitch(audio_data=audio_data, sr=sample_rate)
    histogram = build_pitch_class_histogram(pitch_values)
    result = run_inference(audio_features=histogram)
    result["pitch_count"] = len(pitch_values)
    return result


def infer_scale_from_video(video_pitch_class_histogram: np.ndarray) -> Dict[str, object]:
    return run_inference(video_features=video_pitch_class_histogram)
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import numpy as np


PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJOR_INTERVALS = [0, 2, 4, 5, 7, 9, 11]
NATURAL_MINOR_INTERVALS = [0, 2, 3, 5, 7, 8, 10]


@dataclass
class ScaleScore:
    name: str
    score: float


class ScaleClassifier:
    def __init__(self) -> None:
        self._trained = False

    def train(self, audio_features, video_features=None, labels=None) -> None:
        self._trained = True

    def _scale_mask(self, root: int, intervals: Iterable[int]) -> np.ndarray:
        mask = np.zeros(12, dtype=np.float32)
        for interval in intervals:
            mask[(root + interval) % 12] = 1.0
        return mask

    def _prepare_histogram(self, features: np.ndarray) -> np.ndarray:
        vector = np.asarray(features, dtype=np.float32).reshape(-1)
        if vector.size != 12:
            raise ValueError("Expected a 12-bin pitch-class feature vector.")

        total = float(np.sum(vector))
        if total <= 0:
            return np.zeros(12, dtype=np.float32)
        return vector / total

    def _score_all_scales(self, histogram: np.ndarray) -> List[ScaleScore]:
        scores: List[ScaleScore] = []
        for root in range(12):
            major_mask = self._scale_mask(root, MAJOR_INTERVALS)
            minor_mask = self._scale_mask(root, NATURAL_MINOR_INTERVALS)

            major_score = float(np.sum(histogram * major_mask))
            minor_score = float(np.sum(histogram * minor_mask))

            scores.append(ScaleScore(name=f"{PITCH_CLASSES[root]} Major", score=major_score))
            scores.append(ScaleScore(name=f"{PITCH_CLASSES[root]} Minor", score=minor_score))

        scores.sort(key=lambda item: item.score, reverse=True)
        return scores

    def predict(self, audio_features, video_features: Optional[np.ndarray] = None) -> Dict[str, object]:
        if audio_features is None and video_features is None:
            raise ValueError("At least one feature source is required.")

        if audio_features is None and video_features is not None:
            audio_features = np.asarray(video_features, dtype=np.float32)

        histogram = self._prepare_histogram(np.asarray(audio_features, dtype=np.float32))
        ranked = self._score_all_scales(histogram)

        if not ranked:
            return {
                "scale": "Unknown",
                "confidence": 0.0,
                "candidates": [],
            }

        best = ranked[0]
        second = ranked[1] if len(ranked) > 1 else ranked[0]
        confidence = max(0.0, min(1.0, best.score - second.score + 0.5))

        return {
            "scale": best.name,
            "confidence": round(confidence, 3),
            "candidates": [
                {"scale": item.name, "score": round(item.score, 3)} for item in ranked[:5]
            ],
        }

    def evaluate(self, test_audio_features, test_video_features=None, test_labels=None):
        if test_labels is None:
            raise ValueError("test_labels are required for evaluation.")

        predictions = [self.predict(features).get("scale") for features in test_audio_features]
        total = len(test_labels)
        if total == 0:
            return {"accuracy": 0.0}

        correct = sum(pred == label for pred, label in zip(predictions, test_labels))
        return {"accuracy": correct / total}
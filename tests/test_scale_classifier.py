import unittest
import numpy as np

from src.models.scale_classifier import ScaleClassifier


class TestScaleClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = ScaleClassifier()

    def test_predict_major_scale(self):
        # C major pitch classes: C D E F G A B
        histogram = np.zeros(12, dtype=np.float32)
        for index in [0, 2, 4, 5, 7, 9, 11]:
            histogram[index] = 1

        result = self.classifier.predict(audio_features=histogram)
        self.assertEqual(result["scale"], "C Major")
        self.assertGreater(result["confidence"], 0.5)

    def test_predict_minor_scale(self):
        # A minor pitch classes: A B C D E F G
        histogram = np.zeros(12, dtype=np.float32)
        for index in [9, 11, 0, 2, 4, 5, 7]:
            histogram[index] = 1

        result = self.classifier.predict(audio_features=histogram)
        self.assertEqual(result["scale"], "A Minor")

    def test_reject_invalid_feature_length(self):
        with self.assertRaises(ValueError):
            self.classifier.predict(audio_features=np.array([1, 2, 3], dtype=np.float32))

if __name__ == '__main__':
    unittest.main()
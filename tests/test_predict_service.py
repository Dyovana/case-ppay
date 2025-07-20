import unittest
from unittest.mock import patch, MagicMock

from src.entities.predict_model import Predict, PredictResponse
from src.services.predict_service import PredictService


class TestPredictService(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_model.feature_names_in_ = ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
        self.mock_model.predict.return_value = [1]  # 1 -> Iris-versicolor

        self.service = PredictService(model=self.mock_model)

    def test_predict(self):
        payload = Predict( # out of order parameters
            PetalWidthCm=0.2,
            SepalLengthCm=4.1,
            PetalLengthCm=1.4,
            SepalWidthCm=3.5,
        )

        response = self.service.predict(payload)

        self.assertIsInstance(response, PredictResponse)
        self.assertEqual(response.category, "Iris-versicolor")

        self.mock_model.predict.assert_called_once_with([[4.1, 3.5, 1.4, 0.2]])

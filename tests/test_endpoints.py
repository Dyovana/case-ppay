import unittest
from unittest.mock import MagicMock

from starlette.testclient import TestClient

from src.controllers.default import get_model
from src.entities.predict_model import PredictResponse, Predict
from src.main import app
from src.services.predict_service import PredictService
from src.services.repository import HistoryService


class TestPredictEndpoint(unittest.TestCase):

    def setUp(self):
        self.mock_service = MagicMock()
        self.mock_service.predict.return_value = PredictResponse(category="Iris-setosa")

        self.mock_db = MagicMock()

        app.dependency_overrides[get_model] = lambda: self.mock_service
        app.dependency_overrides[HistoryService] = lambda: self.mock_db

        self.client = TestClient(app)

    def test_predict_endpoint(self):
        payload = {
            "SepalLengthCm": 5.1,
            "SepalWidthCm": 3.5,
            "PetalLengthCm": 1.4,
            "PetalWidthCm": 0.2
        }

        response = self.client.post("/predict", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"category": "Iris-setosa"})

        self.mock_service.predict.assert_called_once_with(Predict.model_validate(payload))
        self.mock_db.insert_log.assert_called_once_with(
            request=Predict.model_validate(payload),
            result=PredictResponse(category="Iris-setosa")
        )

import unittest
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.entities.predict_model import Predict, PredictResponse
from src.entities.history_model import LogRequestResponse
from src.services.repository import Base, HistoryService, LogRequest


class TestHistoryService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "postgresql://userpicpay@localhost:5433/bdpicpay_test",
            echo=False
        )
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

    def setUp(self):
        self.db = self.SessionLocal()
        self.history_service = HistoryService(db=self.db)

    def tearDown(self):
        self.db.query(LogRequest).delete()
        self.db.commit()
        self.db.close()

    def test_insert_and_get_history(self):

        payload = {
            "SepalLengthCm": 0.0,
            "SepalWidthCm": 1.57,
            "PetalLengthCm": 5,
            "PetalWidthCm": -1.0
        }
        request = Predict.model_validate(payload)

        result = PredictResponse(category="Iris-versicolor")

        self.history_service.insert_log(request=request, result=result)

        history = self.history_service.get_history()

        self.assertEqual(len(history), 1)
        self.assertIsInstance(history[0], LogRequestResponse)
        self.assertEqual(history[0].category, result.category)

    def test_get_history_with_date_filters(self):
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        day_before_yesterday = now - timedelta(days=2)

        payload = {
            "SepalLengthCm": 5.1,
            "SepalWidthCm": 3.5,
            "PetalLengthCm": 1.4,
            "PetalWidthCm": 0.2
        }

        for dt in [yesterday, now, day_before_yesterday]:
            self.history_service.insert_log(
                request=Predict.model_validate(payload),
                result=PredictResponse(
                    category=f"Iris-versicolor"
                ),
                date_time=dt
            )

        filtered = self.history_service.get_history(start_date=day_before_yesterday, end_date=now)
        self.assertEqual(len(filtered), 3)
        self.assertTrue(all(isinstance(item, LogRequestResponse) for item in filtered))
        self.assertTrue(all(day_before_yesterday <= log.created_at <= now for log in filtered))

        filtered = self.history_service.get_history(start_date=yesterday, end_date=now)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(yesterday <= log.created_at <= now for log in filtered))

        filtered_eq_date = self.history_service.get_history(start_date=now)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(log.created_at.date() == now.date() for log in filtered_eq_date))
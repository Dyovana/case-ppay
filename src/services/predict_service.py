from src.config.logging import setup_logger
from src.entities.predict_model import Predict, PredictResponse

logger = setup_logger()


class PredictService:
    classify = {
        0: "Iris-setosa",
        1: "Iris-versicolor",
        2: "Iris-virginica"
    }

    def __init__(self, model):
        self.model = model

    def predict(self, request: Predict) -> PredictResponse:
        try:
            request = request.model_dump(by_alias=True)
            feats = [request[feat] for feat in self.model.feature_names_in_]
            prediction_label = self.model.predict([feats])[0]

            return PredictResponse(
                category=self.classify[prediction_label]
            )
        except KeyError as e:
            raise KeyError(f"Unknown prediction label: {prediction_label} / {e}")

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise

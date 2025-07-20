from pydantic import BaseModel, Field


class Predict(BaseModel):
    sepal_length_cm: float = Field(alias='SepalLengthCm')
    sepal_width_cm: float = Field(alias='SepalWidthCm')
    petal_length_cm: float = Field(alias='PetalLengthCm')
    petal_width_cm: float = Field(alias='PetalWidthCm')

class PredictResponse(BaseModel):
    category: str
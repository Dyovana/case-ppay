from datetime import datetime
from typing import Optional

from fastapi import Depends, Query, APIRouter, Request

from src.config.logging import setup_logger
from src.entities.history_model import LogRequestResponse
from src.entities.predict_model import Predict, PredictResponse
from src.services.predict_service import PredictService
from src.services.repository import HistoryService

logger = setup_logger()
default_router = APIRouter()

def get_model(request: Request) -> PredictService:
    if not hasattr(request.app.state, 'ml_model') or request.app.state.ml_model is None:

        logger.error("Attempt to access the model before it has been loaded!")
        raise RuntimeError("ML model was not loaded at startup. Check the startup logs.")
    return PredictService(model=request.app.state.ml_model)

@default_router.post("/health")
async def health():
    return {"status": "success"}


@default_router.post("/predict")
async def predict(
        body: Predict,
        service: PredictService = Depends(get_model),
        db: HistoryService = Depends()
) -> PredictResponse:
    """Returns the inference for an input"""

    logger.info("Processing prediction request")
    result = service.predict(body)
    db.insert_log(request=body, result=result)

    return result


@default_router.get("/history")
async def get_history(
        start_date: Optional[datetime] = Query(
            None,
            description="start date in the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"),
        end_date: Optional[datetime] = Query(
            None,
            description="end date in the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"),
        db: HistoryService = Depends()
) -> list[LogRequestResponse]:
    """
    Retrieves the complete history, or filtered by date or range.
    """
    logger.info(f"Fetching history logs with filters - start_date: {start_date}, end_date: {end_date}")
    return db.get_history(start_date=start_date, end_date=end_date)

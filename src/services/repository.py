from typing import Optional
from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy import Column, DateTime, Text, JSON, Date, Integer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, Session

from src.config.logging import setup_logger
from src.entities.history_model import LogRequestResponse
from src.entities.predict_model import Predict, PredictResponse
from src.models.history_model import get_session

logger = setup_logger()

Base = declarative_base()


class LogRequest(Base):
    """
    Defines the model for the logs_request table for SQLAlchemy.
    """
    __tablename__ = 'logs_request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    request = Column(JSON)
    category = Column(Text)
    result = Column(JSON)


class HistoryService:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    def insert_log(
            self,
            request: Predict,
            result: PredictResponse,
            date_time: Optional[datetime] = None
    ) -> None:
        """
        Inserts a new log record into the database.
        """
        if date_time is None:
            date_time = datetime.now(timezone.utc)

        log_entry = LogRequest(
            created_at=date_time,
            request=request.model_dump(by_alias=True),
            category=result.category,
            result=result.model_dump()
        )

        try:
            self.db.add(log_entry)
            self.db.commit()
            self.db.refresh(log_entry)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to insert log: {e}")
            raise

    def get_history(
            self,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> list[LogRequestResponse]:
        """
        Retrieves the log history from the database, with optional date filters.
        """
        try:
            query = self.db.query(LogRequest)

            if start_date and end_date:
                query = query.filter(LogRequest.created_at.between(start_date, end_date))
            elif start_date:
                query = query.filter(LogRequest.created_at >= start_date)
            elif end_date:
                query = query.filter(LogRequest.created_at <= end_date)

            query = query.order_by(LogRequest.created_at.desc())

            rows = query.all()
            return [LogRequestResponse.model_validate(row) for row in rows]

        except SQLAlchemyError as e:
            logger.error(f"An error occurred while retrieving the history: {e}")
            raise
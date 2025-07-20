from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogRequestResponse(BaseModel):
    id: int
    created_at: datetime
    request: dict
    category: str
    result: dict

    model_config = ConfigDict(from_attributes=True)
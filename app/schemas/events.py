from typing import Optional

from datetime import datetime

from pydantic import (
    BaseModel,
    PositiveInt,
    Extra,
    NonNegativeInt,
    Field,
)


class EventsCreate(BaseModel):
    author: Optional[NonNegativeInt] = Field(None)
    model: str
    data: str
    type_id: NonNegativeInt

    class Config:
        extra = Extra.forbid


class EventsDB(EventsCreate):
    date: datetime
    id: NonNegativeInt

    class Config:
        orm_mode = True
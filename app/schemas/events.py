from datetime import datetime

from pydantic import (
    BaseModel,
    PositiveInt,
    Extra,
    NonNegativeInt,
)


class EventsCreate(BaseModel):
    author: NonNegativeInt
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
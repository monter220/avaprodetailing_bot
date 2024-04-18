from typing import Optional

from datetime import datetime

from pydantic import (
    BaseModel,
    PositiveInt,
    Extra,
    Field,
)


class EventsCreate(BaseModel):
    author: Optional[PositiveInt] = Field(None)
    model: str
    data: str
    type_id: PositiveInt

    class Config:
        extra = Extra.forbid


class EventsDB(EventsCreate):
    date: datetime
    id: PositiveInt

    class Config:
        orm_mode = True

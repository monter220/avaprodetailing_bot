from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    NonNegativeInt,
    validator,
    Extra,
)


class UserCreate(BaseModel):
    tg_id: Optional[PositiveInt]
    surname: str = Field(min_length=2)
    name: str = Field(min_length=2)
    patronymic: Optional[str]
    date_birth: datetime
    phone: str


class UserDB(UserCreate):
    reg_date: datetime
    # discount_points: NonNegativeInt
    # end_points_date: datetime

    class Config:
        orm_mode = True

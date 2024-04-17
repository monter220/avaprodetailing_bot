from typing import Optional

from pydantic import Field, PositiveInt

from app.core.config import settings
from app.schemas.base_name_descr import BaseNameDescrSchema


class ShortServiceBase(BaseNameDescrSchema):
    cost: Optional[PositiveInt] = None
    default_bonus: Optional[PositiveInt] = Field(
        None,
        max_value=settings.max_bonus_value
    )


class ServiceBase(ShortServiceBase):
    category_id: Optional[PositiveInt] = None


class ServiceCreate(ServiceBase):
    name: str = Field(
        ...,
        min_length=settings.min_name_len,
        max_length=settings.max_name_len
    )
    cost: PositiveInt
    default_bonus: PositiveInt = Field(
        ...,
        max_value=settings.max_bonus_value
    )
    category_id: PositiveInt


class ServiceUpdate(ServiceBase):
    pass


class ServiceDB(ShortServiceBase):
    id: PositiveInt
    category_id: PositiveInt

    class Config:
        orm_mode = True

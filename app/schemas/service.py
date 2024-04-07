from typing import Optional

from pydantic import Field, PositiveInt, field_validator
from pydantic_core.core_schema import ValidationInfo

from app.core.config import settings
from app.schemas.base_name_descr import BaseNameDescrSchema
from app.translate.ru import FIELD_ERROR


class ServiceBase(BaseNameDescrSchema):
    cost: Optional[PositiveInt] = None
    default_bonus: Optional[PositiveInt] = Field(
        None,
        max_value=settings.max_bonus_value
    )
    category_id: Optional[PositiveInt] = None
    point_id: Optional[PositiveInt] = None


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
    point_id: PositiveInt


class ServiceUpdate(ServiceBase):
    @field_validator(
        'name',
        'cost',
        'default_bonus',
        'category_id',
        'point_id',
        mode='before'
    )
    def field_cannot_be_null(cls, value: str, info: ValidationInfo):
        if value is None:
            raise ValueError(FIELD_ERROR.format(info.field_name))
        return value


class ServiceDB(ServiceBase):
    id: int

    class Config:
        orm_mode = True

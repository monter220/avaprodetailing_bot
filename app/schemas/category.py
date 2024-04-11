from typing import Optional

from pydantic import Field, field_validator, PositiveInt
from pydantic_core.core_schema import ValidationInfo

from app.core.config import settings
from app.translate.ru import FIELD_ERROR
from .base_name_descr import BaseNameDescrSchema
from .service import ServiceDB


class CategoryBase(BaseNameDescrSchema):
    point_id: Optional[PositiveInt] = None


class CategoryCreate(BaseNameDescrSchema):
    name: str = Field(
        ...,
        min_length=settings.min_name_len,
        max_length=settings.max_name_len
    )
    point_id: PositiveInt


class CategoryUpdate(CategoryBase):
    @field_validator(
        'name',
        'point_id',
        mode='before'
    )
    def field_cannot_be_null(cls, value: str, info: ValidationInfo):
        if value is None:
            raise ValueError(FIELD_ERROR.format(info.field_name))
        return value


class CategoryBaseDB(BaseNameDescrSchema):
    id: PositiveInt
    point_id: PositiveInt

    class Config:
        orm_mode = True


class CategoryDB(CategoryBaseDB):
    services: list[ServiceDB]

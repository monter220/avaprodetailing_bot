from typing import Optional

from pydantic import Field, PositiveInt

from app.core.config import settings
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
    name: Optional[str] = Field(
        None,
        min_length=settings.min_name_len,
        max_length=settings.max_name_len
    )
    description: Optional[str] = Field(
        None,
        max_length=255
    )


class CategoryBaseDB(BaseNameDescrSchema):
    id: PositiveInt
    point_id: PositiveInt

    class Config:
        orm_mode = True


class CategoryDB(CategoryBaseDB):
    services: list[ServiceDB]

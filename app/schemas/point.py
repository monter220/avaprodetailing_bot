from typing import Optional

from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from app.core.config import settings
from app.schemas.base_name_descr import BaseNameDescrSchema
from app.schemas.service import ServiceCategoryDB
from app.schemas.user import UserDB
from app.translate.ru import FIELD_ERROR


class PointBase(BaseNameDescrSchema):
    address: Optional[str] = Field(
        None,
        min_length=settings.min_address_len,
        max_length=settings.max_address_len
    )


class PointCreate(PointBase):
    name: str = Field(
        ...,
        min_length=settings.min_name_len,
        max_length=settings.max_name_len
    )
    address: str = Field(
        ...,
        min_length=settings.min_address_len,
        max_length=settings.max_address_len
    )


class PointUpdate(PointBase):
    @field_validator('name', 'address', mode='before')
    def field_cannot_be_null(cls, value: str, info: ValidationInfo):
        if value is None:
            raise ValueError(FIELD_ERROR.format(info.field_name))
        return value


class ShortPointDB(PointBase):
    class Config:
        orm_mode = True


class IDShortPointDB(ShortPointDB):
    id: int


class PointDB(ShortPointDB):
    admins: list[UserDB]
    services: list[ServiceCategoryDB]


class FullPointDB(IDShortPointDB, PointDB):
    pass

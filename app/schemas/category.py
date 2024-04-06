from pydantic import Field, field_validator

from app.core.config import settings
from app.schemas.base_name_descr import BaseNameDescrSchema
from app.translate.ru import NAME_ERROR


class CategoryCreate(BaseNameDescrSchema):
    name: str = Field(
        ...,
        min_length=settings.min_name_len,
        max_length=settings.max_name_len
    )


class CategoryUpdate(BaseNameDescrSchema):
    @field_validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(NAME_ERROR)
        return value


class CategoryDB(BaseNameDescrSchema):
    id: int

    class Config:
        orm_mode = True

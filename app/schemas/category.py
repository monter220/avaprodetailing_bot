from pydantic import Field, field_validator

from app.core.config import settings
from app.schemas.base_name_descr import BaseNameDescrSchema
from app.schemas.service import ServicePointDB
from app.translate.ru import FIELD_ERROR


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
            raise ValueError(FIELD_ERROR)
        return value


class BaseCategoryDB(BaseNameDescrSchema):
    class Config:
        orm_mode = True


class ShortCategoryServicesDB(BaseCategoryDB):
    services: list[ServicePointDB]


class CategoryDB(BaseCategoryDB):
    id: int


class CategoryServicesDB(CategoryDB, ShortCategoryServicesDB):
    pass

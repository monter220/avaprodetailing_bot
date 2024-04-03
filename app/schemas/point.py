from typing import Optional, Annotated

from pydantic import BaseModel, Field, Extra, field_validator

from app.core.config import settings
from app.core.constrants import POINT_CREATE_EXAMPLES, POINT_UPDATE_EXAMPLES


class PointBase(BaseModel):
    name: Annotated[
        Optional[str], Field(
            min_length=settings.min_name_len,
            max_length=settings.max_name_len
        )
    ] = None
    description: Annotated[
        Optional[str], Field(
            min_length=settings.min_description_len,
        )
    ] = None
    address: Annotated[
        Optional[str], Field(
            min_length=settings.min_address_len,
            max_length=settings.max_address_len
        )
    ] = None

    class Config:
        extra = Extra.forbid


class PointCreate(PointBase):
    name: Annotated[str, Field(
        min_length=settings.min_name_len,
        max_length=settings.max_name_len
    )]
    address: Annotated[str, Field(
        min_length=settings.min_address_len,
        max_length=settings.max_address_len
    )]

    class Config:
        schema_extra = {
            'examples': POINT_CREATE_EXAMPLES
        }


class PointUpdate(PointBase):
    @field_validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(settings.name_error)
        return value

    @field_validator('address')
    def address_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(settings.address_error)
        return value

    class Config:
        schema_extra = {
            'examples': POINT_UPDATE_EXAMPLES
        }


class PointDB(PointBase):
    id: int

    class Config:
        orm_mode = True

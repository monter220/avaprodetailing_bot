from typing import Optional

from pydantic import BaseModel, Field, Extra

from app.core.config import settings


class BaseNameDescrSchema(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=settings.min_name_len,
        max_length=settings.max_name_len
    )
    description: Optional[str] = None

    class Config:
        extra = Extra.forbid
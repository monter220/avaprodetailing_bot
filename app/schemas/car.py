import json

from typing import Optional
from gosnomer import normalize
from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    NonNegativeInt,
    validator,
    Extra,
    model_validator,
)

from app.core.config import settings


class CarCreate(BaseModel):
    image: Optional[str] = Field(None)
    brand: str
    model: str
    license_plate_number: str
    user_id: int

    @validator('brand')
    def check_alphabet_only(cls, value):
        check = value.replace(' ', '').replace('-', '')
        if check.isalpha():
            return value
        raise ValueError(settings.alphabet_error)

    @validator('license_plate_number')
    def check_license_plate_number(cls, value):
        return normalize(value)

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CarDB(CarCreate):
    
    class Config:
        orm_mode = True

from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    NonNegativeInt,
    validator,
    Extra,
)


class CarCreate(BaseModel):
    brand: str
    model: str
    license_plate_number: Optional[str]
    user_id: int

class CarDB(CarCreate):
    
    class Config:
        orm_mode = True

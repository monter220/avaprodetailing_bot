from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt, validator

from app.schemas.bonus_event import BonusCreate


class OrderCreate(BaseModel):
    cost: PositiveInt
    user_id: int
    author_id: int
    car_id: int
    pay_type: int
    bonus_event: BonusCreate
    services: List[int]

    @validator('services')
    def check_services(cls, value):
        if not value:
            raise ValueError('Нужно добавить минимум 1 услугу')
        return value
    
    @validator('cost')
    def check_positive_int(cls, value):
        if value < 0:
            raise ValueError('cost должно быть положительным числом')
        return value


class OrderUpdate(BaseModel):
    cost: Optional[PositiveInt]
    user_id: Optional[int]
    author_id: Optional[int]
    car_id: Optional[int]
    pay_type: Optional[int]
    bonus_event_id: Optional[int]
    service_ids: Optional[List[int]]

class ReturnOrder(OrderCreate):
    id: int

class OrderDB(BaseModel):
    id: int
    cost: PositiveInt
    user_id: int
    author_id: int
    car_id: int
    date: datetime
    pay_type: int
    bonus_event_id: int

    class Config:
        orm_mode = True

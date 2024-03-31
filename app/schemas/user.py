from datetime import datetime, date, timedelta
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    validator,
    Extra,
)

from app.core.managment.phonecheck import PhoneNumber


class UserCreate(BaseModel):
    tg_id: Optional[PositiveInt]
    surname: str = Field(min_length=2)
    name: str = Field(min_length=2)
    patronymic: Optional[str]
    date_birth: date
    phone: PhoneNumber

    @validator('surname', 'name', 'patronymic')
    def check_alphabet_only(cls, value):
        check = value.replace(' ', '').replace('-', '')
        if check.isalpha():
            return value
        raise ValueError('Поле содержит недопустимые символ')

    @validator('date_birth')
    def check_age(cls, value):
        if (
                timedelta(days=40177.5) >=
                date.today()-value >=
                timedelta(days=5844)
        ):
            return value
        raise ValueError('Ваш возраст не соответствует допустимому')

    class Config:
        extra = Extra.forbid


class UserDB(UserCreate):
    reg_date: datetime

    class Config:
        orm_mode = True

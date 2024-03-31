from datetime import datetime, date, timedelta
from typing import Optional

# from phonenumbers.phonenumber import PhoneNumber
from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    validator,
    Extra,
)

# from app.core.managment.phonecheck import PhoneNumber
from app.core.config import settings


class UserCreate(BaseModel):
    tg_id: Optional[PositiveInt]
    surname: str = Field(min_length=settings.max_fio_len)
    name: str = Field(min_length=settings.max_fio_len)
    patronymic: Optional[str] = Field(None, min_length=settings.max_fio_len)
    date_birth: date
    phone: str

    @validator('surname', 'name', 'patronymic')
    def check_alphabet_only(cls, value):
        check = value.replace(' ', '').replace('-', '')
        if check.isalpha():
            return value
        raise ValueError(settings.fio_alphabet_error)

    @validator('date_birth')
    def check_age(cls, value):
        if (
                timedelta(days=settings.max_age) >=
                date.today()-value >=
                timedelta(days=settings.max_age)
        ):
            return value
        raise ValueError(settings.age_error)

    class Config:
        extra = Extra.forbid


class UserDB(UserCreate):
    reg_date: datetime

    class Config:
        orm_mode = True

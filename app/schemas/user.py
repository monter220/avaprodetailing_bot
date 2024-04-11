import phonenumbers

from datetime import datetime, date, timedelta
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    validator,
    Extra,
    NonNegativeInt,
)

from app.core.config import settings


class UserUpdateTG(BaseModel):
    tg_id: NonNegativeInt

    class Config:
        extra = Extra.forbid


class UserUpdate(BaseModel):
    surname: Optional[str] = Field(None, max_length=settings.max_fio_len)
    name: Optional[str] = Field(None, max_length=settings.max_fio_len)
    patronymic: Optional[str] = Field(None, max_length=settings.max_fio_len)
    date_birth: Optional[date] = Field(None)

    @validator('surname', 'name', 'patronymic')
    def check_alphabet_only(cls, value):
        check = value.replace(' ', '').replace('-', '')
        if check.isalpha():
            return value
        raise ValueError(settings.alphabet_error)

    @validator('date_birth')
    def check_age(cls, value):
        if (
                timedelta(days=settings.max_age) >=
                date.today() - value >=
                timedelta(days=settings.min_age)
        ):
            return value
        raise ValueError(settings.age_error)


class UserCreate(BaseModel):
    tg_id: Optional[NonNegativeInt] = Field(None)
    surname: str = Field(max_length=settings.max_fio_len)
    name: str = Field(max_length=settings.max_fio_len)
    patronymic: Optional[str] = Field(None, max_length=settings.max_fio_len)
    date_birth: date
    phone: str = Field(max_length=settings.max_phone_len)

    @validator('surname', 'name', 'patronymic')
    def check_alphabet_only(cls, value):
        check = value.replace(' ', '').replace('-', '')
        if check.isalpha():
            return value
        raise ValueError(settings.alphabet_error)

    @validator('date_birth')
    def check_age(cls, value):
        if (
                timedelta(days=settings.max_age) >=
                date.today()-value >=
                timedelta(days=settings.min_age)
        ):
            return value
        raise ValueError(settings.age_error)

    @validator('phone')
    def check_phone(cls, value):
        if value[0] == '8' or value[0] == '7':
            value = '+7' + value[1::]
        try:
            return phonenumbers.format_number(
                phonenumbers.parse(value),
                phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError(settings.phone_error)

    class Config:
        extra = Extra.forbid


class UserDB(UserCreate):
    reg_date: datetime

    class Config:
        orm_mode = True

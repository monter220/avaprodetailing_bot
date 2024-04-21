import phonenumbers

from typing import Optional, Union
from datetime import datetime, date, timedelta
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud import user_crud, service_crud, category_crud, car_crud
from app.models import User, Car
from app.core.config import settings
from app.translate.ru import (
    ERR_MSG_FIELD_NOT_UNIQUE,
    OBJ_NOT_EXIST,
    SERVICE_NOT_UNIQUE,
    CATEGORY_NOT_UNIQUE,
)


async def check_duplicate(
    phone: str,
    session: AsyncSession,
) -> Optional[User]:
    user = await user_crud.get_user_by_phone_number(phone, session)
    if user:
        if user.is_ban:
            raise HTTPException(
                status_code=451,
                detail='Пользователь заблокирован!',
            )
        if user.tg_id:
            raise HTTPException(
                status_code=422,
                detail='Пользователь уже существует!',
            )
        return user


async def check_category_duplicate_on_point(
    name: str,
    point_id: int,
    session: AsyncSession
) -> None:
    """
    Функция проверки категории на автомойке.
    Функция принимает на вход имя категории и id автомойки.
    Вызывает функцию проверки этих полей в БД.
    В случае совпадения значений, выбрасывает исключение об ошибке.
    """
    if await category_crud.check_unique_field(name, point_id, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CATEGORY_NOT_UNIQUE.format(name, point_id),
        )


async def check_service_duplicate_in_category(
    name: str,
    category_id: int,
    session: AsyncSession
) -> None:
    """
    Функция проверки услуги в категории.
    Функция принимает на вход имя услуги и id категории.
    Вызывает функцию проверки этих полей в БД.
    В случае совпадения значений, выбрасывает исключение об ошибке.
    """
    if await service_crud.check_unique_field(name, category_id, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=SERVICE_NOT_UNIQUE.format(name, category_id),
        )


async def check_fields_duplicate(
    model_crud,
    fields: dict,
    session: AsyncSession
) -> None:
    """
    Функция проверки данных на уникальность.
    Функция принимает на вход экземпляр класса CRUD для конкретной модели и
    словарь с данными {Имя-поля: Значение_поля}.
    Вызывает функцию проверки этих полей в БД.
    В случае совпадения значений, выбрасывает исключение об ошибке.
    """
    for name, value in fields.items():
        if await model_crud.check_unique_field(name, value, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERR_MSG_FIELD_NOT_UNIQUE.format(name),
            )


async def check_exist(model_crud, obj_id: int, session: AsyncSession):
    """
    Функция проверки существования объекта в БД.
    Функция принимает на вход crud-объект модели
    и id категории и проверяет его существование.
    В случае отсутствия выбрасывает исключение об ошибке.
    Если объект существует в БД, то возвращает его.
    """
    obj = await model_crud.get(obj_id, session)
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail=OBJ_NOT_EXIST.format(obj_id, model_crud.model.__name__)
        )
    return obj


async def check_user_by_tg_exist(tg_id: int, session: AsyncSession):
    user = await user_crud.get_user_by_telegram_id(tg_id, session)
    if user is None:
        raise HTTPException(
            status_code=406,
            detail='Пользователь не существует или заблокирован',
        )
    return user


async def check_user_exist(
    user_id: int,
    session: AsyncSession,
) -> None:
    if not await user_crud.user_exist(user_id, session):
        raise HTTPException(
            status_code=406,
            detail='Пользователь не существует или заблокирован',
        )


def check_file_format(
    file_format: str,
) -> None:
    if file_format not in ['image/jpeg', 'image/png']:
        raise HTTPException(
            status_code=406,
            detail='Only .jpeg or .png  files allowed'
        )


async def check_that_are_few_cars(
        user_id: int,
        session: AsyncSession,
) -> None:
    cars = await car_crud.get_user_cars(session=session, user_id=user_id)
    if len(cars) == 1:
        raise HTTPException(
            status_code=406,
            detail='У вас всего одна машина',
        )


async def check_admin_or_myprofile_car(
        user_id: int,
        user_telegram_id: int,
        session: AsyncSession,
        car: Optional[Car] = None,
) -> None:
    """
    Функция проверки прав на редактирование.
    Функция принимает на вход имя id пользователя, id авто,
    tg_id пользователя, который пытается внести правки
    В случае если у меняющего не соответствует роль
    или не совпадает id пользователя с изменяемыми данными,
    выбрасывает исключение об ошибке.
    """
    if car:
        if car.user_id != user_id:
            raise HTTPException(
                status_code=406,
                detail='Это не твоя машина',
            )
    author = await check_user_by_tg_exist(user_telegram_id, session)
    if not (user_id == author.id or author.role in (2, 3)):
        raise HTTPException(
            status_code=406,
            detail='нельзя трогать чужое',
        )


async def check_car_unique(
        license_plate_number: str,
        session: AsyncSession,
) -> None:
    if await car_crud.unique_car(license_plate_number, session):
        raise HTTPException(
            status_code=404,
            detail='Такое номер уже есть в базе!',
        )


def check_is_superadmin(current_user: User):
    """
    Функция для проверки является ли пользователь суперадмином.
    Если нет - редиректит в его профиль.
    """

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND
        )


def valid_phone(phone: str):
    check = phone.replace(
        '(', '').replace(')', '').replace(' ', '').replace('-', '')
    if check[0] == '8' or check[0] == '7':
        check = '+7' + check[1::]
    try:
        return phonenumbers.format_number(
            phonenumbers.parse(check),
            phonenumbers.PhoneNumberFormat.E164
        )
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValueError(settings.phone_error)


def valid_user(key: str, value: Union[str, datetime]):
    if key in ['surname', 'name', 'patronymic']:
        if value:
            check = value.replace(' ', '').replace('-', '')
            if not check.isalpha():
                raise ValueError(settings.alphabet_error)
    elif key in ['date_birth']:
        if (
                timedelta(days=settings.max_age) >=
                date.today() - value.date() >=
                timedelta(days=settings.min_age)
        ):
            return value
        raise ValueError(settings.age_error)

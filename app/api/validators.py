from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud import user_crud
from app.translate.ru import (
    ERR_MSG_FIELD_NOT_UNIQUE,
    OBJ_NOT_EXIST,
)


async def check_duplicate(
    phone: str,
    session: AsyncSession,
) -> None:
    user_id = await user_crud.phone_number_exist(phone, session)
    if user_id:
        tg_id = await user_crud.tg_exist(user_id, session)
        if tg_id is not None:
            raise HTTPException(
                status_code=422,
                detail='Пользователь уже существует!',
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
        raise HTTPException(status_code=404, detail=OBJ_NOT_EXIST)
    return obj


async def check_user_exist(
    user_id: str,
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

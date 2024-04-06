from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud import user_crud, point_crud
from app.models import Point
from app.translate.ru import ERR_MSG_FIELD_NOT_UNIQUE, POINT_NOT_EXIST


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



async def check_fields_duplicate(fields: dict, session: AsyncSession) -> None:
    """
    Функция проверки данных на уникальность.
    Функция принимает на вход словарь с данными {Имя-поля: Значение_поля}.
    Вызывает функцию проверки этих полей в БД.
    В случае совпадения значений, выбрасывает исключение об ошибке.
    """
    for name, value in fields.items():
        if await point_crud.check_unique_field(name, value, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERR_MSG_FIELD_NOT_UNIQUE.format(name),
            )


async def check_point_exist(point_id: int, session: AsyncSession) -> Point:
    """
    Функция проверки существования автомойки в БД.
    Функция принимает на вход id автомойки и проверяет его существование.
    В случае отсутствия выбрасывает исключение об ошибке.
    Если автомойка существует в БД, то возвращает ее.
    """
    point = await point_crud.get(point_id, session)
    if point is None:
        raise HTTPException(status_code=404, detail=POINT_NOT_EXIST)
    return point

  
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


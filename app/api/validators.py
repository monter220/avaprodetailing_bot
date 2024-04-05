from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user_crud


async def check_duplicate(
        phone: str,
        session: AsyncSession,
) -> None:
    user_id = await user_crud.phone_number_exist(phone, session)
    if user_id:
        tg_id = await user_crud.tg_exist(user_id,session)
        if tg_id is not None:
            raise HTTPException(
                status_code=422,
                detail='Пользователь уже существует!',
            )


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

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.crud import user_crud, point_crud


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


async def check_name_duplicate(
    field_name: str,
    session: AsyncSession,
) -> None:
    if await point_crud.check_unique_name(field_name, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=settings.err_msg_field_not_unique.format(field_name),
        )


async def check_address_duplicate(
    field_name: str,
    session: AsyncSession,
) -> None:
    if await point_crud.check_unique_address(field_name, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=settings.err_msg_field_not_unique.format(field_name),
        )

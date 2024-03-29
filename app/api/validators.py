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
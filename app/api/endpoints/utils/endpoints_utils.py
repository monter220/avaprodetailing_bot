from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.user import user_crud
from app.models import User


async def get_tg_id_cookie(request: Request):
    """Функция для получения куки tg_id.  """
    return request.cookies.get('tg_id')


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie)
):
    """
    Функция для получения текущего пользователя.
    """

    user: Optional[User] = await user_crud.get_user_by_telegram_id(
        user_telegram_id=int(user_telegram_id),
        session=session
    )

    return user

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User


class CRUDUser(CRUDBase):

    async def get_user_by_phone_number(
            self,
            phone: str,
            session: AsyncSession,
    ) -> Optional[User]:
        db_user = await session.execute(
            select(User).where(
                User.phone == phone
            )
        )
        return db_user.scalars().first()

    async def get_user_by_telegram_id(
            self,
            user_telegram_id: int,
            session: AsyncSession,
    ) -> Optional[User]:
        db_user = await session.execute(
            select(User).where(
                User.tg_id == user_telegram_id
            )
        )
        return db_user.scalars().first()

    async def tg_login_check(
            self,
            tg_id: int,
            session: AsyncSession,
    ) -> Optional[User]:
        db_user_id = await session.execute(
            select(User).where(
                User.tg_id == tg_id
            )
        )
        return db_user_id.scalars().first()

    async def user_exist(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> Optional[int]:
        db_user_id = await session.execute(
            select(User.id).where(
                User.id == user_id and User.is_ban == 0)
        )
        return db_user_id.scalars().first()


user_crud = CRUDUser(User)

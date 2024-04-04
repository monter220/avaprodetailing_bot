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
    ) -> Optional[int]:
        db_user_id = await session.execute(
            select(User.id).where(
                User.phone == phone
            )
        )
        return db_user_id.scalars().first()

    async def tg_exist(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> Optional[int]:
        db_user_tg = await session.execute(
            select(User.tg_id).where(
                User.id == user_id
            )
        )
        return db_user_tg.scalars().first()

    async def get_user_by_telegram_id(
            self,
            tg_id: int,
            session: AsyncSession,
    ) -> Optional[int]:
        db_user_id = await session.execute(
            select(User).where(
                User.tg_id == tg_id
            )
        )
        return db_user_id.scalars().first()


user_crud = CRUDUser(User)

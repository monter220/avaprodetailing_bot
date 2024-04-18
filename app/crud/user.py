from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.core.managment.utils import insert_into_events
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.user import UserBan
from app.crud.car import car_crud


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

    async def user_ban(
        self,
        user_id: int,
        author: User,
        session: AsyncSession,
    ) -> None:
        user = await self.get(user_id, session)
        ban: dict[str, bool] = dict.fromkeys(['is_ban'])
        ban['is_ban'] = False if user.is_ban else True
        await self.update(
            db_obj=user,
            obj_in=UserBan(**ban),
            user=author,
            model='User',
            session=session,
        )

    @staticmethod
    async def update_bonus_amount(
        user_id: int,
        bonus_amount: int,
        session: AsyncSession,
    ) -> int | None:
        """Обновление бонусов у пользователя при начислении или списании."""
        user = await session.get(User, user_id)
        user.bonus += bonus_amount
        await session.commit()
        await session.refresh(user)
        return user


user_crud = CRUDUser(User)

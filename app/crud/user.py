from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User, Events


class CRUDUser(CRUDBase):

    async def phone_number_exist(
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

    async def create_t(
            self,
            obj_in,
            session: AsyncSession,
            model: str,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        if model:
            event = dict.fromkeys(['author', 'model', 'data', 'type_id'])
            if user:
                event['user'] = user.id
            event['model'] = model
            event['type_id'] = 1
            event_data: dict[str, dict[str, str]] = dict.fromkeys(['old', 'new'])
            event_data['new'] = obj_in_data
            event['data'] = f'{event_data}'
            session.add(Events(**event))
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


user_crud = CRUDUser(User)

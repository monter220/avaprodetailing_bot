from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User


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


user_crud = CRUDUser(User)

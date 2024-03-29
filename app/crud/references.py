from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.references import Role


class CRUDRole(CRUDBase):

    async def empty(
            self,
            session: AsyncSession,
    ) -> Optional[int]:
        role_id = await session.execute(
            select(Role.id)
        )
        return role_id.scalars().first()


role_crud = CRUDRole(Role)
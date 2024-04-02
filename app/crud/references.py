from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Role, PayType


class CRUDReferences(CRUDBase):

    async def empty(
            self,
            session: AsyncSession,
    ) -> Optional[int]:
        role_id = await session.execute(
            select(self.model)
        )
        return role_id.scalars().first()


role_crud = CRUDReferences(Role)
paytype_crud = CRUDReferences(PayType)

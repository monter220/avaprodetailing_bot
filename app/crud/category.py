from typing import Union

from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Category


class CRUDCategory(CRUDBase):

    @staticmethod
    async def check_unique_field(
        field_name: str,
        field_value: str,
        session: AsyncSession,
    ) -> Union[None, Boolean]:
        exists_criteria = (
            select(Category).where(
                Category.name == field_value
            ).exists()
        )

        db_field_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return db_field_exists.first()


category_crud = CRUDCategory(Category)

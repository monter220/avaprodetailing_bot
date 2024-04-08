from typing import Union

from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Category


class CRUDCategory(CRUDBase):

    @staticmethod
    async def check_unique_field(
        _: str,
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

    @staticmethod
    async def all_categories(session: AsyncSession):
        category = await session.execute(
            select(Category)
            .options(selectinload(Category.services))
        )
        return category.unique().scalars().all()

    @staticmethod
    async def category_by_id(category_id, session: AsyncSession):
        category = await session.execute(
            select(Category)
            .filter_by(id=category_id)
            .options(selectinload(Category.services))
        )
        return category.unique().scalars().first()


category_crud = CRUDCategory(Category)

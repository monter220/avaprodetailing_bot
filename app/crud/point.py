from typing import Union

from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Point


class CRUDPoint(CRUDBase):

    @staticmethod
    async def check_unique_name(
        field_name: str,
        session: AsyncSession,
    ) -> Union[None, Boolean]:
        exists_criteria = (
            select(Point).where(
                Point.name == field_name
            ).exists()
        )
        db_field_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return db_field_exists.first()

    @staticmethod
    async def check_unique_address(
        field_name: str,
        session: AsyncSession,
    ) -> Union[None, Boolean]:
        exists_criteria = (
            select(Point).where(
                Point.address == field_name
            ).exists()
        )
        db_field_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return db_field_exists.first()


point_crud = CRUDPoint(Point)

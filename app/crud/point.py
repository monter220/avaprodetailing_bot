from typing import Union

from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Point


class CRUDPoint(CRUDBase):

    @staticmethod
    async def check_unique_field(
        field_name: str,
        field_value: str,
        session: AsyncSession,
    ) -> Union[None, Boolean]:
        if field_name == 'name':
            exists_criteria = (
                select(Point).where(
                    Point.name == field_value
                ).exists()
            )
        else:
            exists_criteria = (
                select(Point).where(
                    Point.address == field_value
                ).exists()
            )
        db_field_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return db_field_exists.first()


point_crud = CRUDPoint(Point)

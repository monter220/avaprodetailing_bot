from typing import Union

from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Point, Category, User


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

    @staticmethod
    async def point_by_id(point_id: int, session: AsyncSession):
        point = await session.execute(
            select(Point).filter_by(
                id=point_id).options(
                selectinload(Point.admins)).options(
                selectinload(Point.categories).options(
                    selectinload(Category.services))
            )
        )
        return point.unique().scalars().first()

    @staticmethod
    async def all_points(session: AsyncSession):
        point = await session.execute(
            select(Point).options(
                selectinload(Point.admins)
            ).options(
                selectinload(Point.categories).options(
                    selectinload(Category.services))
            )
        )
        return point.unique().scalars().all()


point_crud = CRUDPoint(Point)

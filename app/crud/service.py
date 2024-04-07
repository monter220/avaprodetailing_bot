from typing import Union

from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Service


class CRUDService(CRUDBase):

    @staticmethod
    async def check_unique_field(
        name: str,
        point_id: str,
        session: AsyncSession,
    ) -> Union[None, Boolean]:
        exists_criteria = (
            select(Service)
            .where(
                (Service.name == name) &
                (Service.point_id == point_id)
            )
            .exists()
        )
        db_field_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return db_field_exists.first()

    @staticmethod
    async def get_services_by_category(
        category_id: int,
        session: AsyncSession
    ):
        services = await session.execute(
            select(Service)
            .where(Service.category_id == category_id)
        )
        return services.scalars().all()

    @staticmethod
    async def get_services_by_point(
        point_id: int,
        session: AsyncSession
    ):
        services = await session.execute(
            select(Service)
            .where(Service.point_id == point_id)
        )
        return services.scalars().all()

    @staticmethod
    async def get_services_by_point_category(
        point_id: int,
        category_id: int,
        session: AsyncSession
    ):
        services = await session.execute(
            select(Service)
            .where(
                (Service.point_id == point_id) &
                (Service.category_id == category_id)
            )
        )
        return services.scalars().all()


service_crud = CRUDService(Service)

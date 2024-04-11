from typing import Union

from sqlalchemy import Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import Service


class CRUDService(CRUDBase):

    @staticmethod
    async def check_unique_field(
        name: str,
        category_id: str,
        session: AsyncSession,
    ) -> Union[None, Boolean]:
        exists_criteria = (
            select(Service).where(
                (Service.name == name) &
                (Service.category_id == category_id)
            ).exists()
        )
        db_field_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return db_field_exists.first()

    @staticmethod
    async def service_by_id(
            service_id: int,
            session: AsyncSession
    ):
        services = await session.execute(
            select(Service)
            .filter_by(id=service_id)
        )
        return services.scalars().first()

    @staticmethod
    async def services_by_category(
            category_id: int,
            session: AsyncSession
    ):
        services = await session.execute(
            select(Service)
            .filter_by(category_id=category_id)
        )
        return services.scalars().all()


service_crud = CRUDService(Service)

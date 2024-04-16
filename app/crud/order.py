from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Order, OrderedService


class CRUDOrder(CRUDBase):
    """CRUD для модели заказов."""

    async def get_orders_by_user_id(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> list[Order]:
        """Получение заказов пользователя."""
        orders = await session.execute(
            select(self.model).options(joinedload(self.model.bonus)).where(
                self.model.user_id == user_id,
                self.model.is_active,
            )
        )
        return orders.scalars().all()


class CRUDOrderedService(CRUDBase):
    """CRUD для модели заказанных услуг."""
    pass


order_crud = CRUDOrder(Order)
ordered_service_crud = CRUDOrderedService(OrderedService)

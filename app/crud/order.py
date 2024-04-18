from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Order, OrderedService, Car, Bonus, User, PayType


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

    async def get_orders_report(
        self,
        session: AsyncSession,
    ):
        """Получение отчета по заказам."""
        orders = await session.execute(
            select(
                Order.date.label('date'),
                Car.license_plate_number.label('license_plate_number'),
                Order.cost.label('cost'),
                Bonus.amount.label('bonus_amount'),
                User.phone.label('user_phone'),
            ).join(Order.car)
            .join(Order.bonus)
            .join(Order.user)
            .where(Order.is_active == true())
        )
        return orders.all()

    async def get_payments_report(
        self,
        session: AsyncSession,
    ):
        """Получение отчета по оплатам."""
        orders = await session.execute(
            select(
                Order.date.label('date'),
                Order.cost.label('cost'),
                PayType.name.label('pay_type')
            ).join(Order.pay_type)
            .where(Order.is_active == true())
        )
        return orders.all()


class CRUDOrderedService(CRUDBase):
    """CRUD для модели заказанных услуг."""
    pass


order_crud = CRUDOrder(Order)
ordered_service_crud = CRUDOrderedService(OrderedService)

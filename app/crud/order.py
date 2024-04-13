from app.crud.base import CRUDBase
from app.models import Order, Bonus_event, Service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CRUDOrder(CRUDBase):
    async def create_order_with_bonus(self, object_in, session: AsyncSession):
        object_data = object_in.dict()
        #создаем бонусы
        bonus_data = object_data.pop('bonus_event')
        bonus = Bonus_event(**bonus_data)
        session.add(bonus)
        service_ids = object_data.pop('services')
        #Создаем заказ
        order = self.model(**object_data, bonus_event=bonus)
        #получаем услуги и связываем с заказом
        services = await session.execute(select(Service).filter(Service.id.in_(service_ids)))
        order.services.extend(services.scalars().all())
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order

order_crud = CRUDOrder(Order)

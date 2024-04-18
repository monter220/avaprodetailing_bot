from datetime import datetime

from sqlalchemy import true, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Bonus


class CRUDBonus(CRUDBase):
    """CRUD для модели бонусов."""

    async def burn_user_bonuses(
        self,
        user_id: int,
        amount: int,
        session: AsyncSession
    ) -> None:
        """Сжигание бонусов у пользователя при их списании."""
        active_bonuses = await self.get_active_bonuses(user_id, session)
        for bonus in active_bonuses:
            available_bonus = bonus.amount - bonus.used
            if available_bonus >= amount:
                bonus.used += amount
                break
            else:
                bonus.used += available_bonus
                amount -= available_bonus
            bonus.is_active = False
        await session.commit()

    async def get_active_bonuses(
        self,
        user_id: int,
        session: AsyncSession,
    ):
        """Получение активных бонусов."""
        bonuses = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id,
                self.model.is_active == true(),
                self.model.amount > 0,
                self.model.used < self.model.amount,
            )
        )
        return bonuses.scalars().all()

    async def get_bonuses_by_user_id(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> list[Bonus]:
        """Получение бонусов пользователя."""
        bonuses = await session.execute(
            select(self.model).options(joinedload(self.model.order)).where(
                self.model.user_id == user_id,
                self.model.is_active,
            ).order_by(self.model.id.desc())
        )
        return bonuses.scalars().all()

    async def burn_bonuses(
        self,
        session: AsyncSession,
    ):
        """Обработка сгоревших бонусов."""
        bonuses = await session.execute(
            select(self.model).options(joinedload(self.model.user)).where(
                self.model.is_active == true(),
                self.model.date_end < datetime.now(),
            )
        )
        bonuses = bonuses.scalars().all()
        for bonus in bonuses:
            bonus.is_active = False
            if bonus.amount > 0:
                bonus.user.bonus -= bonus.amount - bonus.used

        await session.commit()


bonus_crud = CRUDBonus(Bonus)

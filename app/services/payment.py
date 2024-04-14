import contextlib

from app.core.db import get_async_session
from app.crud import bonus_crud, user_crud
from app.crud.order import order_crud
from app.services.telegram import send_message
from app.translate.ru import PAYMENT_SUCCESSFUL_ADMIN


async def process_payment(order_id: int):
    """Обработка успешного платежа."""
    async_session_context = contextlib.asynccontextmanager(get_async_session)
    async with async_session_context() as session:
        order = await order_crud.get(order_id, session)
        bonus = await bonus_crud.get(order.bonus_id, session)
        order.is_active = True
        bonus.is_active = True
        await session.commit()
        await user_crud.update_bonus_amount(
            order.user_id, bonus.amount, session)
        if bonus.amount < 0:
            await bonus_crud.burn_user_bonuses(
                order.user_id, abs(bonus.amount), session)

    await send_message(
        chat_id=order.admin_id,
        text=PAYMENT_SUCCESSFUL_ADMIN.format(order.cost),
    )

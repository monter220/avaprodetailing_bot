from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message

from app.core.config import bot
from app.services.payment import process_payment

router = Router()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Подтверждение проведения оплаты."""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.content_type.in_(['successful_payment']))
async def process_successful_payment(message: Message):
    """Проведение успешной оплаты."""
    await process_payment(int(message.successful_payment.invoice_payload))

import logging

from aiogram.types import LabeledPrice

from app.core.config import bot, settings
from app.translate.ru import PAYMENT_TITLE, PAYMENT_DESCRIPTION


async def send_message(text: str, chat_id: int):
    """Отправка сообщения пользователю."""
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logging.exception(f'Ошибка при отправке сообщения в TG {e}')


async def send_invoice(
    chat_id: int,
    order_id: str,
    price: int,
):
    """Отправка инвойса пользователю."""
    prices = [LabeledPrice(label='Услуги', amount=price * 100)]
    try:
        await bot.send_invoice(
            chat_id=chat_id,
            title=PAYMENT_TITLE,
            description=PAYMENT_DESCRIPTION,
            payload=str(order_id),
            provider_token=settings.telegram_provider_token,
            currency=settings.telegram_currency,
            prices=prices,
        )
    except Exception as e:
        logging.exception(f'Ошибка при отправке инвойса в TG {e}')

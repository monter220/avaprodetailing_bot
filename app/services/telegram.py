import logging

from aiogram.types import LabeledPrice, BufferedInputFile

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


async def send_excel(excel, filename: str, chat_id: int):
    """Отправка excel пользователю."""
    try:
        excel.seek(0)
        byte_data = excel.read()
        input_file = BufferedInputFile(file=byte_data, filename=filename)
        await bot.send_document(chat_id, document=input_file)
    except Exception as e:
        logging.exception(f'Ошибка при отправке excel в TG {e}')

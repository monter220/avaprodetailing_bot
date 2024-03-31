from aiogram import html, types, Router
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.config import settings
from app.bot.constants.answer_messages import START_COMMAND_MESSAGE_ANSWER

router = Router()


@router.message(
    CommandStart(),
    # types.Chat.type == 'private'
)
async def start(message: types.Message):
    """
    Хэндлер обрабатывает комманду старт и присылает
    сообщение с кнопкой для перехода в вэбапп.
    """

    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        types.InlineKeyboardButton(
            text='Открыть веб-страницу',
            web_app=types.WebAppInfo(settings.telegram_webapp_url),
        )
    )

    await message.answer(
        text=f'{START_COMMAND_MESSAGE_ANSWER}'.format(
            user_full_name=html.quote(message.from_user.full_name)   
        ),
        reply_markup=keyboard.as_markup()
    )
    return

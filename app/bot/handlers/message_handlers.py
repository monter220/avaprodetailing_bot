from aiogram import F, html, types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.config import settings
from app.bot.translates.ruRU.answer_messages import ANY_MESSAGE_ANSWER

router = Router()


@router.message(
    F.chat.type == 'private'
)
async def start(message: types.Message):
    """
    Хэндлер обрабатывает комманду старт и присылает
    сообщение с кнопкой для перехода в вэбапп.
    """

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
            text='Открыть веб-страницу',
            web_app=types.WebAppInfo(url=settings.web_app_url),
    )

    await message.answer(
        text=ANY_MESSAGE_ANSWER.format(
            user_full_name=html.quote(message.from_user.full_name)
        ),
        reply_markup=keyboard.as_markup()
    )

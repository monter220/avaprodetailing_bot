from contextlib import asynccontextmanager

from aiogram import types, Bot
from aiogram.client.bot import DefaultBotProperties
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.api.routers import main_router
from app.core.config import settings
from app.core.config_logger import logger
from app.bot.handlers import command_router
from app.core.init_db import create_role, create_paytype, create_eventtypes
from app.middlewares import TelegramIDCheckingMiddleware


bot: Bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(
        parse_mode=settings.bot_parse_mode,
    )
)
web_hook_path: str = f'{settings.host_url}/webhook'


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция для обработки запуска и остановки бота."""

    logger.info('Приложение запущено.')
    await create_role()
    await create_paytype()
    await create_eventtypes()
    await bot.set_webhook(
        url=web_hook_path,
        # Дропает апдейты, которые пришли во время запуска бота.
        drop_pending_updates=settings.bot_drop_pending_updates,
        # Таймаут на обработку запроса - позволяет не загонять
        # бота в цикл, при получении ошибки от API.
        request_timeout=settings.bot_request_timeout,
    )
    settings.dp.include_routers(
        command_router,
    )

    yield

    await bot.delete_webhook(
        drop_pending_updates=settings.bot_drop_pending_updates,
        # Дропает апдейты, которые пришли во время остановки бота.
    )
    logger.info('Приложение остановлено.')


app = FastAPI(title=settings.app_title,
              lifespan=lifespan)

if not settings.testing:
    app.add_middleware(TelegramIDCheckingMiddleware)

# Подключение статических файлов.
app.mount(
    '/static',
    StaticFiles(directory='app/templates/static'),
    name='static'
)

app.include_router(main_router)


@app.post(path=web_hook_path)
async def bot_webhook(update: dict):
    """Функция для приёма сообщений из Telegram."""

    telegram_update = types.Update(**update)
    await settings.dp.feed_update(bot=bot,
                                  update=telegram_update)


if __name__ == '__main__':

    uvicorn.run(app, host=settings.host_ip, port=settings.app_port)

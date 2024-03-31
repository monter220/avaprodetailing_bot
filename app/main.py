from contextlib import asynccontextmanager

from aiogram import types
from fastapi import FastAPI
import uvicorn

from app.api.routers import main_router
from app.core.config import settings
from app.core.config_logger import logger
from bot.handlers import command_router
from app.core.init_db import create_role


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция для обработки запуска и остановки бота."""

    logger.info('Приложение запущено.')
    await settings.bot.set_webhook(
        url=settings.web_hook_path,
        drop_pending_updates=True,  # Дропает апдейты, которые пришли во время запуска бота.
        request_timeout=30,  # Таймаут на обработку запроса - позволяет не загонять бота в цикл, при получении ошибки от API.
    )
    app.include_router(main_router)
    settings.dp.include_routers(
        command_router,
    )

    yield

    await settings.bot.delete_webhook(
        drop_pending_updates=True,  # Дропает апдейты, которые пришли во время остановки бота.
    )
    logger.info(f'Приложение остановлено.')


app = FastAPI(title=settings.app_title,
              lifespan=lifespan)
app.include_router(main_router)


@app.post(path=settings.web_hook_path)
async def bot_webhook(update: dict):
    """Функция для приёма сообщений из Telegram."""

    telegram_update = types.Update(**update)
    await settings.dp.feed_update(bot=settings.bot,
                                  update=telegram_update)

    
@app.on_event('startup')
async def startup():
    await create_role()


if __name__ == '__main__':
    
    uvicorn.run(app, host='0.0.0.0', port=settings.app_port)

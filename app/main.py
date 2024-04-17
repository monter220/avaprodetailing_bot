from contextlib import asynccontextmanager

from aiogram import types
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn

from app.api.routers import main_router
from app.crud import evettypes_crud, role_crud, paytype_crud
from app.core.config import settings, web_hook_path, bot
from app.core.config_logger import logger
from app.bot.handlers import command_router, payment_router
from app.core.init_db import create_reference, create_superadmin
from app.middlewares import TelegramIDCheckingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция для обработки запуска и остановки бота."""

    logger.info('Приложение запущено.')
    await create_reference(role_crud, settings.role_list)
    await create_reference(paytype_crud, settings.paytype_list)
    await create_reference(evettypes_crud, settings.eventtypes_list)
    await create_superadmin()
    await bot.set_webhook(
        url=web_hook_path,
        drop_pending_updates=settings.bot_drop_pending_updates,
        # Дропает апдейты, которые пришли во время запуска бота.
        request_timeout=settings.bot_request_timeout,
        # Таймаут на обработку запроса - позволяет не загонять бота в цикл,
        # при получении ошибки от API.
    )
    settings.dp.include_routers(
        payment_router,
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
    app.add_middleware(HTTPSRedirectMiddleware)

app.mount('/static', StaticFiles(directory='app/templates/static'),
          name='static')  # Подключение статических файлов.

app.include_router(main_router)


@app.post(path='/webhook')
async def bot_webhook(update: dict):
    """Функция для приёма сообщений из Telegram."""

    telegram_update = types.Update(**update)
    await settings.dp.feed_update(bot=bot,
                                  update=telegram_update)


if __name__ == '__main__':
    uvicorn.run(app, host=settings.host_ip, port=settings.app_port)

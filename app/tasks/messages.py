import asyncio
import contextlib

from app.core.config import celery_app
from app.core.db import get_async_session
from app.crud import user_crud
from app.services.telegram import send_message

celery = celery_app
SENDING_WAIT_TIME = 0.1


@celery.task(max_retries=1)
def sending_ads(text: str):
    """Задача. Отправка информационной рассылки."""
    asyncio.get_event_loop().run_until_complete((
        _sending_ads(text)
    ))


async def _sending_ads(text: str):
    """Реальная отправка информационной рассылки."""
    async_session_context = contextlib.asynccontextmanager(get_async_session)
    async with async_session_context() as session:
        users = await user_crud.get_multi(session)
        for user in users:
            if not user.tg_id:
                continue
            await send_message(text, user.tg_id)
            await asyncio.sleep(SENDING_WAIT_TIME)

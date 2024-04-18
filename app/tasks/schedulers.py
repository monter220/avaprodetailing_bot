import asyncio
import contextlib

from celery.schedules import crontab

from app.core.config import celery_app
from app.core.db import get_async_session
from app.crud import bonus_crud

celery = celery_app


@celery_app.task(max_retries=1)
def daily_burning():
    """Задача. Ежедневное сжигание бонусов."""
    asyncio.get_event_loop().run_until_complete((
        _daily_burning()
    ))


async def _daily_burning():
    """Ежедневная обработка сгоревших бонусов."""
    get_async_session_context = contextlib.asynccontextmanager(
        get_async_session)
    async with get_async_session_context() as session:
        await bonus_crud.burn_bonuses(session)


celery_app.conf.beat_schedule = {
    'daily_burning': {
        'task': 'app.tasks.schedulers.daily_burning',
        'schedule': crontab(hour='0', minute='0'),
        'args': (),
    }
}

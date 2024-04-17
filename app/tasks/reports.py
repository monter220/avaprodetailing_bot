import asyncio

from app.core.config import celery_app
from app.services.report import process_report

celery = celery_app


@celery.task(max_retries=1)
def send_report(
    key: str, user_tg_id: int, field_names: list[str] = None,
):
    """Задача. Получение отчета."""
    asyncio.get_event_loop().run_until_complete((
        process_report(
            key=key,
            user_tg_id=user_tg_id,
            field_names=field_names,
        )
    ))

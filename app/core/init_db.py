import contextlib

from datetime import datetime
from app.core.config import settings
from app.core.db import get_async_session
from app.schemas.references import ReferenceCreate
from app.crud import user_crud


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_reference(model_crud, data: str):
    """Функция для предварительного наполнения справочных таблиц."""
    if data is not None:
        reference_dict = eval(data)
        async with get_async_session_context() as session:
            if not await model_crud.check_empty(session):
                for id in reference_dict.keys():
                    await model_crud.create(
                        ReferenceCreate(
                            id=id, name=reference_dict[id]
                        ), session)


async def create_superadmin():
    """Функция создания суперпользователя в проекте."""
    if settings.superadmin is not None:
        superadmin_dict = eval(settings.superadmin)
        async with get_async_session_context() as session:
            if not await user_crud.get(1, session):
                superadmin_dict['date_birth'] = datetime.strptime(
                    superadmin_dict['date_birth'], '%Y-%m-%d')
                await user_crud.create_from_dict(superadmin_dict, session)

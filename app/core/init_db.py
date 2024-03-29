import contextlib

from app.core.config import settings
from app.core.db import get_async_session
from app.schemas.references import RoleCreate
from app.crud.references import role_crud


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_role():
    if settings.role_list is not None:
        role_dict = eval(settings.role_list)
        async with get_async_session_context() as session:
            if not await role_crud.empty(session):
                for id in role_dict.keys():
                    await role_crud.create(
                        RoleCreate(
                            id=id,name=role_dict[id]
                        ), session)

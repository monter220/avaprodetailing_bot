from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user_crud


async def process_report(
    session: AsyncSession,
    key: str,
    user_id: Optional[int] = None
):
    types_query = {
        'users': user_crud.get_multi(session),
    }
    objects = await types_query[key]
    return objects

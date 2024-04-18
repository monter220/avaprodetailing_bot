from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Events, User


async def insert_into_events(
        event_data: dict[str, dict[str, str]],
        model: str,
        type: int,
        session: AsyncSession,
        user: Optional[User] = None,
):
    event = dict.fromkeys(['author', 'model', 'data', 'type_id'])
    try:
        if user:
            event['author'] = user.id
        event['model'] = model
        event['type_id'] = type
        event['data'] = f'{event_data}'
        session.add(Events(**event))
    except Exception as e:
        raise HTTPException(
            status_code=507,
            detail=f'{e}. Не удалось записать в лог!',
        )

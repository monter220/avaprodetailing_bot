from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Events, User


async def insert_into_events(
        obj_in_data,
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
        event_data: dict[str, dict[str, str]] = dict.fromkeys(['old', 'new'])
        event_data['new'] = obj_in_data
        event['data'] = f'{event_data}'
        session.add(Events(**event))
    except:
        raise HTTPException(
            status_code=507,
            detail='Не удалось записать в лог!',
        )

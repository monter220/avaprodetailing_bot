from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.managment.utils import insert_into_events
from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            model: Optional[str] = None,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        if model:
            event_data: dict[str, dict[str, str]] = dict.fromkeys(['old', 'new'])
            event_data['new'] = obj_in_data
            await insert_into_events(event_data, model, 1, session, user)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            user: User,
            session: AsyncSession,
            model: Optional[str] = None,
    ):
        obj_data = jsonable_encoder(db_obj)
        event_data: dict[str, dict[str, str]] = dict.fromkeys(['old', 'new'])
        event_data['old'] = obj_data
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if update_data[field]:
                    setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if model:
            event_data['new'] = jsonable_encoder(db_obj)
            await insert_into_events(event_data, model, 2, session, user)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            user: User,
            session: AsyncSession,
            model: Optional[str] = None,
    ):
        if model:
            obj_data = jsonable_encoder(db_obj)
            event_data: dict[str, dict[str, str]] = dict.fromkeys(['old', 'new'])
            event_data['old'] = obj_data
            await insert_into_events(event_data, model, 3, session, user)
        await session.delete(db_obj)
        await session.commit()
        return db_obj

from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Car, User

from app.core.managment.utils import insert_into_events


class CRUDCar(CRUDBase):

    async def create_car(
            self,
            obj_in,
            user: User,
            session: AsyncSession,
            path: Optional[str] = None,
            model: Optional[str] = None,
    ):
        obj_in_data = obj_in.dict()
        if path is not None:
            obj_in_data['image'] = path
        db_obj = self.model(**obj_in_data)
        if model:
            event_data: dict[str, dict[str, str]] = dict.fromkeys(['old', 'new'])
            event_data['new'] = obj_in_data
            await insert_into_events(event_data,model,1,session,user)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    # async def update_car(
    #         self,
    #         db_obj,
    #         obj_in,
    #         user: User,
    #         session: AsyncSession,
    #         path: Optional[str] = None,
    #         model: Optional[str] = None,
    # ):
    #     obj_data = jsonable_encoder(db_obj)
    #     update_data = obj_in.dict(exclude_unset=True)
    #     event_data: dict[str, dict[str, str]] = dict.fromkeys(['old', 'new'])
    #
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     session.add(db_obj)
    #     await session.commit()
    #     await session.refresh(db_obj)
    #     return db_obj

    async def get_user_cars(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        db_cars = await session.execute(select(Car).where(
                Car.user_id == user_id
            ))
        return db_cars.scalars().all()


car_crud = CRUDCar(Car)

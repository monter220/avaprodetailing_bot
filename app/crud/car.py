from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Car

from app.core.managment.utils import insert_into_events


class CRUDCar(CRUDBase):

    async def create_car(
            self,
            obj_in,
            session: AsyncSession,
            path: Optional[str] = None,
            model: Optional[str] = None,
            user: Optional[int] = None,
    ):
        obj_in_data = obj_in.dict()
        if path is not None:
            obj_in_data['image'] = path
        db_obj = self.model(**obj_in_data)
        if model:
            await insert_into_events(obj_in_data,model,1,session,user)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


car_crud = CRUDCar(Car)

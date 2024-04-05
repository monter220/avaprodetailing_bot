from typing import Optional

from app.crud.base import CRUDBase
from app.models import Car
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDCar(CRUDBase):

    async def create_car(
            self,
            obj_in_data: dict[str,str],
            session: AsyncSession,
            path: Optional[str] = None,
    ):
        if path is not None:
            obj_in_data['image'] = path
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj



car_crud = CRUDCar(Car)

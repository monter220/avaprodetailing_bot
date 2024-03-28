from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.car import car_crud
from app.schemas.car import CarCreate, CarDB

router = APIRouter()


@router.post(
    '/car/',
    response_model=CarDB,
    response_model_exclude_none=True,
)
async def create_new_user(
        new_user: CarCreate,
        session: AsyncSession = Depends(get_async_session),
):
    new = await car_crud.create(new_user, session)
    return new

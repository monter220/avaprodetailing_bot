from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_address_duplicate
from app.core.db import get_async_session
from app.crud import point_crud
from app.models import Point
from app.schemas.point import PointDB, PointCreate

router = APIRouter()


@router.post(
    '/',
    response_model=PointDB,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def create_new_point(
    new_point_json: PointCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Point:
    """
    Создание автомойки.
    """
    await check_name_duplicate(new_point_json.name, session)
    await check_address_duplicate(new_point_json.address, session)
    new_point_db = await point_crud.create(new_point_json, session)
    return new_point_db

@router.get(
    '/',
    response_model=list[PointDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех автомоек."""
    return await point_crud.get_multi(session)
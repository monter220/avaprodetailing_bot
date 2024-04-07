from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_exist,
    check_service_duplicate_on_point
)
from app.core.db import get_async_session
from app.crud import service_crud, point_crud, category_crud
from app.models import Service
from app.schemas.service import ServiceDB, ServiceCreate, ServiceUpdate

router = APIRouter()


@router.post(
    '/',
    response_model=ServiceDB,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def create_new_service(
    new_service_json: ServiceCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Service:
    """
    Создание услуги.
    Только для суперюзеров.
    """

    # Проверка на существование автомойки.
    await check_exist(point_crud, new_service_json.point_id, session)

    # Проверка на существование категории услуг.
    await check_exist(category_crud, new_service_json.category_id, session)

    # Проверка на уникальность услуги на автомойке
    await check_service_duplicate_on_point(
        new_service_json.name,
        new_service_json.point_id,
        session
    )
    # Создание услуги
    new_service_db = await service_crud.create(new_service_json, session)
    return new_service_db


@router.get(
    '/',
    response_model=list[ServiceDB],
    response_model_exclude_none=True,
)
async def get_all_services(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех услуг."""
    return await service_crud.get_multi(session)


@router.patch(
    '/{service_id}',
    response_model=ServiceDB,
    # dependencies=[Depends(current_superuser)],
)
async def update_service(
    service_id: int,
    service_json: ServiceUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Редактирование услуги.
    """

    # Проверка на существование услуги в базе.
    service_db = await check_exist(service_crud, service_id, session)

    # Проверка на существование автомойки.
    await check_exist(point_crud, service_json.point_id, session)

    # Проверка на существование категории услуг.
    await check_exist(category_crud, service_json.category_id, session)

    # Проверка на уникальность переданных данных
    if service_json.name is not None:
        await check_service_duplicate_on_point(
            service_json.name,
            service_json.point_id,
            session
        )

    # Изменяем поля услуги
    return await service_crud.update(service_db, service_json, session)


@router.delete(
    '/{service_id}',
    response_model=ServiceDB,
    # dependencies=[Depends(current_superuser)],
)
async def delete_service(
    service_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Удаляет услугу.
    """
    # Проверка на существование услуги в базе
    service_db = await check_exist(service_crud, service_id, session)

    # Удаляем услугу.
    service = await service_crud.remove(service_db, session)
    return service

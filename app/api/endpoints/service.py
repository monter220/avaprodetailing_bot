from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_exist,
    check_service_duplicate_in_category
)
from app.core.db import get_async_session
from app.crud import service_crud, point_crud, category_crud
from app.models import Service
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceDB


router = APIRouter(
    prefix='/services',
    tags=['Услуги']
)


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

    name = new_service_json.name
    category_id = new_service_json.category_id

    # Проверка на уникальность услуги в указанной категории
    await check_service_duplicate_in_category(name, category_id, session)

    # Проверка на существование категории с переданным category_id
    await check_exist(category_crud, category_id, session)

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
    services = await service_crud.get_multi(session)
    return services


@router.get(
    'category/{category_id}',
    response_model=list[ServiceDB],
    response_model_exclude_none=True,
)
async def get_services_by_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех услуг с определенной категорией."""

    # Проверка на существование категории услуг.
    await check_exist(category_crud, category_id, session)
    return await service_crud.services_by_category(category_id, session)


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

    # Проверка на существование категории услуг.
    if service_json.category_id is not None:
        await check_exist(category_crud, service_json.category_id, session)

    # Проверка на уникальность переданных данных
    if service_json.name is not None and service_json.category_id is not None:
        name = service_json.name
        category_id = service_json.category_id
        await check_service_duplicate_in_category(name, category_id, session)

    if service_json.name is None and service_json.category_id is not None:
        name = service_db.name
        category_id = service_json.category_id
        await check_service_duplicate_in_category(name, category_id, session)

    if service_json.name is not None and service_json.point_id is None:
        name = service_json.name
        category_id = service_db.category_id
        await check_service_duplicate_in_category(name, category_id, session)

    # Изменяем поля услуги
        service_db = await service_crud.update(service_db, service_json, session)
    return service_db


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

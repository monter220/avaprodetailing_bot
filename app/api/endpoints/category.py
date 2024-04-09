from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_exist, check_category_duplicate_on_point
from app.core.db import get_async_session
from app.crud import point_crud
from app.crud.category import category_crud
from app.models import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryDB,
    CategoryBaseDB
)

router = APIRouter(
    prefix='/category',
    tags=['Категории услуг']
)


@router.post(
    '/',
    response_model=CategoryBaseDB,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def create_new_category(
    new_category_json: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Category:
    """
    Создание категории услуг.
    Только для суперюзеров.
    """

    name = new_category_json.name
    point_id = new_category_json.point_id

    # Проверка на уникальность категории на указанной автомойке
    await check_category_duplicate_on_point(name, point_id, session)

    # Проверка на существование автомойки с переданным point_id
    await check_exist(point_crud, point_id, session)

    # Создание категории услуг
    new_category_db = await category_crud.create(new_category_json, session)
    return new_category_db


@router.get(
    '/',
    response_model=list[CategoryDB],
    response_model_exclude_none=True,
)
async def get_all_categories(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех категорий."""
    categories = await category_crud.all_categories(session)
    return categories


@router.get(
    'point/{point_id}',
    response_model=list[CategoryDB],
    response_model_exclude_none=True,
)
async def get_caterories_by_point(
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех категорий с определенной автомойки."""

    # Проверка на существование автомойки.
    await check_exist(point_crud, point_id, session)

    categories = await category_crud.categories_by_point(point_id, session)

    return categories


@router.patch(
    '/{category_id}',
    response_model=CategoryBaseDB,
    # dependencies=[Depends(current_superuser)],
)
async def update_category(
    category_id: int,
    category_json: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Редактирование категории.
    """

    # Проверка на существование категории в базе
    category_db = await check_exist(category_crud, category_id, session)

    # Проверка на существование автомойки.
    if category_json.point_id is not None:
        await check_exist(point_crud, category_json.point_id, session)

    # Проверка на уникальность переданных данных
    if category_json.name is not None and category_json.point_id is not None:
        name = category_json.name
        point_id = category_json.point_id
        await check_category_duplicate_on_point(name, point_id, session)

    if category_json.name is None and category_json.point_id is not None:
        name = category_db.name
        point_id = category_json.point_id
        await check_category_duplicate_on_point(name, point_id, session)

    if category_json.name is not None and category_json.point_id is None:
        name = category_json.name
        point_id = category_db.point_id
        await check_category_duplicate_on_point(name, point_id, session)

    # Изменяем поля категории
    category_db = await category_crud.update(category_db, category_json, session)
    return category_db


@router.delete(
    '/{category_id}',
    response_model=CategoryBaseDB,
    # dependencies=[Depends(current_superuser)],
)
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Удаляет категорию.
    """
    # Проверка на существование категории в базе
    category_db = await check_exist(category_crud, category_id, session)

    # Удаляем категорию.
    category = await category_crud.remove(category_db, session)
    return category

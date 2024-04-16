from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.point.categories.category import (
    router as category_router
)
from app.api.endpoints.utils import get_current_user
from app.core.db import get_async_session
from app.crud.point import point_crud
from app.models.user import User

router = APIRouter(
    prefix='/points',
    tags=['points']
)

router.include_router(category_router)

templates = Jinja2Templates(directory='app/templates')


@router.get('/add')
async def get_point_add_page(
    request: Request,
    point_id: int = None,
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для получения формы добавления новой точки."""

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    return templates.TemplateResponse(
        '/point/add-point.html',
        {'request': request,
         'title': 'Добавление точки'}
    )


@router.post('/add')
async def add_point(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для обработки добавления новой точки. """

    # TODO: Добавить обработку данных из формы.

    pass


@router.get('/{point_id}')
async def get_point(
        point_id: int,
        request: Request,
        current_user: Optional[User] = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    point = await point_crud.get(
        session=session,
        obj_id=point_id
    )
    points = await point_crud.point_by_id(point_id, session)

    if current_user.is_admin:
        return templates.TemplateResponse(
            '/point/point.html',
            {
                'request': request,
                'point': points,
            }
        )

    elif current_user.is_superadmin:
        return templates.TemplateResponse(
            '/point/point.html',
            {
                'request': request,
                'point': points,
                'from_superadmin': True

            }
        )

    else:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )


@router.get('/{point_id}/edit')
async def get_point_edit_page(
    request: Request,
    point_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения страницы редактирования точки. """

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    point = await point_crud.get(session, point_id)

    return templates.TemplateResponse(
        '/point/edit-point.html',
        {'request': request,
         'point': point}
    )


@router.post('/{point_id}/edit')
async def update_point(
    request: Request,
    point_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для обработки изменения точки. """

    # TODO: Добавить обработку изменений из формы.

    pass


@router.get('/{point_id}/delete')
async def delete_point(
    request: Request,
    point_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для удаления точки. """

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    # TODO: Добавить обработку удаления точки.

    pass

# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.api.validators import check_fields_duplicate, check_exist
# from app.core.db import get_async_session
# from app.crud import point_crud
# from app.models import Point
# from app.schemas.point import PointDB, PointCreate, PointUpdate, PointFullDB
#
# router = APIRouter()
#
#
# @router.post(
#     '/',
#     response_model=PointDB,
#     response_model_exclude_none=True,
#     # dependencies=[Depends(current_superuser)],
# )
# async def create_new_point(
#     new_point_json: PointCreate,
#     session: AsyncSession = Depends(get_async_session),
# ) -> Point:
#     """
#     Создание автомойки.
#     Только для суперюзеров.
#     """
#     # Словарь с данными, которые нужно проверить на уникальность.
#     fields_for_check = {
#         'name': new_point_json.name,
#         'address': new_point_json.address
#     }
#     # Проверка на уникальность всех данных
#     await check_fields_duplicate(point_crud, fields_for_check, session)
#     # Создание автомойки
#     new_point_db = await point_crud.create(new_point_json, session)
#     return new_point_db
#
#
# @router.get(
#     '/',
#     response_model=list[PointDB],
#     response_model_exclude_none=True,
# )
# async def get_all_points(
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Возвращает список всех автомоек."""
#     return await point_crud.get_multi(session)
#
#
# @router.patch(
#     '/{point_id}',
#     response_model=PointDB,
#     # dependencies=[Depends(current_superuser)],
# )
# async def update_point(
#     point_id: int,
#     point_json: PointUpdate,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """
#     Только для суперюзеров.
#
#     Редактирование автомойки.
#     """
#
#     # Проверка на существование автомойки в базе
#     project_db = await check_exist(point_crud, point_id, session)
#
#     # Проверка на уникальность переданных данных
#     if point_json.name is not None:
#         fields_for_check = {'name': point_json.name, }
#         await check_fields_duplicate(point_crud, fields_for_check, session)
#     if point_json.address is not None:
#         fields_for_check = {'address': point_json.address, }
#         await check_fields_duplicate(point_crud, fields_for_check, session)
#
#     # Изменяем поля автомойки
#     return await point_crud.update(project_db, point_json, session)
#
#
# @router.delete(
#     '/{point_id}',
#     response_model=PointDB,
#     # dependencies=[Depends(current_superuser)],
# )
# async def delete_point(
#     point_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """
#     Только для суперюзеров.
#
#     Удаляет автомойку.
#     """
#     # Проверка на существование автомойки в базе
#     point_db = await check_exist(point_crud, point_id, session)
#
#     # Удаляем поля автомойки
#     point = await point_crud.remove(point_db, session)
#     return point
#
#
# @router.get(
#     '/{point_id}',
#     response_model=list[PointFullDB],
#     response_model_exclude_none=True,
# )
# async def get_all_data_by_point(
#     point_id,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Возвращает все данные по автомойке."""
#
#     # Проверка на существование автомойки в базе
#     await check_exist(point_crud, point_id, session)
#
#     return await point_crud.get_all_by_id(point_id, session)

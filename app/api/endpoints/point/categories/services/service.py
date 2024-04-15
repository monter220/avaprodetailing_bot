from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.utils import get_current_user
from app.core.db import get_async_session
from app.crud.category import category_crud
from app.crud.service import service_crud
from app.models.user import User


router = APIRouter(
    prefix='/services',
    tags=['services']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/add')
async def get_service_add_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для получения страницы добавления услуги. """

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    categories = await category_crud.get_multi(session)

    return templates.TemplateResponse(
        'point/category/add-service.html',
        {'request': request,
         'categories': categories}
    )


@router.post('/add')
async def create_category(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки добавления услуги. """

    # TODO: Добавить обработку добавления услуги.

    pass


@router.get('/{service_id}')
async def get_service_edit_page(
    request: Request,
    service_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения шаблона изменения услуги. """

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    service = await service_crud.get(service_id, session)
    categories = await category_crud.get_multi(session)

    return templates.TemplateResponse(
        'point/category/edit-service.html',
        {'request': request,
         'service': service,
         'categories': categories}
    )


@router.post('/{service_id}')
async def update_category(
    request: Request,
    service_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки изменения категории услуг. """

    # TODO: Добавить обработку изменения услуги.

    pass


@router.get('{service_id}/delete')
async def delete_category(
    request: Request,
    service_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Функция для удаления категории."""

    # TODO: Добавить обработку удаления услуги.

    pass


# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.validators import (
#     check_exist,
#     check_service_duplicate_on_point
# )
# from app.core.db import get_async_session
# from app.crud import service_crud, point_crud, category_crud
# from app.models import Service
# from app.schemas.service import ServiceDB, ServiceCreate, ServiceUpdate

# router = APIRouter()


# # @router.post(
# #     '/',
# #     response_model=ServiceDB,
# #     response_model_exclude_none=True,
# #     # dependencies=[Depends(current_superuser)],
# # )
# # async def create_new_service(
# #     new_service_json: ServiceCreate,
# #     session: AsyncSession = Depends(get_async_session),
# # ) -> Service:
# #     """
# #     Создание услуги.
# #     Только для суперюзеров.
# #     """

# #     # Проверка на существование автомойки.
# #     await check_exist(point_crud, new_service_json.point_id, session)

# #     # Проверка на существование категории услуг.
# #     await check_exist(category_crud, new_service_json.category_id, session)

# #     # Проверка на уникальность услуги на автомойке
# #     await check_service_duplicate_on_point(
# #         new_service_json.name,
# #         new_service_json.point_id,
# #         session
# #     )
# #     # Создание услуги
# #     new_service_db = await service_crud.create(new_service_json, session)
# #     return new_service_db


# # @router.get(
# #     '/',
# #     response_model=list[ServiceDB],
# #     response_model_exclude_none=True,
# # )
# # async def get_all_services(
# #     session: AsyncSession = Depends(get_async_session),
# # ):
# #     """Возвращает список всех услуг."""
# #     return await service_crud.get_multi(session)


# # @router.get(
# #     '/{category_id}',
# #     response_model=list[ServiceDB],
# #     response_model_exclude_none=True,
# # )
# # async def get_services_by_category(
# #     category_id: int,
# #     session: AsyncSession = Depends(get_async_session),
# # ):
# #     """Возвращает список всех услуг с определенной категорией."""

# #     # Проверка на существование категории услуг.
# #     await check_exist(category_crud, category_id, session)
# #     return await service_crud.get_services_by_category(category_id, session)


# # @router.get(
# #     '/{point_id}',
# #     response_model=list[ServiceDB],
# #     response_model_exclude_none=True,
# # )
# # async def get_services_by_point(
# #     point_id: int,
# #     session: AsyncSession = Depends(get_async_session),
# # ):
# #     """Возвращает список всех услуг с определенной автомойки."""

# #     # Проверка на существование автомойки.
# #     await check_exist(point_crud, point_id, session)
# #     return await service_crud.get_services_by_point(point_id, session)


# # @router.get(
# #     '/{point_id}/{category_id}',
# #     response_model=list[ServiceDB],
# #     response_model_exclude_none=True,
# # )
# # async def get_services_by_point_category(
# #     point_id: int,
# #     category_id: int,
# #     session: AsyncSession = Depends(get_async_session),
# # ):
# #     """Возвращает список всех услуг с определенной автомойки и категории."""

# #     # Проверка на существование автомойки.
# #     await check_exist(point_crud, point_id, session)

# #     # Проверка на существование категории услуг.
# #     await check_exist(category_crud, category_id, session)

# #     return await service_crud.get_services_by_point_category(
# #         point_id,
# #         category_id,
# #         session
# #     )


# # @router.patch(
# #     '/{service_id}',
# #     response_model=ServiceDB,
# #     # dependencies=[Depends(current_superuser)],
# # )
# # async def update_service(
# #     service_id: int,
# #     service_json: ServiceUpdate,
# #     session: AsyncSession = Depends(get_async_session),
# # ):
# #     """
# #     Только для суперюзеров.

# #     Редактирование услуги.
# #     """

# #     # Проверка на существование услуги в базе.
# #     service_db = await check_exist(service_crud, service_id, session)

# #     # Проверка на существование автомойки.
# #     await check_exist(point_crud, service_json.point_id, session)

# #     # Проверка на существование категории услуг.
# #     await check_exist(category_crud, service_json.category_id, session)

# #     # Проверка на уникальность переданных данных
# #     if service_json.name is not None:
# #         await check_service_duplicate_on_point(
# #             service_json.name,
# #             service_json.point_id,
# #             session
# #         )

# #     # Изменяем поля услуги
# #     return await service_crud.update(service_db, service_json, session)


# # @router.delete(
# #     '/{service_id}',
# #     response_model=ServiceDB,
# #     # dependencies=[Depends(current_superuser)],
# # )
# # async def delete_service(
# #     service_id: int,
# #     session: AsyncSession = Depends(get_async_session),
# # ):
# #     """
# #     Только для суперюзеров.

# #     Удаляет услугу.
# #     """
# #     # Проверка на существование услуги в базе
# #     service_db = await check_exist(service_crud, service_id, session)

# #     # Удаляем услугу.
# #     service = await service_crud.remove(service_db, session)
# #     return service

from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.point.categories.services.service import (
    router as service_router
)
from app.api.endpoints.utils import get_current_user
from app.core.db import get_async_session
from app.crud.category import category_crud
from app.models.user import User


router = APIRouter(
    prefix='/categories',
    tags=['categories']
)

router.include_router(service_router)

templates = Jinja2Templates(directory='app/templates')


@router.get('/')
async def get_categories_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения страницы со списком категорий. """

    if not current_user:
        return RedirectResponse(
            url='/registration',
            status_code=status.HTTP_403_FORBIDDEN
        )

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    categories = await category_crud.get_multi(session)

    return templates.TemplateResponse(
        'point/category/categories.html',
        {'request': request,
         'categories': categories}
    )


@router.get('/add')
async def get_category_add_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения страницы добавления категории услуг. """

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    return templates.TemplateResponse(
        'point/category/add-category.html',
        {'request': request}
    )


@router.post('/add')
async def create_category(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки добавления категории. """

    # TODO: Добавить обработку добавления категории.

    pass


@router.get('/{category_id}')
async def get_category_edit_page(
    request: Request,
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения шаблона изменения услуги. """

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )

    category = await category_crud.get(category_id, session)

    return templates.TemplateResponse(
        'point/category/edit-category.html',
        {'request': request,
         'category': category}
    )


@router.post('/{category_id}')
async def update_category(
    request: Request,
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки изменения категории услуг. """

    # TODO: Добавить обработку изменения услуги.

    pass


@router.get('{category_id}/delete')
async def delete_category(
    request: Request,
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Функция для удаления категории."""

    # TODO: Добавить обработку удаления услуги.

    pass


# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.validators import check_fields_duplicate, check_exist
# from app.core.db import get_async_session
# from app.crud.category import category_crud
# from app.models import Category
# from app.schemas.category import CategoryDB, CategoryCreate, CategoryUpdate, \
#     CategoryServicesDB


# @router.post(
#     '/',
#     response_model=CategoryDB,
#     response_model_exclude_none=True,
#     # dependencies=[Depends(current_superuser)],
# )
# async def create_new_category(
#     new_category_json: CategoryCreate,
#     session: AsyncSession = Depends(get_async_session),
# ) -> Category:
#     """
#     Создание категории услуг.
#     Только для суперюзеров.
#     """
#     # Словарь с данными, которые нужно проверить на уникальность.
#     fields_for_check = {
#         'name': new_category_json.name,
#     }
#     # Проверка на уникальность всех данных
#     await check_fields_duplicate(category_crud, fields_for_check, session)
#     # Создание категории услуг
#     new_category_db = await category_crud.create(new_category_json, session)
#     return new_category_db


# @router.get(
#     '/full',
#     response_model=list[CategoryServicesDB],
#     response_model_exclude_none=True,
# )
# async def get_all_categories(
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Возвращает список всех категорий и услуг."""
#     return await category_crud.get_all_categories_and_services(session)


# @router.get(
#     '/',
#     response_model=list[CategoryDB],
#     response_model_exclude_none=True,
# )
# async def get_all_categories(
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """Возвращает список всех категорий."""
#     return await category_crud.get_multi(session)


# @router.patch(
#     '/{category_id}',
#     response_model=CategoryDB,
#     # dependencies=[Depends(current_superuser)],
# )
# async def update_category(
#     category_id: int,
#     category_json: CategoryUpdate,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """
#     Только для суперюзеров.

#     Редактирование категории.
#     """

#     # Проверка на существование категории в базе
#     category_db = await check_exist(category_crud, category_id, session)

#     # Проверка на уникальность переданных данных
#     if category_json.name is not None:
#         fields_for_check = {'name': category_json.name, }
#         await check_fields_duplicate(category_crud, fields_for_check, session)

#     # Изменяем поля категории
#     return await category_crud.update(category_db, category_json, session)


# @router.delete(
#     '/{category_id}',
#     response_model=CategoryDB,
#     # dependencies=[Depends(current_superuser)],
# )
# async def delete_category(
#     category_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     """
#     Только для суперюзеров.

#     Удаляет категорию.
#     """
#     # Проверка на существование категории в базе
#     category_db = await check_exist(category_crud, category_id, session)

#     # Удаляем категорию.
#     category = await category_crud.remove(category_db, session)
#     return category

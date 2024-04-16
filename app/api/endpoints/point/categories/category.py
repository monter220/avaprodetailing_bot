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
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.api.validators import (
    check_is_superadmin,
    check_category_duplicate_on_point
)


router = APIRouter(
    prefix='/{point_id}/categories',
    tags=['categories']
)

router.include_router(service_router)

templates = Jinja2Templates(directory='app/templates')


@router.get('/')
async def get_categories_page(
    request: Request,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения страницы со списком категорий. """

    check_is_superadmin(current_user)

    categories = await category_crud.get_all_categories_by_point_id(
        point_id=point_id,
        session=session
    )

    return templates.TemplateResponse(
        'point/category/categories.html',
        {
            'request': request,
            'point_id': point_id,
            'categories': categories,
        }
    )


@router.get('/add')
async def get_category_add_page(
    request: Request,
    point_id: int,
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения страницы добавления категории услуг. """

    check_is_superadmin(current_user)

    return templates.TemplateResponse(
        'point/category/add-category.html',
        {'request': request,
         'point_id': point_id}
    )


@router.post('/add')
async def create_category(
    request: Request,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки добавления категории. """
    check_is_superadmin(current_user)

    form_data = await request.form()

    category_data = {
        'name': form_data['name'],
        'description': form_data['desc'],
        'point_id': point_id
    }

    errors = []

    # Проверка на уникальность категории на точке
    try:
        await check_category_duplicate_on_point(
            name=category_data['name'],
            point_id=point_id,
            session=session
        )
    except Exception as e:
        errors.append(str(e))

        return templates.TemplateResponse(
            'point/category/add-category.html',
            {'request': request,
             'point_id': point_id,
             'errors': errors}
        )

    # Создание категории, с применением pydantic-схемы
    # для валидации входных данных
    try:
        await category_crud.create(
            obj_in=CategoryCreate(**category_data),
            session=session,
            model='Category',
            user=current_user
        )
    except Exception as e:
        errors.append(str(e))

        return templates.TemplateResponse(
            'point/category/add-category.html',
            {'request': request,
             'point_id': point_id,
             'errors': errors}
        )

    # Редирект на страницу категорий, привязанных к точке,
    # при успешном создании категории
    return RedirectResponse(
        url=f'/points/{point_id}/categories',
        status_code=status.HTTP_302_FOUND
    )


@router.get('/{category_id}')
async def get_category_edit_page(
    request: Request,
    category_id: int,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения шаблона изменения услуги. """

    check_is_superadmin(current_user)

    category = await category_crud.get(
        obj_id=category_id,
        session=session
    )

    # Если категория не найдена - редирект на страницу категорий,
    # привязанных к точке
    if category is None:
        return RedirectResponse(
            url=f'/points/{point_id}/categories',
            status_code=status.HTTP_302_FOUND
        )

    return templates.TemplateResponse(
        'point/category/edit-category.html',
        {
            'request': request,
            'point_id': point_id,
            'category': category
        }
    )


@router.post('/{category_id}')
async def update_category(
    request: Request,
    category_id: int,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки изменения категории услуг. """
    check_is_superadmin(current_user)

    from_data = await request.form()

    category_update_data = {
        'name': from_data['name'],
        'description': from_data['desc']
    }

    errors = []

    # Здесь не проверяем, что категория найдена,
    # подразумевается, что этот сценарий отрабатывается в get-запросе
    category = await category_crud.get(
        obj_id=category_id,
        session=session
    )

    # Проверка на уникальность названия категории на точке
    try:
        await check_category_duplicate_on_point(
            name=category_update_data['name'],
            point_id=point_id,
            session=session
        )
    except Exception as e:
        errors.append(str(e))

        return templates.TemplateResponse(
            'point/category/edit-category.html',
            {'request': request,
             'category': category,
             'point_id': point_id,
             'errors': errors}
        )

    # Обновление категории, с применением pydantic-схемы,
    # для валидации входных данных
    try:
        await category_crud.update(
            db_obj=category,
            obj_in=CategoryUpdate(**category_update_data),
            session=session,
            model='Category',
            user=current_user
        )
    except Exception as e:
        errors.append(str(e))

        return templates.TemplateResponse(
            'point/category/edit-category.html',
            {'request': request,
             'category': category,
             'point_id': point_id,
             'errors': errors}
        )

    # Редирект на страницу категорий, привязанных к точке,
    # при успешном обновлении категории
    return RedirectResponse(
        url=f'/points/{point_id}/categories',
        status_code=status.HTTP_302_FOUND
    )


@router.get('{category_id}/delete')
async def delete_category(
    request: Request,
    category_id: int,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Функция для удаления категории."""
    check_is_superadmin(current_user)

    category = await category_crud.get(
        obj_id=category_id,
        session=session
    )

    # Т.к. это get-запрос, то проверяем, что указанная точка существует
    if category is None:
        return RedirectResponse(
            url=f'/points/{point_id}',
            status_code=status.HTTP_302_FOUND
        )

    errors = []

    # Удаление категории
    try:
        await category_crud.remove(
            db_obj=category,
            user=current_user,
            session=session,
            model='Category'
        )
    except Exception as e:
        errors.append(str(e))

        return templates.TemplateResponse(
            'point/category/edit-category.html',
            {'request': request,
             'category': category,
             'point_id': point_id,
             'errors': errors}
        )

    # Редирект на страницу категорий, привязанных к точке,
    # при успешном удалении категории
    return RedirectResponse(
        url=f'/points/{point_id}/categories',
        status_code=status.HTTP_302_FOUND
    )

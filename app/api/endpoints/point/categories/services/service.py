from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.utils import get_current_user
from app.core.config import settings
from app.core.db import get_async_session
from app.crud.category import category_crud
from app.crud.service import service_crud
from app.models.user import User
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.api.validators import (
    check_is_superadmin,
    check_service_duplicate_in_category
)


router = APIRouter(
    prefix='/{category_id}/services',
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
    check_is_superadmin(current_user)

    categories = await category_crud.get_multi(session)

    return templates.TemplateResponse(
        'point/category/service/add-service.html',
        {
            'request': request,
            'categories': categories,
        }
    )


@router.post('/add')
async def create_service(
    request: Request,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки добавления услуги. """
    check_is_superadmin(current_user)

    form_data = await request.form()

    service_data = {
        'name': form_data.get('name'),
        'description': form_data.get('descr'),
        'cost': int(form_data.get('cost')),
        'default_bonus': int(form_data.get('bonus', settings.default_bonus)),
        'category_id': int(form_data.get('category')),
    }

    errors = []

    # Проверяем, что в данной категории нет услуги с таким именем
    try:
        await check_service_duplicate_in_category(
            name=service_data['name'],
            category_id=service_data['category_id'],
            session=session
        )
    except Exception as e:
        errors.append(str(e))

        categories = await category_crud.get_multi(session)

        return templates.TemplateResponse(
            'point/category/service/add-service.html',
            {'request': request,
             'errors': errors,
             'categories': categories}
        )

    # Создаем услугу с применением pydantic-схемы для валидации
    try:
        service = await service_crud.create(
            obj_in=ServiceCreate(**service_data),
            session=session,
            model='Service',
            user=current_user
        )

    except Exception as e:
        errors.append(str(e))

        categories = await category_crud.get_multi(session)

        return templates.TemplateResponse(
            'point/category/service/add-service.html',
            {'request': request,
             'errors': errors,
             'categories': categories}
        )

    # Перенаправляем на страницу категории, к которой принадлежит новая услуга
    return RedirectResponse(
        url=f'/points/{point_id}/categories/{service.category_id}',
        status_code=status.HTTP_302_FOUND
    )


@router.get('/{service_id}')
async def get_service_edit_page(
    request: Request,
    service_id: int,
    category_id: int,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для отображения шаблона изменения услуги. """
    check_is_superadmin(current_user)

    service = await service_crud.get(
        obj_id=service_id,
        session=session
    )

    # Перенаправляем на страницу категории, если услуга не найдена
    if service is None:
        return RedirectResponse(
            url=f'/categories/{category_id}',
            status_code=status.HTTP_302_FOUND,
        )

    categories = await category_crud.get_multi(session)

    return templates.TemplateResponse(
        'point/category/service/edit-service.html',
        {
            'request': request,
            'service': service,
            'point_id': point_id,
            'categories': categories,
        }
    )


@router.post('/{service_id}')
async def update_service(
    request: Request,
    service_id: int,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для обработки изменения услуги. """
    check_is_superadmin(current_user)

    service = await service_crud.get(
        obj_id=service_id,
        session=session)

    form_data = await request.form()
    errors = []

    service_update_data = {
        'name': form_data.get('name'),
        'description': form_data.get('descr'),
        'cost': form_data.get('cost'),
        'default_bonus': form_data.get('bonus'),
        'category_id': form_data.get('category'),
    }

    # Преобразуем значения cost, bonus и category_id в числа
    if service_update_data['cost'] is not None:
        service_update_data['cost'] = int(service_update_data['cost'])

    if service_update_data['default_bonus'] is not None:
        service_update_data['default_bonus'] = int(
            service_update_data['default_bonus']
        )

    if service_update_data['category_id'] is not None:
        service_update_data['category_id'] = int(
            service_update_data['category_id']
        )

    # Проверяем, что в данной категории нет услуги с таким именем
    try:
        await check_service_duplicate_in_category(
            name=service_update_data['name'],
            category_id=service_update_data['category_id'],
            session=session
        )
    except Exception as e:
        errors.append(str(e))

        categories = await category_crud.get_multi(session)

        return templates.TemplateResponse(
            'point/category/service/edit-service.html',
            {'request': request,
             'errors': errors,
             'categories': categories}
        )

    # Обновляем услугу с применением pydantic-схемы для валидации
    await service_crud.update(
        db_obj=service,
        obj_in=ServiceUpdate(**service_update_data),
        session=session,
        model='Service',
        user=current_user
    )

    # Перенаправляем на страницу категории, к которой принадлежит услуга
    return RedirectResponse(
        url=f'/points/{point_id}',
        status_code=status.HTTP_302_FOUND
    )


@router.get('/{service_id}/delete')
async def delete_service(
    request: Request,
    service_id: int,
    category_id: int,
    point_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Функция для удаления категории."""
    check_is_superadmin(current_user)

    service = await service_crud.get(service_id, session)

    # Перенаправляем на страницу категории, если услуга не найдена
    if service is None:
        return RedirectResponse(
            url=f'/points/{point_id}/categories/{category_id}',
            status_code=status.HTTP_302_FOUND
        )

    # Удаляем услугу
    await service_crud.remove(
        db_obj=service,
        session=session,
        model='Service',
        user=current_user
    )

    # Перенаправляем на страницу категории, к которой принадлежит услуга
    return RedirectResponse(
        url=f'/points/{point_id}',
        status_code=status.HTTP_302_FOUND
    )

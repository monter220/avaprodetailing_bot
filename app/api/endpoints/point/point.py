from typing import Optional

from fastapi import APIRouter, Depends, Request, status, Form
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
from app.schemas.point import PointUpdate, PointCreate


router = APIRouter(
    prefix='/points',
    tags=['points']
)

router.include_router(category_router)

templates = Jinja2Templates(directory='app/templates')


@router.get('/add')
async def get_point_add_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для получения формы добавления новой точки."""

    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND,
        )

    return templates.TemplateResponse(
        '/point/add-point.html',
        {
            'request': request,
            'title': 'Добавление точки',
        }
    )


@router.post('/add')
async def add_point(
    request: Request,
    name: str = Form(...),
    address: str = Form(...),
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Функция для обработки добавления новой точки. """
    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND,
        )

    point = {
        'name': name,
        'address': address,
    }
    point = await point_crud.create(
        obj_in=PointCreate(**point),
        session=session,
        model='Point',
        user=current_user,
    )

    return RedirectResponse(
        request.url_for('get_point', point_id=point.id),
        status_code=status.HTTP_302_FOUND,
    )


@router.get('/{point_id}')
async def get_point(
        point_id: int,
        request: Request,
        current_user: Optional[User] = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):

    points = await point_crud.point_by_id(point_id, session)

    if current_user.is_superadmin:
        return templates.TemplateResponse(
            '/point/point.html',
            {
                'request': request,
                'point': points,
                'from_superadmin': True

            }
        )
    else:
        return templates.TemplateResponse(
            '/point/point.html',
            {
                'request': request,
                'point': points,
            }
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

    point = await point_crud.get(point_id, session)

    return templates.TemplateResponse(
        '/point/edit-point.html',
        {
            'request': request,
            'point': point,
            'title': 'Редактирование точки',
        }
    )


@router.post('/{point_id}/edit')
async def update_point(
    request: Request,
    point_id: int,
    name: str = Form(...),
    address: str = Form(...),
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для обработки изменения точки. """
    point = await point_crud.get(point_id, session)
    if point:
        new_data = {
            'name': name,
            'address': address,
        }
        obj_in = PointUpdate(**new_data)
        await point_crud.update(
            db_obj=point,
            obj_in=obj_in,
            user=current_user,
            session=session,
            model='Point',
        )
        return RedirectResponse(
            url=f'/points/{point_id}',
            status_code=status.HTTP_302_FOUND,
        )


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

    point = await point_crud.get(point_id, session)
    if point:
        await point_crud.remove(
            db_obj=point, user=current_user, session=session)

    return RedirectResponse(
        url='/users/me',
        status_code=status.HTTP_302_FOUND,
    )

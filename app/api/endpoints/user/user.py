from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import car_crud, user_crud, point_crud
from app.models import User
from app.schemas.user import UserUpdate
from app.api.endpoints.utils import get_current_user, get_tg_id_cookie
from app.api.endpoints.user.car.car import router as car_router
from app.api.endpoints.user.search.search import router as search_router
from app.api.validators import (
    check_user_exist,
    check_user_by_tg_exist,
    check_admin_or_myprofile_car,
)


router = APIRouter(
    prefix="/users",
    tags=["user"]
)

router.include_router(car_router)
router.include_router(search_router)

templates = Jinja2Templates(directory="app/templates")


@router.get("/me")
@router.post('/me')
async def get_profile_template(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения собственного профиля пользователя."""

    cars = await car_crud.get_user_cars(
        session=session,
        user_id=current_user.id
    )
    points = await point_crud.all_points(session=session)

    return templates.TemplateResponse(
        "user/profile.html",
        {
            "request": request,
            "title": 'Профиль пользователя',
            "user": current_user,
            "cars": cars,
            'points': points
        }
    )


@router.get("/{user_id}")
async def process_redirect_from_phone(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    user_telegram_id: str = Depends(get_tg_id_cookie),
):
    """Функция для обработки редиректа из /search."""

    await check_admin_or_myprofile_car(
        user_id=user_id,
        user_telegram_id=int(user_telegram_id),
        session=session,
    )
    found_user = await user_crud.get(obj_id=user_id, session=session)
    cars = await car_crud.get_user_cars(session=session, user_id=user_id)
    points = await point_crud.all_points(session=session)

    if current_user.role in (2,3):
        return templates.TemplateResponse(
            "user/profile.html",
            {
                "request": request,
                "user": found_user,
                "page_title": 'Профиль пользователя',
                "from_admin": True,
                "from_search": True,
                "cars": cars,
                'points': points
            }
        )
    else:
        return RedirectResponse(
            url='/users/me',
            # status_code=status.HTTP_403_FORBIDDEN
        )


@router.get("/{user_id}/edit")
async def get_edit_profile_template(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie),
):
    """Функция для получения формы редактирования профиля пользователя."""
    await check_admin_or_myprofile_car(
        user_id=user_id,
        user_telegram_id=int(user_telegram_id),
        session=session,
    )
    await check_user_exist(user_id, session)
    user = await user_crud.get(user_id, session)
    return templates.TemplateResponse(
        "user/profile-edit.html",
        {
            "request": request,
            "user": user
        }
    )


@router.post("/{user_id}/edit")
async def process_edit_profile(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie),
):
    """Функция для обработки формы редактирования профиля пользователя."""
    await check_user_exist(user_id, session)
    user = await user_crud.get(user_id, session)
    author = await check_user_by_tg_exist(int(user_telegram_id), session)
    form_data = await request.form()
    new_user_data = dict.fromkeys(
        ['surname', 'name', 'patronymic', 'date_birth'])
    new_user_data['surname'] = form_data.get('surname')
    new_user_data['name'] = form_data.get('name')
    new_user_data['patronymic'] = form_data.get('patronymic')
    new_user_data['date_birth'] = form_data.get('date_birth')
    await user_crud.update(
        db_obj=user,
        obj_in=UserUpdate(**new_user_data),
        user=author,
        session=session,
        model='User',
    )
    return RedirectResponse(
        f'/users/{user_id}',
        status_code=status.HTTP_302_FOUND,
    )

@router.get("/{user_id}/payments-history")
async def get_payments_template(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для отображения шаблона с платежами."""

    # TODO: Добавить обработку шаблона с платежами.
    # На данный момент модели платежей нет.
    # В шаблон в контексте должны передаваться payments,
    # список объектов платежей для данного пользователя.

    pass

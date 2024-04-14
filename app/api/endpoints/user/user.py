from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.utils import get_current_user
from app.api.endpoints.user.car.car import router as car_router
from app.api.endpoints.user.search.search import router as search_router
from app.core.db import get_async_session
from app.crud.car import car_crud
from app.crud.user import user_crud
from app.models import User


router = APIRouter(
    prefix="/users",
    tags=["user"]
)

router.include_router(car_router)
router.include_router(search_router)

templates = Jinja2Templates(directory="app/templates")


@router.get("/me")
async def get_profile_template(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения собственного профиля пользователя."""

    cars = await car_crud.get_user_cars(
        session=session,
        user_id=current_user.id
    )

    return templates.TemplateResponse(
        "user/profile.html",
        {
            "request": request,
            "page_title": 'Профиль пользователя',
            "user": current_user,
            "cars": cars
        }
    )


@router.post("/{user_id}")
async def process_redirect_from_phone(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Функция для обработки редиректа из /search."""

    found_user = await user_crud.get(obj_id=user_id, session=session)

    cars = await car_crud.get_user_cars(session=session, user_id=user_id)

    if current_user.is_admin:
        return templates.TemplateResponse(
            "user/user-profile.html",
            {
                "request": request,
                "user": found_user,
                "page_title": 'Профиль пользователя',
                "from_admin": True,
                "from_search": True,
                "cars": cars
            }
        )
    elif current_user.is_superadmin:
        return templates.TemplateResponse(
            "user/user-profile.html",
            {
                "request": request,
                "user": found_user,
                "page_title": 'Профиль пользователя',
                "from_superadmin": True,
                "from_search": True,
                "cars": cars
            }
        )
    else:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )


@router.get("/{user_id}/edit")
async def get_edit_profile_template(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Функция для получения формы редактирования профиля пользователя."""

    user = await user_crud.get(obj_id=user_id, session=session)

    if (
        current_user.id == user.id
        or current_user.is_admin
        or current_user.is_superadmin
    ):

        return templates.TemplateResponse(
            "user/profile-edit.html",
            {
                "request": request,
                "user": user
            }
        )

    else:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )


@router.post("/{user_id}/edit")
async def process_edit_profile(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для обработки формы редактирования профиля пользователя."""

    # TODO: Добавить обработку формы редактирования профиля пользователя.

    pass


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

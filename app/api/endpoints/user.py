from fastapi import APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from starlette import status

from app.core.db import get_async_session
from app.crud import user_crud, car_crud
from app.api.validators import check_user_exist, check_user_by_tg_exist, check_admin_or_myprofile_car
from app.schemas.user import UserUpdate
from app.api.endpoints.guest import get_tg_id_cookie


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/profile/{user_id}")
async def get_profile_template(
    request: Request,
    user_id: int,
    user_telegram_id: str = Depends(get_tg_id_cookie),
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения шаблона профиля пользователя."""
    await check_admin_or_myprofile_car(
        user_id=user_id,
        user_telegram_id=int(user_telegram_id),
        session=session,
    )
    user = await user_crud.get(obj_id=user_id, session=session)
    cars = await car_crud.get_user_cars(session=session, user_id=user_id)

    return templates.TemplateResponse(
        "user/profile.html",
        {
            "request": request,
            "user": user,
            "cars": cars
        }
    )


@router.post("/profile/{user_id}")
async def process_redirect_from_phone(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Функция для обработки редиректа из /phone."""

    user = await user_crud.get(obj_id=user_id, session=session)
    cars = await car_crud.get_user_cars(session=session, user_id=user_id)

    return templates.TemplateResponse(
        "user/profile.html",
        {
            "request": request,
            "user": user,
            "cars": cars
        }
    )


@router.get("/profile/{user_id}/edit")
async def get_edit_profile_template(
        request: Request,
        user_id: int,
        user_telegram_id: str = Depends(get_tg_id_cookie),
        session: AsyncSession = Depends(get_async_session),
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


@router.post("/profile/{user_id}/edit")
async def process_edit_profile(
        request: Request,
        user_id: int,
        user_telegram_id: str = Depends(get_tg_id_cookie),
        session: AsyncSession = Depends(get_async_session),
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
        f'/user/profile/{user_id}',
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/profile/{user_id}/payments")
async def get_payments_template(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для отображения шаблона с платежами."""

    #TODO: Добавить обработку шаблона с платежами.
    # На данный момент модели платежей нет.
    # В шаблон в контексте должны передаваться payments,
    # список объектов платежей для данного пользователя.

    pass

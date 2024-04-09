from fastapi import APIRouter, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.car import car_crud
from app.crud.user import user_crud


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/profile/{user_id}")
async def get_profile_template(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения шаблона профиля пользователя."""

    user = await user_crud.get(obj_id=user_id, session=session)

    # TODO: Этого метода в круде автомобиля нет - нужно добавить.
    # cars = await car_crud.get_user_cars(session, user_id)

    return templates.TemplateResponse(
        "user/profile.html",
        {
            "request": request,
            "user": user,
            # "cars": cars
        }
    )


@router.get("/profile/{user_id}/edit")
async def get_edit_profile_template(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения формы редактирования профиля пользователя."""

    user = await user_crud.get(
        obj_id=user_id,
        session=session
    )

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
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для обработки формы редактирования профиля пользователя."""

    # TODO: Добавить обработку формы редактирования профиля пользователя.

    pass


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

"перенести в guest"
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserDB
from app.api.validators import check_duplicate


router = APIRouter()


@router.post(
    '/user',
    response_model=UserDB,
    response_model_exclude_none=True,
)
async def create_new_user(
        new_user: UserCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_duplicate(new_user.phone, session)
    new = await user_crud.create(
        obj_in=new_user, session=session, model='User')
    return new

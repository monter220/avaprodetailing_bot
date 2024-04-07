from fastapi import APIRouter, Depends, Request
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

    user = await user_crud.get(session, user_id)
    cars = await car_crud.get_user_cars(session, user_id)

    return templates.TemplateResponse(
        "user/profile.html",
        {
            "request": request,
            "user": user,
            "cars": cars
        }
    )

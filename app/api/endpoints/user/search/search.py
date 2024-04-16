from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db import get_async_session
from app.crud.user import user_crud


router = APIRouter(
    prefix="/me/search"
)

templates = Jinja2Templates(
    directory='app/templates'
)


@router.get('/phone-number/{phone_number}')
async def get_profile_page_from_qr(
    request: Request,
    phone_number: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Функция обработывает get-запросы, полученные из сканера qr-кодов. """

    user = await user_crud.get_user_by_phone_number(
        phone=phone_number,
        session=session
    )

    if not user:
        return RedirectResponse(
            url='/users/me/search/not-found',
            status_code=status.HTTP_302_FOUND
        )

    return RedirectResponse(
        url=f'/users/{user.id}',
        status_code=status.HTTP_302_FOUND
    )


@router.post('/phone-number')
async def get_profile_page(
    request: Request,
    phone: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Функция для поиска пользователя.
    Если полбзователь найден - перенаправляет на страницу пользователя.
    Если пользователь не найден - перенаправляет на страницу с ошибкой.
    """
    form_data = await request.form()
    phone_number = form_data.get('phone')

    found_user = await user_crud.get_user_by_phone_number(
        session=session,
        phone=phone_number,
    )

    if found_user:
        return RedirectResponse(
            url=f'/users/{found_user.id}',
            status_code=status.HTTP_302_FOUND
        )

    return RedirectResponse(
        url='/users/me/search/not-found',
        status_code=status.HTTP_302_FOUND,
    )


@router.get('/not-found')
async def get_not_found_page(
    request: Request,
):
    """Функция для получения страницы с ошибкой. """

    return templates.TemplateResponse(
        'user/search/user-not-found.html',
        {'request': request},
    )

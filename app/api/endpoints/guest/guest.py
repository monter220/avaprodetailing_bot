from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.endpoints.user.user import router as user_router
from app.core.db import get_async_session
from app.core.config import settings
from app.crud import user_crud, bonus_crud
from app.models import User
from app.schemas.user import UserCreate, UserUpdateTG
from app.api.endpoints.utils import get_current_user, get_tg_id_cookie
from app.api.validators import check_duplicate, check_user_by_tg_exist

router = APIRouter(
    tags=['guest']
)

templates = Jinja2Templates(
    directory='app/templates'
)


@router.get('/')
async def render_sign_in_template(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для рендеринга страницы из шаблона. """
    if current_user and not current_user.is_ban:
        return RedirectResponse(
            '/users/me',
            status_code=status.HTTP_302_FOUND,
        )

    return templates.TemplateResponse(
        'guest/sign-in.html',
        {'request': request,
         'title': 'Добро пожаловать!'}
    )


@router.get('/phone')
async def render_phone_template(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
):
    """
    Проверяет, есть ли Телеграм айди пользователя в БД.
    Если есть, то проверяет, есть ли у него номер телефона.
    Если есть - редиректит его согласно его роли.
    Если нет - открывает страницу для ввода номера.
    """

    if current_user and not current_user.is_ban and current_user.tg_id is not None:
        return RedirectResponse(
            '/users/me',
            status_code=status.HTTP_302_FOUND,
        )
    else:
        return templates.TemplateResponse(
            'guest/phone.html',
            {
                'request': request,
                'title': 'Введите номер телефона'
            }
        )


@router.post('/phone')
async def process_user_phone(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: int = Depends(get_tg_id_cookie),
):
    """Функция для редиректа пользователя, согласно его роли."""
    form_data = await request.form()
    phone_number = form_data.get('phone')

    errors = []

    try:
        user = await check_duplicate(phone_number, session)
    except Exception as e:
        errors.append(str(e))

        return templates.TemplateResponse(
            'guest/phone.html',
            {
                'request': request,
                'title': 'Введите номер телефона',
                'errors': errors,
            }
        )

    if not user:
        response = RedirectResponse(
            '/registration',
            status_code=status.HTTP_302_FOUND,
        )

        response.set_cookie(
            key='phone',
            value=phone_number,
            expires=settings.cookies_ttl,
        )

        return response

    await user_crud.update(
        db_obj=user,
        obj_in=UserUpdateTG(tg_id=user_telegram_id),
        user=user,
        session=session,
        model='User',
    )

    return RedirectResponse(user_router.url_path_for('get_profile_template'))


@router.get('/registration')
def render_registration_template(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для рендеринга страницы из шаблона. """
    if current_user:
        if current_user.is_admin or current_user.is_superadmin:
            return templates.TemplateResponse(
                'guest/registration.html',
                {
                    'request': request,
                    'from_admin': True,
                    'title': 'Регистрация',
                }
            )
        else:
            return RedirectResponse(
                user_router.url_path_for('get_profile_template'),
                status_code=status.HTTP_302_FOUND,
            )

    return templates.TemplateResponse(
        'guest/registration.html',
        {
            'request': request,
            'title': 'Регистрация',
        }
    )


@router.post('/registration')
async def registrate_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie),
):
    """Функция для регистрации пользователя."""

    form_data = await request.form()
    if form_data.get('phone'):
        phone = form_data.get('phone')
    else:
        phone = request.cookies.get('phone')

    surname = form_data.get('surname')
    name = form_data.get('name')
    patronymic = form_data.get('patronymic')
    date_birth = form_data.get('date_birth')
    author = await user_crud.get_user_by_telegram_id(
        user_telegram_id=int(user_telegram_id),
        session=session,
    )
    if author:
        user_create_data = {
            'phone': phone,
            'surname': surname,
            'name': name,
            'patronymic': patronymic,
            'date_birth': datetime.strptime(date_birth, '%Y-%m-%d'),
        }
    else:
        user_create_data = {
            'tg_id': user_telegram_id,
            'phone': phone,
            'surname': surname,
            'name': name,
            'patronymic': patronymic,
            'date_birth': datetime.strptime(date_birth, '%Y-%m-%d'),
        }

    user = await user_crud.create(
        obj_in=UserCreate(**user_create_data),
        session=session,
        model='User',
        user=author,
    )

    bonus = {
        'amount': settings.default_bonus,
        'user_id': user.id,
        'admin_id': settings.system_user_id,
        'is_active': True,
    }
    await bonus_crud.create_from_dict(bonus, session)

    if author:
        response = RedirectResponse(
            url=f'/users/{user.id}',
            status_code=status.HTTP_302_FOUND,
        )
    else:
        response = RedirectResponse(
            '/success_registration',
            status_code=status.HTTP_302_FOUND,
        )

    return response


@router.get('/success_registration')
async def render_success_registration_template(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie),
):
    """Функция для рендеринга страницы из шаблона. """
    user = await check_user_by_tg_exist(int(user_telegram_id), session)

    return templates.TemplateResponse(
        'guest/success_registration.html',
        {
            'request': request,
            'user_id': user.id,
            'title': 'Вы успешно зарегистрировались!',
        }
    )


@router.get('/call/{phone_number}')
async def render_phone_template(
    request: Request,
    phone_number: str,
):
    """Отображение шаблона для набора номера."""
    return templates.TemplateResponse(
        'guest/phone_number.html',
        {
            'request': request,
            'phone_number': phone_number,
            'title': 'Набор номера телефона',
        }
    )

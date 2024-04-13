from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db import get_async_session
from app.core.config import settings
from app.crud import user_crud
from app.models import User
from app.schemas.user import UserCreate, UserUpdateTG
from app.api.validators import check_duplicate, check_user_by_tg_exist


router = APIRouter(
    tags=['guest']
)

templates = Jinja2Templates(
    directory='app/templates'
)


async def get_tg_id_cookie(request: Request):
    """Функция для получения куки tg_id.  """
    return request.cookies.get('tg_id')


@router.get('/')
async def render_sign_in_template(request: Request):
    """Функция для рендеринга страницы из шаблона. """

    return templates.TemplateResponse(
        'guest/sign-in.html',
        {'request': request,
         'title': 'Добро пожаловать!'}
    )


@router.get('/phone')
async def render_phone_template(
    request: Request,
    user_telegram_id: str = Depends(get_tg_id_cookie),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Функция для рендеринга страницы из шаблона.
    Проверяет, есть ли Телеграм айди пользоваителя в бд.
    Если есть,то проверяет, есть ли у него номер телефона.
    Если есть - редиректит его, согласно его роли.
    Если нет - открывает страницу для ввода номера.
    """

    user: Optional[User] = await user_crud.get_user_by_telegram_id(
        user_telegram_id=int(user_telegram_id),
        session=session
    )

    if user is not None and user.phone is not None:

        if user.role == 3:  # Шаблонов и роутеров нет, superuser
            response = RedirectResponse('/superuser')
            return response

        elif user.role == 2:  # Шаблонов и роутеров нет, administrator
            response = RedirectResponse('/administrator')
            return response

        elif user.role == 1:  # user
            response = RedirectResponse(f'/user/profile/{user.id}')
            return response

        else:
            return templates.TemplateResponse(
                'guest/phone.html',
                {'request': request,
                 'title': 'Введите номер телефона'}
            )
    return templates.TemplateResponse(
        'guest/phone.html',
        {'request': request,
         'title': 'Введите номер телефона'}
    )


@router.post('/phone')
async def process_user_phone(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie)
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
            {'request': request,
             'title': 'Введите номер телефона',
             'errors': errors}
        )

    if not user:
        response = RedirectResponse(
            '/registration',
            status_code=status.HTTP_302_FOUND,
        )

        response.set_cookie(
            key='phone',
            value=phone_number,
            expires=settings.cookies_ttl
        )

        return response

    user = await user_crud.update(
        db_obj=user,
        obj_in=UserUpdateTG(tg_id=user_telegram_id),
        user=user,
        session=session,
        model='User',
    )

    if user.role == 3:  # Шаблонов и роутеров нет
        response = RedirectResponse('/superuser')
        return response

    elif user.role == 2:  # Шаблонов и роутеров нет
        response = RedirectResponse('/administrator')
        return response

    elif user.role == 1:  # Шаблонов и роутеров нет
        response = RedirectResponse(f'/user/profile/{user.id}')
        return response


@router.get('/registration')
def render_registration_template(request: Request):
    """Функция для рендеринга страницы из шаблона. """

    return templates.TemplateResponse(
        'guest/registration.html',
        {'request': request,
         'title': 'Регистрация'}
    )


@router.post('/registration')
async def registrate_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user_telegram_id: str = Depends(get_tg_id_cookie),
):
    """Функция для регистрации пользователя."""

    # Здесь обрабатывается только процесс регистрации
    # обычного пользователя, поля is_admin или is_superuser нету

    form_data = await request.form()
    phone = request.cookies.get('phone')

    surname = form_data.get('surname')
    name = form_data.get('name')
    patronymic = form_data.get('patronymic')
    date_birth = form_data.get('date_birth')

    user_create_data = {
        'tg_id': user_telegram_id,
        'phone': phone,
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'date_birth': datetime.strptime(date_birth, '%Y-%m-%d'),
    }

    await user_crud.create(
        obj_in=UserCreate(**user_create_data), session=session, model='User')

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
        {'request': request,
         'user_id': user.id,
         'title': 'Вы успешно зарегистрировались!'}
    )


# @router.post('/success_registration')
# def redirect_to_add_auto(request: Request):
#     # Здесь должен быть редирект на добавление авто
#     # если пользователь нажал да, либо редирект на профиль, если нет,
#     # этих веток пока нет.
#     pass

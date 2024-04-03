from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserDB
from app.api.validators import check_duplicate


router = APIRouter()

templates = Jinja2Templates(
    directory='app/templates'
)

@router.get('/')
def render_sign_in_template(request: Request):
    """Функция для рендеринга страницы из шаблона. """

    return templates.TemplateResponse(
        'sign-in.html',
        {'request': request}
    )


@router.get('/phone/{user_telegram_id}')
async def process_user_telegram_id(request: Request, user_telegram_id: str):
    """Промежуточный эндпойнт для добавления куки. """

    return RedirectResponse(
        '/phone', {'request': request}
    ).set_cookie(key='user_telegram_id', value=user_telegram_id)


@router.get('/phone')
def render_phone_template(request: Request):
    """Функция для рендеринга страницы из шаблона. """

    return templates.TemplateResponse(
        'phone.html',
        {'request': request}
    )


@router.post('/phone')
async def process_user_phone(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):

    """Функция для редиректа пользователя, согласно его роли."""

    form_data = await request.form()
    phone_number = form_data.get('phone')
    user_telegram_id = await request.cookies.get('user_telegram_id')

    user = await user_crud.phone_number_exist(phone_number, session)

    if not user:
        response = RedirectResponse('/registration')
        response.set_cookie(key='user_telegram_id', value=user_telegram_id)
        response.set_cookie(key='phone', value=phone_number)
        return response

    if user.tg_id is None:
        update_data = {'tg_id': user_telegram_id}
        user = await user_crud.update(user, update_data, session)

    if user.role.name == 'superuser':  # Шаблонов и роутеров нет
        response = RedirectResponse('/superuser')
        return response

    elif user.role.name == 'administrator':  # Шаблонов и роутеров нет
        response = RedirectResponse('/administrator')
        return response

    elif user.role.name == 'client':  # Шаблонов и роутеров нет
        response = RedirectResponse('/client')
        return response


@router.get('/registration')
def render_registration_template(request: Request):
    """Функция для рендеринга страницы из шаблона. """

    return templates.TemplateResponse(
        'registration.html',
        {'request': request}
    )


@router.post('/registration')
async def registrate_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для регистрации пользователя."""

    # Здесь обрабатывается только процесс регистрации
    # обычного пользователя, поля is_admin или is_superuser нету

    form_data = await request.form()
    telegram_id = request.cookies.get('user_telegram_id')
    phone = request.cookies.get('phone')

    surname = form_data.get('surname')
    name = form_data.get('name')
    patronymic = form_data.get('patronymic')
    date_birth = form_data.get('date_birth')

    user_create_data = {
        'tg_id': telegram_id,
        'phone': phone,
        'surname': surname,
        'name': name,
        'patronymic': patronymic,
        'date_birth': date_birth,
    }

    await user_crud.create(user_create_data, session)

    response = RedirectResponse('/success_registration')

    return response


@router.get('/success_registration')
def render_success_registration_template(request: Request):
    """Функция для рендеринга страницы из шаблона. """

    return templates.TemplateResponse(
        'success_registration.html',
        {'request': request}
    )


@router.post('/success_registration')
def redirect_to_add_auto(request: Request):
    # Здесь должен быть редирект на добавление авто
    # если пользователь нажал да, либо редирект на профиль, если нет,
    # этих веток пока нет.
    pass

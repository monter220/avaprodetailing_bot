from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.utils import get_current_user
from app.models import User
from app.core.db import get_async_session
from app.tasks.reports import send_report

router = APIRouter(
    prefix='/reports',
    tags=['reports']
)

templates = Jinja2Templates(directory="app/templates")


@router.get('/')
async def get_reports_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для получения страницы с отчётами."""
    if current_user.is_superadmin or current_user.is_admin:
        return templates.TemplateResponse(
            'reports/reports.html',
            {
                'request': request,
            }
        )
    else:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND,
        )


@router.get('/users')
async def get_users_report(
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Функция для получения отчётов пользователей."""
    if not (current_user.is_superadmin or current_user.is_admin):
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND,
        )

    send_report.delay(
        key='users',
        user_tg_id=current_user.tg_id,
    )

    return RedirectResponse(
        url='/users/me',
        status_code=status.HTTP_302_FOUND,
    )


@router.get('/orders')
async def get_orders_report(
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Функция для получения отчётов по услугам."""
    if not (current_user.is_superadmin or current_user.is_admin):
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND,
        )

    send_report.delay(
        key='orders',
        user_tg_id=current_user.tg_id,
        field_names=[
            'Дата', 'Номер машины', 'Стоимость', 'Бонусы', 'Телефон клиента',
        ],
    )

    return RedirectResponse(
        url='/users/me',
        status_code=status.HTTP_302_FOUND,
    )


@router.get('/payments')
async def get_orders_report(
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Функция для получения отчётов по оплатам."""
    if not (current_user.is_superadmin or current_user.is_admin):
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND,
        )

    send_report.delay(
        key='payments',
        user_tg_id=current_user.tg_id,
        field_names=[
            'Дата', 'Стоимость', 'Тип платежа',
        ],
    )

    return RedirectResponse(
        url='/users/me',
        status_code=status.HTTP_302_FOUND,
    )

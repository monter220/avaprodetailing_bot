from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.api.endpoints.utils import get_current_user
from app.models import User, Service, Order, Bonus
from app.services.excel import create_excel
from app.services.report import process_report
from app.services.telegram import send_excel, send_message
from app.core.db import get_async_session
from app.crud import car_crud, user_crud, service_crud, bonus_crud



router = APIRouter(
    prefix='/reports',
    tags=['reports']
)

templates = Jinja2Templates(directory="app/templates")


@router.get('/')
async def get_reports_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user)
):
    """Функция для получения страницы с  отчётами. """

    if current_user.is_superadmin:
        return templates.TemplateResponse(
            'reports/reports.html',
            {
                'request': request,
            }
        )
    else:
        return RedirectResponse(
            url='users/me',
            status_code=status.HTTP_403_FORBIDDEN
        )


@router.post('/')
async def process_reports(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """Функция для получения отчётов. """

    # TODO: Добавить получение отчёта и отправку его через Telegram.
    pass


@router.get('/users')
async def process_reports(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Функция для получения отчётов пользователей. """
    user = await user_crud.get(user_id, session)
    objects = await process_report(session=session, key='users')
    excel = create_excel(objects)
    await send_excel(excel=excel, filename='users.xlsx', chat_id=user.tg_id)
    return status.HTTP_200_OK

from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.api.endpoints.utils import get_current_user
from app.models import User, Service, Order, Bonus
from app.services.excel import create_excel
from app.core.db import get_async_session



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

    params = dict(request.query_params)
    report_type = params.get('type')
    #user_id = params.get('user_id', None)

    types_query = {
        'clients': select(User).where(
            User.role == 'client'
        ),
        #'services': select(Service),
        #'payments': select(Order).where(Order.user_id == user_id),
        #'bonuses': select(Bonus).where(
        #    and_(
        #       Bonus.user_id == user_id,
        #        Bonus.is_active == True,
        #    )
        #)
        

    }

    objects = await session.execute(
        types_query[report_type]
    )
    excel = create_excel(objects.scalars().all())
    pass

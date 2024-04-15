from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.endpoints.utils import get_current_user
from app.models.user import User


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
):
    """Функция для получения отчётов. """

    # TODO: Добавить получение отчёта и отправку его через Telegram.

    pass

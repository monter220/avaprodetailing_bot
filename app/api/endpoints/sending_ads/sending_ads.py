from typing import Optional

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.endpoints.utils import get_current_user
from app.models.user import User


router = APIRouter(
    prefix='/sending-ads',
    tags=['sending-ads']
)

templates = Jinja2Templates(directory="app/templates")


@router.get('/')
async def get_sending_ads_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user)
):
    """Функция для получения страницы отправки рекламных предложений. """

    if current_user.is_superadmin:
        return templates.TemplateResponse(
            'sending_ads/add-sender.html',
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
async def process_sending_ads(
    request: Request,
):
    """Функция для рассылки рекламных сообщений. """

    # TODO: Добавить рассылку рекламных сообщений.

    pass

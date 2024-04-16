from typing import Optional

from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.endpoints.utils import get_current_user
from app.models.user import User
from app.tasks.messages import sending_ads

router = APIRouter(
    prefix='/sending-ads',
    tags=['sending-ads']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/')
async def get_sending_ads_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user)
):
    """Функция для получения страницы отправки рекламных предложений."""
    if current_user.is_superadmin:
        return templates.TemplateResponse(
            'sending_ads/add-sender.html',
            {
                'request': request,
                'title': 'Информационная рассылка',
            }
        )
    else:
        return RedirectResponse(
            url='users/me',
            status_code=status.HTTP_302_FOUND,
        )


@router.post('/')
async def process_sending_ads(
    text: str = Form(...),
    current_user: Optional[User] = Depends(get_current_user),
):
    """Функция для рассылки рекламных сообщений. """
    if not current_user.is_superadmin:
        return RedirectResponse(
            url='/users/me',
            status_code=status.HTTP_302_FOUND,
        )

    sending_ads.delay(text)

    return RedirectResponse(
        url='/users/me',
        status_code=status.HTTP_302_FOUND,
    )

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/{user_id}/payments"
)

templates = Jinja2Templates(
    directory='app/templates'
)


@router.get('/payment')
async def get_payment_page(
    request: Request,
    user_id: int
):
    """Функция для получения страниц оплаты. """

    pass

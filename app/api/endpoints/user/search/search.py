from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/me/search"
)

templates = Jinja2Templates(
    directory='app/templates'
)


@router.post('/phone-number')
async def get_payment_page(
    request: Request,
):
    """Функция для поиска пользователя. """

    # TODO: Добавить логику поиска пользователя.
    # В зависимости от нахождения - должна редиректить
    # на страницу пользователя или на страницу с ошибкой.

    pass


@router.get('/not-found')
async def get_not_found_page(
    request: Request,
):
    """Функция для получения страницы с ошибкой. """

    return templates.TemplateResponse(
        'user/search/user-not-found.html',
        status_code=status.HTTP_404_NOT_FOUND,
    )

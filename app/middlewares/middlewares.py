from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class TelegramIDCheckingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        """Мидлварь для проверки наличия tg_id в куках реквеста."""

        exclusions = ('/', '/docs')  # Исключения для которых не проверяется tg_id.

        if request.url.path.startswith('/static'):  # Отдельная обработка для путей статики
            return await call_next(request)

        if request.url.path not in exclusions and 'tg_id' not in request.cookies:
            return RedirectResponse('/')

        response = await call_next(request)

        return response

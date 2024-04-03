from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class TelegramIDCheckingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        """Мидлварь для проверки наличия tg_id в куках реквеста."""

        if 'tg_id' not in request.cookies.keys():
            return RedirectResponse('/sign-in')

        response = await call_next(request)

        return response

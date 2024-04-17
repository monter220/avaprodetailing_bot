import contextlib

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import user_crud
from app.crud.order import order_crud
from app.services.excel import create_excel, create_excel_with_fields
from app.services.telegram import send_excel


async def process_report(
    key: str,
    user_tg_id: int,
    field_names: list[str] = None,
):
    get_async_session_context = contextlib.asynccontextmanager(
        get_async_session)
    async with get_async_session_context() as session:
        types_query = {
            'users': user_crud.get_multi,
            'orders': order_crud.get_orders_report,
            'payments': order_crud.get_payments_report,
        }
        objects = await types_query[key](session)

        if field_names:
            excel = create_excel_with_fields(objects, field_names)
        else:
            excel = create_excel(objects)
        await send_excel(
            excel=excel, filename=f'{key}.xlsx', chat_id=user_tg_id)

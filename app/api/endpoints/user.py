from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserDB

router = APIRouter()


@router.post(
    '/user/',
    response_model=UserDB,
    response_model_exclude_none=True,
)
async def create_new_user(
        new_user: UserCreate,
        session: AsyncSession = Depends(get_async_session),
):
    new = await user_crud.create(new_user, session)
    return new

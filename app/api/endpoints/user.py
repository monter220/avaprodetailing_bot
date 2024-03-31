from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserDB
from app.api.validators import check_duplicate
from app.core.managment.utils import create_access_token, create_refresh_token


router = APIRouter()


@router.post(
    '/user',
    response_model=UserDB,
    response_model_exclude_none=True,
)
async def create_new_user(
        new_user: UserCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_duplicate(new_user.phone, session)
    new = await user_crud.create(new_user, session)
    return new


@router.post(
    '/auth',
    summary="Create access and refresh tokens for user",
)
async def login(
        tg_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    user = await user_crud.tg_login_check(tg_id,session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect telegram id"
        )

    return {
        "access_token": create_access_token(user.phone),
        "refresh_token": create_refresh_token(user.phone),
    }

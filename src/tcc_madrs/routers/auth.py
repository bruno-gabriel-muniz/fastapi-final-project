from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import User
from src.tcc_madrs.schemas import Token
from src.tcc_madrs.security import create_access_token, valid_password_hash

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/', response_model=Token)
async def get_access_token(form_data: T_Form, session: T_Session):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User Not Found')

    if not valid_password_hash(form_data.password, user.password):
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, detail='User Or Password Incorrect'
        )

    token = {
        'token_type': 'barrear',
        'access_token': create_access_token({'sub': user.email}),
    }

    return token

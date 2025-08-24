from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import User
from src.tcc_madrs.routers.novelist import router as router_novelist
from src.tcc_madrs.routers.users import router as router_users
from src.tcc_madrs.schemas import Token
from src.tcc_madrs.security import (
    create_access_token,
    get_current_user,
    valid_password_hash,
)

logger.add('app.log', rotation='500 KB')
logger.info('iniciando o app')
app = FastAPI()

app.include_router(router_novelist)
app.include_router(router_users)

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_User = Annotated[User, Depends(get_current_user)]


@app.post('/token/', response_model=Token)
async def get_access_token(form_data: T_Form, session: T_Session):
    logger.info('inciando a criação de um token')
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    logger.info('validando o username e o password')

    if not user:
        logger.info('user não encontrado')
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User Not Found')

    if not valid_password_hash(form_data.password, user.password):
        logger.info('usuário ou senhas incorretos')
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, detail='User Or Password Incorrect'
        )

    logger.info('criando o token')
    token = {
        'token_type': 'barrear',
        'access_token': create_access_token({'sub': user.email}),
    }

    logger.info('retornando')
    return token


@app.post('/refresh-token/', response_model=Token)
async def refresh_access_token(user: T_User):
    logger.info('fazendo refresh de um token')
    token = {
        'token_type': 'barrear',
        'access_token': create_access_token({'sub': user.email}),
    }

    return token

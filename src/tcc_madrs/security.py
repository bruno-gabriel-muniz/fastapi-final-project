from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from loguru import logger
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import User
from src.tcc_madrs.settings import Settings

pwd_context = PasswordHash.recommended()

oauth2_schme = OAuth2PasswordBearer(tokenUrl='/auth/')

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_Form_Barear = Annotated[str, Depends(oauth2_schme)]


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def valid_password_hash(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    settings = Settings()  # type: ignore

    logger.info('criando token')

    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    token = encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    logger.info('retornando')
    return token


async def get_current_user(session: T_Session, token: T_Form_Barear):
    logger.info('autenticando o user')

    credentials_error = HTTPException(
        HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    stg = Settings()  # type: ignore

    logger.info('lendo e validando os dados do token')

    try:
        pyload = decode(token, stg.SECRET_KEY, [stg.ALGORITHM])
        email: str = pyload.get('sub')

        if not email:
            raise credentials_error
    except DecodeError:
        raise credentials_error
    except ExpiredSignatureError:
        raise credentials_error

    user = await session.scalar(
        select(User).where(User.email == pyload['sub'])
    )

    if not user:
        raise credentials_error

    logger.info('retornando')
    return user

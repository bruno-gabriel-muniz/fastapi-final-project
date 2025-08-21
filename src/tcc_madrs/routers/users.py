from http import HTTPStatus
from re import sub
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import User
from src.tcc_madrs.schemas import UserPublic, UserSchema
from src.tcc_madrs.security import get_current_user, get_password_hash


def sanitize(username: str):
    return sub(' {2,}', ' ', username.lower()).strip(' ')


router = APIRouter(prefix='/conta', tags=['conta'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, db: T_Session):
    logger.info('iniciando a criação de um novo usuário')

    # Realiza a sanitização dos dados
    logger.info('sanitizando o username')
    user.username = sanitize(user.username)

    # Verifica se existem conflitos entre os usuários
    logger.info('verificando conflitos')
    user_exist = await db.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if user_exist:
        logger.info('conflito encontrado')
        raise HTTPException(
            HTTPStatus.CONFLICT, 'Email or UserName Alredy Exist'
        )

    # Cria um novo usuário
    logger.info('criando o usuário')
    new_user = User(
        user.username, user.email, get_password_hash(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    id: int, user: UserSchema, session: T_Session, db_user: T_User
):
    logger.info('iniciando a alteração de um user')

    logger.info('validando as permissões e os conflitos')
    if db_user.id != id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            'Alterações em outras contas não são permitadas',
        )

    data_in_use = await session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )
    if data_in_use and data_in_use.id != id:
        raise HTTPException(
            HTTPStatus.CONFLICT, 'email ou username já consta no MADR'
        )

    logger.info('alterando o user')
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    logger.info('salvando as alterações')
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    logger.info('retornando')
    return db_user

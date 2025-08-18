from http import HTTPStatus
from re import sub
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import User
from src.tcc_madrs.schemas import UserPublic, UserSchema
from src.tcc_madrs.security import get_password_hash


def sanitize(username: str):
    return sub(' {2,}', ' ', username.lower()).strip(' ')


router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, db: T_Session):
    logger.info('iniciando a criação de um novo usuário')

    # Realiza a sanitização dos dados
    logger.info('sanitizando o username')
    user.username = sanitize(user.username)

    # Verifica se existem conflitos entre os usuários
    logger.info('verificando conflitos')
    user_exist = db.scalar(
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
    db.commit()
    db.refresh(new_user)

    return new_user

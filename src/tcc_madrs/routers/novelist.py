from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import Novelist, User
from src.tcc_madrs.sanitize import sanitize
from src.tcc_madrs.schemas import NovelistDB, NovelistInput
from src.tcc_madrs.security import get_current_user

router = APIRouter(prefix='/romancista', tags=['romancistas'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=NovelistDB, status_code=HTTPStatus.CREATED)
async def create_novelist(
    novelist: NovelistInput,
    session: T_Session,
    user: T_User,
):
    logger.info('criando um novo romancista')

    # Sanitizando o nome
    logger.info('sanitizando o nome do novo romancista')
    novelist.name = sanitize(novelist.name)

    # Validando conflitos
    logger.info('validando conflitos')

    name_in_use = await session.scalar(
        select(Novelist).where(Novelist.name == novelist.name)
    )
    if name_in_use:
        logger.info('conflito encontrado, informando')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='romancista já consta no MADR',
        )

    # Criando o novo romancista
    logger.info('add romancista no DB')
    novelist_db = Novelist(novelist.name)

    session.add(novelist_db)
    await session.commit()
    await session.refresh(novelist_db)

    return novelist_db

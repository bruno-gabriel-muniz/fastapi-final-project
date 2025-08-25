from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import Novelist, User
from src.tcc_madrs.sanitize import sanitize
from src.tcc_madrs.schemas import (
    FilterNovelist,
    ListNovelist,
    Message,
    NovelistDB,
    NovelistInput,
)
from src.tcc_madrs.security import get_current_user

router = APIRouter(prefix='/romancista', tags=['romancistas'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]
T_Filter = Annotated[FilterNovelist, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=NovelistDB)
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


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_novelist(
    id: int,
    user: T_User,
    session: T_Session,
):
    logger.info('inciando a remoção de um romancista')

    logger.info('procurando o romancista')
    novelist = await session.scalar(select(Novelist).where(Novelist.id == id))

    if not novelist:
        logger.info('romancista não encontrado')
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no MADR',
        )

    logger.info('removendo o romancista')
    await session.delete(novelist)

    logger.info('retornando')
    return {'message': 'Romancista deletada no MADR'}


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=NovelistDB)
async def get_novelist_id(
    id: int,
    session: T_Session,
):
    logger.info('iniciando o get_novelist_id')

    logger.info('procurando o novelista')
    novelist = await session.scalar(select(Novelist).where(Novelist.id == id))

    if not novelist:
        logger.info('novelista não encontrado')
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Romancista não consta no MADR'
        )

    logger.info('retornando o novelista')
    return novelist


@router.get('/', status_code=HTTPStatus.OK, response_model=ListNovelist)
async def get_novelist_by_filter(
    filter: T_Filter,
    session: T_Session,
):
    logger.info('iniciando um get romancista por filtro')

    logger.info('criando os filtros')
    query = select(Novelist)

    if filter.name:
        query = query.filter(Novelist.name.contains(filter.name))

    logger.info('retornando os resultados')
    result = await session.scalars(
        query.offset(filter.offset).limit(filter.limit)
    )
    return {'romancistas': result.all()}

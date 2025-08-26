from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import Book, User
from src.tcc_madrs.sanitize import sanitize
from src.tcc_madrs.schemas import BookDB, BookInput
from src.tcc_madrs.security import get_current_user

router = APIRouter(prefix='/livro', tags=['livros'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookDB)
async def create_book(
    book: BookInput,
    session: T_Session,
    user: T_User,
):
    logger.info('iniciando a criação de um livro')

    logger.info('sanitizando o nome')
    book.name = sanitize(book.name)

    logger.info('procurando conflitos')
    conflict = await session.scalar(select(Book).where(Book.name == book.name))

    if conflict:
        logger.info('informando o conflito')
        raise HTTPException(
            HTTPStatus.CONFLICT, detail='livro.name já consta no MADR'
        )

    logger.info('adicionando o livro no db')
    book_db = Book(book.year, book.name, book.romancista_id)

    session.add(book_db)
    await session.commit()
    await session.refresh(book_db)

    logger.info('retornando')
    return book_db

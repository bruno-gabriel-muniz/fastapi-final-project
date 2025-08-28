from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import Book, User
from src.tcc_madrs.sanitize import sanitize
from src.tcc_madrs.schemas import (
    BookDB,
    BookInput,
    BookPatch,
    FilterBooks,
    ListBookDB,
)
from src.tcc_madrs.security import get_current_user

router = APIRouter(prefix='/livro', tags=['livros'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]
T_Filter = Annotated[FilterBooks, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookDB)
async def create_book(
    book: BookInput,
    session: T_Session,
    user: T_User,
):
    logger.info('iniciando a criação de um livro')

    logger.info('sanitizando o nome')
    book.titulo = sanitize(book.titulo)

    logger.info('procurando conflitos')
    conflict = await session.scalar(
        select(Book).where(Book.titulo == book.titulo)
    )

    if conflict:
        logger.info('informando o conflito')
        raise HTTPException(
            HTTPStatus.CONFLICT, detail='livro.titulo já consta no MADR'
        )

    logger.info('adicionando o livro no db')
    book_db = Book(book.ano, book.titulo, book.romancista_id)

    session.add(book_db)
    await session.commit()
    await session.refresh(book_db)

    logger.info('retornando')
    return book_db


@router.get('/{id}', status_code=HTTPStatus.OK, response_model=BookInput)
async def get_book_by_id(id: int, session: T_Session):
    logger.info('inciando get_book_by_id')

    logger.info('procurando o livro no banco')
    book = await session.scalar(select(Book).where(Book.id == id))

    if not book:
        logger.info('informando que o livro não foi encontrado')
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    logger.info('retornando o  livro')
    return book


@router.get('/', status_code=HTTPStatus.OK, response_model=ListBookDB)
async def get_books_by_filter(session: T_Session, filter: T_Filter):
    logger.info('iniciando get_books_by_filter')

    logger.info('montando a query')
    query = select(Book)

    if filter.titulo:
        query = query.filter(Book.titulo.contains(filter.titulo))

    if filter.ano:
        query = query.filter(Book.ano == filter.ano)

    logger.info('realizando a busca')
    result = await session.scalars(
        query.offset(filter.offset).limit(filter.limit)
    )

    logger.info('retornando')
    return {'livros': result}


@router.patch('/{id}', status_code=HTTPStatus.OK, response_model=BookInput)
async def update_book(
    id: int,
    book: BookPatch,
    session: T_Session,
    user: T_User,
):
    logger.info('iniciando update_book')

    logger.info('procurando o livro')
    book_db = await session.scalar(select(Book).where(Book.id == id))

    if not book_db:
        logger.info('livro não encontrado')
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    logger.info('validando conflitos')
    if book.titulo:
        have_conflict = await session.scalar(
            select(Book).where(Book.titulo == sanitize(book.titulo))
        )

    if have_conflict:
        logger.info('conflito encontrado')
        raise HTTPException(
            HTTPStatus.CONFLICT, detail='book.titulo já consta no MADR'
        )

    logger.info('atualizando o livro')
    if book.titulo:
        book_db.titulo = sanitize(book.titulo)

    if book.ano:
        book_db.ano = book.ano

    if book.romancista_id:
        book_db.romancista_id = book.romancista_id

    logger.info('salvando as alterações')
    session.add(book_db)
    await session.commit()
    await session.refresh(book_db)

    logger.info('retornando')
    return book_db

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.tcc_madrs.settings import Settings

logger.info('criando a engine do DB')
engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:  # pragma: no cover
        logger.info('disponibilizando uma sessão')
        yield session

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.tcc_madrs.settings import Settings

logger.info('criando a engine do DB')
engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(
        engine, expire_on_commit=False
    ) as session:  # pragma: no cover
        logger.info('disponibilizando uma sessão')
        yield session

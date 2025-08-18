from http import HTTPStatus

from fastapi import FastAPI
from loguru import logger

from src.tcc_madrs.routers.users import router as router_users
from src.tcc_madrs.schemas import Message

logger.add('app.log', rotation='500 KB')
logger.info('iniciando o app')
app = FastAPI()

app.include_router(router_users)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def test():
    logger.info('enviando a mensagem de test')
    return {'message': 'Hello Wolrd!'}

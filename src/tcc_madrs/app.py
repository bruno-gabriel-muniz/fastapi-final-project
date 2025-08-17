from http import HTTPStatus

from fastapi import FastAPI

from src.tcc_madrs.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def test():
    return {'message': 'Hello Wolrd!'}

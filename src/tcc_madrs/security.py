from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

from src.tcc_madrs.settings import Settings

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def valid_password_hash(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    settings = Settings()  # type: ignore

    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    token = encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token

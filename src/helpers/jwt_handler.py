import datetime

from jwt import decode, encode

from src.core.settings import settings


class JWT:

    secret_key = settings.SECRET_KEY
    algorithm = settings.ALGORITHM
    access_expire_minutes = settings.ACCESS_EXPIRE_MINUTES
    refresh_expire_minutes = settings.REFRESH_EXPIRE_MINUTES

    @staticmethod
    def encode_access_token(payload: dict, algorithm="HS256") -> str:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=JWT.access_expire_minutes
        )
        payload.update({"exp": expire, "type": "access"})
        return encode(payload, JWT.secret_key, algorithm=algorithm)

    @staticmethod
    def encode_refresh_token(payload: dict, algorithm="HS256") -> str:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=JWT.refresh_expire_minutes
        )
        payload.update({"exp": expire, "type": "refresh"})
        return encode(payload, JWT.secret_key, algorithm=algorithm)

    @staticmethod
    def decode(token, algorithm="HS256"):
        return decode(token, JWT.secret_key, algorithms=[algorithm])

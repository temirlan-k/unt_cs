import os


class Settings:

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_EXPIRE_MINUTES = 60
    REFRESH_EXPIRE_MINUTES = 60 * 24 * 7


settings = Settings()

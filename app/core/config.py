from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'AvaProDetailing_Bot'
    database_url: str
    role_list: str = '{1:"client",2:"administrator",3:"superuser"}'

    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 10080
    hash_algorithm: str = 'HS256'
    jwt_secret_key: str = 'JWT_SECRET_KEY'
    jwt_refresh_secret_key: str = 'JWT_REFRESH_SECRET_KEY'

    class Config:
        env_file = '.env'


settings = Settings()

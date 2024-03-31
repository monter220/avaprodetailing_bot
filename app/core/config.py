from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'AvaProDetailing_Bot'
    database_url: str
    role_list: str = '{1:"client",2:"administrator",3:"superuser"}'
    default_role: int = 1

    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 10080
    hash_algorithm: str = 'HS256'
    jwt_secret_key: str = 'JWT_SECRET_KEY'
    jwt_refresh_secret_key: str = 'JWT_REFRESH_SECRET_KEY'

    min_fio_len: int = 2
    max_fio_len: int = 100
    fio_alphabet_error: str = 'Поле содержит недопустимые символ'
    min_age: int = 5844
    max_age: int = 40178
    age_error: str = 'Ваш возраст не соответствует допустимому'
      
    telegram_bot_token: str
    # bot: Bot = Bot(
    #     token=telegram_bot_token,
    #     default=DefaultBotProperties(
    #         parse_mode=ParseMode.HTML,
    #     )
    # )
    # dp: Dispatcher = Dispatcher()
    # web_hook_path: str = f'/webhook/bot/{telegram_bot_token}'
    telegram_webapp_url: str
    app_port: int

    class Config:
        env_file = '.env'


settings = Settings()

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'AvaProDetailing_Bot'
    database_url: str
    telegram_bot_token: str
    bot: Bot = Bot(
        token=telegram_bot_token,
        default=DefaultBotProperties(
            parse_mode=types.ParseMode.HTML,
        )
    )
    dp: Dispatcher = Dispatcher()
    web_hook_path: str = f'/webhook/bot/{telegram_bot_token}'
    telegram_webapp_url: str
    app_port: str

    class Config:
        env_file = '.env'


settings = Settings()

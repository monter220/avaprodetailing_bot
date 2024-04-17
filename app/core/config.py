import os

from celery import Celery
from pydantic_settings import BaseSettings
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties


class Settings(BaseSettings):
    app_title: str = 'AvaProDetailing_Bot'
    database_url: str
    role_list: str = '{1:"client",2:"administrator",3:"superuser"}'
    default_role: int = 1
    paytype_list: str = '{1:"наличный расчет",2:"безналичный расчет"}'
    eventtypes_list: str = '{1:"создан",2:"изменен",3:"удален"}'
    superadmin: str = '{"id":1,"surname":"Великий","name":"Админ","patronymic":" ","date_birth":"1991-11-11","phone":"+79998887766","role":3}'

    pay_type_cash: int = 1
    pay_type_online: int = 2
    system_user_id: int = 1

    min_fio_len: int = 2
    max_fio_len: int = 100
    alphabet_error: str = 'Поле содержит недопустимые символ'
    min_age: int = 5844
    max_age: int = 40178
    age_error: str = 'Ваш возраст не соответствует допустимому'
    max_phone_len: int = 15
    phone_error: str = 'invalid phone number format'
    default_bonus: int = 100
    bonus_expiration_period: int = 365
    basedir: str = os.getcwd()
    folder: str = 'app/templates/static/media'
    host_folder: str = 'static/media'

    min_name_len: int = 1
    max_name_len: int = 50
    min_address_len: int = 1
    max_address_len: int = 250
    max_bonus_value: int = 99

    dp: Dispatcher = Dispatcher()
    bot_drop_pending_updates: bool = 1
    bot_request_timeout: int = 30
    bot_parse_mode: str = 'html'
    telegram_bot_token: str = '123456789'
    web_app_url: str = 'https://ya.ru'
    host_ip: str = '0.0.0.0'
    host_url: str = 'https://example.com'
    app_port: int = 443
    cookies_ttl: int = (30 * 24 * 60 * 60)  # 30 дней
    testing: int = 0
    local_test: int = 1

    telegram_provider_token: str = '381764678:TEST: 82806'
    telegram_currency: str = 'RUB'

    redis_url: str = 'redis://127.0.0.1:6379'

    class Config:
        env_file = '.env'


settings = Settings()
bot: Bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(
        parse_mode=settings.bot_parse_mode,
    )
)
web_hook_path: str = f'{settings.host_url}/webhook'

celery_app = Celery(
    main=settings.app_title,
    broker=settings.redis_url,
    broker_connection_retry_on_startup=True,
)
tasks_routes = {
    'app.tasks.messages.*': {
        'queue': f'{settings.app_title}_messages',
    },
    'app.tasks.schedulers.*': {
        'queue': f'{settings.app_title}_schedulers',
    },
}
celery_app.conf.task_routes = tasks_routes

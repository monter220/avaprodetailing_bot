# Bot Avaprodetailing

## 1. Команда
- Беликов Дмитрий - [monter220](https://github.com/monter220)
- Сергей Иванов - [isv160179](https://github.com/isv160179)
- Сергей Филатов - [Serhioth](https://github.com/Serhioth)
- Колтыгин Сергей - [cmipro](https://github.com/cmipro)
- Лаврушенков Александр - [lavralex](https://github.com/lavralex)

## 2. О проекте
Наш проект представляет собой телеграм бот для сети автомоек с возможностью регистрации клиентов, формирования заказов и оплаты, также реализована система лояльности и отчетности.
### Возможности пользователей:
***Регистрация по номеру телефона с заполнением данных:***

<img src="readme_img/phone.jpg" width="340" height="450"> <img src="readme_img/reg.jpg" width="340" height="450">

***Добавление автомобиля:***

<img src="readme_img/avto.jpg" width="340" height="450">

***В меню личного кабинета можно посмотреть бонусы, мой автомобиль, есть возможность добавить или отредактировать марку, модель и гос. номер автомобиля***

<img src="readme_img/user_qr.jpg" width="340" height="450">

***Админ часть: наполнение каталога услуг с возможностью редактирования, Отчеты по выбранному клиенту (заказы, начисления и списание бонусов), общий отчет по дням, отчет по клиентам. Рассылка новостей клиентам.***

<img src="readme_img/admin_scan.jpg" width="340" height="450"> <img src="readme_img/admin_rep.jpg" width="340" height="450">

***Также реализовано получение приветственных бонусов и бонусов от каждой оплаченной услуги, и онлайн оплата из бота с помощью QRcode.***

## 3. Инструкция по запуску.
### Локально:
1) Клонировать проект себе

    `git clon git@github.com:Studio-Yandex-Practicum/avaprodetailing_bot_3.git`

2) Перейти в дерикторию проекта

    `cd avaprodetailing_bot_3/`

3) В активированном виртуальном окружении установить зависимости

    `pip install -r requirements.txt`

4) Создать файл .env по примеру .env.template
5) Создать папку versions в alembic/

   `mkdir alembic/versions`

6) создать и применить миграции
   
   `alembic revision --autogenerate -m "first migration"`

   `alembic upgrade head`


7) Запустить проект
   
   `uvicorn app.main:app`

### Удаленный сервер:
    ¯\_(ツ)_/¯

## 4. Используемые технологии:
[python](https://www.python.org/) | 
[html5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) | 
[css](https://www.w3.org/Style/CSS/) | 
[javaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | 
[fastapi](https://fastapi.tiangolo.com/) | 
[pydantic](https://pydantic-docs.helpmanual.io/) | 
[SQLAlchemy](https://www.sqlalchemy.org/) | 
[iogram](https://tg.iogram.xyz/) | 
[aiohttp](https://pypi.org/project/aiohttp/) | 
[Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) | 
[uvicorn](https://www.uvicorn.org/) | 
[openpyxl](https://openpyxl.readthedocs.io/en/stable/) | 
[alembic](https://alembic.sqlalchemy.org/en/latest/) | 
[redis](https://redis.io/) | 
[gosnomer](https://pypi.org/project/gosnomer/) | 
[phonenumbers](https://pypi.org/project/phonenumbers/)

<!-- BACK TO TOP LINK -->
<a name="readme-top"></a>


<!-- PROJECT SHIELDS -->
[![Python][Python-shield]][Python-url]
[![Django][Django-shield]][Django-url]
[![PostgreSQL][PostgreSQL-shield]][PostgreSQL-url]
[![Pillow][Pillow-shield]][Pillow-url]

[![Python-Telegram-Bot][Python-Telegram-Bot-shield]][Python-Telegram-Bot-url]

[![Docker][Docker-shield]][Docker-url]
[![Nginx][Nginx-shield]][Nginx-url]
[![Uvicorn][Uvicorn-shield]][Uvicorn-url]
[![GitHub][GitHub-shield]][GitHub-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Studio-Yandex-Practicum/Premium_product_bot_team_3">
    <img src="images/logo-big.jpg" alt="Logo" width="320" height="180">
  </a>

  <h3 align="center">Премиум Продукт</h3>

  <p align="center">
    Удобный Telegram-бот для поиска коммерческой недвижимости!
    <br />
    <a href="https://t.me/Comm_Real_Estate_Bot"><strong>Перейти в Telegram »</strong></a>
    <br />
    <br />
    <a href="https://realty-service.hopto.org/admin/">Демо-версия админ-панели</a>
    ·
    <a href="https://github.com/Studio-Yandex-Practicum/Premium_product_bot_team_3/issues/new?labels=bug">Сообщить об ошибке</a>
    ·
    <a href="https://github.com/Studio-Yandex-Practicum/Premium_product_bot_team_3/issues/new?labels=enhancement">Предложить улучшение</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a href="#описание-проекта">Описание проекта</a>
      <ul>
        <li><a href="#применяемые-технологии">Применяемые технологии</a></li>
      </ul>
    </li>
    <li>
      <a href="#запуск-проекта">Запуск проекта</a>
      <ul>
        <li><a href="#локально">Локально</a></li>
        <li><a href="#на-удалённом-сервере">На удалённом сервере</a></li>
      </ul>
    </li>
    <li><a href="#использование-бота">Использование бота</a>
      <ul>
        <li><a href="#функционал-для-пользователей">Функционал для пользователей</a></li>
        <li><a href="#функционал-для-пользователей">Функционал для администраторов</a></li>
      </ul>
    </li>
    <li><a href="#команда-разработчиков">Команда разработчиков</a></li>
  </ol>
</details>


___
<!-- ABOUT THE PROJECT -->
## Описание проекта
Telegram-бот предназначен для упрощения поиска коммерческой недвижимости для аренды или покупки. Бот предоставляет пользователям возможность быстро находить подходящие объекты недвижимости по заданным критериям, а также получать подробную информацию о каждом объекте, контактную информацию владельцев или агентов, и подписываться на уведомления о новых предложениях.

<p align="right">(<a href="#readme-top">вернуться наверх</a>)</p>

### Применяемые технологии
* [![Python][Python-shield]][Python-url]
* [![Django][Django-shield]][Django-url]
* [![PostgreSQL][PostgreSQL-shield]][PostgreSQL-url]
* [![Pillow][Pillow-shield]][Pillow-url]
* [![Python-Telegram-Bot][Python-Telegram-Bot-shield]][Python-Telegram-Bot-url]
* [![Docker][Docker-shield]][Docker-url]
* [![Nginx][Nginx-shield]][Nginx-url]
* [![Uvicorn][Uvicorn-shield]][Uvicorn-url]
* [![GitHub][GitHub-shield]][GitHub-url]

<p align="right">(<a href="#readme-top">вернуться наверх</a>)</p>


___
<!-- GETTING STARTED -->
## Запуск проекта

### Локально
#### Требование к системе: На компьютере должен быть установлен Docker. Проект можно развернуть только в контейнерах.
 
1. Клонировать репозиторий:
```
git clone git@github.com:Studio-Yandex-PracticumPremium_product_bot_team_3.git
```
1. Заполнить переменные окружения в файл .env по образцу .env.example
2. Запустить docker-контейнеры:
```
docker compose up --build -d
```
1. Выполнить миграции:
```
docker compose exec real_estate python manage.py migrate
```
1. Создать суперпользователя для админ-панели:
```
docker compose exec -it real_estate python manage.py createsuperuser
```
1. Загрузить тестовые данные в базу (при необходимости)
```
docker compose exec real_estate python manage.py upload_objects --file example_data.csv
```
1. Зайти в админ-панель по адресу http://localhost:8000/admin/ и загрузить изображение для логотипа. Изображение будет использоваться для тех случаев, когда объявление не содержит фото объекта недвижимости. Загружать можно в любое объявление, но имя файла должно быть logo_v3.jpg
2. После этих действий можно зайти в бота через Telegram и протестировать его работу


### На удалённом сервере
1. Клонируйте репозиторий.
```
git clone git@github.com:Studio-Yandex-Practicum/Premium_product_bot_team_3.git
```
2. Установите и настройте Docker.
- Зайдите на [официальный сайт проекта](https://www.docker.com/products/docker-desktop) и скачайте установочный файл Docker Desktop.
3. Переименуйте файл '.env.example' на 'env' и подставте свои данные.
4. Установите и настройте Nginx.
5. Получите и настройте SLL-сертификат

<p align="right">(<a href="#readme-top">вернуться наверх</a>)</p>


___
<!-- USAGE -->
## Использование бота

### Функционал для пользователей
1. Поиск объектов недвижимости:
   - Поиск по городам (например, Москва, Санкт-Петербург, Казань и т.д.).
   - Поиск по категориям (офисы, склады, магазины и т.д.).
   - Фильтры поиска по цене, площади, типу ремонта, наличию парковки и другим параметрам.
   - Сортировка результатов поиска по цене, площади, дате публикации.
   - Сохранение объектов в избранное.
   - Подписка на уведомления о новых объектах, соответствующих критериям поиска пользователя.
2. Просмотр информации об объектах:
   - Возможность отправить запрос на просмотр объекта.
   - Возможность оставить текстовый отзыв об объекте (отзывы модерируются администратором).
   - Возможность добавлять объект в избранное.
3. Общение и поддержка:
   - Получение инструкций по работе с ботом.

### Функционал для администраторов
1. Управление объявлениями:
   - Добавление и изменение объявлений.
   - Модерация и удаление объявлений (удаленные объявления помечаются как "Удалено администратором").
   - Управление типами объектов недвижимости.
3. Управление пользователями:
   - Блокировка, разблокировка и редактирование пользователей.
   - Удаление пользователей и их данных.
4. Модерация отзывов:
   - Модерация и удаление отзывов к объектам недвижимости.
5. Настройка администраторов:
   - Назначение и удаление обычных администраторов.

<p align="right">(<a href="#readme-top">вернуться наверх</a>)</p>


___
<!-- TEAM -->
## Команда разработчиков
[Алексей Данилов](https://github.com/AlexeyDanilov)

Занимался управлением командой (TeamLead):
* декомпозиция и распределение задач,
* ежедневная проверка отчётов,
* проведение ревью и тестирование,
* помощь команде в проблемных задачах.

[Софья Боровкова](https://github.com/SofiaBorovkova)

Занималась функционалом бота, админ-панели и стандартизацией кода:
* разработка функционала добавления в избранное,
* контактная информация в боте,
* оформление админ-панели,
* оформление кода согласно PEP8,
* помощь сокомандникам в проблемных задачах.

[Андрей Щапов](https://github.com/somwhereAway)

Занимался логикой поиска бота и функционалом рассылки:
* разработка логики поиска объектов,
* разработка функционала рассылки,
* помощь сокомандникам в проблемных задачах.

[Дарья Семенова](https://github.com/OFF1GHT)

Занималась функционалом бота и первичной документацией:
* разработка функционала отзывов,
* график работы для объектов недвижимости,
* разработка первичной документации бота,
* помощь сокомандникам в проблемных задачах.

[Павел Найденов](https://github.com/meteopavel)

Занимался созданием экосистемы бота, контейнеризацией, деплоем, документацией и презентацией:
* разработка первоначальной структуры асинхронного бота, работающего совместно с Django через механизм webhook-ов,
* упаковка проекта в контейнеры при соблюдении условия использования облегчённых версий основных пакетов,
* написание сценариев автоматизации сборки и деплоя проекта,
* работа по настройке сервера
* приведение первичной документации к более подробному виду, разработка видеопрезентации, 
* помощь сокомандникам в проблемных задачах.

<p align="right">(<a href="#readme-top">вернуться наверх</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python-shield]: https://img.shields.io/badge/Python-v3.10--alpine-blue?style=flat&logo=python&labelColor=FDEBD0&logoColor=blue
[Python-url]: https://www.python.org/downloads/release/python-31010/
[Django-shield]: https://img.shields.io/badge/Django-v5.0-green?style=flat&logo=django&labelColor=FDEBD0&logoColor=blue
[Django-url]: https://docs.djangoproject.com/en/5.0/releases/5.0/
[PostgreSQL-shield]: https://img.shields.io/badge/PostgreSQL-v13.15--alpine-blue?style=flat&logo=PostgreSQL&labelColor=FDEBD0&logoColor=blue
[PostgreSQL-url]: https://www.postgresql.org/docs/13/release-13-15.html 
[Pillow-shield]: https://img.shields.io/badge/Pillow-v10.3-green?style=flat&logo=pillow&labelColor=FDEBD0&logoColor=blue
[Pillow-url]: https://pillow.readthedocs.io/en/stable/releasenotes/10.3.0.html
[Python-Telegram-Bot-shield]: https://img.shields.io/badge/Python--telegram--bot-v21.2-blue?style=flat&logo=telegram&labelColor=FDEBD0&logoColor=blue
[Python-Telegram-Bot-url]: https://docs.python-telegram-bot.org/en/v21.2/
[Docker-shield]: https://img.shields.io/badge/Docker-v26.1-green?style=flat&logo=docker&labelColor=FDEBD0&logoColor=blue
[Docker-url]: https://docs.docker.com/engine/release-notes/26.1/
[Nginx-shield]: https://img.shields.io/badge/Nginx-v1.26--alpine-blue?style=flat&logo=nginx&labelColor=FDEBD0&logoColor=blue
[Nginx-url]: https://nginx.org/en/docs/
[Uvicorn-shield]: https://img.shields.io/badge/Uvicorn-v0.23-green?style=flat&logo=gunicorn&labelColor=FDEBD0&logoColor=blue
[Uvicorn-url]: https://www.uvicorn.org/release-notes/
[GitHub-shield]: https://img.shields.io/badge/GitHub-Actions-blue?style=flat&logo=github&labelColor=FDEBD0&logoColor=blue
[GitHub-url]: https://docs.github.com/en/actions

![Python](https://img.shields.io/badge/Python-v3.10--alpine-blue?style=flat&logo=python&labelColor=FDEBD0&logoColor=blue)
![Django](https://img.shields.io/badge/Django-v5.0-green?style=flat&logo=django&labelColor=FDEBD0&logoColor=blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v13.15--alpine-blue?style=flat&logo=PostgreSQL&labelColor=FDEBD0&logoColor=blue)

![Python Telegram Bot](https://img.shields.io/badge/Python--telegram--bot-v21.2-blue?style=flat&logo=telegram&labelColor=FDEBD0&logoColor=blue)
![Pillow](https://img.shields.io/badge/Pillow-v10.3-blue?style=flat&logo=pillow&labelColor=FDEBD0&logoColor=blue)

![Docker](https://img.shields.io/badge/Docker-v26.1-green?style=flat&logo=docker&labelColor=FDEBD0&logoColor=blue)
![Nginx](https://img.shields.io/badge/nginx-1.26--alpine-blue?style=flat&logo=nginx&labelColor=FDEBD0&logoColor=blue)
![Uvicorn](https://img.shields.io/badge/Uvicorn-v0.23-green?style=flat&logo=gunicorn&labelColor=FDEBD0&logoColor=blue)
![GitHub](https://img.shields.io/badge/GitHub-blue?style=flat&logo=github&labelColor=FDEBD0&logoColor=blue)


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
    <a href="https://github.com/Studio-Yandex-Practicum/Premium_product_bot_team_3"><strong>Просмотреть документацию »</strong></a>
    <br />
    <br />
    <a href="https://t.me/Comm_Real_Estate_Bot">Демо-версия</a>
    ·
    <a href="https://github.com/Studio-Yandex-Practicum/Premium_product_bot_team_3/issues/new?labels=bug&template=bug-form.yml">Сообщить об ошибке</a>
    ·
    <a href="https://github.com/Studio-Yandex-Practicum/Premium_product_bot_team_3/issues/new?labels=enhancement&template=feature-request---.md">Предложить улучшение</a>
  </p>
</div>


## Описание проекта
Telegram-бот предназначен для упрощения поиска коммерческой недвижимости для аренды или покупки. Бот предоставляет пользователям возможность быстро находить подходящие объекты недвижимости по заданным критериям, а также получать подробную информацию о каждом объекте, контактную информацию владельцев или агентов, и подписываться на уведомления о новых предложениях.

## Функционал бота
### Основные функции для пользователей:
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

### Функции для администраторов:
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

## Запуск проекта:
### На удаленном сервере:
1. Клонируйте репозиторий.
```
git clone git@github.com:Studio-Yandex-Practicum/Premium_product_bot_team_3.git
```

2. Установите и настройте Docker.
- Зайдите на [официальный сайт проекта](https://www.docker.com/products/docker-desktop) и скачайте установочный файл Docker Desktop.

3. Переименуйте файл '.env.example' на 'env' и подставте свои данные.

4. Установите и настройте Nginx.

5. Получите и настройте SLL-сертификат

## Технологии, используемые в проекте:
- Django
- PostgreSQL
- Docker
- Nginx
- ASGI
- Uvicorn
- Telegram API
- python-telegram-bot

## Команда разработчиков:
- [Алексей Данилов](https://github.com/AlexeyDanilov/ )
- [Софья Боровкова](https://github.com/SofiaBorovkova)
- [Андрей Щапов](https://github.com/somwhereAway)
- [Павел Найденов](https://github.com/meteopavel)
- [Дарья Семенова](https://github.com/OFF1GHT)

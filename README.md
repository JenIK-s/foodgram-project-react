# Foodgram

Онлайн-сервис «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

#### Стек технологий:
- Python
- Django
- DRF
- PostgreSQL
- Djoser
- Docker
- Nginx
- Gunicorn

## Запуск проекта
- 1 Клонирование репозитория
- - `git clone git@github.com:JenIK-s/foodgram-project-react.git`
- 2 Создание .env файла с переменными окружения в директории backend/infra
- 3 Запуск Docker compose
- - `Из директории backend/infra выполнить команду ####docker-compose up`
- 4 Выполнение миграций
- - `python manage.py makemigrations users`
- - `python manage.py makemigrations recipes`
- - `python manage.py makemigrations`
- - `python manage.py migrate users`
- - `python manage.py migrate recipes`
- - `python manage.py migrate`
- 5 Загрузка ингредиентов
- - `ИЗ директории backend/ выполнить команду ####python manage.py load_ingredients`
- 6 Создание супер пользователя

## Информация о проекте
Проект расположен по андресу - http://158.160.69.44/
## Аккаунт суперпользователя
Почта - s@gmail.com
Логин - s
Пароль - test123


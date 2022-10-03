[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
![Foodgram workflow](https://github.com/agatinet31/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)
### Описание проекта:
Проект Foodgram - сервис, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
### Тестовый стенд:

http://foodgram-sky.ddns.net/

### Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:agatinet31/foodgram-project-react.git
```

```
cd infra
```

Создать файл .env с переменными окружения для работы с базой данных PostgreSQL:

```
# Указываем, что работаем с postgresql
DB_ENGINE=django.db.backends.postgresql
# Имя базы данных
DB_NAME=postgres 
# Логин для подключения к базе данных
POSTGRES_USER=postgres 
# Пароль для подключения к БД (установите свой)
POSTGRES_PASSWORD=postgres 
# Название сервиса (контейнера)
DB_HOST=db 
# Порт для подключения к БД
DB_PORT=5432 
```
Указываем IP адрес или DNS имя хоста, если проект разворачивается не локально:

```
- переходим в директорию nginx
- в файле default.conf вносим корректировку для параметра server_name 
```

Создаем и запускаем сервисы приложения:

```
docker-compose up
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собираем статику проекта:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Компилируем локали проекта:

```
docker-compose exec web django-admin compilemessages
```

Импорт тестовых данных в БД из файла с фикстурами:

```
docker-compose exec web python manage.py loaddata /app/static/data/fixtures.json
```

Доступ к админке проекта:

```
http://localhost/admin/ для локально расплоложенного проекта.
Если проект расположен на другом узле в сети, 
вместо localhost необходимо указать IP адрес или имя хоста.
```

Остановить сервисы проекта:

```
сочетание клавиш Ctrl+C в терминале
```

Повторный запуск сервисов проекта:

```
docker-compose start
```

### Эндроинты сервиса
```
POST /api/users/ - регистрация
POST /api/auth/token/login - создание токена
POST /api/auth/token/logout/ - удаление токена
GET /api/users/ - просмотр информации о пользователях

POST /api/users/set_password/ - изменение пароля
GET /api/users/{id}/subscribe/ - подписаться на пользователя
DEL /api/users/{id}/subscribe/ - отписаться от пользователя

POST /api/recipes/ - создать рецепт
GET /api/recipes/ - получить рецепты
GET /api/recipes/{id}/ - получить рецепт по id
DEL /api/recipes/{id}/ - удалить рецепт по id

GET /api/recipes/{id}/favorite/ - добавить рецепт в избранное
DEL /api/recipes/{id}/favorite/ - удалить рецепт из избранного

GET /api/users/{id}/subscribe/ - подписаться на пользователя
DEL /api/users/{id}/subscribe/ - отписаться от пользователя

GET /api/ingredients/ - получить список всех ингредиентов

GET /api/tags/ - получить список всех тегов

GET /api/recipes/{id}/shopping_cart/ - добавить рецепт в корзину
DEL /api/recipes/{id}/shopping_cart/ - удалить рецепт из корзины
```
### Документация проекта
```
Полный список эндпоинтов и примеров запросов расположен по адресу http://localhost/api/docs/
```
### Алгоритм регистрации пользователей
```
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт api/users/.Также пользователя может создать администратор — через админ-зону сайта.
Для получения токена пользователь отправляет POST-запрос с параметрами email и password на эндпоинт /api/auth/token/.
```
### Уровни доступа пользователей
```
- Гость (неавторизованный пользователь)
- Авторизованный пользователь
- Администратор
```
### Что могут делать неавторизованные пользователи
```
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.
```
### Что могут делать авторизованные пользователи
```
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
```
### Что может делать администратор
```
Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.
Все эти функции реализованы в стандартной админ-панели Django.
```
### Автор:
Андрей Лабутин

![YaMDb workflow](https://github.com/agatinet31/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
### Описание проекта:
Проект YaMDb - агрегатор отзывов пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка» и т.д. Список категорий может быть расширен администратором системы.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведению может быть присвоен жанр. Новые жанры может создавать только администратор системы.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

### Тестовый стенд:

http://yatube-sky.ddns.net/

### Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:agatinet31/yamdb_final.git
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

### Алгоритм регистрации пользователей

Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).


### Пользовательские роли
Аноним — может просматривать описания произведений, читать отзывы и комментарии.
Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
Суперюзер Django — обладет правами администратора (admin)


### Примеры вызывов API.

### Регистрация нового пользователя

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
```

Тело запроса:
```
{
    "email": "string",
    "username": "string"
}
```

Ответ:
```
{
    "email": "string",
    "username": "string"
}
```


### Получение JWT-токена

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/auth/token/
```

Тело запроса:
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

Ответ:
```
{
    "token": "string"
}
```


### Получение списка всех категорий

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/categories/
```

Ответ:
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
]
```

### Добавление новой категории

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/categories/
```

Тело запроса:
```
{
    "name": "string",
    "slug": "string"
}
```

Ответ:
```
{
    "name": "string",
    "slug": "string"
}
```


### Удаление категории

Пример URL:
```
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
```


### Получение списка всех жанров

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/genres/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

### Добавление жанра

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/genres/
```

Ответ:
```
{
  "name": "string",
  "slug": "string"
}
```


### Удаление жанра

Пример URL:
```
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
```


### Получение списка всех произведений

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/titles/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```


### Добавление произведения

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/titles/
```

Тело запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


### Получение информации о произведении

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


### Частичное обновление информации о произведении

Пример URL:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Тело запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


### Удаление произведения

Пример URL:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```


### Получение списка всех отзывов

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


### Добавление нового отзыва

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Тело запроса:
```
{
  "text": "string",
  "score": 1
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Получение отзыва по id

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Частичное обновление отзыва по id

Пример URL:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Тело запроса:
```
{
  "text": "string",
  "score": 1
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Удаление отзыва по id

Пример URL:
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```


### Получение списка всех комментариев к отзыву

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


### Добавление комментария к отзыву

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Тело запроса:
```
{
  "text": "string"
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Получение комментария к отзыву

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Частичное обновление комментария к отзыву

Пример URL:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Тело запроса:
```
{
  "text": "string"
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Удаление комментария к отзыву

Пример URL:
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```


### Получение списка всех пользователей

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/users/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```


### Добавление пользователя

Пример URL:
```
POST http://127.0.0.1:8000/api/v1/users/
```

Тело запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


### Получение пользователя по username

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/users/{username}/
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


### Изменение данных пользователя по username

Пример URL:
```
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
```

Тело запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


### Удаление пользователя по username

Пример URL:
```
DELETE http://127.0.0.1:8000/api/v1/users/{username}/
```


### Получение данных своей учетной записи

Пример URL:
```
GET http://127.0.0.1:8000/api/v1/users/me/
```

Ответ:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```


### Изменение данных своей учетной записи

Пример URL:
```
PATCH http://127.0.0.1:8000/api/v1/users/me/
```

Тело запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Автор:
Андрей Лабутин

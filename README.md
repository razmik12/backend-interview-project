# Backend Interview Project

Учебный backend-проект на **Python и FastAPI**: REST API для управления проектами, участниками, задачами и комментариями. Проект предназначен для практики backend-разработки и подготовки к собеседованиям на позицию Junior Python Backend Developer.

## Содержание

- [Возможности](#возможности)
- [Технологии](#технологии)
- [Архитектура](#архитектура)
- [Запуск через Docker Compose](#запуск-через-docker-compose)
- [Миграции базы данных](#миграции-базы-данных)
- [API](#api)
- [Тестирование](#тестирование)
- [Проверки качества кода](#проверки-качества-кода)
- [Переменные окружения](#переменные-окружения)

## Возможности

### Аутентификация и безопасность

- Регистрация и вход пользователя.
- Access JWT для авторизации запросов.
- Refresh-токен в `HttpOnly` cookie.
- Обновление токенов с ротацией refresh-токена.
- Хранение состояния refresh-сессий в Redis.
- Хеширование паролей с помощью `pwdlib` и Argon2.
- Проверка прав доступа к проектам, задачам и комментариям.

### Проекты и задачи

- Создание, просмотр, изменение и удаление проектов.
- Добавление участников в проект.
- Роли владельца и участника проекта.
- Создание, просмотр, изменение и удаление задач.
- Изменение статуса задачи и назначение исполнителя.
- Фильтрация списка задач.
- Создание, просмотр и удаление комментариев к задачам.
- Валидация входных данных с помощью Pydantic.

### Инженерные практики

- Асинхронный доступ к PostgreSQL через SQLAlchemy 2.x.
- Разделение HTTP-слоя, бизнес-логики и доступа к данным.
- Repository pattern и Unit of Work.
- Миграции схемы БД через Alembic.
- Обработка ошибок приложения.
- Логирование запросов.
- Тесты API с `pytest` и `httpx`.
- Линтинг и форматирование через Ruff.
- Контейнеризация и CI на GitHub Actions.

## Технологии

| Категория | Технологии |
|---|---|
| Язык | Python 3.11 |
| API | FastAPI, Uvicorn |
| Валидация и настройки | Pydantic v2, pydantic-settings |
| База данных | PostgreSQL 15, SQLAlchemy 2.x, asyncpg |
| Миграции | Alembic |
| Кэш и состояние refresh-сессий | Redis 7 |
| Аутентификация | JWT, `python-jose`, `pwdlib[argon2]` |
| Управление зависимостями | uv, `uv.lock` |
| Тестирование | pytest, pytest-asyncio, HTTPX |
| Качество кода | Ruff, mypy |
| Инфраструктура | Docker, Docker Compose, GitHub Actions |

## Архитектура

```text
app/
├── main.py                 # создание FastAPI-приложения, middleware и роутеры
├── config.py               # настройки из переменных окружения
├── database.py             # SQLAlchemy engine, сессии и Base
├── dependencies.py         # зависимости FastAPI
├── core/
│   ├── security.py         # работа с JWT и паролями
│   ├── redis_app.py        # зависимость Redis
│   └── uow.py              # Unit of Work
├── middleware/
│   └── logging.py          # middleware логирования
├── exceptions/             # ошибки и обработчики исключений
├── models/                 # ORM-модели SQLAlchemy
├── routers/                # HTTP endpoints
├── schemas/                # Pydantic-схемы запросов и ответов
├── repositories/           # запросы к PostgreSQL и Redis
└── services/               # бизнес-логика и проверки доступа

alembic/
├── env.py
└── versions/               # версии миграций

tests/                      # тесты API

docker/
└── Dockerfile

docker-compose.yml
pyproject.toml
uv.lock
```

Основной поток обработки запроса:

```text
HTTP request
    ↓
Router / FastAPI dependencies
    ↓
Service — бизнес-правила и права доступа
    ↓
Unit of Work / Repository
    ↓
PostgreSQL или Redis
    ↓
Pydantic response → HTTP response
```

## Запуск через Docker Compose

### Требования

- Git
- Docker Desktop или Docker Engine с Docker Compose

### 1. Клонировать репозиторий

```bash
git clone https://github.com/razmik12/backend-interview-project.git
cd backend-interview-project
```

### 2. Создать файл окружения

Скопируй пример конфигурации:

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Перед запуском замени значения-заглушки в `.env`, особенно `POSTGRES_PASSWORD` и `SECRET_KEY`. Не добавляй `.env` в Git и не публикуй его содержимое.

### 3. Запустить сервисы

```bash
docker compose up --build -d
```

Команда запускает приложение, PostgreSQL и Redis. После запуска примени миграции:

```bash
docker compose exec app uv run alembic upgrade head
```

Проверить состояние контейнеров и логи:

```bash
docker compose ps
docker compose logs -f app
```

Остановить сервисы, сохранив данные PostgreSQL:

```bash
docker compose down
```

Для локальной разработки Compose подключает исходники к контейнеру. Это конфигурация разработки, а не готовая production-конфигурация.

## Миграции базы данных

Применить все доступные миграции:

```bash
docker compose exec app uv run alembic upgrade head
```

```bash
docker compose exec app uv run alembic revision --autogenerate -m "describe_change"
```

Автогенерируемую миграцию необходимо проверить вручную перед применением. Не редактируй уже применённые миграции так, будто они ещё не использовались.

## API

После запуска доступны:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI schema:** http://localhost:8000/openapi.json

### Основные маршруты

| Метод | Маршрут | Назначение |
|---|---|---|
| `POST` | `/auth/register` | Регистрация пользователя |
| `POST` | `/auth/login` | Вход и получение access-токена |
| `GET` | `/auth/me` | Получение профиля текущего пользователя |
| `POST` | `/auth/refresh` | Обновление токенов с refresh-cookie |
| `POST` | `/auth/logout` | Завершение refresh-сессии |
| `POST` | `/projects` | Создание проекта |
| `GET` | `/projects` | Список проектов текущего пользователя |
| `GET` | `/projects/{project_id}` | Получение проекта и информации об участниках |
| `PATCH` | `/projects/{project_id}` | Изменение проекта |
| `DELETE` | `/projects/{project_id}` | Удаление проекта |
| `POST` | `/projects/{project_id}/members` | Добавление участника в проект |
| `POST` | `/projects/{project_id}/tasks` | Создание задачи |
| `GET` | `/projects/{project_id}/tasks` | Список задач проекта с фильтрами |
| `PATCH` | `/projects/{project_id}/tasks/{task_id}` | Изменение задачи |
| `PATCH` | `/projects/{project_id}/tasks/{task_id}/status` | Изменение статуса задачи |
| `DELETE` | `/projects/{project_id}/tasks/{task_id}` | Удаление задачи |
| `POST` | `/tasks/{task_id}/comments` | Создание комментария |
| `GET` | `/tasks/{task_id}/comments` | Список комментариев задачи |
| `DELETE` | `/comments/{comment_id}` | Удаление комментария |

Большинство маршрутов, кроме регистрации и входа, требуют авторизации. Используй Swagger UI, чтобы посмотреть актуальные схемы запросов, ответы и требования к авторизации.

## Тестирование

Для тестов используется отдельная PostgreSQL-база `postgres_test` и отдельная Redis DB (индекс `1`). Не запускай тесты против базы с важными данными.

Запустить сервисы, включая тестовую БД из профиля `test`:

```bash
docker compose --profile test up -d --build --wait
```

Запустить тесты внутри контейнера приложения:

```bash
docker compose exec app uv run pytest
```

Запустить тесты с подробным выводом:

```bash
docker compose exec app uv run pytest -v
```

Остановить контейнеры после тестирования:

```bash
docker compose --profile test down
```

**Важно:** `docker compose down -v` удаляет именованные volumes, в том числе данные основной PostgreSQL-базы. Используй эту команду только если действительно хочешь удалить данные.

## Проверки качества кода

Запустить Ruff:

```bash
docker compose exec app uv run ruff check .
```

Проверить форматирование без изменения файлов:

```bash
docker compose exec app uv run ruff format --check .
```

Автоматически отформатировать код:

```bash
docker compose exec app uv run ruff format .
```

Запустить mypy:

```bash
docker compose exec app uv run mypy app
```

Проверить Python-файлы на синтаксические ошибки:

```bash
docker compose exec app uv run python -m compileall -q app tests alembic
```

В CI на GitHub Actions выполняются проверки Ruff, форматирования, запуск Docker Compose, миграции Alembic и тесты.

## Переменные окружения

Основные настройки из `.env.example`:

| Переменная | Назначение |
|---|---|
| `POSTGRES_USER` | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL |
| `POSTGRES_DB` | Имя основной базы данных |
| `POSTGRES_HOST` | Имя хоста PostgreSQL; в Compose — `postgres` |
| `POSTGRES_PORT` | Порт PostgreSQL внутри сети Compose, обычно `5432` |
| `TEST_POSTGRES_DB` | Имя тестовой базы данных |
| `TEST_POSTGRES_HOST` | Хост тестовой БД; в Compose — `postgres_test` |
| `TEST_POSTGRES_PORT` | Порт тестовой БД внутри сети Compose, обычно `5432` |
| `SECRET_KEY` | Секрет для подписи JWT; задай случайное непредсказуемое значение |
| `ALGORITHM` | Алгоритм подписи JWT, например `HS256` |
| `access_token_expire_minutes` | Время жизни access-токена в минутах |
| `refresh_token_expire_days` | Срок жизни refresh-сессии в днях |
| `REDIS_HOST` | Хост Redis; в Compose — `redis` |
| `REDIS_PORT` | Порт Redis внутри сети Compose, обычно `6379` |
| `CORS_ORIGINS` | JSON-массив разрешённых origins, например `[`"`http://localhost:3000`"`]` |
| `COOKIE_SECURE` | `true` для HTTPS в production; локально по HTTP может быть `false` |

Значения `postgres`, `postgres_test` и `redis` используются для связи контейнеров внутри сети Docker Compose. Если приложение запускается напрямую на компьютере, эти имена обычно недоступны как сетевые хосты — тогда нужно настроить соответствующие адреса и порты для локального запуска.

## Статус проекта

Это учебный проект, развиваемый итеративно. Конфигурация Docker Compose ориентирована на локальную разработку и тестирование; перед production-развёртыванием необходимо отдельно настроить секреты, HTTPS, доступ к внутренним сервисам, мониторинг и политику резервного копирования.

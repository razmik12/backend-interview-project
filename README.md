# Backend Interview Project

Backend-проект для практики разработки REST API на Python и FastAPI.

## Стек

- Python 3.11
- FastAPI
- PostgreSQL 15
- SQLAlchemy 2.0
- Pydantic v2
- Docker
- Docker Compose

## Реализовано

- регистрация пользователей;
- аутентификация;
- JWT-аутентификация;
- проекты и участники проектов;
- роли участников проекта;
- задачи;
- назначение задач пользователям;
- комментарии к задачам;
- валидация входных данных через Pydantic;
- асинхронная работа с PostgreSQL через SQLAlchemy;
- разделение приложения на API, services, repositories и database layer;
- проверка прав доступа.

## Архитектура

```text
app/
├── api/            # HTTP endpoints
├── core/           # configuration and security
├── db/             # database, sessions and Unit of Work
├── models/         # SQLAlchemy ORM models
├── repositories/   # database operations
├── schemas/        # Pydantic schemas
└── services/       # business logic
```

## Запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/razmik12/backend-interview-project.git
cd backend-interview-project
```

### 2. Создание `.env`

Создай файл `.env` в корне проекта:

```env
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_USER=your_postgres_user
POSTGRES_DB=your_postgres_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
access_token_expire_minutes=30
refresh_token_expire_days=7
```

### 3. Запуск Docker Compose

```bash
docker compose up --build
```

После запуска:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Docker

Приложение запускается в отдельном контейнере и подключается к PostgreSQL.

Docker Compose поднимает:

- FastAPI application;
- PostgreSQL 15;
- PostgreSQL volume для сохранения данных.

PostgreSQL запускается с healthcheck, а FastAPI зависит от успешного запуска базы данных.

## Цель проекта

Учебный backend-проект для практики разработки REST API и подготовки к собеседованиям на позицию Junior Python Backend Developer.

В проекте практикуются:

- FastAPI;
- асинхронный Python;
- PostgreSQL;
- SQLAlchemy;
- REST API;
- аутентификация и авторизация;
- работа с ролями и правами доступа;
- Docker;
- разделение бизнес-логики и работы с базой данных.
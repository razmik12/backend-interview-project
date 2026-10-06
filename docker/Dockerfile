FROM python:3.11-slim

WORKDIR /backend

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /backend/

RUN uv sync --frozen

COPY . /backend/

CMD [ "uv","run","uvicorn","app.main:app","--reload","--host","0.0.0.0","--port","8000" ]
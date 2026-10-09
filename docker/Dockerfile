FROM python:3.11-slim

WORKDIR /backend

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project

COPY . ./

RUN uv sync --locked --no-dev

RUN useradd --create-home --shell /usr/sbin/nologin app \
    && chown -R app:app /backend

USER app

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
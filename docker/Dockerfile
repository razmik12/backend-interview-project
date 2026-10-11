FROM python:3.11-slim

RUN useradd --system --no-create-home app

WORKDIR /backend

COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project

COPY . ./

ENV PATH="/backend/.venv/bin:$PATH"

EXPOSE 8000

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
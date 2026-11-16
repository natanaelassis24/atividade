# Contexto de build: raiz do repositorio.
# docker build -f ci-fastapi/Dockerfile -t fastapi-app:latest .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app
RUN pip install --no-cache-dir poetry==2.1.3
COPY ci-fastapi/pyproject.toml ./
RUN poetry install --only main --no-root --no-interaction
COPY ci-fastapi/main.py ./
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

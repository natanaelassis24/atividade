FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY celery_app.py main.py ./
RUN useradd --create-home estudante
USER estudante
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]

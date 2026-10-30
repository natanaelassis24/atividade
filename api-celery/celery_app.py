"""Tarefas executadas pelo worker, em um processo separado da API."""
import os
import time
from math import factorial

from celery import Celery
from celery.utils.log import get_task_logger

app = Celery(
    "calculos",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
)
app.conf.update(
    task_serializer="json", result_serializer="json", accept_content=["json"],
    result_expires=3600, task_track_started=True,
    broker_connection_retry_on_startup=True,
    task_publish_retry=False, broker_connection_timeout=2,
    broker_transport_options={"socket_connect_timeout": 2, "socket_timeout": 2},
)
logger = get_task_logger(__name__)


@app.task(name="calcular_soma")
def calcular_soma(a: float, b: float):
    time.sleep(5)  # Simula trabalho demorado somente no worker.
    resultado = a + b
    logger.info("SOMA: %s + %s = %s", a, b, resultado)
    return resultado


@app.task(name="calcular_fatorial")
def calcular_fatorial(numero: int):
    # Valida também chamadas diretas, fora da API.
    if isinstance(numero, bool) or not isinstance(numero, int) or not 0 <= numero <= 500:
        raise ValueError("Informe um inteiro entre 0 e 500.")
    time.sleep(5)
    resultado = factorial(numero)  # Implementação eficiente, sem recursão Python.
    logger.info("FATORIAL: %s! = %s", numero, resultado)
    return resultado

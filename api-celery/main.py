"""API: publica tarefas no Redis sem aguardar a execução pelo worker."""
from fastapi import FastAPI, HTTPException
from kombu.exceptions import OperationalError
from pydantic import BaseModel, ConfigDict, Field

from celery_app import app as celery, calcular_fatorial, calcular_soma

app = FastAPI(title="Cálculos em background com Celery")


class SomaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    a: float = Field(ge=-1e100, le=1e100)
    b: float = Field(ge=-1e100, le=1e100)


class FatorialEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")
    numero: int = Field(ge=0, le=500, strict=True)


def publicar(tarefa, *argumentos):
    try:
        resultado = tarefa.delay(*argumentos)
    except OperationalError as erro:
        raise HTTPException(status_code=503, detail="Não foi possível acessar a fila.") from erro
    return {"task_id": resultado.id, "status": "enfileirada"}


# Endpoints síncronos são executados no threadpool do FastAPI: a publicação
# síncrona do Celery não bloqueia o event loop. Não há chamada a result.get().
@app.post("/soma", status_code=202)
def soma(dados: SomaEntrada):
    return publicar(calcular_soma, dados.a, dados.b)


@app.post("/fatorial", status_code=202)
def fatorial(dados: FatorialEntrada):
    return publicar(calcular_fatorial, dados.numero)


@app.get("/tarefas/{task_id}")
def consultar_tarefa(task_id: str):
    resultado = celery.AsyncResult(task_id)
    resposta = {"task_id": task_id, "status": resultado.state}
    if resultado.successful():
        resposta["resultado"] = resultado.result
    elif resultado.failed():
        resposta["erro"] = "Falha no processamento. Consulte o log do worker."
    return resposta

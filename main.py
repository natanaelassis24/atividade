"""Aplicação FastAPI de exemplo; consulte o README para executar."""
import os

from fastapi import FastAPI

app = FastAPI(title=os.getenv("APP_NAME", "Pokédex API"))


@app.get("/")
async def inicio():
    return {
        "mensagem": "Bem-vindo à Pokédex API!",
        "aplicacao": app.title,
        "ambiente": os.getenv("APP_ENV", "development"),
    }


@app.get("/health")
async def health():
    return {"status": "ok"}

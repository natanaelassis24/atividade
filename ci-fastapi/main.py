"""Aplicação didática de apoio: credenciais fixas, sem sessão ou token real.

Não representa uma implementação de autenticação para produção.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Credenciais(BaseModel):
    email: str
    senha: str


@app.post("/auth")
def autenticar(credenciais: Credenciais):
    if credenciais.email == "aluno@exemplo.com" and credenciais.senha == "senha-de-teste":
        return {"mensagem": "Autenticação realizada com sucesso."}
    raise HTTPException(status_code=401, detail="Email ou senha inválidos.")

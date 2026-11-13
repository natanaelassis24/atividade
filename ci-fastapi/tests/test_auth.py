# Dependências: python -m pip install fastapi httpx pytest
# Execute nesta pasta: python -m pytest test_auth.py
# O TestClient chama a API em memória, sem iniciar Uvicorn.

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Cria e fecha o cliente HTTP usado por cada teste."""
    with TestClient(app) as cliente:
        yield cliente


def test_autenticacao_com_credenciais_corretas(client):
    resposta = client.post(
        "/auth",
        json={"email": "aluno@exemplo.com", "senha": "senha-de-teste"},
    )

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Autenticação realizada com sucesso."}


@pytest.mark.parametrize(
    "email,senha",
    [
        ("aluno@exemplo.com", "senha-incorreta"),
        ("outro@exemplo.com", "senha-de-teste"),
        ("outro@exemplo.com", "senha-incorreta"),
    ],
)
def test_autenticacao_com_credenciais_invalidas(client, email, senha):
    resposta = client.post("/auth", json={"email": email, "senha": senha})

    assert resposta.status_code == 401
    assert resposta.json() == {"detail": "Email ou senha inválidos."}

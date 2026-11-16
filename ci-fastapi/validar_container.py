"""Smoke test HTTP da imagem em execucao, usando apenas a biblioteca padrao."""
import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:8000"


def autenticar(senha):
    dados = json.dumps({"email": "aluno@exemplo.com", "senha": senha}).encode()
    pedido = Request(BASE + "/auth", data=dados, headers={"Content-Type": "application/json"})
    try:
        with urlopen(pedido, timeout=5) as resposta:
            return resposta.status, json.load(resposta)
    except HTTPError as resposta:
        return resposta.code, json.load(resposta)


def main():
    # Tentativas limitadas para aguardar o startup; nao ignora falhas finais.
    for _ in range(30):
        try:
            with urlopen(BASE + "/openapi.json", timeout=2) as resposta:
                assert resposta.status == 200
                assert "/auth" in json.load(resposta)["paths"]
            break
        except (URLError, TimeoutError):
            time.sleep(1)
    else:
        raise RuntimeError("O container nao disponibilizou a API no prazo.")

    assert autenticar("senha-de-teste") == (
        200, {"mensagem": "Autenticação realizada com sucesso."}
    )
    assert autenticar("senha-errada") == (
        401, {"detail": "Email ou senha inválidos."}
    )
    print("Container validado: OpenAPI 200, autenticacao 200 e rejeicao 401.")


if __name__ == "__main__":
    main()

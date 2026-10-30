"""Teste HTTP real. Execute com a API e o worker já iniciados."""
import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "http://localhost:8003"


def requisitar(rota, dados=None):
    corpo = None if dados is None else json.dumps(dados).encode()
    pedido = Request(BASE + rota, data=corpo, headers={"Content-Type": "application/json"})
    with urlopen(pedido, timeout=10) as resposta:
        return resposta.status, json.load(resposta)


def main():
    for _ in range(60):
        try:
            requisitar("/openapi.json")
            break
        except (URLError, TimeoutError):
            time.sleep(1)
    else:
        raise RuntimeError("A API não iniciou.")

    tarefas = []
    for rota, dados, esperado in [
        ("/soma", {"a": 10, "b": 20}, 30),
        ("/fatorial", {"numero": 5}, 120),
        ("/fatorial", {"numero": 0}, 1),
    ]:
        inicio = time.perf_counter()
        status, resposta = requisitar(rota, dados)
        duracao = time.perf_counter() - inicio
        assert status == 202 and resposta["task_id"]
        assert duracao < 5, "A resposta demorou mais que a tarefa simulada."
        print(f"POST {rota}: HTTP {status}, {duracao:.3f}s, task_id={resposta['task_id']}", flush=True)
        tarefas.append((resposta["task_id"], esperado))

    for identificador, esperado in tarefas:
        for _ in range(60):
            _, resposta = requisitar(f"/tarefas/{identificador}")
            assert resposta["status"] != "FAILURE", resposta
            if resposta["status"] == "SUCCESS":
                assert resposta["resultado"] == esperado, resposta
                print(f"Tarefa {identificador}: SUCCESS, resultado={esperado}", flush=True)
                break
            time.sleep(1)
        else:
            raise AssertionError("Worker não finalizou a tarefa.")

    try:
        requisitar("/fatorial", {"numero": -1})
    except HTTPError as erro:
        assert erro.code == 422
        print("Fatorial negativo: HTTP 422", flush=True)
    else:
        raise AssertionError("Entrada negativa deveria ser rejeitada.")
    print("Todos os testes passaram.", flush=True)


if __name__ == "__main__":
    main()

# FastAPI, Celery e Redis: cálculos em background

A API publica tarefas na fila Redis; processos do worker executam a soma e o
fatorial. Cada tarefa simula cinco segundos de trabalho. Os endpoints retornam
HTTP **202** com `task_id` após publicar, sem aguardar o cálculo.

## Executar com Docker (recomendado no Windows)

Com Docker Desktop em execução e usando containers Linux, na raiz do projeto:

```sh
cd api-celery
docker compose up --build -d
docker compose logs -f worker
```

Abra http://localhost:8003/docs. O Compose inicia Redis, API e um worker com
dois processos. O Redis não publica portas no host. Para encerrar:
`docker compose down`.

## Executar com Python (Linux/WSL)

Requer Python 3.10+, Redis e terminais separados. Na pasta `api-celery`:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
docker run --rm -d --name redis-calculos -p 127.0.0.1:6379:6379 redis:7.4-alpine
```

No primeiro terminal, inicie o worker:

```sh
celery -A celery_app worker -l info
```

No segundo, ative o mesmo ambiente e inicie a API:

```sh
python -m uvicorn main:app --port 8003
```

Use Docker/WSL para o worker no Windows. API e worker usam os padrões
`CELERY_BROKER_URL=redis://localhost:6379/0` e
`CELERY_RESULT_BACKEND=redis://localhost:6379/1`. No Compose, o host é `redis`.
O banco 0 distribui mensagens; o banco 1 armazena resultados por uma hora.
Para encerrar a alternativa local, interrompa API/worker e use
`docker stop redis-calculos`.

## Testar com curl

Comandos para Bash/Git Bash (use curl.exe ou Postman no Windows):

```sh
curl -i -w '\nTempo: %{time_total}s\n' -X POST http://localhost:8003/soma -H 'Content-Type: application/json' -d '{"a":10,"b":20}'
curl -i -w '\nTempo: %{time_total}s\n' -X POST http://localhost:8003/fatorial -H 'Content-Type: application/json' -d '{"numero":5}'
```

Ambos retornam 202 e `{"task_id":"...","status":"enfileirada"}` sem esperar
os cinco segundos da tarefa. A publicação ainda requer comunicação com o broker;
"enfileirada" não significa que o cálculo já terminou.
Copie cada ID e consulte, sem bloquear esperando a conclusão:

```sh
curl http://localhost:8003/tarefas/COLE_O_TASK_ID
```

Ao finalizar, a resposta terá `status: SUCCESS` e `resultado: 30.0` para soma
ou `resultado: 120` para 5!. O log do worker mostra `SOMA`, `FATORIAL` e
as mensagens de tarefa concluída. PENDING também pode significar ID desconhecido
ou resultado expirado; o endpoint de consulta não mantém um cadastro de IDs.

O fatorial aceita somente inteiros de 0 a 500, inclusive 0! = 1. Usa
`math.factorial`, sem recursão Python. O limite evita respostas e logs
excessivamente grandes. Entradas inválidas retornam 422; falhas de publicação
na fila retornam 503. As tarefas usam `def`: a execução assíncrona é fornecida
pela fila Celery, não por corrotinas. Os endpoints usam o threadpool do FastAPI
para que a publicação síncrona do Celery não bloqueie o event loop.

## Testes e evidências

Com o ambiente iniciado, execute `python testar_api.py`. O script faz requisições
HTTP reais e verifica respostas 202 antes dos cinco segundos, resultados de
soma, 5! e 0!, e rejeição de fatorial negativo com 422.

A automação `.github/workflows/celery.yml` executa os mesmos testes no GitHub
Actions e salva os registros reais em `evidencias/testes.log` e
`evidencias/worker.log` após sucesso. Consulte esses arquivos para a evidência
de execução; não são saídas simuladas.

Referência: [Primeiros passos com Celery](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html).

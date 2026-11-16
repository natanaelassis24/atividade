# CI da aplicação FastAPI com Poetry

Esta atividade fica separada na pasta `ci-fastapi`. Ela reutiliza uma cópia
da aplicação e dos testes de autenticação do exercício anterior.

O arquivo executável do workflow fica em
`../.github/workflows/python-app.yml`: o GitHub exige esse caminho na raiz do
repositório. Os comandos do job usam `working-directory: ci-fastapi`, mantendo
as dependências e os testes desta atividade separados dos outros exercícios.

## Pipeline

A cada push na branch `master` (branch principal deste repositório), o job:

1. Executa em `ubuntu-latest` e usa `actions/checkout@v3`.
2. Instala Python 3.12 e Poetry 2.1.3.
3. Executa `poetry install --no-root --no-interaction`.
4. Executa `poetry run pytest`.
5. Constrói a mesma aplicação testada com
   `docker build -f ci-fastapi/Dockerfile -t "$IMAGE_NAME" .` na raiz do repositório.
6. Executa `docker run`, aguarda o startup e verifica OpenAPI, autenticação
   válida (200) e inválida (401) por HTTP real. Exibe logs e remove o container.

`IMAGE_NAME` é `fastapi-app:latest`. O contexto do build é `.` (raiz), e o
Dockerfile específico desta atividade fica em `ci-fastapi/Dockerfile`.
Esses passos ocorrem depois dos testes e não ignoram falhas de build ou execução.

Se qualquer teste falhar, pytest retorna um código diferente de zero e o job
falha. O workflow também roda em pull requests destinados a `master`.
Para impedir merge quando o CI falhar, é preciso configurar uma regra de
proteção da branch com este check obrigatório; o workflow sozinho detecta
falhas, mas não impede pushes nem bloqueia merges automaticamente.

## Executar localmente

Requer Python 3.12. No Prompt de Comando:

```bat
cd /d C:\Users\natan\Downloads\atividade\ci-fastapi
python -m pip install poetry==2.1.3
poetry install --no-root --no-interaction
poetry run pytest
```

Os testes usam TestClient e não precisam de servidor ou banco de dados.
Há um cenário de autenticação válida e três combinações inválidas.

## Entrega

O arquivo pedido é `.github/workflows/python-app.yml`, na raiz do repositório.
O resultado de cada push pode ser conferido na aba Actions, no workflow
**CI FastAPI com Poetry**.

Referência: [localização de workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).

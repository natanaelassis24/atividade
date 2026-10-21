# FastAPI com Docker, Compose e Poetry

Aplicação de exemplo com endpoints `/` e `/health` e documentação em `/docs`.
O arquivo `pokedex.py` preserva o exercício anterior de terminal e pode ser
executado separadamente com `python pokedex.py`.

## 1. Pré-requisitos

Instale Git e Docker com Docker Compose (por exemplo, Docker Desktop usando
containers Linux). Inicie o Docker e deixe a porta 8000 disponível.
Não é necessário instalar Python ou Poetry no host.

## 2. Obter o projeto

Depois de publicar este projeto, substitua o endereço pelo URL real:

```sh
git clone <URL_DO_REPOSITORIO> pokedex-api
cd pokedex-api
```

Se já está na pasta do projeto, siga para o próximo passo.

## 3. Construir e iniciar

```sh
docker compose up --build -d
```

No Compose legado, use `docker-compose up --build -d`.
O primeiro build precisa de internet para baixar a imagem e os pacotes.
As variáveis necessárias já estão configuradas no Compose.

## 4. Verificar

Abra http://localhost:8000 e http://localhost:8000/docs.
Em http://localhost:8000/health, a resposta deve ser `{"status":"ok"}`.

```sh
docker compose ps
docker compose logs --tail=50 api
```

Após o healthcheck, o serviço deve aparecer como `healthy`.
Altere a mensagem em `main.py`, salve e atualize o navegador para verificar o
recarregamento. O volume `.:/app` sincroniza os arquivos, e `--reload` monitora
alterações. As dependências ficam em `/opt/venvs`, fora do volume de código.

## 5. Encerrar

```sh
docker compose down
```

No Compose legado: `docker-compose down`.
Para verificar um build do zero:

```sh
docker compose down
docker compose build --no-cache
docker compose up -d
```

Repita as verificações do passo 4.

## Configuração

- `APP_NAME`: título da API.
- `APP_ENV`: ambiente exibido pelo endpoint inicial.
- `WATCHFILES_FORCE_POLLING`: detecção de mudanças no volume pelo Docker Desktop.
- `8000:8000`: porta do host e porta do container, respectivamente.

O Dockerfile instala Poetry e usa `poetry install` para instalar as dependências.
O servidor escuta em `0.0.0.0:8000`. O Compose habilita o recarregamento para
uso em desenvolvimento; o comando padrão da imagem executa sem recarregamento:

```sh
docker build -t pokedex-api .
docker run --rm -p 8000:8000 pokedex-api
```

## Lockfile

As versões diretas estão fixadas em `pyproject.toml`. Como não há Poetry/Python
neste ambiente, o lockfile não foi gerado localmente. Sem ele, o build resolve
as dependências transitivas automaticamente. Para gerar o arquivo usando
somente Docker, depois do primeiro build:

```sh
docker compose run --rm --no-deps api poetry lock
docker compose up --build -d
```

Inclua `poetry.lock` no Git para fixar também as dependências transitivas.
O Dockerfile o utiliza automaticamente quando presente. Mudanças nas
dependências exigem reconstruir a imagem.

## Estado da verificação

Docker e Python não estão disponíveis no ambiente de elaboração, portanto o
build e a execução ainda não foram testados. Os passos acima descrevem como
validar o fluxo completo em uma máquina com Docker.

## Referências

- [FastAPI em containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Dependências com Poetry](https://python-poetry.org/docs/basic-usage/)

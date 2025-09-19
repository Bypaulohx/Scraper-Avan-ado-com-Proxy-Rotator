# Scraper Responsável com Proxy Rotator (Python + Selenium) — Docker + Postgres

Este repositório contém um exemplo educativo e responsável de um scraper que usa pool de proxies e pode usar Postgres como armazenamento.
**Importante:** o projeto foi desenhado para scraping responsável — respeite `robots.txt` e termos de uso do site alvo.

## Como usar (com Docker Compose)
1. Copie `.env.example` para `.env` e ajuste as variáveis se necessário.
2. Construa e suba os serviços:

```bash
docker compose up --build -d
```

3. Para ver logs do contêiner da aplicação:

```bash
docker compose logs -f app
```

4. Para executar o script manualmente dentro do container (exemplo):

```bash
docker compose exec app python src/main.py
```

## Estrutura
- `src/` — código fonte Python
- `Dockerfile` — imagem da aplicação
- `docker-compose.yml` — define serviços `app` e `db` (Postgres)
- `.env.example` — variáveis de ambiente

## Observações
- O storage está configurado para `postgres` por padrão no `src/config.yaml`.
- Para desenvolvimento local sem Docker, instale dependências: `pip install -r requirements.txt` e rode `python src/main.py`.

# Run Planner (Flask + Local CI/CD Starter)

A modular-monolith Flask app skeleton for iRacing run planning and setup decisions **with local CI/CD**.

What you get:
- Flask app factory, web + API blueprints
- SQLAlchemy models + Alembic migrations
- **CI pipeline**: lint (ruff, black), type-check (mypy), tests (pytest+coverage)
- **Run CI locally with `act`** (no cloud needed)
- Dockerfile + docker-compose (optional Postgres)
- Pre-commit hooks

## Quickstart (app)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
flask --app wsgi:app run --debug
```

Test the API:

```bash
curl -X POST http://127.0.0.1:5000/api/run-plans/1/decide/camber   -H "Content-Type: application/json"   -d '{"inner":85,"middle":78,"outer":70,"target_spread":10}'
```

## Local CI (no GitHub required)

Install `act`: https://github.com/nektos/act

```bash
# run the same checks GitHub Actions will run
act -W .github/workflows/ci.yml -j lint-test
```

If you see an image error, use our mapping:
```bash
act --container-architecture linux/amd64     -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-22.04     -W .github/workflows/ci.yml -j lint-test
```

## GitHub Actions

- On push/PR: ruff, black --check, mypy, pytest (coverage artifact)
- On tag: Docker build & push to GHCR (optional; requires permissions)

## Docker (optional)

Production-ish:
```bash
docker build -t run-planner:local .
docker run -p 8000:8000 --env-file .env run-planner:local
# http://127.0.0.1:8000
```

Local Postgres:
```bash
docker compose up -d
# DATABASE_URL is set in compose to postgres
alembic upgrade head
```

## Repo layout
(abridged)
```
app/                # your code
.github/workflows/  # CI config
tests/              # pytest suite
migrations/         # alembic
```

## Pre-commit
```bash
pre-commit install
pre-commit run --all-files
```

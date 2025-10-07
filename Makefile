.PHONY: install dev lint format typecheck test cover run migrate act-test docker-build

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

dev:
	flask --app wsgi:app run --debug

lint:
	ruff check app tests
	black --check app tests

format:
	black app tests
	ruff check --fix app tests

typecheck:
	mypy app

test:
	pytest -q

cover:
	pytest --cov=app --cov-report=term-missing

migrate:
	alembic upgrade head

act-test:
	act -W .github/workflows/ci.yml -j lint-test

docker-build:
	docker build -t run-planner:local .

compose-up:
	docker compose up --build
compose-db:
	docker compose up -d db
compose-rev:
	docker compose run --rm app alembic revision --autogenerate -m "$(m)"
compose-migrate:
	docker compose run --rm app alembic upgrade head
compose-down:
	docker compose down -v

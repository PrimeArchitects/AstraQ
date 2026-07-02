.PHONY: help setup up down restart logs ps build \
        backend-shell frontend-shell \
        migrate migrate-new \
        lint lint-fix format test test-backend test-frontend \
        clean

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup: ## First-time setup: copy env files, install local tooling.
	cp -n .env.example .env || true
	cp -n backend/.env.example backend/.env || true
	cp -n frontend/.env.example frontend/.env.local || true
	@echo "Environment files created. Run 'make up' to start the stack."

up: ## Start the full stack in the background.
	docker compose up -d --build

down: ## Stop and remove all containers.
	docker compose down

restart: down up ## Restart the full stack.

logs: ## Tail logs from all services.
	docker compose logs -f

ps: ## Show status of all services.
	docker compose ps

build: ## Rebuild all container images.
	docker compose build --no-cache

backend-shell: ## Open a shell inside the backend container.
	docker compose exec backend bash

frontend-shell: ## Open a shell inside the frontend container.
	docker compose exec frontend sh

migrate: ## Apply database migrations.
	docker compose exec backend alembic upgrade head

migrate-new: ## Generate a new migration. Usage: make migrate-new name="add users table"
	docker compose exec backend alembic revision --autogenerate -m "$(name)"

lint: ## Lint backend and frontend.
	docker compose exec backend ruff check .
	docker compose exec frontend npm run lint

lint-fix: ## Lint and auto-fix backend and frontend.
	docker compose exec backend ruff check --fix .
	docker compose exec frontend npm run lint:fix

format: ## Format backend and frontend code.
	docker compose exec backend black .
	docker compose exec frontend npm run format

test: test-backend test-frontend ## Run all test suites.

test-backend: ## Run backend tests.
	docker compose exec backend pytest

test-frontend: ## Run frontend tests.
	docker compose exec frontend npm run test

clean: ## Stop containers and remove volumes (destroys local DB data).
	docker compose down -v

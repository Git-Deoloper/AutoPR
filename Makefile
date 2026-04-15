# LocalClaw Makefile

.PHONY: help install dev test lint format clean run-cli run-web docker-build docker-up

help:
	@echo "LocalClaw Development Commands"
	@echo "=============================="
	@echo "make install       - Install in production mode"
	@echo "make dev           - Install in development mode with all dependencies"
	@echo "make test          - Run tests"
	@echo "make lint          - Run linting checks"
	@echo "make format        - Format code with black and isort"
	@echo "make clean         - Clean build artifacts"
	@echo "make run-cli       - Run CLI (e.g., make run-cli CMD='analyze README.md')"
	@echo "make run-web       - Run web server"
	@echo "make docker-build  - Build Docker image"
	@echo "make docker-up     - Start Docker containers"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -v

test-cov:
	pytest -v --cov=src/localclaw --cov-report=html

lint:
	flake8 src/localclaw tests
	mypy src/localclaw

format:
	black src/localclaw tests
	isort src/localclaw tests

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

run-cli:
	python -m localclaw.cli.main $(CMD)

run-web:
	python -m localclaw.web.server --reload

docker-build:
	docker build -t localclaw:latest .

docker-up:
	docker-compose up

docker-down:
	docker-compose down

.DEFAULT_GOAL := help

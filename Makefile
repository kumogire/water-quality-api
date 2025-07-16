.PHONY: help install dev test lint format clean docker-build docker-run deploy

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

dev:  ## Install development dependencies
	pip install -r requirements-dev.txt
	pre-commit install

test:  ## Run tests
	pytest tests/ -v --cov=app --cov-report=html

test-watch:  ## Run tests in watch mode
	pytest-watch tests/ -- -v

lint:  ## Run linting
	flake8 app tests
	mypy app
	black --check app tests
	isort --check-only app tests

format:  ## Format code
	black app tests
	isort app tests

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

docker-build:  ## Build Docker image
	docker build -t usgs-water-api .

docker-run:  ## Run Docker container
	docker run -p 8000:8000 --env-file .env usgs-water-api

docker-dev:  ## Run development environment
	docker-compose up -d

deploy-gcp:  ## Deploy to Google Cloud Run
	./scripts/deploy.sh gcp

deploy-aws:  ## Deploy to AWS ECS
	./scripts/deploy.sh aws
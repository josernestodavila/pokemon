.DEFAULT_GOAL := help

PYTHON_VERSION = 3.11.6

.PHONY: run ## Run app docker containers
run:
	echo "💥 Shutting down containers if they are running..."
	docker compose -f docker-compose.yml down
	
	echo "🚀 Launching containers..."
	docker compose -f docker-compose.yml up -d

.PHONY: build ## Build the app docker containers
build:
	echo "🔨 Building containers..."
	docker compose -f docker-compose.yml build

.PHONY: healthcheck ## Makes a get request to verify the app is running
healthcheck:
	echo "🩺 Running healthcheck..."
	curl --silent --fail http://127.0.0.0:8000/health || exit 1

.PHONY: venv ## Create a Python virtualenv and install dependencies
venv:
	echo "🐍 Creating Python virtualenv..."
	PYTHON_VERSION=$$PYTHON_VERSION python3 -m venv venv
	. ./venv/bin/activate
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
	pre-commit install --install-hooks

.PHONY: help ## Display this message
help:
	@grep -E \
		'^.PHONY: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".PHONY: |## "}; {printf "\033[36m%-20s\033[0m %s\n", $$2, $$3}'

DOCKER_COMPOSE_CMD=docker-compose

lint:
	ruff check --select I --fix

fmt:
	ruff format

test-up:
	docker-compose -f tests/docker-compose.yaml up -d

run-api:
	$(DOCKER_COMPOSE_CMD) up --force-recreate --build -d api

run-bot:
	$(DOCKER_COMPOSE_CMD) up --force-recreate --build -d bot

run-load-collections:
	$(DOCKER_COMPOSE_CMD) up --force-recreate --build collections

run-load-items:
	$(DOCKER_COMPOSE_CMD) up --force-recreate --build items

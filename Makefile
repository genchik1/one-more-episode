DOCKER_COMPOSE_CMD=docker-compose

lint:
	ruff check --select I --fix

fmt:
	ruff format

test-up:
	docker-compose -f tests/docker-compose.yaml up -d

down:
	$(DOCKER_COMPOSE_CMD) down

run:
	$(DOCKER_COMPOSE_CMD) up --force-recreate --build -d api bot nginx

run-load-collections:
	$(DOCKER_COMPOSE_CMD) up collections

run-load-items:
	$(DOCKER_COMPOSE_CMD) up --build items

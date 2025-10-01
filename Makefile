lint:
	ruff check --select I --fix

fmt:
	ruff format

test-up:
	docker-compose -f tests/docker-compose.yaml up -d

run-api:
	docker-compose up
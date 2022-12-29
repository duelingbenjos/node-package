COMPOSE_FILE = docker/docker-compose.yml

boot:
	docker compose -f $(COMPOSE_FILE) up -d
	@sleep 3
	nohup python upgrade.py > upgrade.log 2>&1 &

teardown:
	docker compose -f $(COMPOSE_FILE) down
	- pkill -f upgrade

build:
	docker compose -f $(COMPOSE_FILE) build --no-cache

deploy: build boot

reboot: teardown boot

upgrade: build
	docker compose -f $(COMPOSE_FILE) down
	docker compose -f $(COMPOSE_FILE) up -d

enter:
	docker compose -f $(COMPOSE_FILE) exec $(service) bash

clean:
	docker rmi lamden

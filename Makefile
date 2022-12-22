COMPOSE_FILE = docker/docker-compose.yml

boot:
	docker compose -f $(COMPOSE_FILE) up -d
	@sleep 3
	nohup python upgrade_manager.py > upgrade-manager.log 2>&1 &

teardown:
	docker compose -f $(COMPOSE_FILE) down
	- pkill -f upgrade_manager

build:
	docker compose -f $(COMPOSE_FILE) build --no-cache

deploy: build boot

reboot: teardown boot

upgrade: build
	docker compose -f $(COMPOSE_FILE) down
	docker compose -f $(COMPOSE_FILE) up -d

# service=lamden-node make enter
enter:
	docker compose -f $(COMPOSE_FILE) exec $(service) bash

clean:
	docker rmi lamden

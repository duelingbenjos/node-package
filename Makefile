COMPOSE_FILE = docker/docker-compose.yml

boot:
ifeq ($(LAMDEN_NETWORK),arko)
	export LAMDEN_BOOTNODES="TBD"; \
	docker compose -f $(COMPOSE_FILE) up -d
else ifeq ($(LAMDEN_NETWORK),testnet)
	export LAMDEN_BOOTNODES="128.199.9.156:178.62.52.51:142.93.210.208"; \
	docker compose -f $(COMPOSE_FILE) up -d
else
	docker compose -f $(COMPOSE_FILE) up -d
endif
	@sleep 3
	nohup python upgrade.py > /dev/null 2>&1 &

teardown:
	docker compose -f $(COMPOSE_FILE) down
	- pkill -f upgrade

build:
ifeq ($(LAMDEN_NETWORK),arko)
	export LAMDEN_TAG="TBD" CONTRACTING_TAG="TBD"; \
	docker compose -f $(COMPOSE_FILE) build --no-cache
else ifeq ($(LAMDEN_NETWORK),testnet)
	export LAMDEN_TAG="staging-0.0.1" CONTRACTING_TAG="staging"; \
	docker compose -f $(COMPOSE_FILE) build --no-cache
else
	docker compose -f $(COMPOSE_FILE) build --no-cache
endif

deploy: build boot

reboot: teardown boot

enter:
	docker compose -f $(COMPOSE_FILE) exec $(service) bash

clean:
	docker rmi lamden

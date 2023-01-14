COMPOSE_FILE = docker/docker-compose.yml

boot:
ifeq ($(LAMDEN_NETWORK),mainnet)
	export LAMDEN_BOOTNODES="TODO"
endif
ifeq ($(LAMDEN_NETWORK),testnet)
	export LAMDEN_BOOTNODES="128.199.9.156:178.62.52.51:142.93.210.208"
endif
	docker compose -f $(COMPOSE_FILE) up -d
	@sleep 3
	nohup python upgrade.py > upgrade.log 2>&1 &

teardown:
	docker compose -f $(COMPOSE_FILE) down
	- pkill -f upgrade

build:
ifeq ($(LAMDEN_NETWORK),mainnet)
	export LAMDEN_TAG="TODO"
	export CONTRACTING_TAG="TODO"
endif
ifeq ($(LAMDEN_NETWORK),testnet)
	export LAMDEN_TAG="staging"
	export CONTRACTING_TAG="staging"
endif
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

COMPOSE_FILE = docker/docker-compose.yml

HOST_IP := $(shell python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]); s.close()")

start:
	docker compose -f $(COMPOSE_FILE) up -d

stop:
	docker compose -f $(COMPOSE_FILE) down

restart: stop start

build:
ifeq ($(LAMDEN_NETWORK),arko)
	export LAMDEN_TAG="v2.0.15" CONTRACTING_TAG="v2.0.5"; \
	docker compose -f $(COMPOSE_FILE) build --no-cache
else ifeq ($(LAMDEN_NETWORK),testnet)
	export LAMDEN_TAG="v2.0.15" CONTRACTING_TAG="v2.0.5"; \
	docker compose -f $(COMPOSE_FILE) build --no-cache
else
	docker compose -f $(COMPOSE_FILE) build --no-cache
endif

boot:
ifeq ($(LAMDEN_PRIVATE_NETWORK),)
	$(MAKE) boot-original
else
	$(MAKE) boot-private
endif

boot-original:
ifeq ($(LAMDEN_NETWORK),arko)
	export LAMDEN_BOOTNODES="64.225.32.184:170.64.178.113:134.122.98.27"; \
	docker compose -f $(COMPOSE_FILE) up -d
else ifeq ($(LAMDEN_NETWORK),testnet)
	export LAMDEN_BOOTNODES="128.199.9.156:178.62.52.51:142.93.210.208"; \
	docker compose -f $(COMPOSE_FILE) up -d
else
	docker compose -f $(COMPOSE_FILE) up -d
endif
	@sleep 3
	@mkdir -p logs
	nohup python event_handler.py > /dev/null 2>&1 &

boot-private:
	export LAMDEN_PRIVATE_NETWORK=$(HOST_IP); \
	$(MAKE) boot-original

teardown:
	docker compose -f $(COMPOSE_FILE) down
	- pkill -f event_handler.py

deploy: build boot

redeploy: teardown deploy

reboot: teardown boot

enter:
	docker compose -f $(COMPOSE_FILE) exec $(service) bash

clean:
	docker rmi lamden

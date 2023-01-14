# Lamden Node Package
This repository contains lamden node package.

### Prerequisites
- [GNU make](https://www.gnu.org/software/make/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/) 3.6 or later

### Configuration
The Lamden node can be configured using environment variables. The following environment variables are supported:
- `LAMDEN_SK` (required): The secret key of the node owner.
- `LAMDEN_NETWORK` (optional): The network to join to (e.g. `mainnet`, `testnet`). Leave empty to start a new network.
- `LAMDEN_TAG` and `CONTRACTING_TAG`: The version of [lamden](https://github.com/Lamden/lamden) and [contracting](https://github.com/Lamden/contracting) to use. If `LAMDEN_NETWORK` is set this parameters are ignored.

You can use `export` command to set an enviroment variable, for example:
```bash
export LAMDEN_SK=beefbeefbeefbeefbeefbeefbeefbeefbeefbeefbeefbeefbeefbeefbeefbeef
export LAMDEN_NETWORK=mainnet
```

### Managing a node
To manage a node, the following `make` commands are available:
- `make build`: Build a base lamden docker image used by all containers using the latest code of the version specified by `LAMDEN_TAG` and `CONTRACTING_TAG`.
- `make boot`: Start all containers and related scripts.
- `make deploy`: `build` and `boot` executed sequentially.
- `make teardown`: Stop all containers and related scripts.
- `make reboot`: `teardown` and `boot` executed sequentially.
- `make upgrade`: Rebuild a base image and restart the containers with a fresh image.
- `make enter service=<lamden_node|lamden_webserver|lamden_events>`: Open a `bash` session in the specified service (container).
- `make clean`: Delete base lamden docker image.

### Contributing
We welcome contributions to this repository! If you have any suggestions or improvements, please feel free to open an issue or submit a pull request.

# Lamden Node Package
This repository contains lamden node package.

### Prerequisites
- [Python](https://www.python.org/) 3.6 or above
- [GNU make](https://www.gnu.org/software/make/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Configuration
The Lamden node package can be configured using environment variables. The following environment variables are supported:
- `LAMDEN_SK` (required): The secret key of the node owner.
- `LAMDEN_NETWORK` (required): The network to join (`arko` or `testnet`).
- `LAMDEN_TAG` (optional): Check out available tags [here](https://github.com/Lamden/lamden/tags). If not set, latest stable version is used by default.
- `CONTRACTING_TAG` (optional): Check out available tags [here](https://github.com/Lamden/contracting/tags). If not set, latest stable version is used by default.

### Setup
```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Managing the node package
:exclamation: **Run this command to purge `LAMDEN_SK` from command line history when you're done setting up the node:**
```bash
history -c
```

#### Deploying
```bash
export LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network>

# Optional
export LAMDEN_TAG=<tag> CONTRACTING_TAG=<tag>

make deploy
```

#### Redeploying
```bash
export LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network> LAMDEN_TAG=<tag> CONTRACTING_TAG=<tag>
make redeploy
```

#### Restarting
```bash
export LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network>
make reboot
```

#### Stopping
```bash
export LAMDEN_SK=<your_sk>
make teardown
```

### Contributing
We welcome contributions to this repository! If you have any suggestions or improvements, please feel free to open an issue or submit a pull request.

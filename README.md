# Lamden Node Package
This repository contains lamden node package.

### Dependencies
- [Python](https://www.python.org/) 3.6 or above
- [GNU make](https://www.gnu.org/software/make/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation
```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Configuration
The Lamden node package is configured using the following environment variables:
- `LAMDEN_SK` (required): The secret key of the node owner.
- `LAMDEN_NETWORK` (required): The network to join (`arko` or `testnet`).
- `LAMDEN_TAG` and `CONTRACTING_TAG` (optional): Check out available [lamden](https://github.com/Lamden/lamden/tags) and [contracting](https://github.com/Lamden/contracting/tags) tags. If not set, latest stable tags are used by default.

### Usage
:exclamation: **Run this command to purge `LAMDEN_SK` from bash history when you're done:**
```bash
history -c
```

#### Deploying
```bash
# Optional
export LAMDEN_TAG=<tag> CONTRACTING_TAG=<tag>

. venv/bin/activate
LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network> make deploy
```

#### Redeploying
```bash
. venv/bin/activate
LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network> LAMDEN_TAG=<tag> CONTRACTING_TAG=<tag> make redeploy
```

#### Restarting
```bash
. venv/bin/activate
LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network> make reboot
```

#### Stopping
```bash
LAMDEN_SK=<your_sk> make teardown
```

### Contributing
We welcome contributions to this repository! If you have any suggestions or improvements, please feel free to open an issue or submit a pull request.

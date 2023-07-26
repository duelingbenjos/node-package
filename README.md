v1.5.0

# Lamden Node Package
This repository contains lamden node package. It consists of several containerized applications: the [node software](https://github.com/Lamden/lamden), the [webserver](https://github.com/Lamden/lamden/blob/master/lamden/nodes/masternode/webserver.py) and the [events service](https://github.com/Lamden/lamden/blob/master/lamden/nodes/events.py).

### Dependencies
- [Python](https://www.python.org/) 3.6 or above
- [GNU make](https://www.gnu.org/software/make/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation
```bash
$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

### Configuration
The Lamden node package is configured using the following environment variables:
- `LAMDEN_SK` (required): The secret key of the node owner.
- `LAMDEN_NETWORK` (required): The network to join (`arko` or `testnet`).
- `LAMDEN_TAG` and `CONTRACTING_TAG` (optional): Check out available [lamden](https://github.com/Lamden/lamden/tags) and [contracting](https://github.com/Lamden/contracting/tags) tags. If not set, latest stable tags are used by default.

### Usage
:exclamation: **Run this command to purge `LAMDEN_SK` from bash history when you're done:**
```bash
$ history -c
```

#### Deploying
```bash
# Optional
$ export LAMDEN_TAG=<tag> CONTRACTING_TAG=<tag>

$ . venv/bin/activate
$ LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network> make deploy
```

#### Redeploying
```bash
$ . venv/bin/activate
$ LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network> LAMDEN_TAG=<tag> CONTRACTING_TAG=<tag> make redeploy
```

#### Restarting
```bash
$ . venv/bin/activate
$ LAMDEN_SK=<your_sk> LAMDEN_NETWORK=<network> make reboot
```

#### Stopping
```bash
$ LAMDEN_SK=<your_sk> make teardown
```

#### Other
```bash
# Viewing the logs
$ docker logs <lamden_node|lamden_webserver|lamden_events>

# Real-time resource usage
$ docker stats
```

## Lamden Genesis Block Downloader

### Description

This utility downloads the Lamden Genesis Block and its associated state changes from the Lamden GitHub repository. The Genesis Block contains the initial state of the blockchain, and the state changes include all the transactions that modify the blockchain's state. The script prompts you to select an environment (mainnet, testnet, or staging) and optionally allows you to specify a destination directory for the downloaded `genesis_block.json` file.

### Requirements

- Python 3.6+
- `requests` library

### Installation

1. Install the `requests` library:

```bash
pip install requests
```

### Running the Script
To run the script, navigate to the directory containing the `get_genesis_block.py` file and execute the following command:

```bash
python utils/get_genesis_block.py
```

The script will prompt you to enter the environment (mainnet, testnet, or staging). If you don't provide any input, it will default to "mainnet".

Optionally, you can specify a destination directory for the `genesis_block.json` file using the `-d` or `--dest` flag:

```bash
python utils/get_genesis_block.py -d /path/to/destination
```

If a `genesis_block.json` file already exists in the specified destination, the script will prompt you to overwrite it

Once the download is complete, the Genesis Block will be saved as a `genesis_block.json` file in the specified destination directory.

### Example
```bash
python utils/get_genesis_block.py -d /home/user/my-genesis-blocks
```

This command downloads the Genesis Block and associated state changes for the selected environment, saving the `genesis_block.json` file to the `/home/user/my-genesis-blocks` directory.

### Contributing
We welcome contributions to this repository! If you have any suggestions or improvements, please feel free to open an issue or submit a pull request.

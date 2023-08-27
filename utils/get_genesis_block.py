import requests
import logging
import sys
import os
import json
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

GENESIS_URL = "https://github.com/crosschainer/genesis_block/main"

class GenesisBlockDownloader:
    def __init__(self, environment, destination):
        self.genesis_block_url = f"{GENESIS_URL}/{environment}"
        self.destination = destination

    def prompt_overwrite(self, file_path):
        overwrite = input(f"{file_path} already exists. Overwrite? (y/n): ")
        return overwrite.lower() == 'y'

    def download_genesis_block(self):
        logger.info(f"Downloading Genesis Block from Github. ({self.genesis_block_url}/genesis_block.json)")
        try:
            response = requests.get(f"{self.genesis_block_url}/genesis_block.json")
            response.raise_for_status()
            genesis_block = response.json()
        except requests.exceptions.RequestException as err:
            logger.error(f"Cannot download genesis block from github: {err}")
            return None

        return genesis_block

    def download_state_changes(self, genesis_block):
        flag = True
        i = 1
        while flag:
            state_url = f"{self.genesis_block_url}/state_changes_{i}.json"
            logger.info(f"Downloading Genesis States from Github. ({state_url})")
            try:
                response = requests.get(state_url)
                response.raise_for_status()
                genesis_state = response.json() if isinstance(response.json(), list) else []
                i += 1
            except requests.exceptions.RequestException as e:
                flag = False
                if e.response and e.response.status_code == 404:
                    logger.info(f"Genesis States Not Exist: ({state_url})")
                    logger.info(f"Genesis States Json Files Founded: {i - 1} Files.")
                    logger.info("Genesis States Download Finished.")
                    genesis_state = []
                else:
                    logger.error(f"Load genesis state failed, the link is {state_url}")
                    genesis_state = None

            if genesis_state is not None:
                genesis_block["genesis"] = genesis_block["genesis"] + genesis_state
            else:
                break

        if genesis_block.get("genesis"):
            logger.info(f"Genesis Block Downloaded and contains {len(genesis_block['genesis'])} initial state entries.")

        return genesis_block

    def save_genesis_block(self, genesis_block):
        file_path = os.path.join(self.destination, "genesis_block.json")
        if os.path.exists(file_path):
            if not self.prompt_overwrite(file_path):
                print("Aborted.")
                return

        with open(file_path, "w") as f:
            json.dump(genesis_block, f)
        print(f"Genesis block saved to {file_path}")

    def run(self):
        genesis_block = self.download_genesis_block()
        if not genesis_block:
            print("Error: Genesis block not retrieved.")
            return

        genesis_block = self.download_state_changes(genesis_block)
        if not genesis_block:
            print("Error: State changes not retrieved.")
            return

        self.save_genesis_block(genesis_block)

def prompt_environment():
    while True:
        env = input("Enter the environment (mainnet/testnet/staging) [mainnet]: ")
        if not env:
            env = "mainnet"

        if env in ['mainnet', 'testnet', 'staging']:
            return env
        else:
            print("Invalid choice. Please enter mainnet, testnet, or staging.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download Lamden genesis block and state changes.")
    parser.add_argument('-d', '--dest', metavar='destination', type=str, default=os.path.expanduser("~"),
                        help='Destination directory for the genesis_block.json file (default: user home directory)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    destination = args.dest

    environment = prompt_environment()
    downloader = GenesisBlockDownloader(environment, destination)
    downloader.run()
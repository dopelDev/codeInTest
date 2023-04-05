#!/usr/bin/python

"""
This script is used to sync the config files from the remote source_url at github to the local files.
"""

import argparse
import os
import sys
import requests
import filecmp
import json
import shutil
from custom import log_config # Custom logger

class ConfigSync(object):
    def __init__(self, source_url : str, destination : str, action : str):
        self.logger = log_config.build_logger(file_name = 'ConfigSync')
        self.source_url = source_url
        self.destination = destination
        self.destination_path = os.path.dirname(destination)
        self.temp_path = '/tmp/config_sync' 
        self.logger.info(f"Initalized ConfigSync with source_url: {self.source_url} and destination: {self.destination} and action: {action}")

    def action(self, action):
        if action == "sync":
            self.logger.debug("Syncing config files")
            self.sync()
        elif action == "summary":
            self.logger.debug("Generating summary")
            self.summary()

    def download(self):
        try:
            self.logger.warning(f"Make call to {self.source_url} to download config files to {self.temp_path}")
            os.makedirs(self.temp_path, exist_ok=True)
            response = requests.get(self.source_url, stream=True)
        except requests.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            sys.exit(1)

        if response.status_code == 200:
            self.logger.warning(f"Downloaded config files from {self.source_url} to {self.temp_path}")
            contents = json.loads(response.text)
            for content in contents:
                self.logger.warning(f"Downloading {content['name']} from {content['download_url']}")
                file_response = requests.get(content['download_url'], stream=True)
                with open(os.path.join(self.temp_path + content['name']), "wb") as f:
                    f.write(file_response.content)
        else:
            self.logger.error(f"Failed to download config files from {self.source_url} to {self.temp_path}")
            self.logger.error(f"Status code: {response.status_code}")
            sys.exit(1)

    def compare(self):
        self.logger.debug(f"Comparing config files in {self.temp_path} with {self.destination}")
        report = filecmp.dircmp(self.temp_path, self.destination)
        self.logger.info(f"Report: {json.dumps(report.__dict__)}")

    def copy(self):
        self.logger.debug(f"Copying config files from {self.temp_path} to {self.destination}")
        shutil.copytree(self.temp_path, self.destination, dirs_exist_ok=True)

    def cleanup(self):
        self.logger.debug(f"Cleaning up temporary files in {self.temp_path}")
        shutil.rmtree(self.temp_path)

    def sync(self):
        self.download()
        self.compare()
        self.copy()

    def summary(self):
        self.logger.debug("Generating summary")
        self.download()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync config files from remote source_url to local files.')
    parser.add_argument('--source_url', help='Source directory', required=True)
    parser.add_argument('--destination', help='Destination directory', required=True)
    parser.add_argument('--action', help='Action Sync or Summary', required=True)
    args = parser.parse_args()

    ConfigSync(args.source_url, args.destination, args.action).action(args.action)


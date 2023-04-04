#!/usr/bin/python

"""
This script is used to sync the config files from the remote source to the local files.
"""

import argparse
import os
import requests
import filecmp
import tarfile
import json
import shutil
import logging
import logging.config


class ConfigSync_log(logging.Logger):
    def configure_logging(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        logging.config.dictConfig(config)


class ConfigSync(object):
    def __init__(self, source, destination):
        self.logger = ConfigSync_log(__name__)
        self.source = source
        self.destination = destination
        self.destination_path = os.path.dirname(destination)
        self.temp_path = os.path.join(self.destination_path, "temp")

    def action(self, action):
        if action == "sync":
            self.sync()
        elif action == "summary":
            self.summary()

    def download(self):
        self.logger.debug(f"Downloading config files from {self.source}")
        response = requests.get(self.source)
        with open("temp.tar.gz", "wb") as f:
            f.write(response.content)

    def extract(self):
        self.logger.debug(f"Extracting config files to {self.temp_path}")
        with tarfile.open("temp.tar.gz", "r:gz") as tar:
            tar.extractall(self.temp_path)

    def compare(self):
        self.logger.debug(f"Comparing config files in {self.temp_path} with {self.destination}")
        return filecmp.dircmp(self.temp_path, self.destination)

    def copy(self):
        self.logger.debug(f"Copying config files from {self.temp_path} to {self.destination}")
        shutil.copytree(self.temp_path, self.destination, dirs_exist_ok=True)

    def cleanup(self):
        self.logger.debug(f"Cleaning up temporary files in {self.temp_path}")
        shutil.rmtree(self.temp_path)
        os.remove("temp.tar.gz")

    def sync(self):
        self.download()
        self.extract()
        self.compare()
        self.copy()
        self.cleanup()

    def summary(self):
        self.logger.debug("Generating summary")
        comparison = self.compare()
        comparison.report_full_closure()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync config files from remote source to local files.')
    parser.add_argument('--source', help='Source directory', required=True)
    parser.add_argument('--destination', help='Destination directory', required=True)
    parser.add_argument('--action', help='Action Sync or Summary', required=True)
    args = parser.parse_args()

    logger = ConfigSync_log(__name__)
    logger.configure_logging('logging_config.json')

    logger.info(f"Starting config sync from {args.source} to {args.destination}")
    ConfigSync(args.source, args.destination).action(args.action)
    logger.info("Config sync completed successfully")


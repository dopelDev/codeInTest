#!/usr/bin/python

"""
This script is used to sync the config files from the remote user_name at github to the local files.
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
    def __init__(self, user_name : str, repository : str, destination : str):
        self.logger = log_config.build_logger(file_name = 'ConfigSync')
        self.user_name = user_name
        self.destination = destination
        self.destination_path = os.path.dirname(destination)
        self.temp_path = '/tmp/config_sync' 
        self.logger.info(f"Initalized ConfigSync with user_name: {self.user_name} and destination: {self.destination} and temporary path: {self.temp_path}")

    def action(self, action):
        if action == "sync":
            self.logger.debug("Syncing config files")
            self.sync()
        elif action == "summary":
            self.logger.debug("Generating summary")
            self.summary()

    def download(self):
        # code here
        pass

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
        os.remove("temp.tar.gz")

    def sync(self):
        self.download()
        self.compare()
        self.copy()
        self.cleanup()

    def summary(self):
        self.logger.debug("Generating summary")
        self.download()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync config files from remote user_name to local files.')
    parser.add_argument('--user_name', help='Source directory', required=True)
    parser.add_argument('--destination', help='Destination directory', required=True)
    parser.add_argument('--action', help='Action Sync or Summary', required=True)
    args = parser.parse_args()

    ConfigSync(args.user_name, args.destination).action(args.action)


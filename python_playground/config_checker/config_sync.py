#!/usr/bin/python

"""
This script is used to sync the config files from the remote source_url at github to the local files.
"""

import argparse
import os
import sys
from typing import Dict
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
        self.temp_path = 'home/dopel/tmp/config_sync' 
        self.logger.info(f"Initalized ConfigSync with source_url: {self.source_url} and destination: {self.destination} and action: {action}")

    def action(self, action):
        if action == "sync":
            self.logger.debug("Syncing config files")
            self.sync()
        elif action == "summary":
            self.logger.debug("Generating summary")
            self.summary()

    def download(self):
        # download the files from the source_url to the temp_path
        # get a json object from the source_url and iterate through the list
        # if the type is dir, recursively call the download function
        # if the type is file, call the download_file function
        self.logger.debug(f"Downloading config files from {self.source_url} to {self.temp_path}")
        self.recursive_download(self.source_url)
    
    # worker function to download the file
    def download_file(self, url, path) -> None:
        self.logger.debug(f"Downloading file from {url} to {path}")
        response = None
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:    
            self.logger.error(f"Error: {e}")
            sys.exit(1)
        if response.status_code == 200:
            with open(f"{self.temp_path}/{path}", 'wb') as f:
                f.write(response.content)
    
    def create_dir(self, path) -> None:
        # create the directory if it does not exist at the temp_path
        self.logger.debug(f"Creating directory {path}")
        if not os.path.exists(f"{self.temp_path}/{path}"):
            os.makedirs(f"{self.temp_path}/{path}")
            self.logger.debug(f"Directory {path} created successfully")
        else:
            self.logger.debug(f"Directory {path} already exists")
    
    def recursive_download(self, url):
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error: {e}")
            sys.exit(1)
        if response.status_code == 200:
            response_json : Dict = json.loads(response.text)
        else:
            self.logger.error(f"Error: {response.status_code}")
            sys.exit(1)
        if isinstance(response_json, list):
            for item in response_json:
                if item.get('type') == 'dir':
                    self.recursive_download(item.get('html_url'))
                    self.create_dir(item.get('path'))
                elif item.get('type') == 'file':
                    self.download_file(item.get('download_url'), item.get('path'))

    def compare(self):
        self.logger.debug(f"Comparing config files in {self.temp_path} with {self.destination}")
        try:
            report = filecmp.dircmp(self.temp_path, self.destination)
        except OSError as e:
            self.logger.error(f"Error: {self.temp_path} : {e.strerror}")
            sys.exit(1)
        self.logger.info(f"Report: {json.dumps(report.__dict__)}")

    def copy(self):
        self.logger.debug(f"Copying config files from {self.temp_path} to {self.destination}")
        shutil.copytree(self.temp_path, self.destination, dirs_exist_ok=True)

    def cleanup(self):
        self.logger.debug(f"Cleaning up temporary files in {self.temp_path}")
        try:
            shutil.rmtree(self.temp_path)
        except OSError as e:
            self.logger.error(f"Error: {self.temp_path} : {e.strerror}")

    # Action functions

    def sync(self):
        self.logger.debug("Syncing config files")
        self.download()
        self.compare()
        self.copy()
        self.cleanup()

    def summary(self):
        self.logger.debug("Generating summary")
        self.download()
        self.compare()
        self.cleanup()
    
def main():
    parser = argparse.ArgumentParser(description='Sync config files from remote source_url to local files.')
    parser.add_argument('--source_url', help='Source directory', required=True)
    parser.add_argument('--destination', help='Destination directory', required=True)
    parser.add_argument('--action', help='Action Sync or Summary', required=True)
    args = parser.parse_args()

    ConfigSync(args.source_url, args.destination, args.action).action(args.action)

if __name__ == "__main__":
    main()

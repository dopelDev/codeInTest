#!/bin/python3
"""
-------------------------------------------------------------------------------
Author: Dopeldev
repo: https://www.github.com/dopeldev
-------------------------------------------------------------------------------

This script checks the configuration files from $HOME/.config of user accounts on a 
Linux system and compares them with the configuration files from a remote server.
if the configuration files are different, the script will copy the configuration files
from the remote server to the local machine.

first step: check if the user has a .config directory in $HOME if not exist then 
straight copy the remote .config directory to the local machine.
second step: compare the files in the local machine .config directory with the files 
in the remote machine .config directory if not equal copy the remote file to the local machine 
straight copy this file to the local machine.
"""

import os
import sys
import filecmp
import requests
import logging as log

class ConfigChecker:
    def __init__(self):
        self.logger = self.log()
        self.local_config_dir = os.environ["HOME"] + "/.config"
        self.remote_config_dir = self.get_remote_parameters()
        self.response_status_sucess =  self.status_code(self.handle_request(""))
    
    # get the environment parameters
    def get_environment_settings(self):
        self.working_directory = os.getcwd()

    def get_remote_parameters(self) -> str:
        url = sys.argv[1]
        return url

    # logger instance
    def log(self) -> log.Logger:
        file_handler = log.FileHandler(self.working_directory + "/" + __name__ + ".log",
                mode="+w")
        logger = log.getLogger(__name__)
        logger.setLevel(level = log.INFO)
        formatter = log.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stream_handler = log.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.info("Logger initialized")
        
        return logger
        
    # handling the request
    def handle_request(self, url) -> requests.models.Response:
        try:
            response = requests.get(url)
            self.logger.info("Request Success: {}".format(response.status_code))
            return response
        except Exception as e:
            print(e)
            self.logger.error("Request Error: {}".format(e))
            sys.exit(1)
    
    def status_code(self, response) -> bool:
        if response.status_code != 200:
            print("Error: {}".format(response.status_code))
            sys.exit(1)
        else:
            print("Success: {}".format(response.status_code))
            return True

    # more stuff to come

if __name__ == "__main__":
    pass

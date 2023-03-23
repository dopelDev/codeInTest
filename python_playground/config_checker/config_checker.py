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

import sys
import filecmp
import requests
import logging as log

class ConfigChecker:
    def __init__(self):
        self.logger = self.log()
        pass
    
    # log instance
    def log(self) -> log.Logger:
        logger = log.getLogger(__name__)
        
        return logger
        
    # handling the request
    def handle_request(self, url) -> requests.models.Response:
        try:
            response = requests.get(url)
            return response
        except Exception as e:
            
            print(e)
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

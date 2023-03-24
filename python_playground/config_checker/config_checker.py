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
        self.local_config_dir =  self.get_local_parameters()
        self.remote_config_dir = self.get_remote_parameters()
        self.temporary_dir = self.get_temporary_dir()
        self.response_status_sucess =  self.status_code(self.handle_request(self.remote_config_dir))

    # get the environment parameters
    def get_local_parameters(self) -> str:
        self.logger.info("Local parameters initialized successfully")
        return os.environ["HOME"] + "/.config"

    def get_temporary_dir(self) -> str:
        self.logger.info("Temporary directory initialized successfully")
        return os.environ["HOME"] + "/.config/temp"

    def get_remote_parameters(self) -> str:
        if len(sys.argv) <= 1:
            msg_error = "No URL provided"
            self.logger.error(msg_error)
            raise TypeError(msg_error)
        else:
            self.logger.info("Remote parameters initialized successfully")
            url = sys.argv[1]
            return url

    # logger instance
    def log(self) -> log.Logger:
        file_handler = log.FileHandler(os.getcwd()+ "/" + sys.argv[0]+ ".log",
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
    def handle_request(self, url : str) -> requests.models.Response:
        try:
            response = requests.get(url)
            self.logger.info("Request Success: {}".format(response.status_code))
            return response
        except Exception as e:
            print(e)
            self.logger.error("Request Error: {}".format(e))
            sys.exit(1)
    
    def status_code(self, response : requests.models.Response) -> bool:
        if response.status_code != 200:
            self.logger.error("Error: {}".format(response.status_code))
            print("Error: {}".format(response.status_code))
            sys.exit(1)
        else:
            self.logger.info("Success: {}".format(response.status_code))
            print("Success: {}".format(response.status_code))
            return True
    
    def dump_response(self, response : requests.models.Response) -> None:
        if self.response_status_sucess:
            with open(self.temporary_dir + "/config.tar.gz", "wb") as f:
                f.write(response.content)
                self.logger.info("Response dumped successfully")
        else:
            self.logger.error("Response not dumped")
            sys.exit(1)

    # more stuff to come
    
    # compare the files from the local machine and the remote machine

    # check and clean up

    def remove_temporary_dir(self) -> None:
        if os.path.exists(self.temporary_dir):
            os.rmdir(self.temporary_dir)
            self.logger.info("Temporary directory removed")
        else:
            self.logger.info("Temporary directory does not exist")

if __name__ == "__main__":
    pass

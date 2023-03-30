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
in the remote machine .config directory i. not equal copy the remote file to the local machine 
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
        self.local_config_dir_path =  self.get_local_parameters()
        self.remote_url_depository = self.get_url_depository()
        self.temporary_dir_path = self.get_temporary_dir()
        self.response_status_sucess =  self.status_code(self.handle_request(self.remote_url_depository))
        self.temporary_dir_exists = self.create_temporary_dir()

    # get the environment parameters at initialization
    def get_local_parameters(self) -> str:
        self.logger.info("Local parameters initialized successfully")
        return os.environ["HOME"] + "/.config"

    def get_temporary_dir(self) -> str:
        self.logger.info("Temporary directory initialized successfully")
        return os.environ["HOME"] + "/.config/temp"

    def get_url_depository(self) -> str:
        if len(sys.argv) <= 1:
            msg_error = "Error: No URL provided"
            self.logger.error(msg_error)
            raise TypeError(msg_error)
        else:
            self.logger.info("Scuccess: URL provided")
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

    # functions tools for function run
        # handle data from remote depository
    def dump_response(self, response : requests.models.Response) -> None:
        if self.response_status_sucess and self.temporary_dir_exists:
            with open(self.temporary_dir_path + "/config.tar.gz", "wb") as f:
                f.write(response.content)
                self.logger.info("Response dumped successfully")
        else:
            self.logger.error("Response not dumped")
            sys.exit(1)

    def extract_tar(self) -> None:
        if self.response_status_sucess and self.temporary_dir_exists:
            os.system("tar -xzf {} -C {}".format(self.temporary_dir_path + "/config.tar.gz", self.temporary_dir_path))
            self.logger.info("Tar extracted successfully")
        else:
            self.logger.error("Tar not extracted")
            sys.exit(1)
    
    # compare the files from the local machine and the remote machine!!!!
    
    def create_temporary_dir(self) -> bool:
        if not os.path.exists(self.temporary_dir_path):
            try:
                os.mkdir(self.temporary_dir_path)
            except PermissionError as e:
                self.logger.error("Permission denied: {}".format(e))
                sys.exit(1)
            self.logger.info("Temporary directory created successfully")
        else:
            self.logger.info("Temporary directory already exists")
        return True

    def descopress_tar(self) -> None:
        if self.temporary_dir_exists:
            os.system("tar -xzf {} -C {}".format(self.temporary_dir_path + "/config.tar.gz", self.temporary_dir_path))
            self.logger.info("Tar extracted successfully")
        else:
            self.logger.error("Tar not extracted")
            sys.exit(1)

    def check_local_config_files_exists(self) -> bool:
        # code here
        return True
    
    def get_list_config_files(self) -> list:
        # code here
        return []

    def compare_files(self, local_file : str, remote_file : str) -> bool:
        # code here
        return True

    def update_config_files(self, local_file : str, remote_file : str) -> None:
        # code here
        pass

    def get_remote_list_config_files(self):
        if not os.path.exists(self.temporary_dir_path):
            self.logger.error("Temporary directory does not exist")
            raise FileNotFoundError("Temporary directory does not exist")
        else:
            self.logger.info("Temporary directory exists")
            return os.listdir(self.temporary_dir_path)

    # check and clean up

    def remove_temporary_dir(self) -> None:
        if os.path.exists(self.temporary_dir_path):
            os.rmdir(self.temporary_dir_path)
            self.logger.info("Temporary directory removed")
        else:
            self.logger.info("Temporary directory does not exist")
    
    # run function
    # this function will be called others functions after the initialization
    def run(self) -> None:
        pass

if __name__ == "__main__":
    pass

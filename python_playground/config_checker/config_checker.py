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

if __name__ == "__main__":
    # check if the user has a .config directory in $HOME if not exist then 
    # straight copy the remote .config directory to the local machine.
    # second step: compare the files in the local machine .config directory with the files 
    # in the remote machine .config directory if not equal copy the remote file to the local machine 
    # straight copy this file to the local machine.
    pass

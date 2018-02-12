#!/usr/bin/env python3

import argparse
import getpass
import json
import os
import requests
import subprocess
from crontab import CronTab
from os import scandir

### Vars
CONFIGFILE = '/etc/storjalytics/config.json'
APIENDPOINT = 'http://localhost:8080/api/'
PARSER = None

def init_send():
    global APIENDPOINT
    global PARSER

    cmdargs()


def cmdargs():
    global PARSER

    PARSER = argparse.ArgumentParser(prog='storjalytics-register', add_help=True)
    PARSER.add_argument('--email', '-e', help="Your StorjAlytics registered email address", type=str, action='store', dest='arg_email', nargs='?')
    PARSER.add_argument('--password', '-p', help="Your StorjAlytics password", type=str, action='store', dest='arg_password', nargs='?')
    PARSER.add_argument('--description', '-d', help="Description for this server", type=str, action='store', dest='arg_desc', nargs='?')
    PARSER.add_argument('--config-dir', '-c', help="The location to your local Storjshare config file", type=str, action='store', dest='arg_config_dir', nargs='?')

if __name__ == '__main__':
    init_send()

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
APIKEY = None
APISECRET = None
SERVERGUID = None
STORJCONFIG = None

def init_send():

    load_settings()

    storj_cmd = storjalytics_common.check_strojshare()

    result = subprocess_result(['storjshare', 'status'])

    configs = os.scandir(STORJCONFIG)

def load_settings():
    global CONFIGFILE
    global APIKEY
    global APISECRET
    global SERVERGUID
    global STORJCONFIG

    try:
        settings_file = open(CONFIGFILE, 'r')
        settings_data = settings_file.read()
        settings_json = json.loads(settings_data)

        APIKEY = settings['api_key']
        APISECRET = settings['api_secret']
        SERVERGUID = settings['server_guid']
        STORJCONFIG = settings['storj_config']

    except KeyError:
        error_message('Settings file ' + CONFIGFILE + ' invalid. Please check your config.')
    except json.JSONDecodeError:
        error_message('Settings file ' + CONFIGFILE + ' invalid. Please check your config.')
    except FileNotFoundError:
        error_message('Settings file ' + CONFIGFILE + ' not found. Please run storjalytics-register.')


def print_error(error_message):
    print()
    print("ERROR : " + error_message)
    print()

    exit(1)

if __name__ == '__main__':
    init_send()

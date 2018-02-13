#!/usr/bin/env python3

import argparse
import getpass
import json
import os
import requests
import subprocess
from crontab import CronTab
from os import scandir
from storjalytics import storjalytics_common

### Vars
CONFIGFILE = '/etc/storjalytics/config.json'
APIENDPOINT = 'http://localhost:8080/api/'
APIKEY = None
APISECRET = None
SERVERGUID = None
STORJCONFIG = None

def init_send():

    checks();

    load_settings()

    storj_json = storjshare_json()
    conf_json = config_json()




def checks():
    global CONFIGFILE

    if os.geteuid() != 0:
        print_error('Please run this script with root privileges')

    if not os.path.isfile(CONFIGFILE):
        print_error('Server config file does not exist at ' + CONFIGFILE)
        exit(1)

    # Check strojshare exists
    code, result = storjalytics_common.check_strojshare()

    if code != "OK":
        print_error(result, False)


def storjshare_json():
    result_data = subprocess_result(['storjshare', 'status', '--json'])
    result_json = json.loads(result_data)

    return result_json

def config_json():
    configs = os.scandir(STORJCONFIG)

    for f in configs:
        if f.is_file():
            # consume config file


    return result_json


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

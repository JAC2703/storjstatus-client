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
PARSER = argparse.ArgumentParser(prog='storjalytics-register', add_help=True)

def init_register():
    global APIENDPOINT
    global PARSER

    checks()
    header()
    args()

    args = PARSER.parse_args()

    if not args.arg_email:
        email = input('Enter your StorjAlytics email address: ')
    else:
        email = args.arg_email

    if not args.arg_password
        password = input('Enter your StorjAlytics password: ')
    else:
        password = args.arg_password

    if not args.arg_desc:
        desc = input('Enter a description for this server (min 3 characters): ')
    else:
        desc = args.arg_desc

    if not args.arg_config_dir:
        config_dir = input('Enter your Storjshare config directory (eg. /users/storj/.config/storjshare/configs): ')
    else:
        config_dir = args.arg_config_dir

    # Final check on vars
    if not email or len(email < 5):
        print('Email address is invalid')
        PARSER.print_help()
        exit(1)

    if not password or len(password < 6):
        print('Password is invalid')
        PARSER.print_help()
        exit(1)

    if not desc or len(desc < 3):
        print('Server description must be at least 3 characters')
        PARSER.print_help()
        exit(1)

    if not config_dir or len(config_dir < 1):
        print('Config Directory is invalid')
        PARSER.print_help()
        exit(1)

    # Get api creds




def checks():
    if os.geteuid() != 0:
        print('Please run this script with root privileges')
        exit(1)

    if os.path.isfile(CONFIGFILE):
        print('Server config file already exists')
        exit(1)

def header():
    print('####################################################')
    print('#           StorjAlytics Server Registration       #')
    print('#    Written by James Coyle (www.jamescoyle.net)   #')
    print('####################################################')
    print()
    print('Did you know that you can use command line arguments with this command?')


def args();
    global PARSER
    PARSER.add_argument('--email', '-e', help="Your StorjAlytics registered email address", type=str, action='store', dest='arg_email', nargs='?')
    PARSER.add_argument('--password', '-p', help="Your StorjAlytics password", type=str, action='store', dest='arg_password', nargs='?')
    PARSER.add_argument('--description', '-d', help="Description for this server", type=str, action='store', dest='arg_desc', nargs='?')
    PARSER.add_argument('--config-dir', '-c', help="The location to your local Storjshare config file", type=str, action='store', dest='arg_config_dir', nargs='?')

def save_settings(api_key, api_secret, server_guid, storj_config):
    global CONFIGFILE

    settings = {
        'api_key': api_key,
        'api_secret': api_secret,
        'server_guid': server_guid,
        'storj_config': storj_config,
    }

    # Create folder if doesn't exist
    if not os.path.exists(os.path.dirname(CONFIGFILE)):
        try:
        os.makedirs(os.path.dirname(CONFIGFILE))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            print('Error creating directory ' + os.path.dirname(CONFIGFILE))
            exit(1)

    # Output settings
    settings_output = json.dumps(settings, sort_keys=True, indent=4)
    settings_file_path = CONFIGFILE
    settings_file = open(settings_file_path, 'w')
    settings_file.write(settings_output)
    settings_file.close()

if __name__ == '__main__':
    init_register()

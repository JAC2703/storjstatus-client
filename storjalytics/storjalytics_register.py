#!/usr/bin/env python3

import argparse
import getpass
import json
import os
import requests
import socket
from crontab import CronTab
from os import scandir
from storjalytics import storjalytics_common

### Vars
CONFIGFILE = '/etc/storjalytics/config.json'
APIENDPOINT = 'http://localhost:8080/api/'
FORCE = False
PARSER = None
ENV = None

def init_register():
    global APIENDPOINT
    global FORCE
    global PARSER

    storjalytics_common.setup_env()
    header()
    cmdargs()

    args = PARSER.parse_args()

    if args.arg_force:
        FORCE = True;

    checks()

    if not args.arg_email:
        email = input('Enter your StorjAlytics email address: ')
    else:
        email = args.arg_email
        print('Using email :' + email)

    if not args.arg_password:
        password = getpass.getpass('Enter your StorjAlytics password: ')
    else:
        password = args.arg_password
        print('Using password : ****')

    if not args.arg_name:
        name = input('Enter a name for this server (min 3 characters) [' + print(socket.gethostname()) + ']: ')
        name = name or print(socket.gethostname())
    else:
        name = args.arg_name
        print('Using server name :' + name)

    if not args.arg_config_dir:
        config_dir = input('Enter your Storjshare config directory (eg. /users/storj/.config/storjshare/configs): ')
    else:
        config_dir = args.arg_config_dir
        print('Using config directory :' + config_dir)

    # Final check on vars
    if not email or len(email) < 5:
        print_error('Email address is invalid')

    if not password or len(password) < 6:
        print_error('Password is invalid')

    if not name or len(name) < 3:
        print_error('Server name must be at least 3 characters')

    if not config_dir or len(config_dir) < 1:
        print_error('Config Directory is invalid')

    if not os.path.isdir(config_dir):
        print_error('Config Directory does not exist or is not a directory')

    path, dirs, files = os.walk(config_dir).__next__()
    if (len(files) < 1):
        print_error('Unable to find any files in the Config Directory')

    # Get api creds
    key, secret = api_creds(email, password)

    # Server id
    serverid = server_guid(key, secret, name)

    # Save settings
    save_settings(key, secret, serverid, config_dir)

    print()
    print("Setup complete. You will see your statistics appear on your dashboard over the next hour")


def checks():
    global CONFIGFILE
    global FORCE

    if os.geteuid() != 0:
        print_error('Please run this script with root privileges')

    if FORCE == True:
        print("Forcing regeneration of config and crontab. Note cron times may change.")

    elif os.path.isfile(CONFIGFILE):
        print_error('Server config file already exists')
        exit(1)

    # Check strojshare exists
    code, result = storjalytics_common.check_strojshare()

    if code != "OK":
        print_error(result, False)


def header():
    print('####################################################')
    print('#         StorjAlytics Server Registration         #')
    print('#    Written by James Coyle (www.jamescoyle.net)   #')
    print('####################################################')
    print()


def cmdargs():
    global PARSER

    PARSER = argparse.ArgumentParser(prog='storjalytics-register', add_help=True)
    PARSER.add_argument('--email', '-e', help="Your StorjAlytics registered email address", type=str, action='store', dest='arg_email', nargs='?')
    PARSER.add_argument('--password', '-p', help="Your StorjAlytics password", type=str, action='store', dest='arg_password', nargs='?')
    PARSER.add_argument('--server-name', '-n', help="Name for this server to use in the dashboard", type=str, action='store', dest='arg_name', nargs='?')
    PARSER.add_argument('--config-dir', '-c', help="The location to your local Storjshare config file", type=str, action='store', dest='arg_config_dir', nargs='?')
    PARSER.add_argument('--force', '-f', help="This will regenerate the cron and config file if it already exists", action='store_true', dest='arg_force')


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


def api_creds(email, password):
    json_request = {
        'email': email,
        'password': password
    }

    headers = {'content-type': 'application/json'}
    resp = requests.post(APIENDPOINT + "authentication", json=json_request, headers=headers)
    if not resp.status_code == 200:
        print_error("value returned when authenticating : " + resp.json()['description'])

    print("Obtained API key from server")
    key = resp.json()['key']
    secret = resp.json()['secret']

    return key, secret


def server_guid(key, secret, name):
    json_request = {
        'name': name
    }

    headers = {'content-type': 'application/json', 'api-key' : key, 'api-secret' : secret}
    resp = requests.post(APIENDPOINT + "server", json=json_request, headers=headers)
    if not resp.status_code == 200:
        print(resp.content)
        print_error("value returned when creating server : " + resp.json()['description'])

    serverid = resp.json()['serverId']
    print("Obtained server GUID from server : " + serverid)

    return serverid


def cron_job():
    result = storjalytics_common.subprocess_result(['which', 'storjalytics-send'])

    if 'storjalytics-send' in result[0].decode('utf-8'):
        send_command = results[0].decode('utf-8').replace('\n', '') + ' >> /var/log/storjalytics.log 2>&1'

        cron = CronTab(tabfile='/etc/crontab', user=False)
        # Check for existing cronjob and remove
        cron.remove(comment='storjalytics')

        # Add new cron
        job = cron.new(command=send_command, user='root', comment='storjalytics')
        minute = randint(0, 59)
        job.minute.on(minute)

        try:
            system_cron.write()
            storjalytics_common.subprocess_result(['service', 'cron', 'reload'])
        except PermissionError:
            print_error('Unable to create cron job. Exiting.')

    else:
        print_error('There was an error finding the storjalytics-send command. Check your storjalytics installation.')


def print_error(error_message, show_help=True):
    print()
    print("ERROR : " + error_message)
    print()

    if show_help:
        PARSER.print_help()

    exit(1)


if __name__ == '__main__':
    init_register()

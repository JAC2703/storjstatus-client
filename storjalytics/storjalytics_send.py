#!/usr/bin/env python3

import argparse
import getpass
import json
import os
import re
import requests
import subprocess
import time
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

    json_nodes = []

    for node in storj_json:
        # Get values from bridge
        bridge_json = bridge_info(node['id'])

        json_node = {
            'id' = node['id'],
            'status' = node['status'],
            'configPath' = node['configPath'],
            'uptime' = node['uptime'],
            'restarts' = node['restarts'],
            'allocs' = node['allocs'],
            'dataReceivedCount' = node['dataReceivedCount'],
            'shared' = node['shared'],
            'bridgeConnectionStatus' = node['bridgeConnectionStatus'],
            'reputation' = bridge_json['reputation']
            'responseTime' = bridge_json['responseTime']
            'rpcAddress' = conf_json[node[configPath]]['rpcAddress'],
            'rpcPort' = conf_json[node[configPath]]['rpcPort'],
            'storagePath' = conf_json[node.configPath]['storagePath'],
            'storageAllocation' = conf_json[node[configPath]]['storageAllocation'],
            'storageAllocation' = conf_json[node[configPath]]['storageAllocation'],
        }
        json_nodes.append(json_node)

    json_request = {
        'serverId' = SERVERGUID,
        'datetime' = time.time(),
        'version' = storjshare_version()
        'nodes' = json_nodes
    }

    headers = {'content-type': 'application/json'}
    resp = requests.post(APIENDPOINT + "stats", json=json_request, headers=headers)
    if not resp.status_code == 200:
        print_error("Value returned when posting stats : " + resp.json()['description'], False)


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


def storjshare_version():
    result_data = subprocess_result(['storjshare', '-V'])
    re_match = re.match( r"daemon: ([0-9\.]+), core: ([0-9\.]+), protocol: ([0-9\.]+)", result_data)
    if re_match:
        result = {
            'daemon' = re_match.group(1),
            'core' = re_match.group(2),
            'protocol' = re_match.group(3),
        }

        return result
    else:
        print_error("Error finding strojshare version")


def bridge_info(id):
    resp = requests.get("https://api.storj.io/contacts/" + id)
    if not resp.status_code == 200:
        print_error("Code returned when querying bridge : " + rstatus_code, False)

    return resp

def storjshare_json():
    result_data = subprocess_result(['storjshare', 'status', '--json'])
    result_json = json.loads(result_data)

    return result_json

def config_json():
    configs = os.scandir(STORJCONFIG)
    nodes = []

    for f in configs:
        if f.is_file():
            # consume config file
            with open(r, 'r') as f_open:
                try:
                    f_json = json.load(f_open)

                    node['rpcAddress'] = f_json['rpcAddress']
                    node['rpcPort'] = f_json['rpcPort']
                    node['storagePath'] = f_json['storagePath']
                    node['storageAllocation'] = f_json['storageAllocation']

                    nodes[f_json['storageAllocation']] = node
                    print("Found valid config for " + f_json['storageAllocation'])
                except:
                    print("File " + f + " is not a valid Storjshare JSON config file")

    return nodes


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

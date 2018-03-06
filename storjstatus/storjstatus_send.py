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
from storjstatus import storjstatus_common

### Vars
APIKEY = None
APISECRET = None
SERVERGUID = None
STORJCONFIG = None

def init_send():

    storjstatus_common.setup_env()

    checks();

    load_settings()

    storj_json = storjshare_json()
    conf_json = config_json()

    json_nodes = []

    for node in storj_json:
        # Get values from bridge
        print("Processing nodeid: " + node['id'])

        # Check to see if a config exists for this node, if not, ignore it.
        if node['configPath'] in conf_json:

            bridge_json = bridge_info(node['id'])

            json_node = {
                'id': node['id'],
                'status': node['status'],
                'storagePath': node['configPath'],
                'uptime': node['uptime'],
                'restarts': node['restarts'],
                'allocs': node['allocs'],
                'dataReceivedCount': node['dataReceivedCount'],
                'shared': node['shared'],
                'bridgeConnectionStatus': node['bridgeConnectionStatus'],
                'reputation': bridge_json['reputation'],
                'responseTime': bridge_json['responseTime'],
                'lastTimeout': bridge_json.get('lastTimeout',''),
                'timeoutRate': bridge_json.get('timeoutRate',0),
                'spaceAvailable': bridge_json['spaceAvailable'],
                'lastSeen': bridge_json['lastSeen'],
                'rpcAddress': conf_json[node['configPath']]['rpcAddress'],
                'rpcPort': conf_json[node['configPath']]['rpcPort'],
                'storageAllocation': conf_json[node['configPath']]['storageAllocation']
            }
            json_nodes.append(json_node)
        else:
            print_warning("No config file found for Node: " + node['id'] + ". Data for this node will not be sent.")

    json_request = {
        'serverId': SERVERGUID,
        'datetime': time.time(),
        'storjclientVerion': storjstatus_common.get_version(),
        'storjshareVersion': storjshare_version(),
        'nodes': json_nodes
    }
    print_info('\nJSON Request...\n'+json.dumps(json_request, indent=4, sort_keys=True))
    headers = {'content-type': 'application/json', 'api-key' : APIKEY, 'api-secret' : APISECRET}
    try:
        resp = requests.post(storjstatus_common.APIENDPOINT + "stats", json=json_request, headers=headers)
        if not resp.status_code == 200:
            print_error("Value returned when posting stats : " + resp.json()['description'])
    except Exception as e:
        print(str(e))
        print_error("Error sending report to: " + storjstatus_common.APIENDPOINT + "stats. Please try again later")



def checks():
    if os.geteuid() != 0:
        print_error('Please run this script with root privileges')

    if not os.path.isfile(storjstatus_common.CONFIGFILE):
        print_error('Server config file does not exist at ' + storjstatus_common.CONFIGFILE)

    # Check strojshare exists
    code, result = storjstatus_common.check_strojshare()

    if code != "OK":
        print_error(result)


def storjshare_version():
    result_data = storjstatus_common.subprocess_result(['storjshare', '-V'])
    re_match = re.match( r"daemon: ([0-9\.]+), core: ([0-9\.]+), protocol: ([0-9\.]+)", result_data[0].decode('utf-8'))
    if re_match:
        result = {
            'daemon': re_match.group(1),
            'core': re_match.group(2),
            'protocol': re_match.group(3),
        }

        return result
    else:
        print_error("Error finding strojshare version")


def bridge_info(id):
    resp = requests.get("https://api.storj.io/contacts/" + id)
    if not resp.status_code == 200:
        print_error("Code returned when querying bridge : " + rstatus_code)

    return json.loads(resp.content.decode('utf-8'))


def storjshare_json():
    result_data = storjstatus_common.subprocess_result(['storjshare', 'status', '--json'])

    return json.loads(result_data[0].decode('utf-8')) #result_json


def config_json():
    configs = os.scandir(STORJCONFIG)
    nodes = {}

    for root, dirs, filenames in os.walk(STORJCONFIG):
        for f in filenames:
            # consume config file
            with open(os.path.join(root, f), 'r', encoding = "ISO-8859-1") as f_open:
                print_info("Parsing config file: " + os.path.join(root, f))
                node = {}
                f_data = f_open.read()
                f_clean = storjstatus_common.cleanup_json(f_data)

                try:
                    f_json = json.loads(f_clean)

                    node['rpcAddress'] = f_json['rpcAddress']
                    node['rpcPort'] = f_json['rpcPort']
                    node['storagePath'] = f_json['storagePath']
                    node['storageAllocation'] = f_json['storageAllocation']

                    nodes[f_json['storagePath']] = node
                    print_info("Found valid config for " + f_json['storagePath'])
                except KeyError:
                    print_warning('JSON config file ' + f + ' invalid. Please check your config.')
                except json.JSONDecodeError:
                    print_warning('JSON config file ' + f + ' invalid. Please check your config.')
                except:
                    print_warning("File " + f + " is not a valid Storjshare JSON config file")

    if nodes:
        return nodes
    else:
        print_error('No valid config files found. Exiting.')
        exit(1)




def load_settings():
    global APIKEY
    global APISECRET
    global SERVERGUID
    global STORJCONFIG

    try:
        settings_file = open(storjstatus_common.CONFIGFILE, 'r')
        settings_data = settings_file.read()
        settings_json = json.loads(settings_data)

        APIKEY = settings_json['api_key']
        APISECRET = settings_json['api_secret']
        SERVERGUID = settings_json['server_guid']
        STORJCONFIG = settings_json['storj_config']

    except KeyError:
        print_error('Settings file ' + storjstatus_common.CONFIGFILE + ' invalid. Please check your config.')
    except json.JSONDecodeError:
        print_error('Settings file ' + storjstatus_common.CONFIGFILE + ' invalid. Please check your config.')
    except FileNotFoundError:
        print_error('Settings file ' + storjstatus_common.CONFIGFILE + ' not found. Please run storjstatus-register.')


def print_error(error_message):
    print()
    print("ERROR : " + error_message)
    print()

    exit(1)

def print_warning(warning_message):
    print()
    print("WARNING : " + warning_message)
    print()

def print_info(warning_message):
    print()
    print("INFO : " + warning_message)
    print()

if __name__ == '__main__':
    init_send()

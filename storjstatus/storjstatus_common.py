import os
import re
import subprocess
from storjstatus import version
import logging


CONFIGFILE = '/etc/storjstatus/config.json'
APIENDPOINT = 'https://www.storjstatus.com/api/'
log = None

def setup_env():
    global ENV

    ENV = os.environ
    ENV['PATH'] = ENV.get('PATH') + ':/usr/local/bin:/usr/bin/'


def get_version():
    return version.__version__


def get_log():
    global log

    if (log == None):
        logFormatter = logging.basicConfig(format='%(asctime)s [%(levelname)s]  %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    return log

def cleanup_json(json):
    json = re.sub(r'(?<!https:)//.*', '', json, flags = re.MULTILINE)
    json = json.strip().replace('\r', '').replace('\n', '')

    return json


def check_strojshare():
    result = subprocess_result(['which', 'storjshare'])
    if 'storjshare' in result[0].decode('utf-8'):
        try:
            result = subprocess_result(['storjshare', '-V'])

        except FileNotFoundError:
            return "fail", "Unable to find storjshare binary in PATH"

    else:
        return "fail", "Unable to find storjshare binary in PATH"

    return "OK", result[0].decode('utf-8').strip()


def subprocess_result(args):
    global ENV

    proc = subprocess.Popen(args, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.communicate()

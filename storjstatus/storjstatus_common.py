import os
import re
import sys
import subprocess
from storjstatus import version
import logging


CONFIGFILE = '/etc/storjstatus/config.json'
CONFIGREG = 'Software\StorjStatus\StorjStatusClient\config'
APIENDPOINT = 'https://www.storjstatus.com/api/'
log = None

def setup_env():
    global ENV

    ENV = os.environ
    ENV['PATH'] = ENV.get('PATH') + ':/usr/local/bin:/usr/bin/'


def get_version():
    return version.__version__


def setup_logger():
    global log

    if (log == None):

        ssLog = logging.getLogger('storjstatus')
        ssLog.setLevel(logging.DEBUG)
        ssLog.propagate = False

        logFormatter = logging.Formatter('%(asctime)s %(levelname)8s  %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

        ch = logging.StreamHandler()
        ch.setFormatter(logFormatter)

        ssLog.addHandler(ch)

        log = ssLog


def get_os_type():
    if (os.name == "posix"):
        return "linux"
    elif (os.name == "nt"):
        return "win"
    else:
        return "x"

def cleanup_json(json):
    json = re.sub(r'(?<!https:)//.*', '', json, flags = re.MULTILINE)
    json = json.strip().replace('\r', '').replace('\n', '')

    return json


def check_strojshare():
    if get_os_type() == "win":
        return check_strojshare_win()

    elif get_os_type() == "linux":
        return check_strojshare_linux()


def check_strojshare_win():
    result = subprocess_result(['storjshare', '-V'])
    print(result[0].decode('utf-8').strip())
    return "OK", result[0].decode('utf-8').strip()


def check_strojshare_linux():
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

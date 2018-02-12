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
PARSER = argparse.ArgumentParser()

def init_send():

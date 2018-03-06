from storjstatus import storjstatus_send
from storjstatus import storjstatus_register
from storjstatus import storjstatus_common
from version import __version__

def send():
    storjstatus_send.init_send()

def register():
    storjstatus_register.init_register()

from storjstatus import storjstatus_send
from storjstatus import storjstatus_register
from storjstatus import storjstatus_common
from storjstatus import version

def send():
    storjstatus_send.init_send()

def register():
    storjstatus_register.init_register()

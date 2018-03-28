import os
from crate.client import connect

exec(open('storjstatus/version.py').read())

def main():
    print("Updating database to version " + __version__)

    connection = connect('data2.jamescoyle.net:4200')
    cursor = connection.cursor()
    cursor.execute("UPDATE storj.settings SET setting_value = '" + __version__ + "' WHERE setting_name = 'storjstatus-client-version' ")

if __name__ == "__main__":
    main()

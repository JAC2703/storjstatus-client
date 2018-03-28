import os
import setuptools
from crate.client import connect

def main():
    exec(open('storjstatus/version.py').read())
    print("Updating database to version " + __VERSION__)

    connection = connect('data2.jamescoyle.net:4200')
    cursor = connection.cursor()
    cursor.execute("UPDATE storj.settings SET setting_value = '" + __VERSION__ + "' WHERE setting_name = 'storjstatus-client-version' ")

if __name__ == "__main__":
    main()

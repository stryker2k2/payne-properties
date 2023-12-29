# Easy script to either 'create' or 'show' databases
# Usage: 'python3 create_db.py --task create' or
# Usage: 'python3 create_db.py --task show'

import argparse
import mysql.connector

argParser = argparse.ArgumentParser()

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'db-admin',
    passwd = 'password'
)

my_cursor = mydb.cursor()

argParser.add_argument('-t', '--task', type=str, help='Task to be performed (ex: create)')
args = argParser.parse_args()

if args.task and 'create' in args.task:
    print('\n[+] Creating Database')
    my_cursor.execute("CREATE DATABASE tenants")
    my_cursor.execute("SHOW DATABASES")

else:
    print('\n[+] Showing Databases')
    my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)
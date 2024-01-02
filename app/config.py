import os
import json

try:    
    with open('/etc/config.json', 'r') as config_file:
        config = json.load(config_file)
except:
    with open('./config.json', 'r') as config_file:
        config = json.load(config_file)

class Config:

    def get_folder():
        flask_debug = os.environ.get('FLASK_DEBUG')
        if flask_debug:
            return 'LOCAL_UPLOAD_FOLDER'
        else:
            return 'REMOTE_UPLOAD_FOLDER'
    
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = config.get('SECRET_KEY')
    UPLOAD_FOLDER = config.get(get_folder())
    ADMIN_ID = config.get('ADMIN_ID')
    # SESSION_TYPE = config.get('SESSION_TYPE')

    # print("\n[+] UPLOAD_FOLDER: " + str(UPLOAD_FOLDER))

###
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://db-admin:password@localhost/tenants'
# SECRET_KEY = '9fa87cf0-62f2-11ee-b650-9dcbc88ae8b7'
###
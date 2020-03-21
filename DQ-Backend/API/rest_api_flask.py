from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, DATA
from flask import send_from_directory
from jinja2 import Environment, FileSystemLoader
from flaskext.mysql import MySQL
import json
from logging.handlers import RotatingFileHandler
import logging
import time, datetime
import configparser
import hashlib
import os
import subprocess
import shlex
import jwt
import re
from flask_cors import CORS
from dateutil import tz
import collections
import decimal
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import ast

######################
######################
### Configurations ###
######################
######################
CONFIG_FILE = './config.ini'
config = configparser.ConfigParser(allow_no_value=True)
config.read(CONFIG_FILE)

#######################
### Logging Handler ###
#######################

file_handler = RotatingFileHandler(config['LOGS']['api_logs_dir'], maxBytes=int(config['LOGS']['maxBytes']),
                                       backupCount=int(config['LOGS']['backupCount']))#'../logs/rest_api.log',
file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
log.addHandler(file_handler)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
CORS(app, expose_headers=["x-suggested-filename"])

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = config['MYSQL']['MYSQL_DATABASE_HOST']#localhost
app.config['MYSQL_DATABASE_PORT'] = int(config['MYSQL']['MYSQL_DATABASE_PORT'])#3306
app.config['MYSQL_DATABASE_USER'] = config['MYSQL']['MYSQL_DATABASE_USER']#root'
app.config['MYSQL_DATABASE_PASSWORD'] = config['MYSQL']['MYSQL_DATABASE_PASSWORD']#None
app.config['MYSQL_DATABASE_DB'] = config['MYSQL']['MYSQL_DATABASE_DB']#None
#app.config['MYSQL_DATABASE_CHARSET'] = 'utf-8'

mysql.init_app(app)

app.config['SECRET_KEY'] = 'Antarctic2020$'
app.config['TOKEN_TIMER'] = config['TOKEN']['token_timer']

####################
####################
#### app.routes ####
####################
####################

############
### Test ###
############

@app.route('/ping', methods = ['GET'])
def ping():
    return 'pong'

@app.route('/<db>/<table>', methods = ['GET'])
def get_table(db, table):
    if request.headers['Authorization']:
        return extract_db_data(db, table)
    else:
        response = app.response_class(
                    response = json.dumps({"Error":"Database or Table doesn´t exist."}),
                    status = 400,
                    mimetype = 'application/json'
                    )
        return response

def extract_db_data(db, table):
    sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    frame = pd.read_sql(f"select * from {db}.{table}", dbConnection);
    pd.set_option('display.expand_frame_repr', False)
    dbConnection.close()
    return str(frame.to_dict(orient='records'))

if __name__=='__main__':
    app.run(debug=True, port=5000)

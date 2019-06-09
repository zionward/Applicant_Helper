import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "applicant-helper"
# SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.format(conn_type=conn_type, user=user, password=password, host=host, port=port, DATABASE_NAME=DATABASE_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
MODEL_PATH = "models/logreg.pkl"
DATA_PATH = "data/admission_to_train.csv"
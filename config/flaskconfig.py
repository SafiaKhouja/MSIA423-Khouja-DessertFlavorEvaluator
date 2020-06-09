from src import config
from src import buildInputDB
import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "safia"

if config.BUILD_AWS_RDS==True:
    CONNECTION_TYPE = "mysql+pymysql"
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = os.environ.get('MYSQL_PORT')
    MYSQL_DATABASE_NAME = os.environ.get('MYSQL_DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(CONNECTION_TYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                         MYSQL_PORT, MYSQL_DATABASE_NAME)
else:
    LOCAL_DB_NAME = "input.db"
    LOCAL_DB_PATH = PROJECT_HOME + "/data/database/" + LOCAL_DB_NAME
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(LOCAL_DB_PATH)

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100
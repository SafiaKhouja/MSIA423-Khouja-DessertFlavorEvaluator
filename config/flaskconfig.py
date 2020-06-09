from src import config
from src import buildInputDB
import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "DessertFlavorEvaluator"
DB_FLAG = os.environ.get('BUILD_AWS_RDS')

if DB_FLAG==True:
    CONNECTION_TYPE = "mysql+pymysql"
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = os.environ.get('MYSQL_PORT')
    MYSQL_DATABASE_NAME = os.environ.get('MYSQL_DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(CONNECTION_TYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                         MYSQL_PORT, MYSQL_DATABASE_NAME)
else:
    SQLALCHEMY_DATABASE_URI = config.SQLITE_ENGINE_STRING

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100
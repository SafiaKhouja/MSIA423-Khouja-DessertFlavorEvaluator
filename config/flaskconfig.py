from src import config
from src import buildInputDB
import os

DEBUG = True
LOGGING_CONFIG = "config/local.conf"
PORT = 5000
APP_NAME = "DessertFlavorEvaluator"
DB_FLAG = config.BUILD_AWS_RDS

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif DB_FLAG == False:
    SQLALCHEMY_DATABASE_URI = config.SQLITE_ENGINE_STRING
else:
    CONNECTION_TYPE = "mysql+pymysql"
    MYSQL_USER = config.MYSQL_USER
    MYSQL_PASSWORD = config.MYSQL_PASSWORD
    MYSQL_HOST = config.MYSQL_HOST
    MYSQL_PORT = config.MYSQL_PORT
    MYSQL_DATABASE_NAME = config.MYSQL_DATABASE_NAME
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(CONNECTION_TYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                        MYSQL_PORT, MYSQL_DATABASE_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100
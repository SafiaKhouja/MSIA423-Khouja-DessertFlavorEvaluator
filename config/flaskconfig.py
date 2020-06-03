from src import config
from src import buildInputDB

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "safia"

if config.BUILD_AWS_RDS==True:
    # Passing the AWS_RDS_ENGINE_STRING from the config file doesn't seem to work (try to fix)
    # SQLALCHEMY_DATABASE_URI = config.AWS_RDS_ENGINE_STRING
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:Database2020@msia423safia.ceqsmly1rv8f.us-east-2.rds.amazonaws.com:3306/msia423safiadb"
else:
    SQLALCHEMY_DATABASE_URI = config.SQLITE_ENGINE_STRING
    # SQLALCHEMY_DATABASE_URI = "sqlite:////Users/safia/Desktop/MSIA423AVC/data/database/input.db"

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100
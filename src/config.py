### CONFIGURATIONS FOR PYTHON SCRIPTS IN THE SRC DIRECTORY

import os
from os import path
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# File configurations for Dessert Dataset (from Kaggle)
DESSERTS_FILENAME="desserts.csv"
DESSERTS_PATH=PROJECT_HOME+"/data/external/rawData/"+DESSERTS_FILENAME

# File configurations for the full Recipe Dataset
RECIPES_URL="https://archive.org/download/recipes-en-201706/epicurious-recipes.json.xz"
RECIPES_COMPRESSED_FILENAME="epicurious-recipes.json.xz"
RECIPES_COMPRESSED_PATH=PROJECT_HOME+"/data/external/rawData/"+RECIPES_COMPRESSED_FILENAME
RECIPES_DECOMPRESSED_FILENAME="epicurious-recipes.json"
RECIPES_DECOMPRESSED_PATH=PROJECT_HOME+"/data/external/rawData/"+RECIPES_DECOMPRESSED_FILENAME

# S3 configurations
S3_BUCKET_NAME=os.environ['S3_BUCKET_NAME']

# AWS configurations
AWS_PUBLIC_KEY=os.environ['AWS_PUBLIC_KEY']
AWS_SECRET_KEY=os.environ['AWS_SECRET_KEY']

# AWS RDS MYSQL configurations
BUILD_AWS_RDS=False
CONNECTION_TYPE="mysql+pymysql"
MYSQL_USER=os.environ['MYSQL_USER']
MYSQL_PASSWORD=os.environ['MYSQL_PASSWORD']
MYSQL_HOST=os.environ['MYSQL_HOST']
MYSQL_PORT=os.environ['MYSQL_PORT']
MYSQL_DATABASE_NAME=os.environ['MYSQL_DATABASE_NAME']

# Local SQLite configurations
BUILD_SQLITE_LOCAL_DB=True
LOCAL_DB_NAME="desserts.db"
LOCAL_DB_PATH=PROJECT_HOME+"/data/sample/"+LOCAL_DB_NAME




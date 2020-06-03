### CONFIGURATIONS FOR PYTHON SCRIPTS IN THE SRC DIRECTORY
import os
from os import path
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

########## DATA INGESTION CONFIGS ##########
# File configurations for ingestion of  Dessert Dataset (from Kaggle) into the data/external/rawData directory
DESSERTS_FILENAME="desserts.csv"
DESSERTS_PATH=PROJECT_HOME+"/data/external/rawData/"+DESSERTS_FILENAME

# File configurations for ingestion of full Recipe Dataset into the data/external/rawData directory
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
BUILD_AWS_RDS=True
CONNECTION_TYPE="mysql+pymysql"
MYSQL_USER=os.environ['MYSQL_USER']
MYSQL_PASSWORD=os.environ['MYSQL_PASSWORD']
MYSQL_HOST=os.environ['MYSQL_HOST']
MYSQL_PORT=os.environ['MYSQL_PORT']
MYSQL_DATABASE_NAME=os.environ['MYSQL_DATABASE_NAME']
AWS_RDS_ENGINE_STRING = "{}://{}:{}@{}:{}/{}".format(CONNECTION_TYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                             MYSQL_PORT, MYSQL_DATABASE_NAME)

# Local SQLite configurations
BUILD_SQLITE_LOCAL_DB=True
LOCAL_DB_NAME="desserts.db"
LOCAL_DB_PATH=PROJECT_HOME+"/data/database/"+LOCAL_DB_NAME
SQLITE_ENGINE_STRING = 'sqlite:///{}'.format(LOCAL_DB_PATH)

########## DATA INCORPORATION CONFIGS ##########
# File configurations for S3 download of Dessert Dataset into the data/external/rawData directory
DESSERTS_PIPELINE_FILENAME="desserts.csv"
DESSERTS_PIPELINE_PATH=PROJECT_HOME+"/data/pipeline/rawData/"+DESSERTS_FILENAME

# File configurations for S3 download of full Recipe Dataset into the data/pipeline directory
RECIPES_PIPELINE_FILENAME="epicurious-recipes.json"
RECIPES_PIPELINE_PATH=PROJECT_HOME+"/data/pipeline/rawData/"+RECIPES_PIPELINE_FILENAME

########## DATA MERGE CONFIGS ##########
# File configurations for merged data
MERGED_FILENAME="merged.csv"
MERGED_PATH=PROJECT_HOME+"/data/pipeline/"+MERGED_FILENAME

########## DATA CLEAN CONFIGS ##########
# Columns to include moving forward (columns needed in the model or recommender system)
SELECTED_COLUMNS=['recipe_name', 'aggregateRating', 'flavors', 'willMakeAgainPct', 'reviewsCount', "url"]
# File configurations for cleaned data
CLEAN_FILENAME="clean.csv"
CLEAN_PATH=PROJECT_HOME+"/data/pipeline/"+CLEAN_FILENAME

########## MODEL CONFIGS ##########
# Configurations for running the model
SEED=7177135
TEST_SIZE=0.25
# Columns to leave out of the model
LEAVE_OUT_COLUMNS=["recipe_name", "aggregateRating", "url", 'willMakeAgainPct']
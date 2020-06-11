### CONFIGURATIONS FOR PYTHON SCRIPTS IN THE SRC DIRECTORY
import os
from os import path
import yaml

with open('config/config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
S3 = config['S3Buckets']
AWSRDS = config['AWSRDSDatabase']
SQLite = config['SQLite']
modelArtifacts = config['modelArtifacts']
final = config['finalData']



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
S3_BUCKET_NAME=S3['S3BucketName']
print(S3_BUCKET_NAME)

# AWS configurations
AWS_PUBLIC_KEY=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

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

# File configurations for unique flavors list
FLAVOR_FILENAME="flavors.txt"
FLAVOR_PATH=PROJECT_HOME+"/data/model/"+FLAVOR_FILENAME

# File configuration for the final data (cleaned data after it has been one-hot-encoded and is model ready)
FINAL_FILENAME=final['finalName']
FINAL_PATH=PROJECT_HOME+final['finalPath']+FINAL_FILENAME

########## MODEL CONFIGS ##########
# Configurations for running the model
SEED=7177135
TEST_SIZE=0.25

# Columns to leave out of the model
LEAVE_OUT_COLUMNS=["recipe_name", "aggregateRating", "url", 'willMakeAgainPct']

# Pickle model object
MODEL_FILENAME=modelArtifacts['modelObject']
MODEL_PATH=PROJECT_HOME+modelArtifacts['modelObjectPath'] +MODEL_FILENAME

# Column name text file
COLUMN_FILENAME="column.txt"
COLUMN_PATH=PROJECT_HOME+"/data/model/"+COLUMN_FILENAME

# Resulting metrics (R^2) text file path
METRICS_FILENAME =modelArtifacts['metricsName']
METRICS_PATH=PROJECT_HOME+modelArtifacts['modelPath']+METRICS_FILENAME


########## USER INPUT DATABASE CONFIGS ##########
# AWS RDS MYSQL configurations
CONNECTION_TYPE="mysql+pymysql"
MYSQL_USER=AWSRDS['mysqlUser']
MYSQL_PASSWORD=AWSRDS['mysqlPassword']
MYSQL_HOST=AWSRDS['mysqlHost']
MYSQL_PORT=AWSRDS['mysqlPort']
MYSQL_DATABASE_NAME=AWSRDS['mysqlDatabaseName']
AWS_RDS_ENGINE_STRING = "{}://{}:{}@{}:{}/{}".format(CONNECTION_TYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE_NAME)

# Local SQLite configurations
LOCAL_DB_NAME=SQLite['DBName']
LOCAL_DB_PATH=PROJECT_HOME+SQLite['DBPath']+LOCAL_DB_NAME
SQLITE_ENGINE_STRING = 'sqlite:///{}'.format(LOCAL_DB_PATH)

# Which database to build (if false, build a local SQLite database):
BUILD_AWS_RDS=AWSRDS['buildAWSRDS']


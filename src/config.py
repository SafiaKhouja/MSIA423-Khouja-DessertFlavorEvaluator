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
ingestion = config["rawData"]
download = config['downloadData']
processing = config['processing']



PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

########## DATA INGESTION CONFIGS ##########
# File configurations for ingestion of  Dessert Dataset (from Kaggle) into the data/external/rawData directory
DESSERTS_FILENAME=ingestion['dessertsName']
DESSERTS_PATH=PROJECT_HOME+ingestion['dessertsPath']+DESSERTS_FILENAME

# File configurations for ingestion of full Recipe Dataset into the data/external/rawData directory
RECIPES_URL="https://archive.org/download/recipes-en-201706/epicurious-recipes.json.xz"
RECIPES_COMPRESSED_FILENAME=ingestion['recipesName']
RECIPES_COMPRESSED_PATH=PROJECT_HOME+ingestion['recipesPath']+RECIPES_COMPRESSED_FILENAME
RECIPES_DECOMPRESSED_FILENAME= ingestion['recipesDecompressedName']
RECIPES_DECOMPRESSED_PATH=PROJECT_HOME+ingestion['recipesPath']+RECIPES_DECOMPRESSED_FILENAME

# S3 configurations
S3_BUCKET_NAME=S3['S3BucketName']

# AWS configurations
AWS_PUBLIC_KEY=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

########## DATA INCORPORATION CONFIGS ##########
# File configurations for S3 download of Dessert Dataset into the data/external/rawData directory
DESSERTS_PIPELINE_FILENAME=download['dessertsNameDownload']
DESSERTS_PIPELINE_PATH=PROJECT_HOME+download['dessertsPathDownload']+DESSERTS_FILENAME

# File configurations for S3 download of full Recipe Dataset into the data/pipeline directory
RECIPES_PIPELINE_FILENAME=download['recipesNameDownload']
RECIPES_PIPELINE_PATH=PROJECT_HOME+ download['recipesPathDownload'] +RECIPES_PIPELINE_FILENAME

########## DATA MERGE CONFIGS ##########
# File configurations for merged data
MERGED_FILENAME=processing['mergedName']
MERGED_PATH=PROJECT_HOME+processing['mergedPath']+ MERGED_FILENAME

########## DATA CLEAN CONFIGS ##########
# Columns to include moving forward (columns needed in the model or recommender system)
SELECTED_COLUMNS=processing['selectedColumns']

# File configurations for cleaned data
CLEAN_FILENAME=processing["cleanName"]
CLEAN_PATH=PROJECT_HOME+processing["cleanPath"]+CLEAN_FILENAME

# File configurations for unique flavors list
FLAVOR_FILENAME=processing["flavorName"]
FLAVOR_PATH=PROJECT_HOME+processing["flavorPath"]+FLAVOR_FILENAME

# File configuration for the final data (cleaned data after it has been one-hot-encoded and is model ready)
FINAL_FILENAME=final['finalName']
FINAL_PATH=PROJECT_HOME+final['finalPath']+FINAL_FILENAME

########## MODEL CONFIGS ##########
# Configurations for running the model
SEED=modelArtifacts['seed']
TEST_SIZE=modelArtifacts['testSize']

# Columns to leave out of the model
LEAVE_OUT_COLUMNS=modelArtifacts['leaveOutColumns']

# Pickle model object
MODEL_FILENAME=modelArtifacts['modelObject']
MODEL_PATH=PROJECT_HOME+modelArtifacts['modelObjectPath'] +MODEL_FILENAME

# Column name text file
COLUMN_FILENAME=modelArtifacts['columnName']
COLUMN_PATH=PROJECT_HOME+modelArtifacts['columnPath']+COLUMN_FILENAME

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


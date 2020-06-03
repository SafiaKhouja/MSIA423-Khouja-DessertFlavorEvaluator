#### DOWNLOADS BOTH DATASETS FROM S3 TO BE USED IN MODEL BUILDING PIPELINE
import boto3
import botocore
from src import config
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('dataIncorporation')

def downloadDataS3():
    """ Download both datasets from S3"""
    # Establish s3 resource connection
    try:
        s3 = boto3.resource("s3", aws_access_key_id=config.AWS_PUBLIC_KEY, aws_secret_access_key=config.AWS_SECRET_KEY)
        logger.debug("S3 resource connection established")
    except Exception:
        logger.error("Could not establish S3 Client Connection. Please verify AWS credentials.")
        raise
    # Download the datasets
    try:
        # establish the bucket
        bucket = s3.Bucket(config.S3_BUCKET_NAME)
        # Download the Dessert Dataset to data/pipeline/rawData
        bucket.download_file(config.DESSERTS_PIPELINE_FILENAME, config.DESSERTS_PIPELINE_PATH)
        # Download the Epicurious Recipes Dataset to data/pipeline/rawData
        bucket.download_file(config.RECIPES_PIPELINE_FILENAME, config.RECIPES_PIPELINE_PATH)
        logger.info("Files {} and {} successfully downloaded from S3".format(config.DESSERTS_PIPELINE_PATH,
                                                                             config.RECIPES_PIPELINE_PATH))
    except Exception:
        logger.error("Could not download files from S3. Please verify filepaths and S3 bucket names")
        raise

def run():
    """ Runs all the functions to download the data from S3
        Puts the data in a directory (data/pipeline/rawData) for use in the data pipeline
    """
    downloadDataS3()
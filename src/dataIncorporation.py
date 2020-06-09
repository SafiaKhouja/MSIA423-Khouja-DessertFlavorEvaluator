#### DOWNLOADS BOTH DATASETS FROM S3 TO BE USED IN MODEL BUILDING PIPELINE
import boto3
import botocore
from src import config
import logging.config
import logging

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('dataIncorporation')

def downloadDataS3(awsPublicKey, awsSecretKey, S3BucketName, dessertsPipelineFile, dessertsPipelinePath,
                   recipesPipelineFile, recipesPipelinePath):
    """ Download both datasets from S3"""
    # Establish s3 resource connection
    try:
        s3 = boto3.resource("s3", aws_access_key_id=awsPublicKey, aws_secret_access_key=awsSecretKey)
        logger.debug("S3 resource connection established")
    except Exception:
        logger.error("Could not establish S3 Client Connection. Please verify AWS credentials.")
        raise
    # Download the datasets
    try:
        # establish the bucket
        bucket = s3.Bucket(S3BucketName)
        # Download the Dessert Dataset to data/pipeline/rawData
        bucket.download_file(dessertsPipelineFile, dessertsPipelinePath)
        # Download the Epicurious Recipes Dataset to data/pipeline/rawData
        bucket.download_file(recipesPipelineFile, recipesPipelinePath)
        logger.info("Files {} and {} successfully downloaded from S3".format(dessertsPipelinePath,
                                                                             recipesPipelinePath))
    except Exception:
        logger.error("Could not download files from S3. Please verify filepaths and S3 bucket names")
        raise

def run():
    """ Runs all the functions to download the data from S3
        Puts the data in a directory (data/pipeline/rawData) for use in the data pipeline
    """
    downloadDataS3(config.AWS_PUBLIC_KEY, config.AWS_SECRET_KEY, config.S3_BUCKET_NAME,
                   config.DESSERTS_PIPELINE_FILENAME, config.DESSERTS_PIPELINE_PATH,
                   config.RECIPES_PIPELINE_FILENAME, config.RECIPES_PIPELINE_PATH)
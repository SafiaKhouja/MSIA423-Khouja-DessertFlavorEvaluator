#### DATA INGESTION SCRIPT
import requests
import boto3
import pandas as pd
import botocore
# Imported modules below are built into python, so they are not included in the requirements.txt
import lzma
import json
# Import configurations
from src import config
import logging.config
import logging

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('dataIngestion')

def downloadData(url, recipesCompressedPath, recipesCompressedFile):
    """ Downloads Epicurious Recipe data (30,000 recipes) in the .xz file format from the website hosting the data
        Writes the .xz file to the rawData folder
    Args:
        url (str): string where the recipe data is located on the web
        recipesCompressedPath (str): path where the compressed recipe data is located
        recipesCompressedFile (str): file name of the compressed recipe data
    Returns:
        none
    """
    urlRequest = requests.get(url)
    try:
        with open(recipesCompressedPath, 'wb') as infile:
            infile.write(urlRequest.content)
        logger.info("File {} downloaded from website".format(recipesCompressedFile))
    except FileNotFoundError as e:
        raise(e)

def decompressData(recipesCompressedPath, recipesCompressedFile, recipesDecompressedFile):
    """ Decompress the Epicurious recipe data from the json.xz format to json format
    Args:
        recipesCompressedPath (str): path where the compressed recipe data is located
        recipesCompressedFile (str): file name of the compressed recipe data
        recipesDeompressedFile (str): file name of the decompressed recipe data
    Returns:
        xzData (list): the decompressed  data
    """
    xzData = lzma.open(recipesCompressedPath).readlines()
    xzData = [z.decode('utf-8') for z in xzData]
    xzData = [json.loads(z) for z in xzData]
    logger.info("File {} decompressed to {}".format(recipesCompressedFile,
                                                    recipesDecompressedFile))
    return xzData

def writeData(xzData, recipesDecompressedPath, recipesDecompressedFile):
    """ Write the decompressed data to the rawData folder
    Args:
        xzData (list): the decompressed  data
        recipesDecompressedPath (str): path where the decompressed recipe data is located
        recipesDeompressedFile (str): file name of the decompressed recipe data
    Returns:
        None
    """
    out_file = open(recipesDecompressedPath, "w")
    json.dump(xzData, out_file)
    out_file.close()
    logger.info("Decompressed file {} written to {}".format(recipesDecompressedFile,
                                                            recipesDecompressedPath))
    pass

def processEpicuriousRecipes(url, recipesCompressedPath, recipesCompressedFile, recipesDecompressedFile,
                             recipesDecompressedPath):
    """ Downloads the Epicurious Recipe Data (84 MB), decompresses it, and writes it to the rawData folder
        Uses the 3 helper functions above.
    Args:
        url (str): string where the recipe data is located on the web
        recipesCompressedPath (str): path where the compressed recipe data is located
        recipesCompressedFile (str): file name of the compressed recipe data
        recipesDecompressedPath (str): path where the decompressed recipe data is located
        recipesDeompressedFile (str): file name of the decompressed recipe data
    Returns:
        None
    """
    downloadData(url, recipesCompressedPath, recipesCompressedFile)
    xzData = decompressData(recipesCompressedPath, recipesCompressedFile, recipesDecompressedFile)
    writeData(xzData, recipesDecompressedPath, recipesDecompressedFile)

def uploadDataS3(awsPublicKey, awsSecretKey, dessertsPath, S3BucketName, dessertsFile, recipesDecompressedPath,
                 recipesDecompressedFile):
    """ Uploads the two datasets (desserts.csv, epicurious-recipes.json) to S3
    Args:
        awsPublicKey (str): public key for AWS and S3 bucket
        awsSecretKey (str): secret key for AWS and S3 bucket
        dessertsPath (str): path for desserts dataset to be saved to
        S3BucketName (str): name of the S3 bucket
        dessertsFile (str): name of the desserts dataset that is getting saved
        recipesDecompressedPath (str): path fo the decompressed recipes dataset
        recipesDecompressedFile (str): name of the decompressed recipes dataset that is getting saved
    Returns:
    """
    # Establish S3 client connection
    try:
        s3 = boto3.client('s3', aws_access_key_id=awsPublicKey, aws_secret_access_key=awsSecretKey)
    except Exception:
        logger.error("Could not establish S3 Client Connection. Please verify AWS credentials")
        raise
    #Upload the datasets
    try:
        # Upload the Dessert dataset (6500 recipes)
        s3.upload_file(dessertsPath, S3BucketName, dessertsFile)
        # Upload the Recipes dataset (30K recipes)
        s3.upload_file(recipesDecompressedPath, S3BucketName, recipesDecompressedFile)
        logger.info("Files {} and {} successfully uploaded to S3".format(dessertsPath,
                                                                         recipesDecompressedPath))
    except Exception:
        logger.error("Could not upload files to S3. Please verify filepaths and S3 bucket names")
        raise

#if __name__ == "__main__": # comment this and uncomment the next line if importing this to run.py
def run():
    """ Runs all the functions to perform data ingestion
        Processes Epicurious Recipes dataset and then uploading both datasets to S3
    """
    logger.info("Running data ingestion...")
    processEpicuriousRecipes(config.RECIPES_URL, config.RECIPES_COMPRESSED_PATH, config.RECIPES_COMPRESSED_FILENAME,
                             config.RECIPES_DECOMPRESSED_FILENAME, config.RECIPES_DECOMPRESSED_PATH)
    uploadDataS3(config.AWS_PUBLIC_KEY, config.AWS_SECRET_KEY, config.DESSERTS_PATH, config.S3_BUCKET_NAME,
                 config.DESSERTS_FILENAME, config.RECIPES_DECOMPRESSED_PATH, config.RECIPES_DECOMPRESSED_FILENAME)

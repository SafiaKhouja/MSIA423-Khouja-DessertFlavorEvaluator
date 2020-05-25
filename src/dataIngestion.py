#### DATA INGESTION SCRIPT

import requests
import boto3
import pandas as pd
import botocore
# Imported modules below are built into python, so they are not included in the requirements.txt
import lzma
import json
import argparse
# Import configurations
import config
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('dataPipeline')

def processEpicuriousRecipes():
    """
    Downloads the Epicurious Recipe Data (84 MB), decompresses it, and writes it to the data folder.
    """
    urlRequest = requests.get(config.RECIPES_URL)
    with open(config.RECIPES_COMPRESSED_PATH, 'wb') as infile:
        infile.write(urlRequest.content)
    logger.info("File {} downloaded from website".format(config.RECIPES_COMPRESSED_FILENAME))

    # Decompress the data from the json.xz format to the json format
    xzData = lzma.open(config.RECIPES_COMPRESSED_PATH).readlines()
    xzData = [z.decode('utf-8') for z in xzData]
    xzData = [json.loads(z) for z in xzData]
    logger.info("File {} decompressed to {}".format(config.RECIPES_COMPRESSED_FILENAME, config.RECIPES_DECOMPRESSED_FILENAME))

    # Write the decompresed data to the data folder
    out_file = open(config.RECIPES_DECOMPRESSED_PATH, "w")
    json.dump(xzData, out_file)
    out_file.close()
    logger.info("Decompressed file {} written to {}".format(config.RECIPES_DECOMPRESSED_FILENAME, config.RECIPES_DECOMPRESSED_PATH))

    # Below code retained for debugging to assure the data is loaded in the correct format (must uncomment the pandas import)
    #recipes = pd.read_json(config.RECIPES_DECOMPRESSED_PATH)
    #print(len(recipes))

# The If statement ensures the following only runs when the script is executed (rather than imported)
if __name__ == "__main__":
    processEpicuriousRecipes()

    # Upload the data to S3
    s3 = boto3.client('s3', aws_access_key_id=config.AWS_PUBLIC_KEY, aws_secret_access_key=config.AWS_SECRET_KEY)
    # Upload the Dessert dataset (6500 recipes)
    s3.upload_file(config.DESSERTS_PATH, config.S3_BUCKET_NAME, config.DESSERTS_FILENAME)
    # Upload the Recipes dataset (30K recipes)
    s3.upload_file(config.RECIPES_DECOMPRESSED_PATH, config.S3_BUCKET_NAME, config.RECIPES_DECOMPRESSED_FILENAME)
    print("Logger: file was uploaded to S3")
    logger.info("Files {} and {} successfully uploaded to S3".format(config.DESSERTS_PATH, config.RECIPES_DECOMPRESSED_PATH))




# Note to self: Add some exception handling here



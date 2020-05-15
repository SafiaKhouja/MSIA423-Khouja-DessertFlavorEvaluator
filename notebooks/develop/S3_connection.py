### UPLOADS BOTH DATASETS TO S3

import boto3
import argparse

import config

# Argparse used to process configurations given in the shell script
parser = argparse.ArgumentParser()
parser.add_argument('RECIPES_DECOMPRESSED_FILEPATH')
parser.add_argument('RECIPES_DECOMPRESSED_NAME')
args = parser.parse_args()

# Establish an S3 connection
s3 = boto3.client('s3', aws_access_key_id=config.AWS_PUBLIC_KEY, aws_secret_access_key=config.AWS_SECRET_KEY)
# Upload the Dessert dataset (6500 recipes)
s3.upload_file(config.DESSERTS_PATH, config.S3_BUCKET_NAME, config.DESSERTS_FILENAME)
# Upload the Recipes dataset (30K recipes)
s3.upload_file(args.RECIPES_DECOMPRESSED_FILEPATH, config.S3_BUCKET_NAME, args.RECIPES_DECOMPRESSED_NAME)
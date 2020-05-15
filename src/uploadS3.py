import os
import config
import boto3

#docker commmand
#docker run --env - file = config.env pipeline src/uploadS3.py

# S3 Downloaded Data File Configurations
#RECIPES_FILENAME="epicurious-recipes.json"
#RECIPES_PATH= PROJECT_HOME+"/data/external/"+RECIPES_FILENAME


DESSERTS_FILENAME_1= "desserts.csv"
DESSERTS_PATH_1= "src/desserts.csv"

print(config.AWS_SECRET_KEY)
# Download the data from S3
#s3 = boto3.resource('s3', aws_access_key_id=config.AWS_PUBLIC_KEY, aws_secret_access_key=config.AWS_SECRET_KEY)
#bucket = s3.Bucket(config.S3_BUCKET_NAME)
#bucket.download_file(DESSERTS_FILENAME_1, DESSERTS_PATH_1)

#s3client = boto3.client('s3', aws_access_key_id=config.AWS_PUBLIC_KEY, aws_secret_access_key=config.AWS_SECRET_KEY)
#s3client.download_file(config.S3_BUCKET_NAME, config.DESSERTS_FILENAME_1, config.DESSERTS_PATH_1)
#session = boto3.session(
#      region_name = 'us-east-2',
#      aws_access_key_id=config.AWS_PUBLIC_KEY,
#      aws_secret_access_key=config.AWS_SECRET_KEY)
#s3 = session.resource('s3')
#s3.Bucket(config.S3_BUCKET_NAME).download_file(config.DESSERTS_FILENAME_1, config.DESSERTS_PATH_1)

# BELOW WILL RUN WHEN YOU DO IT ON YOUR OWN
s3 = session.resource('s3')
s3.Bucket(config.S3_BUCKET_NAME).download_file(DESSERTS_FILENAME_1, DESSERTS_PATH_1)
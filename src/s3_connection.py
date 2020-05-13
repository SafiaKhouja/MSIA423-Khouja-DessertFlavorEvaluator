import boto3

import config

print(config.AWS_SECRET_KEY)

s3 = boto3.client('s3', aws_access_key_id=config.AWS_PUBLIC_KEY, aws_secret_access_key=config.AWS_SECRET_KEY)
s3.upload_file(config.DESSERTS_PATH, config.S3_BUCKET_NAME, config.DESSERTS_FILENAME)

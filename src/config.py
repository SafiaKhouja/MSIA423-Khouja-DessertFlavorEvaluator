import os

# File locations
DESSERTS_FILENAME = "desserts.csv"
DESSERTS_PATH = "../data/external/" + DESSERTS_FILENAME

# S3 configurations
S3_BUCKET_NAME = 'msia423safia'

# AWS configurations
AWS_PUBLIC_KEY = 'AKIAJ5BE2QD3QXKHRBXA'
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY_MSIA423')


#RAW_DATA_FILENAME = "raw_data.csv"
#RAW_DATA_WRITE_LOCATION = "./data/external/" + RAW_DATA_FILENAME
#RAW_DATA_PATH = './data/external/raw_data.csv'
#S3_PUBLIC_KEY = 'AKIAJUNUGIQUCKQYHMWQ'
#MSIA423_S3_SECRET = os.environ.get('MSIA423_S3_SECRET')


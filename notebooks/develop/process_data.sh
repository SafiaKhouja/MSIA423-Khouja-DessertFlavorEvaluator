#### PROCESSES RECIPE DATA FROM A URL (DOWNLOAD, DECOMPRESS, UPLOAD TO S3)

# Source filenames, filepaths, and URL from shell configuration file
# Argparse is later used to process configurations sourced from the shell configuration file
source config_shell.cfg

# Use curl to rawData the data from the URL and save it to the path for the compressed file
curl -L -o ${RECIPES_COMPRESSED_FILEPATH} ${RECIPES_URL}

# Run dataIngestion.py script to decompress the data
# 2 Argparse arguments expected: (1) compressed filepath (2) decompressed filepath
python3 decompress_data.py ${RECIPES_COMPRESSED_FILEPATH} ${RECIPES_DECOMPRESSED_FILEPATH}

# Run S3_connection.py to rawData the data to S3
# 2 Argparse arguments expected: (1) decompressed filepath (2) decompressed filename
python3 S3_connection.py ${RECIPES_DECOMPRESSED_FILEPATH} ${RECIPES_DECOMPRESSED_NAME}
from src import dataIngestion
from src import dataIncorporation
from src import dataMerge
from src import dataClean
from src import model

from src import config
import logging
import logging.config
logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('driver')

# Runs the whole pipeline
# Once the pipeline is run once and the files and model object are saved to their directories, any of the steps
#  below can be commented out to speed up the pipeline building process in case certain functions are to be
#  examined in depth
if __name__ == "__main__":
    dataIngestion.run()
    dataIncorporation.run()
    dataMerge.run()
    dataClean.run()
    model.run()
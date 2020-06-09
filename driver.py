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

if __name__ == "__main__":
    dataIngestion.run()
    #dataIncorporation.run()
    #dataMerge.run()
    #dataClean.run()
    #model.run()
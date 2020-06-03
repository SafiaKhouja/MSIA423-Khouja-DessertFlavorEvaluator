from src import dataIngestion
from src import dataIncorporation
from src import dataMerge
from src import dataClean
from src import model


if __name__ == "__main__":
    dataIngestion.run()
    #dataIncorporation.run()
    #dataMerge.run()
    #uniqueFlavors = dataClean.run()
    model.run()
## BUILDS THE USER INPUT DATABASE
import os
import argparse
import logging.config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Float
import sqlalchemy as sql
import pandas as pd
from src import config

#logging.config.fileConfig(config.LOGGING_CONFIG)
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('buildInputDB')

Base = declarative_base()

class input(Base):
    """Create a data model for the database to be set up for capturing user input of flavor combinations"""
    __tablename__ = 'input'
    id = Column(Integer, primary_key=True, nullable = False)
    flavor1 = Column(String(100), unique=False, nullable=True)
    flavor2 = Column(String(100), unique=False, nullable=True)
    flavor3 = Column(String(100), unique=False, nullable=True)
    def __repr__(self):
        input_repr = "<input(flavor1='%s', flavor2='%s', flavor3='%s')>"
        return input_repr % (self.flavor1, self.flavor2, self.flavor3)

def establishEngineString():
    print(config.BUILD_AWS_RDS)
    if config.BUILD_AWS_RDS == True:
        engine_string = config.AWS_RDS_ENGINE_STRING
        print("CORRECT")
    else:
        engine_string = config.SQLITE_ENGINE_STRING
        print("nope")
    print(engine_string)
    return engine_string




def add_input(args):
    """Seeds an existing database with additional songs.
    Args:
        args: Argparse args - should include args.flavor1, args.flavor2. args.flavor3 is optional

    Returns:None

    """
    #engine_string = config.ENGINE_STRING

    engine_string = establishEngineString()
    print(engine_string)
    engine = sql.create_engine(engine_string)

    Session = sessionmaker(bind=engine)
    session = Session()

    userInput = input(flavor1=args.flavor1, flavor2=args.flavor2, flavor3=args.flavor3)
    session.add(userInput)
    session.commit()
    logger.info("Flavor combination %s + %s + %s added to database", args.flavor1, args.flavor2, args.flavor3)


#def create_db():
#    # To build a schema in AWS RDS
#     if config.BUILD_AWS_RDS == True:
#         engine_string = config.AWS_RDS_ENGINE_STRING
#         logger.debug("AWS-RDS engine string entered: {}".format(engine_string))
#         connectionMakeTable(engine_string)
#         logger.info("AWS-RDS connection made. User input database built")
#     else:
#         engine_string = config.SQLITE_ENGINE_STRING
#         logger.debug("SQLite engine string entered: {}".format(engine_string))
#         connectionMakeTable(engine_string)
#         logger.info("Local SQLite connection made. User input database built.")








def create_db(args):
    """Creates a database with the data model given by obj:`apps.models.Track`
    Args: args: Argparse args - should include args.title, args.artist, args.album
    """
    #engine_string = config.ENGINE_STRING

    engine_string = establishEngineString()

    print(engine_string)

    engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    userInput = input(flavor1=args.flavor1, flavor2=args.flavor2, flavor3=args.flavor3)
    session.add(userInput)
    session.commit()
    logger.info("Database created with flavor combination %s + %s + %s added to database", args.flavor1, args.flavor2, args.flavor3)
    session.close()



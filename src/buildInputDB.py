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


logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
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

def add_input(args):
    """Seeds an existing database with additional songs.
    Args:
        Argparse args - should include args.flavor1, args.flavor2. args.flavor3 is optional
    Returns:
        none
    """
    engine = sql.create_engine(args.engine_string)
    logger.info("The user input was successfully added to the database located at: {}".format(args.engine_string))
    Session = sessionmaker(bind=engine)
    session = Session()
    userInput = input(flavor1=args.flavor1, flavor2=args.flavor2, flavor3=args.flavor3)
    session.add(userInput)
    session.commit()
    logger.info("Flavor combination %s + %s + %s added to database", args.flavor1, args.flavor2, args.flavor3)

def create_db(args):
    """Creates a database with the data model given by obj:`apps.model.Track`
    Args:
        Argparse args - should include args.flavor1, args.flavor2. args.flavor3 is optional
    Returns:
        none
    """
    engine = sql.create_engine(args.engine_string)
    logger.info("The user input was successfully established at: {}".format(args.engine_string))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    userInput = input(flavor1=args.flavor1, flavor2=args.flavor2, flavor3=args.flavor3)
    session.add(userInput)
    session.commit()
    logger.info("Database created with flavor combination %s + %s + %s added to database", args.flavor1, args.flavor2, args.flavor3)
    session.close()



## BUILDS THE DESSERT DATABASE

import os
import logging.config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Float
import sqlalchemy as sql
import pandas as pd
import config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('buildDessertDB')

Base = declarative_base()

class desserts(Base):
	""" Defines the data model for the table `desserts`. """
	__tablename__ = 'desserts'
	dessert_name = Column(String(200), primary_key=True, unique = True, nullable=False)
	id = Column(String(200), unique=True, nullable=False)
	flavors = Column(String(200), unique=False, nullable=False)
	rating = Column(Float, unique=False, nullable=False)
	make_again_pct = Column(Float, unique=False, nullable=False)
	reviews_count = Column(Integer, unique=False, nullable=False)
	url = Column(String(200), unique=False, nullable=True)
	def __repr__(self):
		dessert_repr = "<Dessert(dessert_name='%s', flavors='%s', rating='%s')>"
		return dessert_repr % (self.dessert_name, self.flavors, self.rating)

def connectionMakeTable(engine_string):
	"""
	Establishes a MYSQL connection and builds the schema
	Args:
		engine_string: (str) either AWS-RDS or SQLite engine string
	"""
	# Set up mysql connection
	engine = sql.create_engine(engine_string)
	# Create the desserts table
	Base.metadata.create_all(engine)
	logger.info("Engine string is valid")


# The If statement ensures the following only runs when the script is executed (rather than imported)
if __name__ == "__main__":

	# To build a schema in AWS RDS
	if config.BUILD_AWS_RDS == True:
		conn_type = config.CONNECTION_TYPE
		user = config.MYSQL_USER
		password = config.MYSQL_PASSWORD
		host = config.MYSQL_HOST
		port = config.MYSQL_PORT
		database = config.MYSQL_DATABASE_NAME
		engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)
		logger.debug("AWS-RDS engine string entered: {}".format(engine_string))
		connectionMakeTable(engine_string)
		logger.info("AWS-RDS connection made")

	#To build a schema in SQLite
	if config.BUILD_SQLITE_LOCAL_DB == True:
		path = config.LOCAL_DB_PATH
		engine_string = 'sqlite:////{}'.format(path)
		logger.debug("SQLite engine string entered: {}".format(engine_string))
		connectionMakeTable(engine_string)
		logger.info("Local SQLite connection made")

# Note to self: it could be a good idea to pass in the BUILD_AWS_RDS and BUILD_SQLITE_LOCAL_DB booleans through argparse
# 				instead of through the config.py file







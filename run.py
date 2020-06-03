import argparse

from src.buildInputDB import create_db, add_input
from config.flaskconfig import SQLALCHEMY_DATABASE_URI


if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--flavor1", default="chocolate", help="First Flavor")
    sb_create.add_argument("--flavor2", default="vanilla", help="Second Flavor")
    sb_create.add_argument("--flavor3", default="almond", help="Third Flavor")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--flavor1", default="chocolate", help="First flavor to be added")
    sb_ingest.add_argument("--flavor2", default="vanilla", help="Second flavor to be added")
    sb_ingest.add_argument("--flavor3",  default="almond", help="Third flavor to be added")
    sb_ingest.set_defaults(func=add_input)

    args = parser.parse_args()
    args.func(args)


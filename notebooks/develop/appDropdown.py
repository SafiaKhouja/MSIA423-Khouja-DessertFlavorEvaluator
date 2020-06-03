import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from notebooks.develop.add_songs import Tracks
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
#db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/indexDropdown.html template.

    Returns: rendered html template

    """
#    pass
    try:
        poop = ['Blue', 'Black', 'Orange']
        logger.debug("Index page accessed")
        return render_template('indexDropdown.html',  poop=poop)
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/drop', methods=['POST'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('indexDropdown.html', colours=colours)




if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

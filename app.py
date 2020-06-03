import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.buildInputDB import input
from flask_sqlalchemy import SQLAlchemy
from src import predict



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
db = SQLAlchemy(app)



@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """
    try:
        #inputTable = db.session.query(input).limit(app.config["MAX_ROWS_SHOW"]).all()
        #logger.debug("Index page accessed")
        #return render_template('index.html', tracks=inputTable)
        return render_template('index.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display input table")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """
    #try:
    userInput = input(flavor1=request.form['flavor1'], flavor2=request.form['flavor2'], flavor3=request.form['flavor3'])
    db.session.add(userInput)
    db.session.commit()
    entry = db.session.query(input).order_by(input.id.desc()).first()
    prediction = predict.make_prediction(entry)
    print(prediction)
    #logger.info("New song added: %s by %s", request.form['Flavor 1'], request.form['Flavor 1'])
    return redirect(url_for('index'))
    #except:
    #    logger.warning("Not able to display tracks, error page returned")
    #    return render_template('error.html')


if __name__ == '__main__':
    print(db)
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

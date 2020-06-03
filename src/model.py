#### FITS THE MODEL TO THE DATA
import pandas as pd
import numpy as np
import pickle
import json
from sklearn.preprocessing import MultiLabelBinarizer
from numpy import loadtxt
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from src import config
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('model')

def trainTestSplit(df):
    """
    Args: df (pandas dataframe): the cleaned, merged dataframe
    """
    logger.debug("Fitting the XGBoost model to the data...")
    # Grab the predictors and response
    y = df['aggregateRating']
    X = df.drop(config.LEAVE_OUT_COLUMNS, axis=1)
    # Need to save the columns for later use
    with open(config.COLUMN_PATH, 'w') as filehandle:
        json.dump(X.columns.tolist(), filehandle)
    # Train-test split
    seed = config.SEED
    test_size = config.TEST_SIZE
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
    return  X_train, X_test, y_train, y_test

def fitModel(X_train, y_train):
    """
    """
    model = XGBRegressor()
    model = model.fit(X_train, y_train)
    pickle.dump(model, open(config.MODEL_PATH, 'wb'))
    return model

def makePredictions(model, X_test):
    # make predictions for test data
    y_pred = model.predict(X_test)
    predictions = [round(value, 3) for value in y_pred]
    logger.debug("The first 10 predictions are {}".format(predictions[:10]))
    return predictions

def evalutePredictions(y_test, predictions):
    r2 = r2_score(y_test, predictions)
    logger.info("The R^2 of this model is {}".format(np.round(r2,3)))
    pass

def run():
    df = pd.read_csv(config.FINAL_PATH)
    X_train, X_test, y_train, y_test = trainTestSplit(df)
    model = fitModel(X_train, y_train)
    predictions = makePredictions(model, X_test)
    evalutePredictions(y_test, predictions)

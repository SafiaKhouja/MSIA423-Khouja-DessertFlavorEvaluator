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
import logging

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('model')

def prepXData(df, leaveOutColumns):
    """ Prepares the X data by dropping the specified columns. Throws an exception if those columns do not exist.
    Args:
        df (pandas dataframe): the final dataframe ready for model fitting
        leaveOutColumns (list): list of columns to leave out
    Returns:
        X (pandas dataframe): the x dataset, which is now ready to be split for training/testing
    """
    try:
        X = df.drop(leaveOutColumns, axis=1)
    except Exception:
        logger.error("Columns specified to leave out are not in the dataset. "
                     "The columns that were specified to leave out are {}. Please check that these columns "
                     "are correctly entered".format(config.leaveOutColumns))
        raise
    return X

def prepYData(df):
    """ Prepares the Y data by selecting the aggregateRating column
        Realistically speaking, this should not throw an exception because this was already checked in previous scripts,
        but it's still good to be careful
    Args:
        df (pandas dataframe): the final dataframe ready for model fitting
    Returns:
        y (pandas dataframe): the y dataset, which is now ready to be split for training/testing
    """
    try:
        y = df['aggregateRating']
    except Exception:
        logger.error("Column 'aggregateRating' is not in the dataset. Please check the dataset and cleaning process")
        raise
    return y

def trainTestSplit(df, leaveOutColumns, columnPath, seed, testSize):
    """ Splits the data into training and testing set. Also pulls the X and y data using helper functions.
    Args:
        df (pandas dataframe): the final dataframe ready for model fitting
        leaveOutColumns (list): list of columns to leave out
        columnPath (str): location where the column list should be saved for later use in predictions
        seed (int): seed for ensuring reproducibility of the model
        testSize (float): size of the test set
    Returns:
        X_train (pandas dataframe): x training data ready for model fitting
        y_train (pandas dataframe): y training data ready for model fitting
        X_test (pandas dataframe): x testing data ready for model testing
        y_test (pandas dataframe): y testing data ready for model testing
    """
    logger.debug("Fitting the XGBoost model to the data...")
    # Grab the predictors and response
    y = prepYData(df)
    X = prepXData(df, leaveOutColumns)
    # Need to save the columns for later use in predictions
    with open(columnPath, 'w') as filehandle:
        json.dump(X.columns.tolist(), filehandle)
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize, random_state=seed)
    return  X_train, X_test, y_train, y_test, X, y

def fitModel(X_train, y_train):
    """  Fit the model on the training data
    Args:
        X_train (pandas dataframe): x training data ready for model fitting
        y_train (pandas dataframe): y training data ready for model fitting
    Returns:
        model (TMO): trained model object fit to the training data
    """
    model = XGBRegressor()
    model = model.fit(X_train, y_train)
    return model

def fitFullModel(X, y, modelPath):
    """ Fits the model on all the data and then pickles the model object for future predictions
    Args:
        X (pandas dataframe): full X data
        y (pandas dataframe): full y data
    Returns: None
    """
    model = XGBRegressor()
    model = model.fit(X, y)
    pickle.dump(model, open(modelPath, 'wb'))
    pass


def makePredictions(model, X_test):
    """ Makes predictions on the test data for upcoming R^2 calculation
    Args:
        X_test (pandas dataframe): x testing data
    Returns:
        predictions (list): ordered list of predictions made for each entry in the X_test dataset
    """
    y_pred = model.predict(X_test)
    predictions = [round(value, 3) for value in y_pred]
    logger.debug("The first 10 predictions are {}".format(predictions[:10]))
    return predictions

def evalutePredictions(y_test, predictions, metricsPath):
    """
    Args:
        y_test (pandas dataframe): true y values to compare to the predictions
        predictions (list): ordered list of predictions made for each entry in the X_test dataset
        metricsPath (str): location to write the R^2 value to
    Returns: none
    """
    r2 = r2_score(y_test, predictions)
    logger.info("The R^2 of this model is {}".format(np.round(r2,3)))
    with open(metricsPath, "w") as file:
        file.write(f"he R^2 of this model is: {r2}")
    pass

def run():
    """ Fits and evaluates the model. """
    df = pd.read_csv(config.FINAL_PATH)
    # Split the data for model training and testing
    X_train, X_test, y_train, y_test, X, y = trainTestSplit(df, config.LEAVE_OUT_COLUMNS, config.COLUMN_PATH,
                                                            config.SEED, config.TEST_SIZE)
    # Fit the model on the training data
    model = fitModel(X_train, y_train)
    # Fit the model on all the data and pickle the model object for future predictions
    fitFullModel(X, y, config.MODEL_PATH)
    # Make predictions using the model fit on the training data
    predictions = makePredictions(model, X_test)
    # Evaluate the predictions and save the R^2 metric to a file
    evalutePredictions(y_test, predictions, config.METRICS_PATH)
    pass

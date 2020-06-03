#### PREDICTS THE FLAVOR COMBINATION'S RATING

import pandas as pd
import numpy as np
import json
import pickle
from src import config
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('predict')


def processRawInput(entry, uniqueFlavors):
    """ Processes the raw user input to verify that at least two of the flavors entered were valid
    Returns: finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
    """
    logger.info("Cleaning user input...")
    # make the user input into a list of strings
    flavorCombo = [entry.flavor1, entry.flavor2, entry.flavor3]
    #Allow users to input a none value, so append that to the list of unique flavors
    uniqueFlavors.append('none')
    # Verify that at least 2 of the flavors entered were valid entries and append valid entries to the finalFlavorList
    finalFlavorCombo = []
    for flavor in flavorCombo:
        if flavor in uniqueFlavors:
            finalFlavorCombo.append(flavor)
    if len(finalFlavorCombo) < 2:
        finalFlavorCombo = ["INVALID"]
    return finalFlavorCombo

def imputeReviewCount(finalFlavorCombo, clean):
    totalReviews = 0
    numRecipeMatches = 0
    for r in range(len(clean)):
        # See if flavor combo is a subset of the flavors in the list
        if set(finalFlavorCombo) <= set(clean["flavors"][r]):
            totalReviews += clean["reviewsCount"][r]
            numRecipeMatches += 1
    imputedReviewCount = totalReviews / numRecipeMatches

    # prevent division by 0
    if numRecipeMatches == 0:
        imputedReviewCount = 0
    else:
        imputedReviewCount = totalReviews / numRecipeMatches
    return imputedReviewCount



def predict(finalFlavorCombo, imputedReviewCount):
    # Read in the pickled model object
    model = pickle.load(open(config.MODEL_PATH, 'rb'))
    # Make a dataframe with all the proper columns. Need to read in the columns
    with open(config.COLUMN_PATH, 'r') as filehandle:
        Xcolumns = json.load(filehandle)
    userInput = pd.DataFrame(columns=Xcolumns)
    # fill the dataframe with one row of 0's that we will fill in
    userInput.loc[0] = 0
    # Make sure the types match
    userInput = userInput.astype(int)
    # Fill in the imputed reviews
    userInput["reviewsCount"].loc[0] = imputedReviewCount
    # One hot encode according to flavors
    for flavor in finalFlavorCombo:
        userInput[flavor].loc[0] = 1
    prediction = model.predict(userInput[0:1])
    return prediction

def make_prediction(entry):
    # Load the unique flavors
    with open(config.FLAVOR_PATH, 'r') as filehandle:
        uniqueFlavors = json.load(filehandle)
    # Load the clean CSVs with lists of flavors
    clean = pd.read_csv(config.CLEAN_PATH)
    # Necessary to preprocess the csv because pandas turns the list of flavor strings into a string
    clean.loc[:, 'flavors'] = clean.loc[:, 'flavors'].apply(
        lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(' '))

    finalFlavorCombo = processRawInput(entry, uniqueFlavors)
    if "INVALID" not in finalFlavorCombo:
        imputedReviewCount = imputeReviewCount(finalFlavorCombo, clean)
        prediction = predict(finalFlavorCombo, imputedReviewCount)
    else:
        print("ERROR - Need to add exception handling later")
        prediction = "ERROR"
    return prediction

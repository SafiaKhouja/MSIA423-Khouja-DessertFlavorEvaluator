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
    # make the user input into a list of strings. Strip of whitespace and make lowercase
    flavorCombo = [entry.flavor1.strip().lower(), entry.flavor2.strip().lower(), entry.flavor3.strip().lower()]
    print(entry.flavor3.strip().lower())
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
    return np.round(prediction, 4)

def topRecommendation(finalFlavorCombo, clean):
    bestRating = 0
    bestRatingIndex = 0
    for r in range(len(clean)):
        if set(finalFlavorCombo) <= set(clean["flavors"][r]):
            # we only want recipes with more than 10 reviews
            if clean["reviewsCount"][r] > 5 and clean["aggregateRating"][r] > 2.5:
                if clean["aggregateRating"][r] > bestRating:
                    bestRating = clean["aggregateRating"][r]
                    bestRatingIndex = r
    if bestRatingIndex == 0 and bestRating == 0:
        bestRecipe, bestURL, bestRating, reviewsCount = ("n/a","","","")
        noRecommendation = "Sorry, I couldn't find any popular and highly rated recipes with this flavor combination 😞"
    else:
        bestRecipe = clean["recipe_name"][bestRatingIndex]
        bestURL = "https://www.epicurious.com/" + clean["url"][bestRatingIndex]
        bestRating = clean["aggregateRating"][bestRatingIndex]
        reviewsCount = clean["reviewsCount"][bestRatingIndex]
        noRecommendation = ""
    return bestRecipe, bestURL, bestRating, reviewsCount, bestRatingIndex, noRecommendation

def nextTopRecommendation(finalFlavorCombo, clean, bestRatingIndex):
    secondBestRating = 0
    secondBestRatingIndex = 0
    for r in range(len(clean)):
        if set(finalFlavorCombo)<=set(clean["flavors"][r]):
            # we only want recipes with more than 10 reviews
            if clean["reviewsCount"][r] > 5 and clean["aggregateRating"][r] > 2.5:
                if clean["aggregateRating"][r] > secondBestRating and r != bestRatingIndex:
                    secondBestRating = clean["aggregateRating"][r]
                    secondBestRatingIndex = r
    print(secondBestRatingIndex)
    print(secondBestRating)
    if secondBestRatingIndex == 0 and secondBestRating == 0:
        secondBestRecipe, secondBestURL,secondBestRating, secondBestReviewsCount = ("","","","")
    else:
        secondBestRecipe = clean["recipe_name"][secondBestRatingIndex]
        secondBestURL = "https://www.epicurious.com/" + clean["url"][secondBestRatingIndex]
        secondBestRating = clean["aggregateRating"][secondBestRatingIndex]
        secondBestReviewsCount = clean["reviewsCount"][secondBestRatingIndex]
    return secondBestRecipe, secondBestURL, secondBestRating, secondBestReviewsCount


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
    topRec = []
    if "INVALID" not in finalFlavorCombo:
        imputedReviewCount = imputeReviewCount(finalFlavorCombo, clean)
        prediction = predict(finalFlavorCombo, imputedReviewCount)
        outputFlavorList  = ' + '.join([str(elem) for elem in finalFlavorCombo])
        topRec = topRecommendation(finalFlavorCombo, clean)
        secondTopRec = nextTopRecommendation(finalFlavorCombo, clean, topRec[4])


    else:
        prediction = ["ERROR: I couldn't recognize enough flavors to make a prediction 😢 "
                      "Please verify that you entered at least two flavors, the flavors are spelled correctly, and the flavors exist in the dataset. "
                      "See the flavor bank on the home page for a complete list of flavors and spellings."]
        if entry.flavor3.strip().lower() == "":
            outputFlavorList = entry.flavor1.strip().lower() + " + " + entry.flavor2.strip().lower()
        else:
            outputFlavorList = entry.flavor1.strip().lower() + " + " + entry.flavor2.strip().lower() + " + " + entry.flavor3.strip().lower()
        topRec = ["", "", "", "", "", "Sorry, I couldn't find any popular and highly rated recipes with this flavor combination 😔"]
        secondTopRec = ["", "", "", ""]
    return [prediction[0], outputFlavorList, topRec, secondTopRec]

#### PREDICTS THE FLAVOR COMBINATION'S RATING
import pandas as pd
import numpy as np
import json
import pickle
from src import config
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('predict')

def cleanEntry(entry):
    """ Helper function that cleans the user input by converting it from an input class to a list of strings and
        by stripping whitespace and making it all lowercase
    Args:
        entry (input class): the inputted data from the user in the input database class form
    Return:
        flavorCombo (list): the cleaned flavor combo
    """
    flavorCombo = [entry.flavor1.strip().lower(), entry.flavor2.strip().lower(), entry.flavor3.strip().lower()]
    return flavorCombo

def cleanFlavorCombo(flavorCombo, uniqueFlavors):
    """ Cleans the flavor combo of invalid flavors. An invalid flavor is misspelled or not included in unique flavors.
        If two or three flavors entered and all are valid, final flavors will return two or three flavors respectively
        If three flavors entered and one is invalid, final flavors will return the two valid flavors.
        If two flavors entered and one is invalid, final flavors will return "INVALID" flag
        If one flavor, final flavors will return "INVALID" flag
    Args:
        flavorCombo (list): the flavor combo that has been converted to strings and cleaned of white space and caps
        uniqueFlavors (list): all unique and valid flavors in the data
    Returns:
        finalFlavorCombo (list): cleaned list of flavors
    """
    finalFlavorCombo = []
    for flavor in flavorCombo:
        if flavor in uniqueFlavors:
            finalFlavorCombo.append(flavor)
    if len(finalFlavorCombo) < 2:
        finalFlavorCombo = ["INVALID"]
    return finalFlavorCombo

def processRawInput(entry, uniqueFlavors):
    """ Processes the raw user input, cleans it, and verifies the flavors are valid.
    Args:
        entry (input class): the inputted data from the user in the input database class form
        uniqueFlavors (list): all unique and valid flavors in the data
    Returns:
        finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
    """
    logger.info("Cleaning user input...")
    # Clean the user input
    flavorCombo = cleanEntry(entry)
    # Verify that at least 2 of the flavors entered were valid entries and append valid entries to the finalFlavorList
    finalFlavorCombo = cleanFlavorCombo(flavorCombo, uniqueFlavors)
    return finalFlavorCombo

def findReviewCount(finalFlavorCombo, clean):
    """ Finds the review count based on the data
    Args:
        finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
        clean (pandas dataframe): the cleaned dataframe before one hot encoding
    Returns:
        reviewCount (int): corresponding review count
    """
    totalReviews = 0
    numRecipeMatches = 0
    for r in range(len(clean)):
        # See if flavor combo is a subset of the flavors in the list
        if set(finalFlavorCombo) <= set(clean["flavors"][r]):
            totalReviews += clean["reviewsCount"][r]
            numRecipeMatches += 1
    # prevent division by 0
    if numRecipeMatches == 0:
        reviewCount = 0
    else:
        reviewCount = totalReviews / numRecipeMatches
    return reviewCount


def predict(finalFlavorCombo, reviewCount):
    """ Wrapper function to make a prediction of the rating for the valid flavorCombo
    Args:
        finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
        reviewCount (int): corresponding review count
    Returns:
        prediction (float): the predicted rating
    """
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
    userInput["reviewsCount"].loc[0] = reviewCount
    # One hot encode according to flavors
    for flavor in finalFlavorCombo:
        userInput[flavor].loc[0] = 1
    prediction = model.predict(userInput[0:1])
    return np.round(prediction, 4)


def topRecommendation(finalFlavorCombo, clean):
    """ Finds the best rated recipe with the given flavor combo.
        Args:
            finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
            clean (pandas dataframe): the cleaned dataframe before one hot encoding
        Returns:
            bestRecipe (str): name of the second best recipe
            bestURL (str): name of the second best recipe url string
            bestRating (float): rating of the second best recipe
            reviewsCount (int): number of reviews of the second best recipe
            bestRatingIndex(int): index of the best rating, used for finding the second best rating
            noRecommendation (str): if there is no recommendation, this returns the error message to be printed
    """
    bestRating = 0
    bestRatingIndex = 0
    for r in range(len(clean)):
        if set(finalFlavorCombo) <= set(clean["flavors"][r]):
            # we only want recipes with more than 5 reviews and a sufficiently high rating
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
    """ Finds the second best rated recipe with the given flavor combo.
    Args:
        finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
        clean (pandas dataframe): the cleaned dataframe before one hot encoding
        bestRatingIndex (int): index of the recipe with the best rating - necessary for finding second best
    Returns:
        secondBestRecipe (str): name of the second best recipe
        secondBestURL (str): name of the second best recipe url string
        secondBestRating (float): rating of the second best recipe
        secondBestReviewsCount (int): number of reviews of the second best recipe
    """
    secondBestRating = 0
    secondBestRatingIndex = 0
    for r in range(len(clean)):
        if set(finalFlavorCombo)<=set(clean["flavors"][r]):
            # we only want recipes with more than 10 reviews and sufficiently high rating
            if clean["reviewsCount"][r] > 5 and clean["aggregateRating"][r] > 2.5:
                if clean["aggregateRating"][r] > secondBestRating and r != bestRatingIndex:
                    secondBestRating = clean["aggregateRating"][r]
                    secondBestRatingIndex = r
    if secondBestRatingIndex == 0 and secondBestRating == 0:
        secondBestRecipe, secondBestURL,secondBestRating, secondBestReviewsCount = ("","","","")
    else:
        secondBestRecipe = clean["recipe_name"][secondBestRatingIndex]
        secondBestURL = "https://www.epicurious.com/" + clean["url"][secondBestRatingIndex]
        secondBestRating = clean["aggregateRating"][secondBestRatingIndex]
        secondBestReviewsCount = clean["reviewsCount"][secondBestRatingIndex]
    return secondBestRecipe, secondBestURL, secondBestRating, secondBestReviewsCount


def predictValid(finalFlavorCombo, clean):
    """ Wrapper function that makes a prediction and recommendations for valid flavor combos
    Args:
        finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
        clean (pandas dataframe): the cleaned dataframe before one hot encoding
    Returns:
        prediction (list): the predicted value. In this case, we set it to an error message
        outputFlavorList (list): the invalid list, outputted to help the user diagnose their error
        topRec (list): the best recommended recipe and its metadata
        secondTopRec (list): the second best recommended recipe and its metadata
    """
    # Find the review count
    reviewCount = findReviewCount(finalFlavorCombo, clean)
    # Make the prediction for the finalFlavorCombo
    prediction = predict(finalFlavorCombo, reviewCount)
    # Save the cleaned valid flavor list to print it on the app
    outputFlavorList = ' + '.join([str(elem) for elem in finalFlavorCombo])
    # Find the top and second top recipe recommendation
    topRec = topRecommendation(finalFlavorCombo, clean)
    secondTopRec = nextTopRecommendation(finalFlavorCombo, clean, topRec[4])
    return prediction, outputFlavorList, topRec, secondTopRec

def predictInvalid(finalFlavorCombo, entry):
    """ Deals with flavor combinations flagged as invalid by displaying error messages in place of the prediction and
           recs. These error messages help the user understand what is wrong and reflect on their input to notice
           misspellings, invalid flavors, or incorrect numbers of flavors
    Args:
        finalFlavorCombo (list): list of flavors that were valid OR a list with the string "INVALID" to flag it
        entry (input class): the inputted data from the user in the input database class form
    Returns:
        prediction (list): the predicted value. In this case, we set it to an error message
        outputFlavorList (list): the invalid list, outputted to help the user diagnose their error
        topRec (list): the best recommended recipe and its metadata
        secondTopRec (list): the second best recommended recipe and its metadata
    """
    # Set the prediction to an error message which explains to the user what is wrong
    prediction = ["ERROR: I couldn't recognize enough flavors to make a prediction 😢 "
                  "Please verify that you entered at least two flavors, the flavors are spelled correctly, "
                  "and the flavors exist in the dataset. "
                  "See the flavor bank on the home page for a complete list of flavors and spellings."]
    # Format the output flavor list to be printed in the app so the user can see what they entered wrong
    if entry.flavor3.strip().lower() == "":
        outputFlavorList = entry.flavor1.strip().lower() + " + " + entry.flavor2.strip().lower()
    else:
        outputFlavorList = entry.flavor1.strip().lower() + " + " + entry.flavor2.strip().lower() + " + " + entry.flavor3.strip().lower()
    # Output empty recommendations and an error
    topRec = ["", "", "", "", "",
              "Sorry, I couldn't find any popular and highly rated recipes with this flavor combination 😔"]
    secondTopRec = ["", "", "", ""]
    return prediction, outputFlavorList, topRec, secondTopRec


def make_prediction(entry):
    """ Makes the prediction using the helper function and loading two datasets and the trained model object"""
    # Load the unique flavors
    with open(config.FLAVOR_PATH, 'r') as filehandle:
        uniqueFlavors = json.load(filehandle)
    # Load the clean CSVs with lists of flavors
    clean = pd.read_csv(config.CLEAN_PATH)
    # Necessary to preprocess the csv because pandas turns the list of flavor strings into a string
    clean.loc[:, 'flavors'] = clean.loc[:, 'flavors'].apply(
        lambda x: x.replace("[", "").replace("]", "").replace("'", "").split(' '))
    # Process the raw input to get the finalFlavorCombo
    finalFlavorCombo = processRawInput(entry, uniqueFlavors)
    # Make the prediction as long as the flavor combo is not flagged as invalid
    if "INVALID" not in finalFlavorCombo:
        prediction, outputFlavorList, topRec, secondTopRec = predictValid(finalFlavorCombo, clean)
    # Deal with flavor combinations flagged as invalid
    else:
        prediction, outputFlavorList, topRec, secondTopRec = predictInvalid(finalFlavorCombo, entry)
    return [prediction[0], outputFlavorList, topRec, secondTopRec]

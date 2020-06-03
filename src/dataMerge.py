#### MERGES THE TWO DATASETS
import pandas as pd
import numpy as np
from src import config
import logging.config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('dataMerge')

def readPipelineData():
    """ Reads the raw data in
    Returns:
        desserts: (pandas dataframe) Original Epicurious Dessert dataset (512 KB)
        recipes: (pandas dataframe) Dataset of all Epicurious Recipes (84.4 MB)
    """
    desserts = pd.read_csv(config.DESSERTS_PIPELINE_PATH)
    recipes = pd.read_json(config.RECIPES_PIPELINE_PATH)
    logger.info("Both files loaded. Beginning data processing...")
    if "recipe_name" not in desserts.columns or "hed" not in recipes.columns:
        raise Exception("Expected column(s) not found. Data cleaning cannot be completed"
                        "The pipeline expected the column 'recipe_name' in the Desserts Dataset and the column"
                        "'hed' in the Epicurious Recipes Dataset. Please verify both raw datasets and change column "
                        "names accordingly.")
    return desserts, recipes

def cleanDessertNames(cleanedDesserts):
    """ Helper function to clean additional spaces from the end of the dessert name strings
    These spaces cause matching problems if they are not properly removed
    Args: cleanedDesserts (pandas dataframe) dessert data that has already undergone a couple of cleaning steps
    Returns: cleanedDesserts (pandas dataframe) the original input dataframe, but with cleaned dessert names
    """
    # Loop to clean the dessert names. Collects the cleaned names in the array dessertNamesCleaned
    dessertNamesCleaned = []
    for d in range(len(cleanedDesserts)):
        dessertName = cleanedDesserts["recipe_name"][d]
        if dessertName[-1] == " ":
            dessertNamesCleaned.append(dessertName[0:-1])
        else:
            dessertNamesCleaned.append(dessertName)
    # Replace the recipe_name column with the cleaned list of dessert names
    cleanedDesserts["recipe_name"] = dessertNamesCleaned
    return cleanedDesserts

def cleanDesserts(desserts):
    """ Fully cleans the raw dessert data: removing NAs, cleaning names, and removing duplicates
    Args: desserts: (pandas dataframe) Original Epicurious Dessert dataset
    Returns: cleanedDesserts: (pandas dataframe) A cleaned version of the original dataset
    """
    # Force dessert recipe name to be a string for future recipe name comparisons
    desserts["recipe_name"] = desserts["recipe_name"].astype(str)
    # Remove NAs. NAs only occurs in recipe_name and flavors field, which are crucial. Imputation is not an option
    cleanedDesserts = desserts.dropna()
    # Reset the index after dropping nan
    cleanedDesserts = cleanedDesserts.reset_index(drop=True)
    # Clean the dessert names using helper function
    cleanedDesserts = cleanDessertNames(cleanedDesserts)
    # Remove duplicate recipe names (if anything appears more than once, I remove ALL occurrences)
    # This was necessary for the following matching process
    # (ICEBOX: figure out a better way to sift through duplicates so I can retain one occurrence)
    cleanedDesserts = cleanedDesserts.drop_duplicates(subset="recipe_name", keep=False)
    cleanedDesserts = cleanedDesserts.reset_index(drop=True)
    # Verify that every entry in the dataframe is unique (throw an exception if not)
    # This assures the following loop will run correctly
    if len(cleanedDesserts["recipe_name"]) != len(set(cleanedDesserts["recipe_name"])):
        raise Exception("Desserts dataframe has non-unique recipe_names. Error in dessert data or data cleaning process")
    logger.debug("Successfully cleaned Desserts Dataset")
    return cleanedDesserts

def cleanRecipes(recipes):
    """ Fully cleans the raw recipe data: changing column names and types
    Args: recipes: (pandas dataframe) Original Epicurious Recipe dataset
    Returns: cleanedRecipes: (pandas dataframe) A cleaned version of the original dataset
    """
    # The upcoming merge won't work unless the recipe name columns have the same name. "hed" refers to the recipe name
    recipes = recipes.rename(columns={'hed': 'recipe_name'})
    # Force recipe name to be a string for future recipe name comparisons
    recipes['recipe_name'] = recipes['recipe_name'].astype(str)
    cleanedRecipes = recipes
    logger.debug("Successfully cleaned Recipes Dataset")
    return cleanedRecipes

def findMatchingRecipes(cleanedDesserts, cleanedRecipes):
    """ Helper function to make a list of the indices of the recipes in the recipe dataset
        that match the desserts in the dessert dataset
    Args:
        cleanedDesserts: (pandas dataframe) cleaned dessert dataset
        recipes: (pandas dataframe) cleaned Epicurious Recipes dataset
    Returns: dessert_matches (list): the indices of recipes in the recipe dataset that are matches
    """
    dessert_matches = []
    for r in range(len(cleanedRecipes)):
        recipe = cleanedRecipes.iloc[r]
        header = recipe["recipe_name"]
        if header in set(cleanedDesserts["recipe_name"]):
            dessert_matches.append(r)
    return dessert_matches

def merge(cleanedDesserts, cleanedRecipes):
    """ Merges the two cleaned datasets based on the recipe names in the dessert dataset
        Uses findMatchingRecipes() to find the recipes from the large dataset that match the dessert dataset entries
        Note to self: the length of the resulting merged dataset *should* be 6627
    Args:
        cleanedDesserts: (pandas dataframe) cleaned dessert dataset
        recipes: (pandas dataframe) cleaned Epicurious Recipes dataset
    Returns: merged: (pandas dataframe) the merged dataset (INNER JOIN dessert dataset, recipes dataset ON recipe_name)
    """
    logger.debug("Attempting to merge Desserts and Recipe datasets")
    # Find the matching indexes in the recipes dataset using the helper function findMatchingRecipes
    dessert_matches = findMatchingRecipes(cleanedDesserts, cleanedRecipes)
    # Filter cleanedRecipes according to the matching indexes
    filteredRecipes = cleanedRecipes[cleanedRecipes.index.isin(dessert_matches)]
    filteredRecipes = filteredRecipes.reset_index(drop=True)
    # Join the datasets on recipe_name
    merged = pd.merge(cleanedDesserts, filteredRecipes, how = 'inner', on=['recipe_name'])
    logger.info("Successfully merged Desserts and Recipe datasets.")
    return merged


def run():
    """ Runs all the functions to merge the data.
    Cleans the individual datasets in order to merge them into a single dataset, which is then saved to data/pipeline
    """
    desserts, recipes = readPipelineData()
    cleanedDesserts = cleanDesserts(desserts)
    cleanedRecipes = cleanRecipes(recipes)
    merged = merge(cleanedDesserts, cleanedRecipes)
    merged.to_csv(config.MERGED_PATH, index=False)
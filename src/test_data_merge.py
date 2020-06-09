import pytest
from src import dataMerge
import pandas as pd
import numpy as np



def test_verifyColumns_happy():
    """ Tests verifyColumns can handle the expected input and verify the correct columns"""
    desserts = pd.DataFrame(np.array([["brownies"]]), columns=["recipe_name"])
    recipes = pd.DataFrame(np.array([["cake"]]), columns=["hed"])
    testResult = dataMerge.verifyColumns(desserts, recipes)
    assert testResult

def test_verifyColumns_unhappy():
    """ Tests verifyColumns can handle the unexpected input, resulting in an exception being thrown"""
    desserts = pd.DataFrame(np.array([["brownies"]]), columns=["dessert"])
    recipes = pd.DataFrame(np.array([["cake"]]), columns=["hed"])
    #testResult = dataMerge.verifyColumns(desserts, recipes)
    with pytest.raises(Exception):
        dataMerge.verifyColumns(desserts, recipes)

def test_removeDessertNameSpaces_happy():
    """ Tests removeDessertNameSpaces can handle the expected input by cleaning the spaces from the names.
        I don't test the unhappy paths here because null values, non-existent columns, and improper data types are
         taken care of in the preceeding data cleaning process"""
    cleanedDesserts = pd.DataFrame(np.array(["cupcake ", "banana bread"]), columns=["recipe_name"])
    testResult = dataMerge.removeDessertNameSpaces(cleanedDesserts)
    expectedResult = pd.DataFrame(np.array(["cupcake", "banana bread"]), columns=["recipe_name"])
    assert testResult.equals(expectedResult)

def test_preliminaryDessertClean_happy():
    """ Tests preliminaryDessertClean can handle the expected input by returning the same dataframe"""
    cleanedDesserts = pd.DataFrame(np.array(["chocolate cake", "banana bread", "cupcake"]), columns=["recipe_name"])
    testResult = dataMerge.preliminaryDessertClean(cleanedDesserts)
    assert testResult.equals(cleanedDesserts)

def test_preliminaryDessertClean_unhappy():
    """ Tests preliminaryDessertClean can handle the unexpected input by cleaning it fully"""
    desserts = pd.DataFrame(np.array([5, "banana bread", "cupcake"]), columns=["recipe_name"])
    testResult = dataMerge.preliminaryDessertClean(desserts)
    expectedResult = pd.DataFrame(np.array(["5", "banana bread", "cupcake"]), columns=["recipe_name"])
    assert testResult.equals(expectedResult)

def test_cleanRecipes_happy():
    """ Tests that cleanRecipes can handle the expected input by returning the same dataframe"""
    recipes = pd.DataFrame(np.array(["cupcake"]), columns=["hed"])
    testResult = dataMerge.cleanRecipes(recipes)
    print("testResult")
    expectedResult = pd.DataFrame(np.array([["cupcake"]]), columns=["recipe_name"])
    assert testResult.equals(expectedResult)

def test_cleanRecipes_unhappy():
    """ Tests that cleanRecipes can handle the unexpected input by cleaning it"""
    recipes = pd.DataFrame(np.array(["cupcake", 5]), columns=["hed"])
    testResult = dataMerge.cleanRecipes(recipes)
    expectedResult = pd.DataFrame(np.array(["cupcake", "5"]), columns=["recipe_name"])
    assert testResult.equals(expectedResult)













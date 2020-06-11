#### TESTS THE DATACLEAN SCRIPT
import pytest
from src import dataClean
import pandas as pd
import numpy as np

def test_preliminaryClean_happy():
    """ Tests primaryClean can handle the expected input and verify the correct columns"""
    selectedColumns = ['recipe_name', 'aggregateRating', 'flavors', 'willMakeAgainPct', 'reviewsCount', "url"]
    merged = pd.DataFrame(np.array([["cupcake", 3.4, "['carrot' 'vanilla']", .93, 50, "epicurious.com/cupcake"]]),
                 columns = ['recipe_name', 'aggregateRating', 'flavors', 'willMakeAgainPct', 'reviewsCount', "url"])
    testResult = dataClean.preliminaryClean(merged, selectedColumns )
    assert testResult.equals(merged)

def test_preliminaryClean_unhappy():
    """ Tests verifyColumns can handle the unexpected input, resulting in an exception being thrown"""
    selectedColumns = ['recipe_name', 'rat', 'flavors', 'willMakeAgainPct', 'reviewsCount', "url"]
    merged = pd.DataFrame(np.array([["cupcake", 3.4, "['carrot' 'vanilla']", .93, 50, "epicurious.com/cupcake"]]),
                          columns=['recipe_name', 'aggregateRating', 'flavors', 'willMakeAgainPct', 'reviewsCount', "url"])
    with pytest.raises(Exception):
        dataClean.preliminaryClean(merged, selectedColumns)

def test_fixFlavors_unhappy():
    """ Tests fixFlavors can handle the unexpected input and fix the flavors column"""
    data = pd.DataFrame(np.array(["vanilla", "tomatoe", "orange", "bay", "mint", "whisky"]), columns = ['flavors'])
    testResult = dataClean.fixFlavors(data)
    expectedResult = pd.DataFrame(np.array(["vanilla", "tomato", "orange", "bay_leaf", "mint", "whiskey"]),
                                  columns = ['flavors'])
    assert testResult.equals(expectedResult)

def test_fixFlavors_happy():
    """ Tests fixFlavors can handle the expected input and return the same values"""
    data = pd.DataFrame(np.array(["champagne", "rose", "chocolate"]), columns = ['flavors'])
    testResult = dataClean.fixFlavors(data)
    assert testResult.equals(data)


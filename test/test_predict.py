#### TESTS THE PREDICT SCRIPT
import pytest
from src import predict
from src import buildInputDB
import pandas as pd
import numpy as np

def test_cleanEntry_happy():
    """ Checks that clean flavor combo can handle the expected input of clean valid flavors"""
    entry = buildInputDB.input(flavor1="vanilla", flavor2="strawberry", flavor3="chocolate")
    testResult = predict.cleanEntry(entry)
    expectedResult = ["vanilla", "strawberry", "chocolate"]
    assert testResult == expectedResult

def test_cleanEntry_happy1():
    """ Checks that cleanEntry can handle the expected input of slightly unclean (with whitespace and
        capital letters) but valid flavors
    """
    entry = buildInputDB.input(flavor1="vanilla ", flavor2="Strawberry", flavor3="chocolate")
    testResult = predict.cleanEntry(entry)
    expectedResult = ["vanilla", "strawberry", "chocolate"]
    assert testResult == expectedResult

def test_cleanEntry_unhappy():
    """ Checks that cleanEntry can handle the unexpected input of only one flavor"""
    entry = buildInputDB.input(flavor1="vanilla ", flavor2="", flavor3="")
    testResult = predict.cleanEntry(entry)
    expectedResult = ["vanilla", '', '']
    assert testResult == expectedResult

def test_cleanFlavorCombo_happy():
    """ Checks that cleanFlavorCombo can handle the expected input of three valid flavors"""
    uniqueFlavors = ["almond", "chocolate", "champagne", "strawberry", "cocoa", "brandy"]
    flavorCombo =["chocolate", "champagne", "strawberry"]
    testResult = predict.cleanFlavorCombo(flavorCombo, uniqueFlavors)
    assert testResult == flavorCombo

def test_cleanFlavorCombo_happy1():
    """ Checks that cleanFlavorCombo can handle the expected input of two valid flavors, by only returning two flavors"""
    uniqueFlavors = ["almond", "chocolate", "champagne", "strawberry", "cocoa", "brandy"]
    flavorCombo =["chocolate", "champagne", ""]
    testResult = predict.cleanFlavorCombo(flavorCombo, uniqueFlavors)
    expectedResult = ["chocolate", "champagne"]
    assert testResult == expectedResult

def test_cleanFlavorCombo_unhappy():
    """ Checks that cleanFlavorCombo can handle the unexpected input of one valid flavors, by returning invalid flag"""
    uniqueFlavors = ["almond", "chocolate", "champagne", "strawberry", "cocoa", "brandy"]
    flavorCombo =["chocolate", "", ""]
    testResult = predict.cleanFlavorCombo(flavorCombo, uniqueFlavors)
    expectedResult = ["INVALID"]
    assert testResult == expectedResult

def test_cleanFlavorCombo_unhappy1():
    """ Checks that cleanFlavorCombo can handle the unexpected input of flavors with spaces, by returning invalid flag"""
    uniqueFlavors = ["almond", "chocolate", "champagne", "strawberry", "cocoa", "brandy"]
    flavorCombo =["chocolate", "apple pie", "smores brownie"]
    testResult = predict.cleanFlavorCombo(flavorCombo, uniqueFlavors)
    print(testResult)
    expectedResult = ["INVALID"]
    assert testResult == expectedResult

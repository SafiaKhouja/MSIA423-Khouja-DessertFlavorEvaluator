#### TESTS THE MODEL SCRIPT
import pytest
from src import model
import pandas as pd
import numpy as np

def test_prepXData_happy():
    """ Tests that the prepXData can handle the expected input by dropping the correct columns"""
    leaveOutColumns = ["aggregateRating"]
    columnNames = ['recipeName', 'aggregateRating']
    df = pd.DataFrame(np.array([["brownies", 2]]), columns=columnNames)
    testResult = model.prepXData(df, leaveOutColumns)
    expectedResult = pd.DataFrame(np.array([["brownies"]]), columns=['recipeName'])
    assert testResult.equals(expectedResult)

def test_prepXData_unhappy():
    """ Tests that prepXData can handle the unexpected input when incorrect columns are asked to be dropped """
    leaveOutColumns = ["aggregateRating"]
    columnNames = ['recipeName']
    df = pd.DataFrame(np.array([["brownies"]]), columns=columnNames)
    with pytest.raises(Exception):
        model.prepXData(df, leaveOutColumns)

def test_prepYData_happy():
    """ Tests that the prepXData can handle the expected input by dropping the correct columns"""
    columnNames = ['recipeName', 'aggregateRating']
    df = pd.DataFrame(np.array([["brownies", "2"]]), columns=columnNames)
    print(df)
    testResult = model.prepYData(df)
    print(testResult)
    expectedResult = pd.DataFrame(np.array([["2"]]))[0]
    print(expectedResult)
    assert testResult.equals(expectedResult)

def test_prepXData_unhappy():
    """ Tests that prepYData can handle the unexpected situation where aggregateRating does not exist in the data """
    columnNames = ['recipe']
    df = pd.DataFrame(np.array([["brownies"]]), columns=columnNames)
    with pytest.raises(Exception):
        model.prepYData(df)

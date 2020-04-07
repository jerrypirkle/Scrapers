#!/usr/bin/env python3
"""
Astrogation csv to json
"""

__author__ = "jerry pirkle"
__version__ = "0.1.0"
__license__ = "MIT"


import csv
import json
import pandas as pd

def main():
    """ Main entry point of the app """
    csvFile = "./Astrogation.csv"
    jsonFile = "./astrodata.json"

    df = pd.read_csv(csvFile)
    df.to_json(jsonFile)



if __name__ == "__main__":
    """ This is executed when run from the command line """


    main()

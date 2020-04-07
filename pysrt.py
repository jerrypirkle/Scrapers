#!/usr/bin/env python3
"""
Creates a list of planets and sorts alphabetically
"""

__author__ = "jerry pirkle"
__version__ = "0.1.0"
__license__ = "MIT"

def main():
    """ Input: Sector text file with items delimited with %
        Output: Sorted list of planets """
    # Should be taken as a command line argument if this is used multiple times
    fileName = "ErtuSector.txt"
    sectorFile = open(fileName, 'r').readlines()
    count = 0
    lineList = ""
    result = []
    for line in sectorFile:
        lineList += line
        if line == "%\n":
            count +=1
            result.append(lineList)
            lineList = ""
    sorted_list = sorted(result)

    f = open("outputFile.txt", "a")
    for i in sorted_list:
        # print(i)
        f.write(i.replace("%", ""))
    f.close()



if __name__ == "__main__":
    """ This is executed when run from the command line """
    sectorFile = ""
    main()

#!/usr/bin/env python3
"""
Experiment for weapons and sensors parsing with less code
"""

__author__ = "thatguyjerry"
__version__ = "0.1.0"
__license__ = "MIT"

from os import listdir
from os.path import isfile, join
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import uuid
from pathlib import Path


def filelist(path):
    """ Get all files in the current directory """
    files = [f for f in listdir(path) if isfile(join(path, f))]
    # print("All Files:")
    # print(files)

    # Sort the weapons and sensor files into their own lists
    weaponfiles = []
    sensorfiles = []
    for file in files:
        if "weapon" in file:
            weaponfiles.append(file)
        if "sensors" in file:
            sensorfiles.append(file)

    # return both variables in a list (new trick)
    return [weaponfiles, sensorfiles]


def parseweapons(file):
    currentFile =  open(file, "r", encoding="utf-8")
    labeldict = {}

    for line in currentFile:
        # print(line)
        if ': ' in str(line):
            label = line.split(': ')[0].lstrip() # .lstrip() methd will remove leading spaces
            data = line.split(': ', 1)[1].lstrip()
            # Making a dict means less code? maybe? what the fuck do I know?
            labeldict[label] = data

    # generate a unique id for the record we're reading
    weapon = labeldict["Name"].replace(" ", "").replace("\n","")

    root = ET.Element("category")
    root.set("name",weapon)
    root.set("baseicon","0")
    root.set("decalicon","0")

    # create the base xml data
    id = str(uuid.uuid4())
    base = ET.SubElement(root,("id-" + id))
    ET.SubElement(base, "name", type="string").text = weapon
    ET.SubElement(base, "notes", type="formattedtext").text = currentFile.read()


    for k,v in labeldict.items():
        dcodefind = re.compile('\d[D]\+\d|\d[D]')

        if dcodefind.search(v) is not None:
            """Search for a die ... this method removes 2 loops and 2 regex
               calls by using a list comprehension and format string elements"""
            dmgid = str(uuid.uuid4())
            dcode = dcodefind.findall(v)
            item = dcode[0]
            posD = [pos for pos, char in enumerate(item) if char == "D"]
            die,plusfind = v[:posD[0]],v[posD[0] + 2:]
            p2number = (int(die)-1)
            p3number = '0'
            if plusfind is not None:
                p3number = plusfind
            dname = die + "D" + plusfind

             # Write xml
            cas = ET.SubElement(base, "damage_list")
            newcas = ET.SubElement(cas, "id-" + dmgid)
            ET.SubElement(newcas, "name", type="string").text = dname
            ET.SubElement(newcas, "description", type="formattedtext").text = ''
            ET.SubElement(newcas, "number_trackers", type="number").text = '5'
            ET.SubElement(newcas, "p1", type="number").text = '1'
            ET.SubElement(newcas, "p1_hidden", type="number").text = '1'
            ET.SubElement(newcas, "p1_tooltip", type="string").text = 'Wild'
            ET.SubElement(newcas, "p2", type="number").text = str(p2number)
            ET.SubElement(newcas, "p2_hidden", type="number").text = '1'
            ET.SubElement(newcas, "p2_tooltip", type="string").text = 'Dice'
            ET.SubElement(newcas, "p3", type="number").text = str(p3number)
            ET.SubElement(newcas, "p3_hidden", type="number").text = '1'
            ET.SubElement(newcas, "p3_tooltip", type="string").text = 'Pips'
            ET.SubElement(newcas, "parameter_formula", type="string").text = '/weg (p1)d6+(p2)d1006+(p3)'
            ET.SubElement(newcas, "clichatcommand", type="string").text = '/weg 1d6+' + str(p2number) + 'd1006+' + str(p3number) + '-0'
            ET.SubElement(newcas, "parameter_formula_enabled", type="number").text = '1'
            ET.SubElement(newcas, "refa", type="string").text = 'Drag Field or Roll Here'
            ET.SubElement(newcas, "refb", type="string").text = 'Drag Field or Roll Here'
            ET.SubElement(newcas, "refc", type="string").text = 'Drag Field or Roll Here'
            ET.SubElement(newcas, "tracker_enabled", type="number").text = '0'

        else:
            ET.SubElement(base, k.lower().replace(" ", "_"), type='string').text = v.lower().replace("\n", "")

    tree = ET.ElementTree(root)
    filename = "./output/" + weapon.replace(" ","") + '.xml'
    pretty_print_xml_given_root(root, filename)


def parsesensors(file):
    print("")
    currentFile =  open(file, "r", encoding="utf-8")
    # currentFile = open("Millenium Falcon.sensors", "r", encoding="utf-8")
    labeldict = {}

    for line in currentFile:
        print(line)
        if ': ' in str(line):
            label = line.split(': ')[0].lstrip() # .lstrip() methd will remove leading spaces
            data = line.split(': ', 1)[1].lstrip().split(",")
            # Making a dict means less code? maybe? what the fuck do I know?
            dataParen = data[0].find("(")
            if dataParen == -1:
                labeldict[label] = data[0].replace(" ","").split("/")
            else:
                labeldict[label] = data[0][:dataParen].replace(" ","").split("/")

    # generate a unique id for the record we're reading
    sensor = currentFile.name.replace(" ","").replace(".","")
    print(sensor)
    print(labeldict)

# ##########

    root = ET.Element("category")
    root.set("name", sensor)
    root.set("baseicon","0")
    root.set("decalicon","0")

    # create the base xml data
    id = str(uuid.uuid4())
    base = ET.SubElement(root,("id-" + id))
    ET.SubElement(base, "name", type="string").text =  sensor
    ET.SubElement(base, "notes", type="formattedtext").text = currentFile.read()


    for k,v in labeldict.items():
        dcodefind = re.compile('\d[D]\+\d|\d[D]')
        print(v[1])
        if dcodefind.search(v[1]) is not None:
            """Search for a die ... this method removes 2 loops and 2 regex
               calls by using a list comprehension and format string elements"""
            dmgid = str(uuid.uuid4())
            dcode = dcodefind.findall(v[1])
            item = dcode[0]
            posD = [pos for pos, char in enumerate(item) if char == "D"]
            die,plusfind = v[1][:posD[0]],v[1][posD[0] + 2:]
            p2number = (int(die)-1)
            p3number = '0'
            if plusfind is not None:
                p3number = plusfind
            dname = die + "D" + plusfind

             # Write xml
            cas = ET.SubElement(base, "damage_list")
            newcas = ET.SubElement(cas, "id-" + dmgid)
            ET.SubElement(newcas, "name", type="string").text = k + ": " + v[0] + "+" + v[1]
            ET.SubElement(newcas, "description", type="formattedtext").text = ''
            ET.SubElement(newcas, "number_trackers", type="number").text = '5'
            ET.SubElement(newcas, "p1", type="number").text = '1'
            ET.SubElement(newcas, "p1_hidden", type="number").text = '1'
            ET.SubElement(newcas, "p1_tooltip", type="string").text = 'Wild'
            ET.SubElement(newcas, "p2", type="number").text = str(p2number)
            ET.SubElement(newcas, "p2_hidden", type="number").text = '1'
            ET.SubElement(newcas, "p2_tooltip", type="string").text = 'Dice'
            ET.SubElement(newcas, "p3", type="number").text = str(p3number)
            ET.SubElement(newcas, "p3_hidden", type="number").text = '1'
            ET.SubElement(newcas, "p3_tooltip", type="string").text = 'Pips'
            ET.SubElement(newcas, "parameter_formula", type="string").text = '/weg (p1)d6+(p2)d1006+(p3)'
            ET.SubElement(newcas, "clichatcommand", type="string").text = '/weg 1d6+' + str(p2number) + 'd1006+' + str(p3number) + '-0'
            ET.SubElement(newcas, "parameter_formula_enabled", type="number").text = '1'
            ET.SubElement(newcas, "refa", type="string").text = 'Drag Field or Roll Here'
            ET.SubElement(newcas, "refb", type="string").text = 'Drag Field or Roll Here'
            ET.SubElement(newcas, "refc", type="string").text = 'Drag Field or Roll Here'
            ET.SubElement(newcas, "tracker_enabled", type="number").text = '0'

        else:
            ET.SubElement(base, k.lower().replace(" ", "_"), type='string').text = v[1].lower().replace("\n", "")

    tree = ET.ElementTree(root)
    filename = "./sensoroutput/" +  sensor.replace(" ","") + '.xml'
    pretty_print_xml_given_root(root, filename)

def pretty_print_xml_given_root(root, output_xml):
    """
    Print xml to file
    """
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    xml_string = os.linesep.join([s for s in xml_string.splitlines() if s.strip()]) # remove the weird newline issue
    with open(output_xml, "w") as file_out:
        file_out.write(xml_string)


def main():
    """ Main entry point of the app """
    # assign two vairbles at once using the returned list of sorted files
    weaponfiles,sensorfiles = filelist("./")
    # print("\nWeapons: " + ', '.join(weaponfiles))
    # print("\nSensors: " + ', '.join(sensorfiles))

    #will take iteration of weapons files as a parameter, using sample file for testing
    # for file in weaponfiles:
    #     parseweapons(file)
    #
    for file in sensorfiles:
        parsesensors(file)


if __name__ == "__main__":
    """ This is executed when run from the command line """

    # Create an output directory
    Path("./output").mkdir(parents=True, exist_ok=True)
    Path("./sensoroutput").mkdir(parents=True, exist_ok=True)
    main()

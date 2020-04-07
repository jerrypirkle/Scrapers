from lxml import html
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
#from bs4 import Comment
import xml.etree.ElementTree as ET
import uuid
import re
import os
#import pprint

def main():
    """ url picker take a parent-level page and get all of the links for the scraper """
    # topiclist = [ "Tools" ]
    topiclist = [ "Accessories" , "Animal_Gear" , "Anti-Security" , "Anti-Surveillance" , "Armor_Accessories" , "Artillery" , "Basic_Survival_Gear" , "Beacons" , "Binoculars" , "Blaster_Carbines" , "Blaster_Rifles" , "Boosters" , "Brawling_Weapons" , "Breathing_Gear" , "Camouflage_Armor" , "Climbing_Gear" , "Combat_Armor" , "Communication_Aids" , "Communication_Disruptors" , "Communicators" , "Computers" , "Concussion_Weapons" , "Cybernetics" , "Dart_Shooters" , "Data_Carriers" , "Defense" , "Demolition_Devices" , "Disguises" , "Disruptor_Blasters" , "Droid_Gear" , "Drugs" , "Energy_Weapons" , "Environmental_Suits" , "Explosive_Grenades" , "Firearms" , "Grenade_Launchers" , "Healing_Equipment" , "Hold-Out_Blasters" , "Individual_Armor" , "Information_Security" , "Ion_Artillery" , "Jet_Packs" , "Laser_Artillery" , "Locking_Systems" , "Medical_Scanners" , "Military_Unit_Armor" , "Mines" , "Miscellaneous" , "Miscellaneous_Artillery" , "Miscellaneous_Blasters" , "Miscellaneous_Grenades" , "Miscellaneous_Ranged_Weapons" , "Miscellaneous_Weapons" , "Missile_Artillery" , "Missile_Launchers" , "Owner_Gear" , "Particle_Weapons" , "Poisons" , "Powered_Melee_Weapons" , "Powersuits" , "Projectile_Shooters" , "Projectile_Weapons" , "Protective_Vests" , "Recorders_%26_Projectors" , "Repeating_Blasters" , "Repulsors" , "Restraining_Devices" , "Rocket_Packs" , "Sensors" , "Sensor_Trips" , "Shelters" , "Shields" , "Slicing" , "Sonic_Weapons" , "Spacesuits" , "Sporting_Blasters" , "Sporting_Blaster_Rifles" , "Stabilizing" , "Storage_Devices" , "Stun_Blasters" , "Stun_Firearms" , "Stun_Melee_Weapons" , "Stun_Missiles" , "Thrown_Weapons" , "Tools" , "Tracking_Devices" , "Vibro-Weapons" , "Weapons_Accessories" ]
    for topic in topiclist:
        print("Starting section - " + topic)
        looper(topic)
#    topic = "Stock_Imperials"

def looper(topic):

    # create the xml data
    root = ET.Element("category")
    root.set("name",topic)
    root.set("baseicon","0")
    root.set("decalicon","0")   

    cwd = os.getcwd()
    path = os.path.join(cwd, topic)
    
    for file in os.listdir(path):
        if file.endswith(".text"):
            f = os.path.join(path, file)
            parser(f, root, topic)
    
    # after all the scraping, format the file 

def parser(f, root, topic):    
    name = os.path.basename(f).split('.')[0]
    print("------------------------------")
    print("Parsing " + name)
    v=open(f, "r", encoding="utf-8")
    if v.mode == 'r':
        content = v.read()
        v.close() 

    # generate a unique id for the record we're reading
    id = str(uuid.uuid4())
        
    # create the base xml data
    base = ET.SubElement(root,("id-" + id))
    ET.SubElement(base, "name", type="string").text = name    
    ET.SubElement(base, "notes", type="formattedtext").text = content
    
    # separate article content into lines for easier parsing
    lines = []

    for part in content.splitlines():
        lines.append(part)

    # Set up die code finding regexes
    dcodefind = re.compile('\d[D]\+\d|\d[D]')
    plusfind = re.compile('[D]\+\d')
    dfind = re.compile('\d[D]')
    
    # Search each line for a colon(:), then split the label from the data
    for line in lines:
        if ': ' in line:
            label = line.split(': ')[0]
            data = line.split(': ', 1)[1]
            # print(label,'/',data)
#           <ammo type="string">ammo</ammo>
            if label == 'Ammo':
                print('has ammo')
                ET.SubElement(base, "ammo", type="string").text = data

# 			<availability type="string">avail</availability>
            if label == 'Availability':
                print('has availability')
                ET.SubElement(base, "availability", type="string").text = data
                
# 			<blast_radius type="string">blastradius</blast_radius>
            if label == 'Blast Radius':
                print('has blast_radius')
                ET.SubElement(base, "blast_radius", type="string").text = data
                
# 			<cost type="string">cost</cost>
            if label == 'Cost':
                print('has cost')
                ET.SubElement(base, "cost", type="string").text = data
                
# 			<fire_rate type="string">firerate</fire_rate>
            if label == 'Fire Rate':
                print('has fire_rate')
                ET.SubElement(base, "fire_rate", type="string").text = data
                
# 			<name type="string">name</name>
#           set a basic name in case one isn't list, but if a 'Model' exists, use that instead
            if label == 'Model':
                print('has name')
                ET.SubElement(base, "name", type="string").text = data
				               
# 			<range type="string">range</range>
            if label == 'Range':
                print('has range')
                ET.SubElement(base, "range", type="string").text = data

# 			<scale type="string">scale</scale>
            if label == 'Scale':
                print('has scale')
                ET.SubElement(base, "scale", type="string").text = data

# 			<skill type="string">skill</skill>
            if label == 'Skill':
                print('has skill')
                ET.SubElement(base, "skill", type="string").text = data

# 			<source type="string">source</source>
            if label == 'Source':
                print('has source')
                ET.SubElement(base, "source", type="string").text = data

# 			<type type="string">type</type>
            if label == 'Type':
                print('has type')
                ET.SubElement(base, "type", type="string").text = data

# 			<weight type="number">0</weight>
            if label == 'Weight':
                print('has weight')
                ET.SubElement(base, "weight", type="string").text = data
                
# 			damage is more complex                
            if label == 'Damage':
                print('has damage')
                cas = ET.SubElement(base, "damage_list")
                dlines = []

                # Search each line for a D, then keep as little as possible, one line each
                if dcodefind.search(line):
                    for segment in re.split(';|,', line):
                        if dcodefind.search(segment):
                            dlines.append(segment.lstrip())
            
                # Separate the dice codes from the text
                for dline in dlines:
                    dcode = dcodefind.findall(dline)
                    item = ''.join(dcode)
                    
                    #Split out the die code pieces
                    die = ''.join(dfind.findall(str(item))).replace('D','')
                    p2number = (int(die)-1)
                    p3number = '0'
                    if plusfind.findall(str(dcode)):
                        p3number = int(''.join(plusfind.findall(str(item))).replace('D+',''))
                    dname = str(''.join(str(dline)))
                    
                    # generate a unique id
                    id = str(uuid.uuid4())
                    
                    # create the xml data
                    newcas = ET.SubElement(cas, "id-" + id)
                    ET.SubElement(newcas, "name", type="string").text = dname
                    
                    # Non-MAP Rolls (Skills and Attributes)
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
                    
                    #Append content to base
                    # base.append(newcas)

    #Append content to file
    tree = ET.ElementTree(root)
    with open(topic + '.xml', "wb") as file:
        tree.write(file)

if __name__ == "__main__":
    """ Execute """
    main()

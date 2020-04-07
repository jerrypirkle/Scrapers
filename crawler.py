from html.parser import HTMLParser
import uuid
import re
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup, Tag
import sys

def main():
    """ url picker take a parent-level page and get all of the links for the scraper """
    topic = "Stock_Imperials"
    parent_url = "redacted" + topic
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(parent_url, headers=headers)

    # parse html
    soup = BeautifulSoup(response.text, 'html.parser')
    parentcontent = soup.find(id='mw-content-text')

    # dictionary with headers as keys and content as values
    sections = {}

    # generate a unique id
    xmlid = str(uuid.uuid4())

    # create the xml data
    root = ET.Element("id-" + xmlid)
    category = ET.SubElement(root, "category")
    category.set("name", topic)
    category.set("baseicon", "0")
    category.set("decalicon", "0")

    links = []
    for aTag in parentcontent.find_all('a', href=True):
        if aTag.text:
            links.append(aTag['href'])

    for i in links:
        scraper("http://d6holocron.com" + str(i), topic, root, category, sections)

    # after all the scraping, format the file
    formatter(sections, topic, root, category)

    # after all the formatting, write the file
    writer(topic, root)

    print("**********\n**********\nfails: " + str(nrun))
    print("successes: " + str(grun))
    print(failures)

def scraper(link, topic, root, category, sections):
    """ takes a link and scrapes the wiki sections for data"""
    # print("------------------------------")
    # print("Reading " + link)

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(link, headers=headers)

    # parse html
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find(id='mw-content-text')
    h2s = content.find_all('h2')

    if len(h2s) != 0:
        multi(content, sections, h2s, topic, root, category)
    elif len(h2s) == 0:
        single(content, sections, topic, root, category)

def multi(content, sections, h2s, topic, root, category):
    """iterates through multi-section"""
    # find the headers
    for header in h2s:
        seccontent = ''
        nextNode = header
        hstring = nextNode.text # just the name of the header
        # create a dictionary with headers as keys
        # sections[nextNode.text] = "" # no need to nextNode.text twice ...
        sections[hstring] = ""

        # iterate through internal nodes
        while True:
            nextNode = nextNode.nextSibling
            if nextNode is None:
                break
            if isinstance(nextNode, Tag):
                if nextNode.name == "h2":
                    break
            # here's the magic ... get the content of the section, and ...
            seccontent = sections[hstring] + str(nextNode)
            # print("------------------------------")
            print("Updating " + hstring)
            sections.update({hstring:seccontent + " "})


def single(content, sections, topic, root, category):
    """iterates through single-section"""
    # no headers
    try:
        singlename = content.find(id='firstHeading').text
        # create a dictionary with just the one section
        sections[singlename] = ""
        # string out content and dump it in (to match 'multi')
        # print("------------------------------")
        # print("Updating " + hstring)
        sections.update({singlename:str(content)})
    except:
        # print("No heading!")
        pass

def formatter(sections, topic, root, category):
    """formats data nice and prettily"""
    for k, v in sections.items():
        vsoup = BeautifulSoup(v, "lxml")
        for br in vsoup.find_all("br"):
            br.replace_with("\n %s \n " % br.text + " ") # more pythonic
        for elem in vsoup.find_all(["a", "p", "div", "h3", "li"]):
            elem.append("\n ")
        roughtext = vsoup.get_text()
        cleantext = re.sub("\n+", "\n ", roughtext)
        sections.pop(k)
        sections.update({k : cleantext})

    for k, v in sections.items():
        # find and delete server messages that are grabbed by mistake
        serverMessageIndex = v.find("NewPP")
        # -1 means the message wasn't found
        if serverMessageIndex == -1:
            pass
        elif serverMessageIndex > 1:
            """ heavy-handed approach - now that you have the index of the
            start of the server message, delete everything after the index"""
            v = v[:serverMessageIndex]

        parser(k, v, topic, root, category)

class MLStripper(HTMLParser):
    """stripper helper functions"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    """strips like a single mother trying to get through college"""
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def parser(k, v, topic, root, category):
    """works the data into a MoreCore/FG compatible format"""
    # print("------------------------------")
    # print("Parsing " + k)
    # generate a unique id
    global nrun
    global grun

    xmlid = str(uuid.uuid4())

    formattedNotes = strip_tags(v)

    # get the category node as a base reference and create the subelement for this npc/object
    base = ET.SubElement(category, ("id-" + xmlid))
    ET.SubElement(base, "name", type="string").text = k
    cas = ET.SubElement(base, "clilist2")
    ET.SubElement(base, "notes", type="formattedtext").text = formattedNotes

    # separate article content into lines for easier parsing
    dlines = []

    # Die code finding regex
    dcodefind = re.compile(r'\d[D]\+\d|\d[D]')
    plusfind = re.compile(r'[D]\+\d')
    dfind = re.compile(r'\d[D]')

    # Search each line for a D, then keep as little as possible, one line each

    for line in v.splitlines():
        if dcodefind.search(line):
            for l in re.split(r'<br\/>|[;|,][\s|\S]', line):
                dlines.append(l)
            # print(dlines)

    # Separate the dice codes from the text
    for dline in dlines:
        # clean up nasty html tags and character entity references

        dcode = dcodefind.findall(dline)
        item = ' '.join(dcode)

        #Split out the die code pieces
        die = ''.join(dfind.findall(str(item))).replace('D', '')
        # print(k)
        # print(dline)
        # print(item)
        # print(die)

        if die == "" and not int():
            p2number = "null"
            nrun += 1
            print("\n************\n" + str(dline) + " | " + str(item) + ": " + str(die) + "\n")
        else:
            p2number = (int(die)-1)
            grun += 1

        p3number = '0'
        if plusfind.findall(str(dcode)):
            p3number = int(''.join(plusfind.findall(str(item))).replace('D+', ''))
        dname = str(''.join(str(dline)))

        # generate a unique id
        xmlid = str(uuid.uuid4())

        # create the xml data
        newcas = ET.SubElement(cas, "id-" + xmlid)
        ET.SubElement(newcas, "name", type="string").text = dname

        # MAP Rolls (Skills and Attributes)
        ET.SubElement(newcas, "description", type="formattedtext").text = 'Notes'
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
        ET.SubElement(newcas, "parameter_formula", type="string").text = '/weg (p1)d6+(p2)d1006+(p3)-(a)'
        ET.SubElement(newcas, "clichatcommand", type="string").text = '/weg 1d6+' + str(p2number) + 'd1006+' + str(p3number) + '-0'
        ET.SubElement(newcas, "parameter_formula_enabled", type="number").text = '1'
        ET.SubElement(newcas, "refa", type="string").text = '...five : (a) available'
        ET.SubElement(newcas, "refa_path", type="string").text = '...five'
        ET.SubElement(newcas, "refb", type="string").text = 'Drag Field or Roll Here'
        ET.SubElement(newcas, "refc", type="string").text = 'Drag Field or Roll Here'
        ET.SubElement(newcas, "tracker_enabled", type="number").text = '0'

        #Append content to base
        base.append(newcas)

def writer(topic, root):
    # print("------------------------------")
    # print("Writing " + topic)
    #Replace file with xml contents
    tree = ET.ElementTree(root)
    with open(topic + '.xml', "wb") as file:
        tree.write(file)
    # print("------------------------------")
    # print("Done!")
    # print("------------------------------")

if __name__ == "__main__":
    """ Execute """
    #p2 error counter
    nrun = 0
    grun = 0
    failures = []
    main()

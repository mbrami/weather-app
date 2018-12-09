#importing all the necessary libraries for execution
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
conda install requests
import requests
import re

#getting the html for the website of spurious correlations
link = "http://www.tylervigen.com/spurious-correlations"
f = requests.get(link)
print(f.text)

#scraping webpage using beautiful soup
from urllib.request import urlopen
import bs4
beautiful=urlopen(link).read()
soup=bs4.BeautifulSoup(beautiful)


#finding all the scripts to find the relevent chart script(Correlation btwn Suicides and US Spending on Science)
scripts = soup.find_all('script')
print (scripts)
#finding relevent script
rel_script = scripts[3].get_text()
print (rel_script)

#finding just the text with the data
plt_script = re.search(r'highcharts\((.*?)\);', rel_script, re.DOTALL)
print(plt_script.group(1))

#getting the string to json format
import json
json1 = plt_script.group(1)   #naming the script string

#function to make the double quotes inside strings into single quotes and changing the \ to be acceptable by json
def processStringInJson(s):
    # String is of the form '.."...".....' 
    # Return: "..'...'....."
    inner = re.search(r"'(.*)'", s)
    replaced1 = re.sub('"', "'", inner.group(1))
    replaced2 = re.sub(r"\\", r"\\\\", replaced1)
    return f'"{replaced2}"'

#function to add double quotes around attributes even if there are more than one attributes on a line
def processNonStringInJson(s):
    # Add double-quotes around attributes
    # Must work even with multiple attributes on one line
    return re.sub(r'(\w+):(.*?)([\s,\n}])', r'"\1": \2\3', s, re.DOTALL)
    
#function to parse string and make it acceptable for json to read ie no commments and unnecessary commas 
def parseJson(j):
    ls = re.split(r"('.*')", j)
    s = "".join(map(lambda s: processStringInJson(s) if re.match("'(.*)'", s) else processNonStringInJson(s), ls))
    # Remove comments in the middle of the json
    s2 = re.sub("//[^\"]*?\n", "", s, re.DOTALL)
    # Remove illegal commas at the end of expressions {"a": 1,}
    return re.sub(r"},\s*}", "}}", s2)

#load the string as json object - like dict in python
pj1 = json.loads(parseJson(json1))

#retreiving data to plot it 
#x data
years = pj1["xAxis"][0]["categories"]
# y data
suicides = pj1["series"][0]["data"]
spending = pj1["series"][1]["data"]




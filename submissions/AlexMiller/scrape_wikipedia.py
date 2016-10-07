from bs4 import BeautifulSoup as bs
import unicodecsv as csv
import urllib2
import pdb
from optparse import OptionParser
import os

parser = OptionParser()
parser.add_option("-o", "--output", dest="output", default="C:\\git\\dc-michelin-challenge\\submissions\\AlexMiller\\supplemental_data\\",
                        help="Output path. Default is wd",metavar="FOLDER")
(options, args) = parser.parse_args()

#Set up headers
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

#Request NY Michelin Star wikipedia page
req = urllib2.Request('https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_New_York_City', None, headers)
response = urllib2.urlopen(req)
source = response.read()
response.close()

#Define header
results = []
header = ["Name","Borough","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016"]
results.append(header)

#Parse using beautiful soup
page = bs(source,"html.parser")
soupTable = page.findAll("table")[0]
rows = soupTable.findAll("tr")[1:]
for row in rows:
    result = []
    cells = row.findAll("td")
    for cell in cells:
        #If we have actual text, keep it
        text = cell.text.strip()
        #Else, the alt text in the image contains the number of stars
        if text=="":
            starImg = cell.findAll("img")
            if len(starImg)>0:
                text = starImg[0].get("alt")[0]
            else:
                text = 0
        result.append(text)
    results.append(result)
    
with open(options.output+"ny_stars.csv","wb") as csvfile:
    #Need latin1 encoding for accent marks!!
    writer = csv.writer(csvfile,delimiter=",",encoding="latin1")
    for row in results:
        writer.writerow(row)
        
#Request Chicago Michelin Star wikipedia page
req = urllib2.Request('https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_Chicago', None, headers)
response = urllib2.urlopen(req)
source = response.read()
response.close()

#Define header
results = []
header = ["Name","Neighborhood","2011","2012","2013","2014","2015","2016"]
results.append(header)

#Parse using beautiful soup
page = bs(source,"html.parser")
soupTable = page.findAll("table")[0]
rows = soupTable.findAll("tr")[1:]
for row in rows:
    result = []
    cells = row.findAll("td")
    for cell in cells:
        #If we have actual text, keep it
        text = cell.text.strip()
        #Else, the alt text in the image contains the number of stars
        if text=="":
            starImg = cell.findAll("img")
            if len(starImg)>0:
                text = starImg[0].get("alt")[0]
            else:
                text = 0
        result.append(text)
    #If the restaurant closed within the time period, the cell merging shortens the row length
    #We can repeat the closed tag for the duration of the missing cells
    while len(result)<8:
        result.append(result[-1])
    results.append(result)
    
with open(options.output+"chi_stars.csv","wb") as csvfile:
    #Need latin1 encoding for accent marks!!
    writer = csv.writer(csvfile,delimiter=",",encoding="latin1")
    for row in results:
        writer.writerow(row)
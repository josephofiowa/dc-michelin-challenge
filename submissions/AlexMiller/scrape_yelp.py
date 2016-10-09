from selenium import webdriver
import pdb
from optparse import OptionParser
import pandas as pd
from urllib import quote
import re
import unicodecsv
import os
import glob

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", default="C:\\git\\dc-michelin-challenge\\submissions\\AlexMiller\\supplemental_data\\ny_stars.csv",
                        help="Output path. Default is wd",metavar="FOLDER")
parser.add_option("-d", "--dcinput", dest="dcinput", default="C:\\git\\dc-michelin-challenge\\submissions\\AlexMiller\\supplemental_data\\dc_possibilities.csv",
                        help="Output path. Default is wd",metavar="FOLDER")
parser.add_option("-o", "--output", dest="output", default="D:\\Documents\\Data\\Yelp\\",
                        help="Output path. Default is wd",metavar="FOLDER")
(options, args) = parser.parse_args()

browser = webdriver.Chrome("C://chromedriver//chromedriver") # Create a session of Chrome
browser.implicitly_wait(30) # Configure the WebDriver to wait up to 30 seconds for each page to load

#Function to make sure we're writing good filenames
def get_valid_filename(s):
    """
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; and anything that is not a unicode
    alphanumeric, dash, underscore, or dot, is removed.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    Adapted from Django
    """
    s = s.strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

#Function to clean messy text
def clean_text(row):
    # Remove characters that are giving us headaches
    return [r.replace(u"\u2026","...").replace(u"\u2019","'").replace(u"\u015b","s").replace(u"\u015f","s").replace(u"\u014d","o").replace(u"\u016b","u").replace(u"\u0113","e") for r in row]

#Function to search for a specific restaurant
def search_yelp(browser, description, location):
    find_loc = location.replace(" ","+").replace("'","%27").replace("&","%26") # Encode strings for URL
    find_desc = description.replace(" ","+").replace("'","%27").replace("&","%26")
    search_url = "https://www.yelp.com/search?find_desc=%s&find_loc=%s" % (find_desc,find_loc)
    browser.get(search_url) # Load page

#Function to lookup reviews based on hit number
def review(browser, description, hit):
    hit_span = browser.find_element_by_xpath("//*[contains(text(), '%s.         ')]" % hit) #Find the first link
    hit_link = hit_span.find_elements_by_tag_name('a')[0]
    hit_link_href = hit_link.get_attribute('href')
    
    browser.get(hit_link_href+"?sort_by=elites_desc") # Load first page. Sort by elites for better reviews
    
    #Name
    name = browser.find_element_by_class_name("biz-page-title").text
    
    #Price range
    price_range = browser.find_element_by_xpath('//*[@class="business-attribute price-range"]').text
    
    #Review count
    review_count = browser.find_element_by_xpath('//*[@itemprop="reviewCount"]').text
    
    # Find all the dates
    dates = browser.find_elements_by_xpath('//*[@itemprop="datePublished"]')
    date_array = [date.get_attribute('content') for date in dates]
    
    # Find all the scores
    scores = browser.find_elements_by_xpath('//*[@itemprop="ratingValue"]')
    score_array = [score.get_attribute('content') for score in scores]
    average_score = score_array[0] #The first review is the average for the whole restaurant
    review_score_array = score_array[1:len(date_array)+1]
    
    # Find all the reviews
    reviews = browser.find_elements_by_xpath('//*[@itemprop="description"]')
    review_array = [review.text for review in reviews]
    #Make a Pandas dataframe
    df = pd.DataFrame({"req.restaurant":description,"result.restaurant":name,"date":date_array,"avg.score":average_score,"price":price_range,"review.count":review_count,"score":review_score_array,"review":review_array})
    df = df.apply(clean_text)
    return df

#Read through our wiki-scraped restaurants and scrape some metadata and reviews
with open(options.input,'rb') as csvfile:
        reader = unicodecsv.reader(csvfile,delimiter=",",quotechar="\"",encoding="latin1")
        header = False
        for row in reader:
            if not header:
                header = row
            else:
                description = row[0]
                filename = options.output+"NYC\\"+get_valid_filename(description)+".csv"
                location = "New York, NY"
                star_year = int(row[2])
                stars = int(row[3])
                if star_year==2016 and stars>0 and not os.path.isfile(filename):
                    print(description)
                    search_yelp(browser, description, location)
                    df = review(browser, description, 1)
                    df["stars"] = stars
                    df["star.year"] = star_year
                    df.to_csv(filename,index=False,encoding="latin1")
                    
#Read through our DC picks and scrape some metadata and reviews
with open(options.dcinput,'rb') as csvfile:
        reader = unicodecsv.reader(csvfile,delimiter=",",quotechar="\"",encoding="latin1")
        header = False
        for row in reader:
            if not header:
                header = row
            else:
                description = row[0]
                filename = options.output+"DC\\"+get_valid_filename(description)+".csv"
                location = "Washington, DC"
                if not os.path.isfile(filename):
                    print(description)
                    search_yelp(browser, description, location)
                    df = review(browser, description, 1)
                    df["stars"] = ""
                    df["star.year"] = 9999
                    df.to_csv(filename,index=False,encoding="latin1")

#Scrape about 200 unstarred NYC restaurants
browser.get("https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY&start=0&sortby=review_count&attrs=RestaurantsPriceRange2.4,RestaurantsPriceRange2.3")
for i in range(1,201):
    df = review(browser,"Unstarred",i)
    df["stars"] = 0
    df["star.year"] = 9999
    description = df["result.restaurant"][0]
    filename = options.output+"NYC\\"+get_valid_filename(description)+".csv"
    if not os.path.isfile(filename):
        df.to_csv(filename,index=False,encoding="latin1")
    browser.back()
    #Advance the page every 10
    if i % 10 == 0:
        next_url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY&start=%s&sortby=review_count&attrs=RestaurantsPriceRange2.4,RestaurantsPriceRange2.3" % i
        browser.get(next_url)

browser.close()
                    
#Find .csvs in NYC folder and concat
output = []
paths = glob.glob(options.output+"NYC\\*.csv")
for csv_file in paths:
    df = pd.read_csv(csv_file, header=0,encoding="latin1")
    output.append(df)
frame = pd.concat(output)
frame.to_csv(options.output+"nyc.csv",index=False,encoding="latin1")

#Find .csvs in DC folder and concat
output = []
paths = glob.glob(options.output+"DC\\*.csv")
for csv_file in paths:
    df = pd.read_csv(csv_file, header=0,encoding="latin1")
    output.append(df)
frame = pd.concat(output)
frame.to_csv(options.output+"dc.csv",index=False,encoding="latin1")
from selenium import webdriver
import pdb
from optparse import OptionParser
import pandas as pd
from urllib import quote
import re
import unicodecsv

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", default="C:\\git\\dc-michelin-challenge\\submissions\\AlexMiller\\supplemental_data\\ny_stars.csv",
                        help="Output path. Default is wd",metavar="FOLDER")
parser.add_option("-o", "--output", dest="output", default="D:\\Documents\\Data\\Yelp\\NYC\\",
                        help="Output path. Default is wd",metavar="FOLDER")
(options, args) = parser.parse_args()

browser = webdriver.Chrome("C://chromedriver//chromedriver") # Create a session of Chrome
browser.implicitly_wait(30) # Configure the WebDriver to wait up to 30 seconds for each page to load

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

def review(browser, description, location):
    find_loc = quote(location,safe='').replace("%20","+") # Encode strings for URL
    find_desc = quote(description,safe='').replace("%20","+")
    search_url = "https://www.yelp.com/search?find_desc=%s&find_loc=%s" % (find_desc,find_loc)
    browser.get(search_url) # Load page
    first_span = browser.find_element_by_xpath("//*[contains(text(), '1.         ')]") #Find the first link
    first_hit = first_span.find_elements_by_tag_name('a')[0]
    first_hit_href = first_hit.get_attribute('href')
    
    browser.get(first_hit_href+"?sort_by=elites_desc") # Load first page. Sort by elites for better reviews
    
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
    review_score_array = score_array[1:]
    
    # Find all the reviews
    reviews = browser.find_elements_by_xpath('//*[@itemprop="description"]')
    review_array = [review.text for review in reviews]
    
    #Make a Pandas dataframe
    df = pd.DataFrame({"restaurant":description,"date":date_array,"avg.score":average_score,"price":price_range,"review.count":review_count,"score":review_score_array,"review":review_array})
    return df

#Read through our wiki-scraped restaurants and scrape some metadata and reviews
#Some restaurants no longer exist...
duds = [
    "Adour"
    ,"Alain Ducasse at the Essex House"
    ,"Allen & Delancey"
    ,"Alto"
    ,""
    ]
with open(options.input,'rb') as csvfile:
        reader = unicodecsv.reader(csvfile,delimiter=",",quotechar="\"",encoding="latin1")
        header = False
        for row in reader:
            if not header:
                header = row
            else:
                description = row[0]
                location = "New York, NY"
                star_year = row[2]
                stars = row[3]
                if int(star_year)==2016 and description not in duds:
                    print(description)
                    df = review(browser, description, location)
                    df["stars"] = stars
                    df["star.year"] = star_year
                    df.to_csv(options.output+get_valid_filename(description)+".csv",index=False,encoding="latin1")
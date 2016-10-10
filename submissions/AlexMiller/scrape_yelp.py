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
    try:
        new_row = [r.replace(u"\u2015","-").replace(u"\u201C","'").replace(u"\uff01","!").replace(u"\u201D","'").replace(u"\u2026","...").replace(u"\u2019","'").replace(u"\u015b","s").replace(u"\u015f","s").replace(u"\u014d","o").replace(u"\u016b","u").replace(u"\u0113","e").replace(u"\uff0c",",") for r in row]
    except:
        new_row = [r.replace(u"\u2015","-").replace(u"\u201C","'").replace(u"\uff01","!").replace(u"\u201D","'").replace(u"\u2026","...").replace(u"\u2019","'").replace(u"\u015b","s").replace(u"\u015f","s").replace(u"\u014d","o").replace(u"\u016b","u").replace(u"\u0113","e").replace(u"\uff0c",",").decode("windows-1251",errors="ignore") for r in row]
    return new_row

#Function to search for a specific restaurant
def search_yelp(browser, description, location):
    find_loc = location.replace(" ","+").replace("'","%27").replace("&","%26") # Encode strings for URL
    find_desc = description.replace(" ","+").replace("'","%27").replace("&","%26")
    search_url = "https://www.yelp.com/search?find_desc=%s&find_loc=%s" % (find_desc,find_loc)
    browser.get(search_url) # Load page
    
#Function to click specific reviews
def click_hit(browser, hit):
    hit_span = browser.find_element_by_xpath("//*[contains(text(), '%s.         ')]" % hit) #Find the first link
    hit_link = hit_span.find_elements_by_tag_name('a')[0]
    hit_link_href = hit_link.get_attribute('href')
    
    # browser.get(hit_link_href+"?sort_by=elites_desc") # Load first page. Sort by elites?
    browser.get(hit_link_href) # Load first page.
    
    if "?" in hit_link_href:
        hit_link_href = hit_link_href.split("?")[0]
    
    return hit_link_href

#Function to lookup reviews based on hit number
def review(browser, description):
    
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
        header = False # Make sure we're not reading in the header
        for row in reader:
            if not header:
                header = row
            else:
                description = row[0]
                filename = options.output+"NYC\\"+get_valid_filename(description)+".csv" #Make a valid filename
                location = "New York, NY"
                star_year = int(row[2])
                stars = int(row[3])
                if star_year==2016 and stars>0 and not os.path.isfile(filename): #As long as it's from 2016 and has stars, and the file doesn't exist
                    print(description)
                    search_yelp(browser, description, location) #Search yelp for our restaurant
                    hit_link = click_hit(browser, 1) #Click the first hit
                    df = review(browser, description) #Grab the review
                    df["stars"] = stars
                    df["star.year"] = star_year
                    df.to_csv(filename,index=False,encoding="latin1") #Write to file
                    pagination_index = 1 # Here's where we start pagination to increase our review count
                    while True and pagination_index<20: #Infinite loop, but break at a reasonable 2k reviews
                        try:
                            next_chev = browser.find_elements_by_xpath('//*[@class="icon icon--24-chevron-right icon--size-24 icon--currentColor"]') #Try and find the chevron icon for next
                            if len(next_chev)==0: #Break if we can't find it
                                break
                            start = "?start=%s" % (pagination_index*20) #Add the pagination attribute to the URL
                            browser.get(hit_link+start)
                            filename = options.output+"NYC\\"+get_valid_filename(description)+"_"+str(pagination_index)+".csv"
                            if not os.path.isfile(filename): #If the file doesn't already exist
                                df = review(browser, description) #Grab the review on the new page
                                if df.count(0)[0]==0: #If there are no reviews, break
                                    break
                                else:
                                    df["stars"] = stars
                                    df["star.year"] = star_year
                                    df.to_csv(filename,index=False,encoding="latin1") #Write to file
                            else:
                                break
                            pagination_index = pagination_index + 1
                        except:
                            break
                    
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
                    hit_link = click_hit(browser, 1)
                    df = review(browser, description)
                    df["stars"] = ""
                    df["star.year"] = 9999
                    df.to_csv(filename,index=False,encoding="latin1")
                    pagination_index = 1
                    while True and pagination_index<20: #Infinite loop, but break at a reasonable 2k reviews
                        try:
                            next_chev = browser.find_elements_by_xpath('//*[@class="icon icon--24-chevron-right icon--size-24 icon--currentColor"]') #Try and find the chevron icon for next
                            if len(next_chev)==0: #Break if we can't find it
                                break
                            start = "?start=%s" % (pagination_index*20) #Add the pagination attribute to the URL
                            browser.get(hit_link+start)
                            filename = options.output+"DC\\"+get_valid_filename(description)+"_"+str(pagination_index)+".csv"
                            if not os.path.isfile(filename): #If the file doesn't already exist
                                df = review(browser, description) #Grab the review on the new page
                                if df.count(0)[0]==0: #If there are no reviews, break
                                    break
                                else:
                                    df["stars"] = stars
                                    df["star.year"] = star_year
                                    df.to_csv(filename,index=False,encoding="latin1") #Write to file
                            else:
                                break
                            pagination_index = pagination_index + 1
                        except:
                            break

#Scrape about 200 unstarred NYC restaurants
browser.get("https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY&start=0&sortby=review_count&attrs=RestaurantsPriceRange2.4,RestaurantsPriceRange2.3")
for i in range(1,201):
    click_hit(browser,i)
    df = review(browser,"Unstarred")
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
frame.drop_duplicates()
frame.to_csv(options.output+"nyc.csv",index=False,encoding="latin1")

#Find .csvs in DC folder and concat
output = []
paths = glob.glob(options.output+"DC\\*.csv")
for csv_file in paths:
    df = pd.read_csv(csv_file, header=0,encoding="latin1")
    output.append(df)
frame = pd.concat(output)
frame.drop_duplicates()
frame.to_csv(options.output+"dc.csv",index=False,encoding="latin1")
# #!/usr/bin/env python3
#
# @Author: Josh Erb <josh.erb>
# @Date:   06-Oct-2016 00:10
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 12-Oct-2016 13:10
#
"""
The purpose of this script is to scrape the web for data about which restaurants
in a given city have a Michelin star and/or have recieved a positive review from
a notable critic.

It includes functions to scrape and generate a list of restaurants & and their number of
Michelin stars, and perform a similar - slightly more complicated - task to generate
a 'positive critical review' binary data point.

Once these additional data points have been gathered, they are inserted into a
MongoDB instance.

Caveat emptor: This approach assumes that Wikipedia has the most up-to-date
information on which restaurants have been awarded Michelin stars.
"""

##########################################################################
## Imports
##########################################################################

import glob
import json
import pymongo
import requests
import time
from rauth import OAuth2Session
from bs4 import BeautifulSoup
from pprint import pprint

##########################################################################
## Module Variables/Constants
##########################################################################

# Yelp API url
url = 'https://api.yelp.com/v3/businesses/search'

# the wikipedia pages that indicate which restaurants have michelin stars
wiki_urls = ('https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_New_York_City#cite_note-14','https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_Chicago', 'https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_San_Francisco')
cities = ('new york', 'chicago', 'san francisco', 'washington dc')
# Unfortunately, NYTimes does not release it's list of top restaurants the end of the year
critic_urls = ('http://www.nytimes.com/2015/12/16/dining/best-restaurants-in-nyc.html', 'http://www.chicagotribune.com/dining/best-restaurants/get-blogroll.html?discads=false&section=/dining/best-restaurants&page=', 'http://projects.sfchronicle.com/2016/top-100-restaurants/', 'https://www.washingtonpost.com/dc-restaurants-guide-spring-2016/')

##########################################################################
## Functions
##########################################################################

def _mongo_connect():
    """
    A function to quickly connect to my MongoDB.
    """
    # Note this function assumes you already have a mongod instance up and running in your terminal
    conn = pymongo.MongoClient()
    db = conn.distribution_center
    return db

def grab_page(url):
    """
    A function that takes url, scrapes the corresponding web page
    and returns its content.

    Argument:
    ** url - a string object that contains a url, which must be
    to a non-password protected website
    """
    # asking for the page to show itself to my python code
    page = requests.get(url)
    # using this opportunity to snatch up the page's content
    loot = page.content
    return loot

def grab_star_values(city, p_content):
    """
    A function to identify and grab values from a wikipedia table. Specifically,
    this will be used to grab values out of wikipedia tables re: the number of
    Michelin stars each cities' restaurants have.

    Arguments:
    ** city - a string parameter specifying
    ** p_content - the content of a requests.get() call
    """
    # Initialize a dictionary to hold the restaurant and corresponding
    # number of Michelin stars
    city_stars = {}

    # Load our wikipedia pages content into a BeautifulSoup object
    grub = BeautifulSoup(p_content, "html.parser")

    # Identify the table, and iterate through each row.
    # Since our Yelp Data isn't timestamped, we'll only be grabbing the restaurants
    # that recieved stars in the most recent guide
    table = grub.find("table", {"class":"wikitable sortable"})

    # This was pain in the butt to scrape, for some reason
    # Once we have the table, we need to iterate through the rows to find those
    # that recieved stars in 2016 (Because our Yelp Data isn't timestamped,
    # we'll only be grabbing the restaurants that recieved stars in the most recent guide
    for row in table.find_all('tr'): # first grab all the rows
        # Because of how the Chicago & SF tables are formatted I need to account
        # for restaurants that have closed down (hence all the odd caveats)
        cells = row.find_all('td') # then grab all the data points within the row
        if len(cells) > 0 and cells[-1].text != 'Closed': # skip that first empty row and any closed restaurants
            name = cells[0].text # grab the name of the restaurant
            if len(cells[-1]) > 0: # skip restaurants that don't have 2016 stars
                star_box = cells[-1].select('a')
                star_str = star_box[0].img['alt'] # grab the alt text, whose first character tells me how many stars
                star_ct = int(star_str[0])
                city_stars[name] = star_ct # add the stars to my dictionary object
            else:
                continue
        else:
            continue # I know there's probably a prettier way to do this, but I'm on a deadline!

    # I want to save these lists to verify I'm pulling correct data, also to
    # make it easier to add to my database after I've scraped
    with open('data/{}_stars.json'.format(city), 'w') as f:
        json.dump(city_stars, f, indent=4)

    return city_stars

def grab_chi_critic(url=critic_urls[1]):
    """
    A function to identify and grab values from Chicago Tribune's 2016 list of
    best local restaurants. This will generate and return a dictionary object,
    which can then be used to add data to a MongoDB instance.

    Chicago Tribune insists on maintaining a horrible, deprecated website so fair
    warning: this one's a bit of a hack job.

    Arguments:
    ** url - the page that contains the list of best restaurants
    """
    # This dictionary will hold the data I pull from the site
    reviewed_restaurants = {}
    # Ask ChicagoTribune to share every one of their site's pages
    for i in range(1, 11):
        # Append the page query and see the goods
        page_url = url + str(i)
        response = grab_page(page_url)
        page = BeautifulSoup(response, "html.parser")
        # grab the proper info & splice it to grab the restaurant names
        listed = page.find_all("a", "trb_blogroll_post_title_a")
        for thing in listed:
            text = thing.text
            # Getting rid of non-essential title text
            name = text.split(': ', 1)[1]
            name = name.split(',', 1)[0]
            # add it to my dictionary real quick before looking for the rest
            reviewed_restaurants[name] = 1
        # don't want CT to get wise, also just being a good citizen of the internet
        time.sleep(.5)

    # This is here just because the CT's web design is so, so crappy
    del reviewed_restaurants['Top 10 scrambled as Oriole joins list']

    # save as a file, for posterity
    with open('data/{}_pos_reviews.json'.format('chicago'), 'w') as f:
        json.dump(reviewed_restaurants, f, indent=4)

    return reviewed_restaurants

def grab_nyc_critic(url=critic_urls[0]):
    """
    A function to identify and grab values from New York Time's Dec. 2015 list
    of best local restaurants. This will generate and return a dictionary
    object, which can then be used to add data to a MongoDB instance.

    Arguments:
    ** url - the page that contains the list of best restaurants
    """
    # This dictionary will hold the data I pull from the site
    reviewed_restaurants = {}
    # Ask ChicagoTribune to share their page with me
    response = grab_page(url)
    # Load the content of the response into a BeautifulSoup object
    page = BeautifulSoup(response, "html.parser")

    # Fortunately, NYTimes has listed all of the names of the listed restaurants
    # in the meta variables on the page, so this is quite simple
    meta_vars = page.find_all("meta", {"name": "org"}) # I now have all 10 instances

    # Now I'll loop through the list of meta tags and add each restaurant to my
    # dictionary with a 1 (indicating that it's recieved a positive review)
    for var in meta_vars:
        name = var['content'].split(' (', 1)[0]
        reviewed_restaurants[name] = 1

    # saving it to disk for posterity
    with open('data/{}_pos_reviews.json'.format('new york'), 'w') as f:
        json.dump(reviewed_restaurants, f, indent=4)

    return reviewed_restaurants

def grab_sf_critic(url=critic_urls[2]):
    """
    A function to identify and grab values from the San Francisco Chronicle's
    2016 list of best local restaurants. This will generate and return a
    dictionary object, which can then be used to add data to a MongoDB instance.

    Arguments:
    ** url - the page that contains the list of best restaurants
    """
    # This dictionary will hold the data I pull from the site
    reviewed_restaurants = {}
    # Ask ChicagoTribune to share their page with me
    response = grab_page(url)
    # Load the content of the response into a BeautifulSoup object
    page = BeautifulSoup(response, "html.parser")

    # This page has it all contained quite neatly actually, I can grab all the
    # info I need using the find_all on div objects, with only one character
    # SF Chronicle wins first prize!
    mega_list = page.find_all("div", "column restaurant-index")

    # Now I want to look at each object, grab the text (which, after minor formatting,
    # will have the name of every restaurant on SF's critic list)
    for thing in mega_list:
        name = thing.text.strip('\n')
        # And I'll populate the dictionary, which the functional will pass back
        reviewed_restaurants[name] = 1

    # saving it to disk for posterity
    with open('data/{}_pos_reviews.json'.format('san francisco'), 'w') as f:
        json.dump(reviewed_restaurants, f, indent=4)

    return reviewed_restaurants

def grab_critic(city):
    """
    Just to save me the time of calling each function every time for each article.
    """
    if city == 'san francisco':
        grab_sf_critic()
    elif city == 'new york':
        grab_nyc_critic()
    elif city == 'chicago':
        grab_chi_critic()
    elif city == 'washington dc':
        grab_dc_critic()
    else:
        print('Sorry, but I don\'t have a corresponding article url to scrape.')
    return

def grab_dc_critic(url=critic_urls[3]):
    """
    A function to identify and grab values from the Washington Post's
    2016 list of best new local restaurants. This will generate and return a
    dictionary object, which can then be used to add data to a MongoDB instance.

    Arguments:
    ** url - the page that contains the list of best restaurants
    """
    # This dictionary will hold the data I pull from the site
    reviewed_restaurants = {}
    # Ask ChicagoTribune to share their page with me
    response = grab_page(url)
    # Load the content of the response into a BeautifulSoup object
    page = BeautifulSoup(response, "html.parser")

    # The way that WaPo set things up, I only want items listed as "best new restaurants"
    # It's a bit of a hack, but I was able to grab those based on the banner style and
    # some soupy navigation
    parent_divs = page.find_all("div", {"style":"color:#FFFFFF;background-color:#D8070E;"})

    # now I want to iterate through my list of divs and grab the names of the
    # restaurants that have been flagged with that chic banner
    for thing in parent_divs:
        name = thing.next.next.next.next.text # STOP JUDGING ME!
        reviewed_restaurants[name] = 1

    # Save the list of restaurants for posterity
    with open('data/{}_pos_reviews.json'.format('washington dc'), 'w') as f:
        json.dump(reviewed_restaurants, f, indent=4)

    # Hand back the dictionary
    return reviewed_restaurants

def add_stars_to_mongo(city, star_dict):
    """
    A function to add any new data points into our MongoDB instance for the
    corresponding restaurant.

    Arguments:
    ** star_dict - a dictionary object that has contains: restaurants,
    and the number of stars that each one has
    """
    # I want to keep track of which Michelin starred restaurants are not currently
    # in my database, so I can add them later if I have time
    yelp_missed = {}

    # Now let me get MongoDB set up really quickly
    db = _mongo_connect()

    # determine what data what database I should be working with
    if city == 'washington dc':
        collection = db.dc_eats
    else:
        collection = db.restaurants

    # The following is to be able to names
    res_names = star_dict.keys()
    db_names = collection.distinct('name')

    # Now I'd like to see if this restaurant exists in my database.
    # If it does, I'll add the corresponding star value.
    for name in res_names:
        if name in db_names:
            collection.update({"name":name},{"$set":{"michelin_stars":star_dict[name]}})
        else:
            # If it doesn't, I'll add it to my yelp_missed and save it for later
            yelp_missed[name] = star_dict[name]

    with open('data/{}_missed.json'.format(city), 'w') as f:
        json.dump(yelp_missed, f, indent=4)

    return

def add_critics_to_mongo(city, crit_dict):
    """
    A function to add the binary classifier of "positive_review" to our MongoDB
    instance. Value key: 1 = "recieved a positive review", 2 = "did not recieve a positive review"

    Arguments:
    ** city - city where the pos criticism was found
    ** crit_dict - a dictionary object that has contains restaurants that were
        identified as having positive reviews
    """
    # I want to keep track of which Michelin starred restaurants are not currently
    # in my database, so I can add them later if I have time
    critic_yelp_add = {}

    # Now let me get MongoDB set up really quickly
    db = _mongo_connect()

    # determine what data what database I should be working with
    if city == 'washington dc':
        collection = db.dc_eats
    else:
        collection = db.restaurants

    # grab reviewed restaurant names & the names of restaurants in my DB
    rev_names = crit_dict.keys()
    coll_names = collection.distinct('name')

    # compare the two & add the positive reviews
    for name in rev_names:
        if name in coll_names:
            collection.update({"name":name}, {"$set":{"pos_review":1}})
        else:
            collection.update({"name":name}, {"$set":{"pos_review":0}})
            critic_yelp_add[name] = 1

    # posterity
    with open('data/{}_missed_critic.json'.format(city), 'w') as f:
        json.dump(critic_yelp_add, f, indent=4)

    return

def calc_relative_rating(city):
    """
    This function runs through a given data set and generates a relative rating
    data point based on the average rating within a city.
    """
    pass


def main():
    """
    The primary execution function.
    """
    # I want to do this efficiently, so I'm just going to loop through my
    # list of cities

    for item in cities:
        if cities.index(item) < 3: # this is because I've got DC in my list and it doesn't have any stars
            page = grab_page(wiki_urls[cities.index(item)]) # grab the wiki_page
            table_data = grab_star_values(item, page) # extrapolate the table data
            add_stars_to_mongo(item, table_data) # add star data to MongoDB
        else:
            continue
    # Is there a better way to do this? Probably.
    crit_files = glob.glob('data/*pos_review*')

    for city in crit_files:
        town = city.split('/', 1)[1] # this is just to grab the city from the file name
        town = town.split('_', 1)[0]
        with open(city, 'r') as f:
            record = json.loads(f.read())
        add_critics_to_mongo(town, record)

    return

##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()

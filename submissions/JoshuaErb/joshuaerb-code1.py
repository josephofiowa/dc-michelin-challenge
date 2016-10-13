#!/usr/bin/env python3
#
# @Author: Josh Erb <josh.erb>
# @Date:   30-Sep-2016 16:09
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 11-Oct-2016 22:10
#
"""
The purpose of this script is to pull data from four cities using the Yelp
Business Search API.

The four cities are: New York, Chicago, San Francisco, & Washington DC
"""

##########################################################################
## Imports
##########################################################################

import json
import glob
import pymongo
from rauth import OAuth2Session
from pprint import pprint

##########################################################################
## Module Variables/Constants
##########################################################################

def _get_creds():
    """
    Quick little function to grab my Yelp API credentials and load them into
    a dictionary object.
    """
    with open('secret_sauce/config_secret.json', 'r') as f:
        my_secret_sauce = json.loads(f.read()) # sorry, don't want to share these with you

    return my_secret_sauce

api_creds = _get_creds()

api_id = api_creds['consumer_key']
api_secret = api_creds['consumer_secret']
api_token = api_creds['token']

cities = ['chicago', 'new york', 'san francisco', 'washington dc']
url = 'https://api.yelp.com/v3/businesses/search'
# initializing parameters
q_params = {'term': 'restaurant','location': '', 'limit': int()}

##########################################################################
## Functions
##########################################################################

def _grab_city_name(file_path):
    """
    Nothing to see here.
    """
    town = file_path.split('/', 1)[1] # this is just to grab the city from the file name
    town = town.split('_', 1)[0]
    return town

def grab_data(session, city, sort='rating', parms=q_params, url=url, n=50):
    """
    After an OAuth2Session has been instantiated, use this function to run a
    GET request against the Yelp API.

    Arguments:
    ** session - a validated OAuth2Session
    ** city - the name of a city which will be added to the params dictionary
    ** sort - how I want the data coming from the Yelp API to be sorted
    ** params - a dictionary object that contains the API parameters to query the data
    ** url - the url of the API to be queried
    ** n - the value to be specified for the limit parameter
    """
    # flesh out the params
    parms['location'] = str(city)
    parms['limit'] = int(n)
    parms['sort_by'] = str(sort)

    # query hit the API with a data query
    response = session.get(url, params=parms)

    # telling python how to understand it
    proper_response = response.json()

    # droppping the unnecessary general category yelp provides of "businesses"
    proper_response = proper_response['businesses']

    # pass back the list of 50 dictionary objects
    return proper_response

def mongo_dump(city, data):
    """
    Takes a list of dictionary objects and adds them to a locoal MongoDB instance.

    Argument:
    ** city - a string object that specifies the city the data came from
    ** data - must be a list of dictionary objects
    """
    # just making sure nothing weird gets thrown at this function
    city_name = str(city)

    # Instantiate the MongoDB client object
    conn = pymongo.MongoClient()

    # Because I'm using pymongo, I can implicitly create my database
    # (And yes, I'm calling my db the distribution center)
    db = conn.distribution_center

    # I'll be keeping the DC data in a seperate collection that I'll use after I
    # train my model(s) on the other cities's data
    if city_name == 'washington dc':
        collection = db.dc_eats
    else:
        collection = db.restaurants # this is the collection I'll keep my training data in

    # Now I'd like to add each restaurant as a document object in whichever
    # collection I'm working with
    for item in data:
        collection.insert_one(item)

    # Close the cursor
    conn.close()

    return

def insert_unique(city, data):
    """
    After the initial data dump into the MongoDB distribution_center database,
    use this function to query the API using different parameters and add any
    novel restaurants that come up into the databse.

    This is an effort to make the Yelp data a bit more robust before (and
    because we're limited to 50 restaurants per query).

    Argument:
    ** city - a string object that specifies the city the data came from
    ** data - must be a list of dictionary objects
    """
    # I don't like to repeat myself, but couldn't be bothered to make a MongoDB
    # set-up function, so this will have to do under the time constraints
    city_name = str(city)
    conn = pymongo.MongoClient()
    db = conn.distribution_center

    if city_name == 'washington dc':
        collection = db.dc_eats
    else:
        collection = db.restaurants

    # Now I'd like to look at the data I've handed the function and add any
    # restaurants it has that are not currently in the database, this requires
    # a bit of creativity
    for item in data:
        if item['coordinates'] in collection.distinct('coordinates'):
            continue # if it's already there, then skip it
        else:
            collection.insert_one(item) # if it's not there, add it to the collection

    # Don't forget to turn off you cursor
    conn.close()

    return

def initial_pull():
    """
    Primary execution for data pulls.
    """
    # Instantiate the OAuth2 session to access Yelp data
    session = OAuth2Session(api_id, api_secret, api_token)
    ## Use a loop to pull data for each city based on parameters
    for city in cities:
        json_data = grab_data(session, city)
        # quickly saving each data file as a json so I can check share it with colleagues
        with open('data/{}.json'.format(city), 'w') as d:
            for item in json_data:
                json.dump(item, d, indent=4)

        # I will now add the data to my local MongoDB instance
        mongo_dump(city, json_data)

    # To make sure the data is as robust as possible, I'm going to run a different
    # search query and have it sorted by 'review_count', then add any unique values
    # to the MongoDB distribution_center
    for city in cities:
        addl_data = grab_data(session, city, sort='review_count')

        # check to see if the values are already in our database, if they aren't
        # add them as new documents in their respective collections
        insert_unique(city, addl_data)

    return

def aug_yelp_data(session, city, addition, parms=q_params, url=url, n=1):
    """
    This function will be used to pull data for restaurants that were initially
    missed when querying yelp for restaurant data, and add new data to MongoDB

    Arguments:
    ** session - a validated OAuth2Session
    ** city - the name of a city which will be added to the params dictionary
    ** parms - a dictionary object that contains the API parameters to query the data
    ** addition - specifies whether this was because of critics or stars
    ** url - the url of the API to be queried
    ** n - the value to be specified for the limit parameter
    """
    # will take use the "missed restaurant" files and use those to query Yelp API
    # flesh out the params
    parms['location'] = str(city)
    parms['limit'] = int(n)

    # Need to iterate through the dict object and search yelp for an entry
    for item in addition.keys():
        parms['term'] = item
        response = session.get(url, params=parms)
        proper_response = response.json() # Basically the same process as grab_data
        proper_response = proper_response['businesses']
        insert_unique(city, proper_response) # adding the data to the MongoDB
        time.sleep(0.5) # Trying not to annoy Yelp

    return

def main():
    """
    Execution function.
    """
    # starting Yelp API session
    session = OAuth2Session(api_id, api_secret, api_token)

    # Grab the titles for our missing data
    missed_reviews = glob.glob('data/*missed_critic.json')
    missed_stars = glob.glob('data/*_missed.json')

    # Re-run our intial pull code
    initial_pull()

    # add all of the items that were overlooked during first pull
    for establishment in missed_reviews:
        name = _grab_city_name(establishment)# need to know which city we're working with
        # open the file that contains the missed values
        with open(establishment, 'r') as f:
            new_data = json.loads(f.read())
        aug_yelp_data(session, name, new_data)

    # open the list of stars that weren't in initial Yelp API pull
    for locale in missed_stars:
        name = _grab_city_name(locale)
        with open(locale, 'r') as f:
            new_stars = json.loads(f.read())
        aug_yelp_data(session, name, new_stars)

    return

##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()

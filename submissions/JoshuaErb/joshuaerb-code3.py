# #!/usr/bin/env python3
#
# @Author: Josh Erb <josh.erb>
# @Date:   10-Oct-2016 12:10
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 12-Oct-2016 21:10
"""
The purpose of this script is extensive. It first extracts data from a MongoDB
instance and loads it into an array that can be used with the Sci-Kit Learn
library's tools (feature extraction).

It then runs several tests in order to decide which features from the data will
be most valuable for modeling purposes. After the above, it then trains a model
on the data for three cities (New York, San Francisco, and Chicago).

Once the model is trained satisfactoraly, it is then applied to the data for
restaurants in Washington, DC in order to predict the number of Michelin stars
each will have when the results are released on October 13, 2016.

The output from this predictive model is then saved in a .csv file with two
columns: the restaurant's name and the number of predicted stars.
"""

##########################################################################
## Imports
##########################################################################

import os
import csv
import json
import pymongo
import flatdict
import numpy as np
from pprint import pprint
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score  # Some of these I didn't use because
from sklearn.feature_extraction import DictVectorizer # I was in crunch time
from sklearn.pipeline import Pipeline # Nothing to see here
from sklearn.pipeline import make_pipeline # Shhhh....
from sklearn.tree import DecisionTreeRegressor


##########################################################################
## Module Variables/Constants
##########################################################################

csv_output = os.path.abspath('./predictions/joshuaerb-submission.csv')
unwanted = ('url', 'image_url', 'phone')

##########################################################################
## Functions
##########################################################################

def drop_cats(cats, the_dict):
    for key in cats:
        if key in the_dict:
            del the_dict[key]
    return

def make_usable(city):
    """
    A quick function to dump the specified collection into an array and hand
    it back to be usable with sklearn's feature extraction module.

    Arguments:
    * city - a string indicating which city collection to make usable
    """
    # open up the MongoDB
    conn = pymongo.MongoClient()
    db = conn.distribution_center

    # verify which collection
    if city == 'washington dc':
        collection = db.dc_eats
    else:
        collection = db.restaurants

    # turn the cursor response into an array object
    init_array = list(collection.find())

    # because sklearn only excepts dict objects with a depth of 1, I need to
    # iterate through the array that MongoDB gives me and iterate through it till
    # it meets my specifications
    array = [] # this will hold my final array of 1-d dict objects

    # iteration goes here
    for restaurant in init_array:
        restaurant.pop('_id')
        cat = restaurant['categories'] # don't want to lose the info in the category array
        flat_cat = ''
        for item in cat:
            title = item['title']
            flat_cat += str(title) + ','
        flat = flatdict.FlatDict(restaurant) # collapsing it down to a 1-d dict object
        flat.update(categories=flat_cat)
        new_restaurant = {}
        for key, value in flat.iteritems(): # can't hand sklearn a flatdictionary object
            new_restaurant[key] = value
        array.append(new_restaurant) # add it to my final array

    # let Mongo rest, it's done it's job
    conn.close()

    return array # this array can now be handed to sklearn's DictVectorizer

def train_n_predict(tr_array, pred_array, path=csv_output, cats=unwanted):
    """
    Doozy of a function that takes a dictionary array, loads it into a sklearn
    pipeline and generates an estimator. It then uses that estimator to iterate
    through a novel array and generate predictions.

    Arguments:
    ** tr_array - array of dictionaries for the model to train on
    ** pred_array - array of dictionaries that the estimator should predict on
    ** path - a string object specifying the path to save predictions at
    """
    # prep the prediction data (you can ignore this, it's hack-y)
    for item in pred_array:
        # adding another conditional here
        if 'pos_review' in item:
            continue
        else:
            item['pos_review'] = 0
        drop_cats(unwanted, item)

    # take the target data and load it into a list, then delete that value from
    # feature data (don't want my model to peak)
    target = []
    for item in tr_array:
        if 'michelin_stars' in item:
            target.append(item['michelin_stars'])
            del item['michelin_stars']
        else:
            target.append(0)

        # adding another conditional here
        if 'pos_review' in item:
            continue
        else:
            item['pos_review'] = 0

        drop_cats(unwanted, item)


    # initalize the vectorizer, estimator & feature selection
    vect = DictVectorizer()
    estimator = DecisionTreeRegressor()

    # specify target & features
    X = tr_array      # non-target, feature data
    y = target        # target is possible number of michelin stars for each restaurant

    # split the training data out so I can cross-validate
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # use the vectorizer to transform training data into arrays
    X_train_dtm = vect.fit_transform(X_train).toarray()
    # Ditto for the test data
    X_test_dtm = vect.transform(X_test).toarray()


    # Attempt to impute data... because for some reason values are missing
    X_train_dtm[np.isnan(X_train_dtm)] = np.median(X_train_dtm[~np.isnan(X_train_dtm)])
    X_test_dtm[np.isnan(X_test_dtm)] = np.median(X_test_dtm[~np.isnan(X_test_dtm)])


    estimator.fit(X_train_dtm, y_train)
    y_pred_class = estimator.predict(X_test_dtm)

    # evaluate our model's accuracy
    accu = metrics.accuracy_score(y_test, y_pred_class)
    accu *= 100
    print('Your model is predicting with an accuracy of {0:.2f}%'.format(accu))


    # vectorize the
    pred_input = vect.transform(pred_array).toarray()

    # Again, not sure why I need to impute...but it's the only thing that's work...
    pred_input[np.isnan(pred_input)] = np.median(pred_input[~np.isnan(pred_input)])

    results = estimator.predict(pred_input) # predict the amount of stars each dc restaurant will have

    # mapping the predicted stars back to their original instances
    i = 0
    for item in pred_array:
        item['michelin_stars'] = results[i]
        i += 1

    pred_star_dict = {} #populate a dictionary object with my answers
    for item in pred_array:
        if item['michelin_stars'] > 0:
            pred_star_dict[item['name']] = int(item['michelin_stars'])
        else:
            continue

    # now I need to save the relevant predictions to a .csv
    fnames = ['Restaurant', 'Stars']
    with open(path, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(fnames)
        for key, value in pred_star_dict.items():
            writer.writerow([key, value])

    return

def main():
    """
    The primary execution function.
    """
    # load the two collections
    dc_array = make_usable('washington dc')
    other_array = make_usable('other')

    # run my ML code
    train_n_predict(other_array, dc_array)

    return

##########################################################################
## Execution
##########################################################################

if __name__ == '__main__':
    main()

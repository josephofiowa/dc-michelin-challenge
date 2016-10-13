{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Final Michelin Submission with Modeling Code - Charles Rice"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Over the course of four notebooks I have scraped, pulled, cleaned, and modeled data from Yelp itself. The following represents the final work of that process in clean, well-commented code. For reference, I have also included the messy working notebooks."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Import all the libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import scipy as sp\n",
    "import re\n",
    "from sklearn.cross_validation import train_test_split, cross_val_score, StratifiedKFold, cross_val_predict\n",
    "from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\n",
    "from sklearn.naive_bayes import MultinomialNB\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn import metrics\n",
    "from sklearn.metrics import confusion_matrix, classification_report\n",
    "from sklearn.ensemble import RandomForestClassifier"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "# Read in the relevant files\n",
    "trainer = pd.read_csv('full_trainer.csv', sep='|', index_col=0)\n",
    "tester = pd.read_csv('DC_reviews.csv', sep='|')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unnamed: 0</th>\n",
       "      <th>url</th>\n",
       "      <th>review</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>1789-restaurant-washington</td>\n",
       "      <td>The restaurants name was inspired by an import...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>2020-restaurant-and-lounge-washington</td>\n",
       "      <td>This is a great venue for groups or to just co...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>acadiana-washington</td>\n",
       "      <td>Located near the Convention Center - I attende...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>art-and-soul-washington</td>\n",
       "      <td>For the first time ever I am stumped as to wha...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4</td>\n",
       "      <td>birch-and-barley-washington</td>\n",
       "      <td>Got turned away at the door, because upstairs ...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Unnamed: 0                                    url  \\\n",
       "0           0             1789-restaurant-washington   \n",
       "1           1  2020-restaurant-and-lounge-washington   \n",
       "2           2                    acadiana-washington   \n",
       "3           3                art-and-soul-washington   \n",
       "4           4            birch-and-barley-washington   \n",
       "\n",
       "                                              review  \n",
       "0  The restaurants name was inspired by an import...  \n",
       "1  This is a great venue for groups or to just co...  \n",
       "2  Located near the Convention Center - I attende...  \n",
       "3  For the first time ever I am stumped as to wha...  \n",
       "4  Got turned away at the door, because upstairs ...  "
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tester.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "# There's an unnecessary column, a result of the reading/writing to CSV process.\n",
    "tester.drop(['Unnamed: 0'], axis=1, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>url</th>\n",
       "      <th>review</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1789-restaurant-washington</td>\n",
       "      <td>The restaurants name was inspired by an import...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2020-restaurant-and-lounge-washington</td>\n",
       "      <td>This is a great venue for groups or to just co...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>acadiana-washington</td>\n",
       "      <td>Located near the Convention Center - I attende...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>art-and-soul-washington</td>\n",
       "      <td>For the first time ever I am stumped as to wha...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>birch-and-barley-washington</td>\n",
       "      <td>Got turned away at the door, because upstairs ...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                     url  \\\n",
       "0             1789-restaurant-washington   \n",
       "1  2020-restaurant-and-lounge-washington   \n",
       "2                    acadiana-washington   \n",
       "3                art-and-soul-washington   \n",
       "4            birch-and-barley-washington   \n",
       "\n",
       "                                              review  \n",
       "0  The restaurants name was inspired by an import...  \n",
       "1  This is a great venue for groups or to just co...  \n",
       "2  Located near the Convention Center - I attende...  \n",
       "3  For the first time ever I am stumped as to wha...  \n",
       "4  Got turned away at the door, because upstairs ...  "
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Everything clear? \n",
    "trainer.head()\n",
    "tester.head()\n",
    "# Yes."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "X = trainer.review.values\n",
    "y = trainer.stars"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Vectorize"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We are working here with text. Lots and lots of text. So very, very much text. It must be turned into words. But also into n-grams (en- to tetra-) in order to find useful features. CountVectorizer, I found, worked best."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "cvec = CountVectorizer(decode_error='ignore', stop_words='english', ngram_range=(1,4), analyzer='char')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "X_dtm = cvec.fit_transform(X)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(66, 102995)"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X_dtm.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Modeling Proper"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# The additional class weight is an attempt to make up for the disproportionate number of zero-starred restaurants.\n",
    "rf1 = RandomForestClassifier(class_weight={0:4})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "RandomForestClassifier(bootstrap=True, class_weight={0: 4}, criterion='gini',\n",
       "            max_depth=None, max_features='auto', max_leaf_nodes=None,\n",
       "            min_samples_leaf=1, min_samples_split=2,\n",
       "            min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,\n",
       "            oob_score=False, random_state=None, verbose=0,\n",
       "            warm_start=False)"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "rf1.fit(X_dtm, y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Random Forest Clf mean Cross-Val Score: 0.65873015873\n",
      "RF CLF Accuracy Score:  0.984848484848\n",
      "             precision    recall  f1-score   support\n",
      "\n",
      "          0       1.00      1.00      1.00        12\n",
      "          1       0.68      0.90      0.78        31\n",
      "          2       0.29      0.14      0.19        14\n",
      "          3       0.50      0.33      0.40         9\n",
      "\n",
      "avg / total       0.63      0.68      0.64        66\n",
      "\n",
      "[[12  0  0  0]\n",
      " [ 0 28  3  0]\n",
      " [ 0  9  2  3]\n",
      " [ 0  4  2  3]]\n"
     ]
    }
   ],
   "source": [
    "cv = StratifiedKFold(y, n_folds=8, shuffle=True, random_state=42)\n",
    "s = cross_val_score(rf1, X_dtm, y, cv=cv)\n",
    "print \"Random Forest Clf mean Cross-Val Score: {}\".format(np.mean(s))\n",
    "print \"RF CLF Accuracy Score: \", rf1.score(X_dtm,y)\n",
    "p = cross_val_predict(rf1, X_dtm, y, cv=cv)\n",
    "print classification_report(y, p)\n",
    "print confusion_matrix(y, p)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "X_f = tester.review.values\n",
    "dtm_f = cvec.transform(X_f)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(77, 102995)"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dtm_f.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## And prediction!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "mich_pred = rf1.predict(dtm_f)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0, 2, 1, 0, 1, 1, 0, 0, 2, 1, 1,\n",
       "       1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 0, 1, 2,\n",
       "       0, 1, 1, 0, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 1, 1, 0, 1,\n",
       "       1, 1, 1, 1, 1, 0, 1, 1])"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mich_pred"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "df = pd.DataFrame(mich_pred, columns=['Pred Stars'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Pred Stars</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Pred Stars\n",
       "0           1\n",
       "1           0\n",
       "2           1\n",
       "3           1\n",
       "4           1"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "final = tester.join(df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>url</th>\n",
       "      <th>review</th>\n",
       "      <th>Pred Stars</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1789-restaurant-washington</td>\n",
       "      <td>The restaurants name was inspired by an import...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2020-restaurant-and-lounge-washington</td>\n",
       "      <td>This is a great venue for groups or to just co...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>acadiana-washington</td>\n",
       "      <td>Located near the Convention Center - I attende...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>art-and-soul-washington</td>\n",
       "      <td>For the first time ever I am stumped as to wha...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>birch-and-barley-washington</td>\n",
       "      <td>Got turned away at the door, because upstairs ...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                     url  \\\n",
       "0             1789-restaurant-washington   \n",
       "1  2020-restaurant-and-lounge-washington   \n",
       "2                    acadiana-washington   \n",
       "3                art-and-soul-washington   \n",
       "4            birch-and-barley-washington   \n",
       "\n",
       "                                              review  Pred Stars  \n",
       "0  The restaurants name was inspired by an import...           1  \n",
       "1  This is a great venue for groups or to just co...           0  \n",
       "2  Located near the Convention Center - I attende...           1  \n",
       "3  For the first time ever I am stumped as to wha...           1  \n",
       "4  Got turned away at the door, because upstairs ...           1  "
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "final.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "submission = final[['url', 'Pred Stars']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>url</th>\n",
       "      <th>Pred Stars</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1789-restaurant-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2020-restaurant-and-lounge-washington</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>acadiana-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>art-and-soul-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>birch-and-barley-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                     url  Pred Stars\n",
       "0             1789-restaurant-washington           1\n",
       "1  2020-restaurant-and-lounge-washington           0\n",
       "2                    acadiana-washington           1\n",
       "3                art-and-soul-washington           1\n",
       "4            birch-and-barley-washington           1"
      ]
     },
     "execution_count": 41,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "submission.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "heads = ['Restaurant Name', 'Pred Stars']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "submission.columns = heads"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Restaurant Name</th>\n",
       "      <th>Pred Stars</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1789-restaurant-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2020-restaurant-and-lounge-washington</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>acadiana-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>art-and-soul-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>birch-and-barley-washington</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                         Restaurant Name  Pred Stars\n",
       "0             1789-restaurant-washington           1\n",
       "1  2020-restaurant-and-lounge-washington           0\n",
       "2                    acadiana-washington           1\n",
       "3                art-and-soul-washington           1\n",
       "4            birch-and-barley-washington           1"
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "submission.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "submission = submission.sort_values(['Pred Stars'], ascending=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Analysis\n",
    "These results are... surprising. Le Diplomate is good, but I doubt that it is worth a special trip to DC. Masstro's is a chain, which I don't think is supposed to happen with Michelin. Overall, I'd say that my results are warped as much by the lack of good '0-star' data as by anything else. The NLP approach, absent sentiment analysis, produces results at least that do match up with intuitions."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Cleaning for Submission"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "submission = submission.reset_index()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "submission.drop(['index'], axis=1, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "submission['Restaurant Name'] = submission['Restaurant Name'].str.replace('-', ' ')\n",
    "\n",
    "submission['Restaurant Name'] = submission['Restaurant Name'].str.replace(' washington', '')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "submission = submission[submission['Pred Stars']!=0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1    55\n",
       "2     9\n",
       "3     1\n",
       "Name: Pred Stars, dtype: int64"
      ]
     },
     "execution_count": 58,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "submission['Pred Stars'].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "submission.to_csv('CharlesRice-Submission.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [Root]",
   "language": "python",
   "name": "Python [Root]"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}

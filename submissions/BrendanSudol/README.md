hello! my code (and explanatory notes) can be found in the
ipython notebook `brendansudol-code.ipynb'

to run locally:

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ jupyter notebook
```

brief writeup (this is a very rudimentary model):

* first i estimate # of michelin restaurants that DC will have (based on other cities)
* then i compile top DC restaurants lists from various sources (zagat, washingtonian, tom sietsema, etc)
* then i augment dataset with yelp stats (cost, percent of 5 star reviews, etc)
* finally i do some rule-based filtering & aggregate metric z-scores to create combined score for sorting

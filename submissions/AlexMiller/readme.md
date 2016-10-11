Thought process:

There are two major hurdles of predicting Michelin Stars that I tried to overcome with these scripts:

Firstly, stars are a relatively rare event. Although there are 72 starred restaurants in New York City, there are literally millions of restaurants that do not have any stars. If we were to try and train any classifier with one observation per restaurant, our data would be too unbalanced. The way I attempted to recify this was by collecting as many reviews for starred restaurants as possible. Although there are only 72 starred restaurants in the dataset, there are a minimum of 2,200 reviews per star category.

Secondly, it would be difficult to obtain enough samples of writing about a restaurant to avoid a dimensionality problem when it comes to vectorizing the words. At one point my dataset reported a corpus of about 20,000 words, if we turned this into a TFIDF vector, our observations would be outnumbered by a factor of 2. This is why I chose to include word2vec (specifically the binary compiled by Google News sources). This allowed me to turn each document into a average vector of just 300, which should still be a pretty good indicator of the overall sentiment of the review.

Once we've obtained estimation vectors for each review in the DC dataset, we can begin to estimate DC stars by either first predicting the star and then averaging over all the reviews, or averaging all of our output nodes and then predicting the outcome based on that average

Technical process:

1. scrape_wikipedia.py
- Built to scrape Wikipedia for the NYC and Chicago 2016 Michelin star tables. Ultimately decided just to go with NYC
--Input: None
--Output: ny_stars.csv and chi_stars.csv

2. scrape_yelp.py
- Using what we've scraped from Wikipedia and our knowledge of the DC restaurant scene, we scrape a set of NYC/DC restaurants as well as some random (unstarred) NYC restaurants for training.
--Input: supplemental_data/ny_stars.csv and supplemental_data/dc_possibilities.csv
--Output: nyc.csv and dc.csv (not included for copywrite reasons), approximately 5,000 textual Yelp reviews

3. process_data.py
- Preprocess data for neural network, including the removal of stop words
--Input: nyc.csv
--Output: train.csv, test.csv, all.csv, to_classify.csv (not included)

4. michelin_word2vec.py
- Utilizing average word2vec vectors for each review, learn how to classify reviews into star categories
--Input: train.csv, test.csv
--Output: model.th

5. michelin_classify_vector.py
- Using our learned model, output prediction vectors
--Input: model.th, to_classify.csv
--Output: prediction_vectors.csv (not included)

6. stitch_and_average.py
- Bind prediction vectors to restaurant names and calculate average likelihoods for stars
--Input: prediction_vectors.csv, dc.csv
--Output: dc_predictions.csv

7. Human intuition
-Removing the 2 Bib Gourmand restaurants that received stars according to the model.
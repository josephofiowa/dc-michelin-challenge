Process:

1. scrape_wikipedia.py
- Built to scrape Wikipedia for the NYC and Chicago 2016 Michelin star tables. Ultimately decided just to go with NYC
--Input: None
--Output: supplemental_data/ny_stars.csv and supplemental_data/chi_stars.csv

2. scrape_yelp.py
- Using what we've scraped from Wikipedia and our knowledge of the DC restaurant scene, we scrape a set of NYC/DC restaurants as well as some random (unstarred) NYC restaurants for training.
--Input: supplemental_data/ny_stars.csv and supplemental_data/dc_possibilities.csv
--Output: nyc.csv and dc.csv (not included for copywrite reasons), approximately 5,000 textual Yelp reviews

3. process_data.py
- Preprocess data for neural network
--Input: nyc.csv
--Output: train.csv and test.csv (not included)


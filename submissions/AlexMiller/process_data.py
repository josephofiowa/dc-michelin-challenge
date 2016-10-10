import pandas as pd
from csv import QUOTE_NONE
from csv import QUOTE_ALL
import pdb
import random

# prefix = "/media/alex/HD/"
prefix = "D:/"

#Process our NYC data for neural network
df = pd.read_csv(prefix+"Documents/Data/Yelp/nyc.csv",header=0,encoding="latin1")

#Keep only stars and reviews
df = df[["stars","review"]]

#Let's remove the return characters and add spacing to common punctuation
def clean_text(row):
    return row.replace("\r","").replace("\n"," ").replace(","," ").replace("."," . ").replace("/"," / ").replace('"',' " ').replace('!',' ! ').replace('?',' ? ').replace('$',' $ ').replace('-',' - ').replace(")"," ) ").replace("("," ( ")
df["review"] = df["review"].apply(clean_text)

#And stringify scores
def stringify(row):
    return str(int(row))
df["stars"] = df["stars"].apply(stringify)

#Create balanced set for training
segmented_reviews = {"0":[],"1":[],"2":[],"3":[]}

for index, row in df.iterrows():
    star = row['stars']
    review = row['review']
    segmented_reviews[star].append(review)

star_length = min([len(segmented_reviews['3']),len(segmented_reviews['2']),len(segmented_reviews['1']),len(segmented_reviews['0'])])
random.shuffle(segmented_reviews['0'])
segmented_reviews['0'] = segmented_reviews['0'][:star_length]
random.shuffle(segmented_reviews['1'])
segmented_reviews['1'] = segmented_reviews['1'][:star_length]
random.shuffle(segmented_reviews['2'])
segmented_reviews['2'] = segmented_reviews['2'][:star_length]
random.shuffle(segmented_reviews['3'])
segmented_reviews['3'] = segmented_reviews['3'][:star_length]

# Segment the data randomly into training and testing
training_ratio = 0.8

zero_stars = pd.DataFrame({"stars":"0","review":segmented_reviews['0']})
training_count = int(zero_stars.count(0)[0]*training_ratio)
zero_training = zero_stars.ix[:training_count]
zero_testing = zero_stars.ix[training_count:]
one_stars = pd.DataFrame({"stars":"1","review":segmented_reviews['1']})
one_training = one_stars.ix[:training_count]
one_testing = one_stars.ix[training_count:]
two_stars = pd.DataFrame({"stars":"2","review":segmented_reviews['2']})
two_training = two_stars.ix[:training_count]
two_testing = two_stars.ix[training_count:]
three_stars = pd.DataFrame({"stars":"3","review":segmented_reviews['3']})
three_training = three_stars.ix[:training_count]
three_testing = three_stars.ix[training_count:]
all_training = [zero_training,one_training,two_training,three_training]
all_testing = [zero_testing,one_testing,two_testing,three_testing]
all_stars = [zero_stars,one_stars,two_stars,three_stars]
df = pd.concat(all_stars,ignore_index=True)
train = pd.concat(all_training,ignore_index=True)
test = pd.concat(all_testing,ignore_index=True)
df = df[["stars","review"]]
train = train[["stars","review"]]
test = test[["stars","review"]]

# Write csvs
train.to_csv(prefix+"Documents/Data/Yelp/train.csv",index=False,encoding="latin1")
train.to_csv(prefix+"Documents/Data/Yelp/train_headless.csv",index=False,header=None,encoding="latin1")
test.to_csv(prefix+"Documents/Data/Yelp/test.csv",index=False,encoding="latin1")
test.to_csv(prefix+"Documents/Data/Yelp/test_headless.csv",index=False,header=None,encoding="latin1")
df.to_csv(prefix+"Documents/Data/Yelp/all.csv",index=False,encoding="latin1")
df.to_csv(prefix+"Documents/Data/Yelp/all_headless.csv",index=False,header=None,encoding="latin1")

#Process our DC data for neural network
df = pd.read_csv(prefix+"Documents/Data/Yelp/dc.csv",header=0,encoding="latin1")

#Create balanced set for prediction
# segmented_reviews = {"0":[],"1":[]}
# 
# for index, row in df.iterrows():
#     bib = str(int(row['bib']))
#     review = row['review']
#     segmented_reviews[bib].append(review)
# 
# min_length = min([len(segmented_reviews['1']),len(segmented_reviews['0'])])
# random.shuffle(segmented_reviews['0'])
# segmented_reviews['0'] = segmented_reviews['0'][:min_length]
# random.shuffle(segmented_reviews['1'])
# segmented_reviews['1'] = segmented_reviews['1'][:min_length]
# 
# zero_bib = pd.DataFrame({"review":segmented_reviews['0']})
# one_bib = pd.DataFrame({"review":segmented_reviews['1']})
# all_bib = [zero_bib,one_bib]
# df = pd.concat(all_bib)
# df = df[["review"]]

#Keep only reviews
df = df[["review"]]

#Let's remove the return characters and add spacing to common punctuation
def clean_text(row):
    return row.replace("\r","").replace("\n"," ").replace(","," ").replace("."," . ").replace("/"," / ").replace('"',' " ').replace('!',' ! ').replace('?',' ? ').replace('$',' $ ').replace('-',' - ').replace(")"," ) ").replace("("," ( ")
df["review"] = df["review"].apply(clean_text)

# Write csv
df.to_csv(prefix+"Documents/Data/Yelp/to_classify.csv",index=False,encoding="latin1")
df.to_csv(prefix+"Documents/Data/Yelp/to_classify_headless.csv",index=False,header=None,encoding="latin1")


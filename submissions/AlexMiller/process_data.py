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

# #Split into sentences?
# reviews = []
# stars = []
# for index, row in df.iterrows():
#     star = row['stars']
#     review = row['review']
#     review_split = review.split(".")
#     for split in review_split:
#         reviews.append(split)
#         stars.append(star)

# #Turn into one-line
# one = pd.DataFrame(df['stars']+" "+df['review'])

# Segment the data randomly into training and testing
training_ratio = 0.8
training_count = int(df.count(0)[0]*training_ratio)
training_rows = random.sample(df.index,training_count)
train = df.ix[training_rows]
test = df.drop(training_rows)

# Write csvs
train.to_csv(prefix+"Documents/Data/Yelp/train.csv",index=False,encoding="latin1")
test.to_csv(prefix+"Documents/Data/Yelp/test.csv",index=False,encoding="latin1")
df.to_csv(prefix+"Documents/Data/Yelp/all.csv",index=False,encoding="latin1")

#Leave the segmentation to DIGITS
# df.to_csv("/media/alex/HD/git/DIGITS/data/nyc/train.csv",index=False,header=False,quoting=QUOTE_ALL,encoding="latin1")

#Process our DC data for neural network
df = pd.read_csv(prefix+"Documents/Data/Yelp/dc.csv",header=0,encoding="latin1")

#Keep only reviews
df = df[["review"]]

#Let's remove the return characters and add spacing to common punctuation
def clean_text(row):
    return row.replace("\r","").replace("\n"," ").replace(","," ").replace("."," . ").replace("/"," / ").replace('"',' " ').replace('!',' ! ').replace('?',' ? ').replace('$',' $ ').replace('-',' - ').replace(")"," ) ").replace("("," ( ")
df["review"] = df["review"].apply(clean_text)

# Write csv
df.to_csv(prefix+"Documents/Data/Yelp/to_classify.csv",index=False,encoding="latin1")

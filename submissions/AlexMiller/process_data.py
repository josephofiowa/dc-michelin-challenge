import pandas as pd
from csv import QUOTE_ALL
import pdb
import random

#Process our NYC data for neural network
df = pd.read_csv("/media/alex/HD/Documents/Data/Yelp/nyc.csv",header=0,encoding="latin1")

#Keep only stars and reviews
df = df[["stars","review"]]

#Let's remove the return characters and reencode
def clean_text(row):
    return row.replace("\r","").replace("\n"," ").encode("utf-8","ignore")
df["review"] = df["review"].apply(clean_text)

#And stringify scores
def stringify(row):
    return str(int(row)+1)
df["stars"] = df["stars"].apply(stringify)

# Segment the data randomly into training and testing
training_ratio = 0.8
training_count = int(df.count(0)[0]*training_ratio)
training_rows = random.sample(df.index,training_count)
train = df.ix[training_rows]
test = df.drop(training_rows)

# Write csvs
train.to_csv("/media/alex/HD/git/DIGITS/data/nyc/train.csv",index=False,header=False,quoting=QUOTE_ALL,encoding="latin1")
test.to_csv("/media/alex/HD/git/DIGITS/data/nyc/test.csv",index=False,header=False,quoting=QUOTE_ALL,encoding="latin1")

#Leave the segmentation to DIGITS
# df.to_csv("/media/alex/HD/git/DIGITS/data/nyc/train.csv",index=False,header=False,quoting=QUOTE_ALL,encoding="latin1")
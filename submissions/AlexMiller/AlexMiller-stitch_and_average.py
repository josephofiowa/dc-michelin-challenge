import pandas as pd
import pdb
import random


prefix = "/media/alex/HD/"
# prefix = "D:/"
prefix2 = "/media/alex/SSD/"
# prefix2 = "C:/"

#Read in the original DC dataset
df = pd.read_csv(prefix+"Documents/Data/Yelp/dc.csv",header=0,encoding="latin1")

#Keep only restaurant name, review date, price rating, average score, review count
df = df[["req.restaurant","date","price","avg.score","review.count"]]

#Read in the prediction vectors
pred = pd.read_csv(prefix+"git/word2vec.torch/prediction_vectors.csv",header=None)
pred.columns = ["star0","star1","star2","star3"]

#We never scrambled them, so we can keep them in the same order
dc = df.join(pred)
dc_means = dc.groupby('req.restaurant').mean()
dc_means['max'] = dc_means[['star0','star1','star2','star3']].idxmax(axis=1)

# Write csv
dc_means.to_csv(prefix2+"git/dc-michelin-challenge/submissions/AlexMiller/dc_predictions.csv")


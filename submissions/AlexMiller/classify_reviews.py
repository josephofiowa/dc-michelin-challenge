import nltk
import random
import pdb
import unicodecsv
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")

# prefix = "/media/alex/HD/"
prefix = "D:/"

def splitStop(x):
    return [word for word in x.split() if word not in cachedStopWords]

documents = []
all_words_raw = []
with open(prefix+'Documents/Data/Yelp/all.csv','r') as csvfile:
    reader = unicodecsv.reader(csvfile,delimiter=',',quotechar="\"",encoding="latin1")
    header = None
    for row in reader:
        if not header:
            header = row
        else:
            splitList = splitStop(row[1])
            documents.append((splitList,row[0]))
            all_words_raw+=splitList     

random.shuffle(documents)
all_words = nltk.FreqDist(w.lower() for w in all_words_raw)
word_features = all_words.keys()[:2000] # [_document-classify-all-words]

def document_features(document): # [_document-classify-extractor]
    document_words = set(document) # [_document-classify-set]
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

featuresets = [(document_features(d), c) for (d,c) in documents]
set_size = int(len(documents)/2)
print("Testing set size: "+str(set_size))
train_set, test_set = featuresets[set_size:], featuresets[:set_size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Accuracy: "+unicode(nltk.classify.accuracy(classifier, test_set)*100)+"%")
classifier.show_most_informative_features(5)

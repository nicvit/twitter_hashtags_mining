import re
import nltk
import numpy as np
import pandas as pd
import pickle

# posmaremo
# '(: :) :] [: :-) (-: [-: :-] (; ;) ;] [; ;-) (-; [-; ;-] :-D :D :-p :p (=: ;=D :=) :S @-) XD' 
# negmaremo
# '\:\(|\)\:|:\-\(|\)\-\:|\;\(|\)\;|\:\-\[|\]\-\:|\;\-\(|\)\-\;|\:\'\[|\:\'\(|\)\'\:|\]\:|\:\[|:\||\:\/|\|\:|\/\:|\:\=\(|\:\=\||\:\=\[|xo|D\:|O\:'
def processTweet(tweet):
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert retweet
    tweet = re.sub('(rt\s)@[^\s]+','RT',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    # Group emoticons
    # detection emoticon positive :-), :D ...
    tweet = re.sub('\(\:|\:\)|\:\]|\[\:|\:\-\)|\(\-\:|\[\-\:|\:\-\]|\(\;|\;\)|\;\]|\[\;|\;\-\)|\(\-\;|\[\-\;|\;\-\]|\:\-D|:D|\:\-p|\:p|\(\=\:|\;\=D|\:\=\)|\:S|@\-\)|XD','posmaremo',tweet)
    # detection emoticon negative )-:, :-/ ...
    tweet = re.sub('\:\(|\)\:|:\-\(|\)\-\:|\;\(|\)\;|\:\-\[|\]\-\:|\;\-\(|\)\-\;|\:\'\[|\:\'\(|\)\'\:|\]\:|\:\[|:\||\:\/|\|\:|\/\:|\:\=\(|\:\=\||\:\=\[|xo|D\:|O\:','negmaremo',tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)



##############################################################################################################



def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('URL')
    stopWords.append('RT')
    stopWords.append('AT_USER')
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords


def getFeatureVector(tweet, stwl):
    featureVector = []
    tweet = processTweet(tweet)
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = re.sub('[^\w\s]','', w)
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stwl or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector

# Load all the CSV file in a dictionary of lisits of the form
# sentiment_ds_p_n = {"ItemID":[...], "Sentiment":[...], "SentimentText":[...]}
df_csv = pd.read_csv('/Users/nicolavitale/Desktop/twitter_data_analysis/develop/data/sentiment_analysis/Sentiment_Analysis_Dataset.csv',header=0, error_bad_lines=False)
# df_csv.drop('SentimentSource')
# df_csv.drop('ItemID')
# 1578612 total classified tweets
# separate in positive and negative
df_pos = df_csv.loc[df_csv['Sentiment'] == 1]
df_neg = df_csv.loc[df_csv['Sentiment'] == 0]
# use around 600 tweets; 2/3 training (400), 1/3 test (200)
pos_train = df_pos[0:344500]
neg_train = df_neg[0:500000]
train_pn = pd.concat([pos_train, neg_train])

pos_test = df_pos[200001:300000]
neg_test = df_neg[200001:300000]
test_pn = pd.concat([pos_test, neg_test])

print len(pos_train)

#Read the tweets one by one and process them
stopWords = getStopWordList('/Users/nicolavitale/Desktop/twitter_data_analysis/develop/data/SmartStoplist.txt')
# tw_sent_p = []
twft_sent_p = []

# tw_sent_n = []
twft_sent_n = []

# ftrs_list = []


for i in range(0,len(pos_train)):
    try:
        tweet = pos_train['SentimentText'][i]
        sentiment = pos_train['Sentiment'][i]
        featureVector = getFeatureVector(tweet, stopWords)
#         ftrs_list.extend(featureVector)
#         tw_sent_p.append((tweet, sentiment))
        twft_sent_p.append((featureVector, sentiment))
    except KeyError:
        continue

        
        
for i in range(0,len(neg_train)):
    try:
        tweet = neg_train['SentimentText'][i]
        sentiment = neg_train['Sentiment'][i]
        featureVector = getFeatureVector(tweet, stopWords)
#         ftrs_list.extend(featureVector)
#         tw_sent_n.append((tweet, sentiment))
        twft_sent_n.append((featureVector, sentiment))
    except KeyError:
        continue


        
# ftrs_list = list(set(ftrs_list))
print len(twft_sent_p)
print len(twft_sent_n)

import random

twft_sent_p = twft_sent_p[0:25000]
# print twft_sent_p[0:10]
# print len(twft_sent_p)

twft_sent_n = twft_sent_n[0:25000]
# print twft_sent_n[0:10]
# print len(twft_sent_n)

documents = []
documents.extend(twft_sent_p)
documents.extend(twft_sent_n)

random.shuffle(documents)

print documents[0:20]
print
print len(documents)

all_ftrs = []

for i in range(0,len(documents)):
    tweet = documents[i][0]
    all_ftrs.extend(tweet)        

all_ftrs = list(set(all_ftrs))
print len(all_ftrs)

all_words = nltk.FreqDist(i.lower() for i in all_ftrs)
print all_words

word_features = list(all_words)

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


featuresets = [(document_features(d), c) for (d,c) in documents]

train_set, test_set = featuresets[:40000], featuresets[40000:]

print len(train_set)
print len(test_set)

NBClassifier_2 = nltk.NaiveBayesClassifier.train(train_set)

with open('NBClassifier_2.pickle', 'wb') as handle:
        pickle.dump(NBClassifier_2, handle)
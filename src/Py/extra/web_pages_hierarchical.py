# hierarchical clustering of web-pages with smoking related content

import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
import sklearn
from pprint import pprint as pprint
import matplotlib
import mpld3
import pickle
# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')
# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

# get paths to files
baseFolder = '/Users/nicolavitale/Desktop/twitter_data_analysis/develop/data/web_pages_mining/txt/all'
for rSDir, rDirs, rFiles in os.walk(baseFolder):
    rFiles = [f for f in rFiles if not f[0] == '.']
    rDirs[:] = [d for d in rDirs if not d[0] == '.']
    paths = []
    books_names_list = []
    for txt in rFiles:
        paths.append(os.path.join(baseFolder, txt))
        txt = re.sub(r'.txt', '', txt, flags=re.DOTALL)
        books_names_list.append(txt)
        
# open each file, append on list
parsed_b_list = []
for f in paths:  
    print '******************************\nProcessing...\t\t\t' + f + '\n******************************'
    with open(f, 'r') as myfile:
        myfile = myfile.read()
        parsed_b_list.append(myfile)

print "Number of books..."
print len(parsed_b_list)

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    stems = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if token not in stopwords:
                filtered_tokens.append(token)
    for t in filtered_tokens:
        stemmer.stem(t).encode("ascii", errors="ignore")
        stems.append(t)
    return stems


# compute tf - idf matrix
print "building TF-IDF matrix..."
from sklearn.feature_extraction.text import TfidfVectorizer
#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(parsed_b_list) #fit the vectorizer to book list

# compute similarity
print "building SIMILARITY MATRIX..."
# compute cosine similarity and distance (1-cos_sim) for the documents: DIT, number included in (0, 1) the bigger is the more similar
from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)
print "FINISHED!"

# hierarchical clustering
from scipy.cluster.hierarchy import ward, dendrogram

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15, 20)) # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=books_names_list);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

#plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters
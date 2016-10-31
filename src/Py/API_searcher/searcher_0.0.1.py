# This script is a general purpose archiver from the twitterAPI to MongoDB.
# It:
#     1. Instantiate a connection with the API
#     2. Store the tweets into MongoDB
# Modifying the API application credentials and the search type (from StreamingAPI or RestAPI) and the storing parameters,
# it is possible to run different search concurrently using different API applications. 

import twitter
import json
import pymongo
import sys
import re

def oauth_login():

    # Use 'unisoton_1' app

    CONSUMER_KEY = 'FqWhSxd57N9zgn3sr2Jm1cUYg'
    CONSUMER_SECRET = 'LpRHxDlWsGp7uuwDrpouVcOrL6dTsx0qPccKxBXbvlENSyRaHw'
    OAUTH_TOKEN = '4061210361-mh8Hn8pvOabKNfj2dohmk7gBknzWQsARAo2A2lk'
    OAUTH_TOKEN_SECRET = 'XHfTHWN3T6oqgFKTfo4fA2WylPxzi44QDNYdoRDsE868c'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)

    print >> sys.stderr, 'Succesfully connected to TwitterAPI ... ... '

    return twitter_api



def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
    
    print >> sys.stderr, 'Saving tweet with the following text ... ... \n "%s" \n' % (data['text'])

    return mongo_db_coll.insert(data)


def is_text_relevant(words_list, tags_list):

    relevant = False 
    
    if set(words_list) & set(tags_list):
        relevant = True

    return relevant









if __name__ == "__main__":


##############################################
##############################################
#   Stream parameters: just modify these, do NOT touch the rest
##############################################
##############################################

    client = pymongo.MongoClient()
    db = client.streamingAPI   # DATABASE_NAME
    collection = db.test2     # COLLECTION_NAME
    TAGS = 'tobacco'         # doublecheck the input to be given to the API method; it has to be like 'tobacco,cigarettes,smoke,' (string of comma separated words)
    TAGS_LIST = ['tobacco']

##############################################
##############################################
##############################################


    twitter_api = oauth_login()
    twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
    stream = twitter_stream.statuses.filter(locations='-135.5,24.4,-52.6,57.4')

    print >> sys.stderr, 'Succesfully created a stream instance ... ... \n'
    print >> sys.stderr, 'Filtering the public timeline for track="%s" \t \t \t' % (TAGS)
    
    for tweet_doc in stream:
        
        try:
            text = tweet_doc['text']
            #print text
            words_list = re.sub("[^\w]", " ",  text).split()
            #print words_list
        except KeyError:
            print "\n \n Tweet with no text. \n \n"

        
        try:
            relevant = is_text_relevant(words_list, TAGS_LIST)
            if relevant:
                print text
        except KeyError:
            print "\n \n Tweet not been compared. \n \n"
        
        # if there.search(text):
        #     print("Tweet Found:\t  %r" % (text))

    # for tweet_doc in stream:

    #     print tweet_doc
        
    #     relevant = is_text_relevant(tweet_doc[u'text'], TAGS_LIST)

    #     if relevant:
    #         # 2 small modificatio to the tweet as it is gathered from API

    #         # 1. Add the tags of the search, to know from which search query the document has been obtained
    #         tweet_doc['tags'] = TAGS  
        
    #         # 2. Substitue the defoult _id assigned by Mongo with the tweet id to prevent the same tweet to be inserted more than once
    #         tweet_doc['_id'] = tweet_doc["id"]
    #         del tweet_doc['id']

    #         save_to_mongo(tweet_doc, db, collection)


        
        



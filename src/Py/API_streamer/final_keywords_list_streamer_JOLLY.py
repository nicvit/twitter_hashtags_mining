# list of keywords
# manually_selected_last = ['drug', 'heroin', 'marijuana', 'stay clean', 'nicotine', 'quit smoking', 'smoke anymore', 'smokeless', 'smoker', 'smoking habit', 'cig', 'cigarette advert', 'cigarette brand', 'cigarette pack', 'malboro', 'ecig', 'electronic cigarette', 'vaping', 'vaporizer', 'hookah', 'shisha', 'tobacco control', 'tobacco illegal', 'tobacco industry', 'tobacco market', 'tobacco product']
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
import time

def oauth_login():

    # Use 'streamer_nv_1' app

    CONSUMER_KEY = 'KKpL9KrfKvVk6GXTXZVQGMQZW'
    CONSUMER_SECRET = 'ABikN5quxusBWsWlbxAyMfKEhUQ9AsP3JJXJm6OM9vBXYU15WL'
    OAUTH_TOKEN = '4061210361-nXNyn9jSUimzsGMzSW0RuG8vrDjNjAwXeA3sJGf'
    OAUTH_TOKEN_SECRET = 'NWf3DvEEL1UeogUjoMai4sQGEHkNYu9MpLuY1xezCQUql'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
     CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)

    print >> sys.stderr, 'Succesfully connected to TwitterAPI ... ... '

    return twitter_api



def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
    try:
        mongo_db_coll.insert_one(data)
        # print "Saving tweet"
    except:
        print "Error message from MongoDB. Continuing."
        pass



def stream_and_stop(stream, kw, db, collection):
    for tweet_doc in stream:

        try:
            print "\n %s \n" % tweet_doc['text']
            # 2 small modificatio to the tweet as it is gathered from API

            # 1. Add the tags of the search, to know from which search query the document has been obtained
            tweet_doc['keyword'] = kw  

            # 2. Substitue the defoult _id assigned by Mongo with the tweet id to prevent the same tweet to be inserted more than once
            tweet_doc['_id'] = tweet_doc["id"]
            del tweet_doc['id']

            save_to_mongo(tweet_doc, db, collection)
            documents_in_collection = collection.find({"keyword": kw}).count()

            if documents_in_collection >= 2000:
                print "Stremed 2000 tweets associated with keyword: \"%s\"" % keyword
                break       


if __name__ == "__main__":

    # search keyword ONE by ONE, gather 2000 tweets for each


    ##############################################
    ##############################################
    #   Stream parameters: just modify these, do NOT touch the rest
    ##############################################
    ##############################################

    client = pymongo.MongoClient()
    db = client.stream   # DATABASE_NAME
    collection = db.get_hashtags     # COLLECTION_NAME

    # search keyword ONE by ONE, gather 2000 tweets for each
    for kw in ['nicotine', 'tobacco', 'smoking', 'nicotine', 'smoker', 'cig', 'ecig', 'vaping', 'vaporizer', 'shisha']:

        keyword = kw

        documents_in_collection = collection.find({"keyword": kw}).count()

        if documents_in_collection >= 2000:
            print "Stremed 2000 tweets associated with keyword: \"%s\"" % keyword
            continue

        print "...zzz...zzz..."
        time.sleep(120)
        print "Hey!"

        ##############################################
        ##############################################
        ##############################################

        twitter_api = oauth_login()
        twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
        stream = twitter_stream.statuses.filter(track=kw, language='en')

        print "Succesfully created a stream instance ... ... \n"
            #print "Filtering the public timeline for track="%s" \t \t " % (TAGS)

            stream_and_stop(stream, kw, db, collection)



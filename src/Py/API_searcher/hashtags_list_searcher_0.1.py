import twitter
import pymongo
import sys


def oauth_login():
    
    CONSUMER_KEY = '6YyEfFZtKh3qoGJ3DTy35ToFl'
    CONSUMER_SECRET = 'dvhZX8j3kp5sPcDNivj8BGLoylJUOUbQkVG3qbICNA81R86kh8'
    OAUTH_TOKEN = '4061210361-6OWiTmHf6JpMBdjWnk3GHzNo57M1AtAXxF1gxdt'
    OAUTH_TOKEN_SECRET = 'QwvuefhvzzSFbuECijEyj1hPMA2jelF1sdpFD7hDmhZZl'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def twitter_search(twitter_api, q, max_results=100000, **kw):
    
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    
    statuses = search_results['statuses']
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results. Maximum count is 100, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval, reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
    max_results = min(18000, max_results)
    
    for _ in range(179): # 180 max number of query we can issue in 15 minutes (1 it is outside the loop)
        print "Length of statuses", len(statuses)
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') 
                        for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)

        statuses.extend(search_results['statuses'])
        
        if len(statuses) > max_results: 
            break
        
    return statuses


def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
    try:
        mongo_db_coll.insert_one(data)
        print "Saving tweet"
    except:
        print "Error message from MongoDB. Continuing."
        pass





if __name__ == "__main__":


    ##############################################
    ##############################################
    #   Stream parameters: just modify these, do NOT touch the rest
    ##############################################
    ##############################################

    client = pymongo.MongoClient()
    db = client.streamingAPI   # DATABASE_NAME
    collection = db.search7     # COLLECTION_NAME
    TAGS = '#tobacco,#smoking,#cigar'         # doublecheck the input to be given to the API method; it has to be like 'tobacco,cigarettes,smoke,' (string of comma separated words)
    TAGS_LIST = ['#tobacco','#smoking','#cigar']

    ##############################################
    ##############################################
    ##############################################


    twitter_api = oauth_login()
    twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
    results = twitter_search(twitter_api, TAGS)

    print "Succesfully queried the search API ... ... \n"
    #print "Filtering the public timeline for track="%s" \t \t " % (TAGS)

    for tweet_doc in results:
        
        try:
            # 2 small modificatio to the tweet as it is gathered from API

            # 1. Add the tags of the search, to know from which search query the document has been obtained
            tweet_doc['tags'] = TAGS_LIST  
        
            # 2. Substitue the defoult _id assigned by Mongo with the tweet id to prevent the same tweet to be inserted more than once
            tweet_doc['_id'] = tweet_doc["id"]
            del tweet_doc['id']

            save_to_mongo(tweet_doc, db, collection)

        except KeyError:
            print "KeyError. Continuing"

            continue




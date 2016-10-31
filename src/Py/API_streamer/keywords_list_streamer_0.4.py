repeat = True    

while repeat == True:
    try:
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

        def oauth_login():

            # Use 'unisoton_0' app

            CONSUMER_KEY = '6YyEfFZtKh3qoGJ3DTy35ToFl'
            CONSUMER_SECRET = 'dvhZX8j3kp5sPcDNivj8BGLoylJUOUbQkVG3qbICNA81R86kh8'
            OAUTH_TOKEN = '4061210361-6OWiTmHf6JpMBdjWnk3GHzNo57M1AtAXxF1gxdt'
            OAUTH_TOKEN_SECRET = 'QwvuefhvzzSFbuECijEyj1hPMA2jelF1sdpFD7hDmhZZl'
            
            auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                                       CONSUMER_KEY, CONSUMER_SECRET)
            
            twitter_api = twitter.Twitter(auth=auth)

            print >> sys.stderr, 'Succesfully connected to TwitterAPI ... ... '

            return twitter_api



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
            collection = db.top_occurrences0     # COLLECTION_NAME
            TAGS = 'tobacco,smoking,smoke,alcohol,cancer,cigarette,vaping,cigar,pipe,marijuana,smokers,cannabis,addiction,weed,lung,nicotine,e-cigarettes,health'         # doublecheck the input to be given to the API method; it has to be like 'tobacco,cigarettes,smoke,' (string of comma separated words)
            TAGS_LIST = ['tobacco','smoking','smoke','alcohol','cancer','cigarette','vaping','cigar','pipe','marijuana','smokers','cannabis','addiction','weed','lung','nicotine','e-cigarettes','health']

        ##############################################
        ##############################################
        ##############################################


            twitter_api = oauth_login()
            twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
            stream = twitter_stream.statuses.filter(track=TAGS, language='en')

            print "Succesfully created a stream instance ... ... \n"
            #print "Filtering the public timeline for track="%s" \t \t " % (TAGS)

            for tweet_doc in stream:
                
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
    except KeyboardInterrupt:
        repeat = False
                

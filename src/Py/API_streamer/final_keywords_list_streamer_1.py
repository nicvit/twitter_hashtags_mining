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
                print "Saving tweet"
            except:
                print "Error message from MongoDB. Continuing."
                pass






        if __name__ == "__main__":

            manually_selected_keywords = ['toke', 'ecig'] 
            # TODO add these keywords
            # modify keyword "cigs" (ony 4 or 5) to "cig"
            todo = ['cig', 'vaporizer', 'hooka']
            done = ['tobacco', 'marijuana', 'smoke', 'cigarette', 'shisha', 'cancer', 'health', 'quit', 'smoking']
            added_keywords = ['nicotine', 'smokeless', 'antismoking', 'menthol',  'eliquids'] 

            ##############################################
            ##############################################
            #   Stream parameters: just modify these, do NOT touch the rest
            ##############################################
            ##############################################

            client = pymongo.MongoClient()
            db = client.final_stream   # DATABASE_NAME
            collection = db.keywords_stream     # COLLECTION_NAME
                
            for idx, keyword in enumerate(manually_selected_keywords):

                TAGS = keyword         # doublecheck the input to be given to the API method; it has to be like 'tobacco,cigarettes,smoke,' (string of comma separated words)
                TAGS_LIST = [keyword]

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
                        
                        # documents_in_collection = collection.count()
                        # if documents_in_collection >= (idx+1)*2000:
                        #     print "Stremed 2000 tweets associated with keyword: \"%s\"" % manually_selected_keywords[idx]
                        #     print "Waiting some time before trying to query API with different keyword..."
                        #     print "I will sleep for 1 minute ... zzz ..."
                        #     time.sleep(60)
                        #     break

                        # 2 small modificatio to the tweet as it is gathered from API

                        # 1. Add the tags of the search, to know from which search query the document has been obtained
                        tweet_doc['keyword'] = TAGS_LIST  
                    
                        # 2. Substitue the defoult _id assigned by Mongo with the tweet id to prevent the same tweet to be inserted more than once
                        tweet_doc['_id'] = tweet_doc["id"]
                        del tweet_doc['id']

                        save_to_mongo(tweet_doc, db, collection)

                        print "Saved tweet associated wit keyword \"%s\"" % manually_selected_keywords[idx]

                    except KeyError:
                        print "KeyError. Continuing"

                        
                        
    except KeyboardInterrupt:
        repeat = False
                
